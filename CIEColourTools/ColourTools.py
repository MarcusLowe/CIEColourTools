import numpy as np

def ASCIIXYtoArr(filename):
    f = np.loadtxt(filename)
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
    wavelengths = np.linspace(360,830)
    spectrum = np.interp(wavelengths,spectra[:,0],spectra[:,1])
    maxLam = max(spectra[:,0])
    spectrum[wavelengths > maxLam] = 0
    spectrum = 10**(-spectrum)

    import matplotlib.pyplot as plt
    
    
    x_b = x_bar(wavelengths)
    y_b = y_bar(wavelengths)
    z_b = z_bar(wavelengths)
    I = D65_ill(wavelengths)

    plt.plot(wavelengths,x_b)
    plt.plot(wavelengths,y_b)
    plt.plot(wavelengths,z_b)
    plt.plot(wavelengths,spectrum)
    
    
    plt.show()

    N = np.trapz(I*y_b,wavelengths)

    X = K*np.trapz(spectrum*x_b*I,wavelengths)/N
    Y = K*np.trapz(spectrum*y_b*I,wavelengths)/N
    Z = K*np.trapz(spectrum*z_b*I,wavelengths)/N

    return X,Y,Z