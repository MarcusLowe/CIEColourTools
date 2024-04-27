import numpy as np

def ASCIIXYtoArr(filename,scale):
    """
    Takes in ASCII xy file generated from GabEdit and converts into a numpy array
    -
    INPUT
    filename: string 
        Filepath of ASCII xy file
    scale: float
        Scaling factor for outputted spectra

    RETURNS\n
    Numpy array of wavelengths, Numpy array of corresponding intensities
    """
    f = np.loadtxt(filename)
    f[:,1] *= scale
    return f[:,0], f[:,1]

def spectrumToArr(filename,scale):
    """
    Takes in .spectrum file generated from Orca's ESD method and converts into a numpy array
    -
    INPUT
    filename: string 
        Filepath of .spectrum file
    scale: float
        Scaling factor for outputted spectra

    RETURNS\n
    Numpy array of wavelengths, Numpy array of corresponding intensities
    """
    f = np.loadtxt(filename)[:,0:2]
    #f[:,0] = 10_000_000/f[:,0]
    f = f[f[:,0] < 850]
    f = f[350 <f[:,0] ]
    f[:,1] *= scale
    f = f[f[:, 0].argsort()]
    return f[:,0], f[:,1]

def x_bar(wavelengths):
    """
    Returns interpolated value of the CIE XYZ 1931 xbar standard observer function at the inputted wavelengths
    -
    """
    colorFuncs = np.loadtxt("CIEColourTools/CIE_xyz_1931_2deg.csv",delimiter=',')
    return np.interp(wavelengths,colorFuncs[:,0],colorFuncs[:,1])

def y_bar(wavelengths):
    """
    Returns interpolated value of the CIE XYZ 1931 ybar standard observer function at the inputted wavelengths
    -
    """
    colorFuncs = np.loadtxt("CIEColourTools/CIE_xyz_1931_2deg.csv",delimiter=',')
    return np.interp(wavelengths,colorFuncs[:,0],colorFuncs[:,2])

def z_bar(wavelengths):
    """
    Returns interpolated value of the CIE XYZ 1931 zbar standard observer function at the inputted wavelengths
    -
    """
    colorFuncs = np.loadtxt("CIEColourTools/CIE_xyz_1931_2deg.csv",delimiter=',')
    return np.interp(wavelengths,colorFuncs[:,0],colorFuncs[:,3])

def D65_ill(wavelengths):
    """
    Returns interpolated value of the CIE standard illuminant D65 spectrum function at the inputted wavelengths
    -
    """
    D65 = np.loadtxt("CIEColourTools/CIE_std_illum_D65.csv",delimiter=',')
    #D65 = D65[360 <= D65[:,0]]
    return np.interp(wavelengths,D65[:,0],D65[:,1])

def spectraToXYZ(spectraWave,spectraInt,K,shift=0):
    """
    Converts an inputted UV-vis absorbance spectra into the 1931 CIE XYZ colour coordinates
    -
    """
    
    #wavelengths = spectra[:,0][np.where((360 <= spectra[:,0]) & (spectra[:,0] <= 830))]
    #spectrum = spectra[:,1][np.where((360 <= spectra[:,0]) & (spectra[:,0] <= 830))]
    wavelengths = np.linspace(360,830,1000)
    spectrum = np.interp(wavelengths-shift,spectraWave,spectraInt)
    

    maxLam = max(spectraWave)
    spectrum[wavelengths > maxLam] = 0
    
    spectrum = np.power(10,-spectrum)
    
    x_b = x_bar(wavelengths)
    y_b = y_bar(wavelengths)
    z_b = z_bar(wavelengths)
    I = D65_ill(wavelengths)

    import matplotlib.pyplot as plt

    plt.plot(wavelengths,x_b)
    plt.plot(wavelengths,y_b)
    plt.plot(wavelengths,z_b)
    plt.plot(wavelengths,spectrum)
    plt.plot(wavelengths,I/100)
    
    
    
    plt.show()

    N = np.trapz(I*y_b,wavelengths)

    X = K*np.trapz(spectrum*x_b*I,wavelengths)/N
    Y = K*np.trapz(spectrum*y_b*I,wavelengths)/N
    Z = K*np.trapz(spectrum*z_b*I,wavelengths)/N

    if X > .950498:
        print("X outside range")
    if Y > 1:
        print("Y outside range")
    if Z > 1.088840:
        print("Z outside range")
    
    return X,Y,Z

def XYZtoLab(X,Y,Z):
    """
    Converts CIE 1931 XYZ coordinates into CIE L*a*b* coordinates
    -
    """
    Xn = .950498
    Yn = 1.00
    Zn = 1.088840
    epsilon = 0.008856
    k = 903.3

    xr = X/Xn
    yr = Y/Yn
    zr = Z/Zn

    if xr > epsilon:
        fx = np.cbrt(xr)
    else:
        fx = (k*xr +16)/116

    if yr > epsilon:
        fy = np.cbrt(yr)
    else:
        fy = (k*yr +16)/116
    
    if zr > epsilon:
        fz = np.cbrt(zr)
    else:
        fz = (k*zr +16)/116

    L = 116*fy - 16
    a = 500*(fx-fy)
    b = 200*(fy-fz)

    return L,a,b

def abtoCh(a,b,units="rad"):
    """
    Converts a* and b* coordinates from the CIELab space to chroma (C*) and hue (h) coordinates
    -
    """
    C = np.sqrt(a**2 + b**2)
    h = np.arctan(b/a)
    if units != "rad":
        h = 180*h/(np.pi)

    return C,h

def XYZtosRGB(X,Y,Z):
    """
    Converts CIE XYZ coordinates to sRGB coordinates using standard illuminant D65 as illuminant
    -
    """
    XYZ = np.array([X,Y,Z])
    M = np.array([[3.2404542, -1.5371385, -0.4985314],
                  [-0.9692660, 1.8760108,  0.0415560],
                  [0.0556434, -0.2040259,  1.0572252]])
    rgb = M@XYZ
    print(rgb)
    RGB = rgb
    for i,v in enumerate(rgb): #Companding
        if v <= 0.0031308:
            RGB[i] = 12.92*v
        else:
            RGB[i] = 1.055*(v**(1/2.4)) - 0.055

    #print(rgb**(1/2.2))
    #print(RGB)
    
    if np.any(RGB < 0):
        #Not in sRGB gamut, approximating by desaturating
        RGB -= np.min(RGB)        
    
    if np.any(RGB > 1): #normalise
        RGB /= np.max(RGB)
    
    return RGB

def XYZtoRGB(X,Y,Z):
    """
    Converts CIE XYZ coordinates to 1998 Adobe RGB coordinates using standard illuminant D65 as illuminant.
    -
    """
    xyz2rgb = np.array([[ 2.0413690, -0.5649464, -0.3446944],
                        [-0.9692660,  1.8760108,  0.0415560],
                        [ 0.0134474, -0.1183897,  1.0154096]])
    XYZ = np.array([X,Y,Z])
    rgb = xyz2rgb@XYZ
    RGB = np.power(rgb,0.45454545454)
    if np.any(RGB > 1): #normalise
        RGB /= np.max(RGB)
    
    return RGB

def rgb_to_hex(RGB):
        """
        Convert from fractional rgb values to HTML-style hex string.
        """
        
        hex_rgb = (255 * RGB).astype(int)
        return '#{:02x}{:02x}{:02x}'.format(*hex_rgb)