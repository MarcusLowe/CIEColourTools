import numpy as np

def ASCIIXYtoArr(filename,scale):
    f = np.loadtxt(filename)
    f[:,1] *= scale
    return f

def spectrumToArr(filename,scale):
    f = np.loadtxt(filename)[:,0:2]
    #f[:,0] = 10_000_000/f[:,0]
    f = f[f[:,0] < 850]
    f = f[350 <f[:,0] ]
    f[:,1] *= scale
    f = f[f[:, 0].argsort()]
    return f

def x_bar(wavelengths):
    colorFuncs = np.loadtxt("CIEColourTools/CIE_xyz_1931_2deg.csv",delimiter=',')
    return np.interp(wavelengths,colorFuncs[:,0],colorFuncs[:,1])

def y_bar(wavelengths):
    colorFuncs = np.loadtxt("CIEColourTools/CIE_xyz_1931_2deg.csv",delimiter=',')
    return np.interp(wavelengths,colorFuncs[:,0],colorFuncs[:,2])

def z_bar(wavelengths):
    colorFuncs = np.loadtxt("CIEColourTools/CIE_xyz_1931_2deg.csv",delimiter=',')
    return np.interp(wavelengths,colorFuncs[:,0],colorFuncs[:,3])

def D65_ill(wavelengths):
    D65 = np.loadtxt("CIEColourTools/CIE_std_illum_D65.csv",delimiter=',')
    #D65 = D65[360 <= D65[:,0]]
    return np.interp(wavelengths,D65[:,0],D65[:,1])

def spectraToXYZ(spectra,K):
    
    #wavelengths = spectra[:,0][np.where((360 <= spectra[:,0]) & (spectra[:,0] <= 830))]
    #spectrum = spectra[:,1][np.where((360 <= spectra[:,0]) & (spectra[:,0] <= 830))]
    wavelengths = np.linspace(360,830,1000)
    spectrum = np.interp(wavelengths,spectra[:,0],spectra[:,1])
    

    maxLam = max(spectra[:,0])
    spectrum[wavelengths > maxLam] = 0
    
    spectrum = 10**(-spectrum)
    
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

    return X,Y,Z

def XYZtoLab(X,Y,Z):
    Xn = 95.0498
    Yn = 100
    Zn = 108.8840
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

def abtoCh(a,b):
    C = np.sqrt(a**2 + b**2)
    h = np.arctan(b/a)

    return C,h

def XYZtosRGB(X,Y,Z):
    XYZ = np.array([X,Y,Z])
    M = np.array([[3.2404542 ,-1.5371385,-0.4985314],
                 [-0.9692660,1.8760108,0.0415560],
                 [0.0556434 ,-0.2040259,1.0572252]])
    rgb = M@XYZ
    print(rgb)
    RGB = rgb
    for i,v in enumerate(rgb):
        if v <= 0.0031308:
            RGB[i] = 12.92*v
        else:
            RGB[i] = 1.055*(v**(1/2.4)) - 0.055

    #print(rgb**(1/2.2))
    print(RGB)
    return RGB[0],RGB[1],RGB[2]