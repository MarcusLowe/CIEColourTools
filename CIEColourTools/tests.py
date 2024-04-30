import ColourTools as CT
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':

    #specW,specI = CT.ASCIIXYtoArr("CIEColourTools\\Spectra\\14aminoAQ gaussian 50.txt",5)
    #spectra = np.loadtxt("CIEColourTools/alazarinEXP.csv",delimiter=',')
    #specW, specI = CT.spectrumToArr("CIEColourTools/Spectra/AQ-A_pbe0-631++g2d2p_esd-ahas2.spectrum",1e-5)
    #spectra[:,1] = 10**(spectra[:,1] - 4)
    #spectra = CT.spectrumToArr("CIEColourTools/AQ-A_pbe0-631++g2d2p_esd-ahas.spectrum",5e-5)
    #print(spectra)
    filepath = "C:\\Users\\axolo\\Downloads\\methyl yellow plot-data.csv"
    #"C:\\Marcus Stuff\\Quantum Dyes Project\\Experimental Spectra\\reactive blue 19 plot-data.csv"
    expSpec = pd.read_csv(filepath)
    specW = np.array(expSpec['x'])
    specI = np.array(expSpec[' y'])*10
    order = specW.argsort()
    specW = specW[order]
    specI = specI[order]
    #print(specW,specI)
    #plt.plot(spectra[:,0],spectra[:,1])
    #plt.show()
    X,Y,Z = CT.spectraToXYZ(specW,specI,1,shift=0)
    L,a,b = CT.XYZtoLab(X,Y,Z)
    C,h = CT.abtoCh(a,b)
    sRGB = CT.XYZtosRGB(X,Y,Z)
    shex = CT.rgb_to_hex(sRGB)
    RGB = CT.XYZtoRGB(X,Y,Z)
    hex = CT.rgb_to_hex(RGB)
    #spectra = CT.ASCIIXYtoArr("CIEColourTools/Alizarin_LHW17_Shift25.txt")
    #spectra = CT.ASCIIXYtoArr("CIEColourTools/alizarin_shifted_big.txt")
    #spectra[:,1] *= 10
    #spectra = np.loadtxt("CIEColourTools/alazarinEXP.csv",delimiter=',')
    #spectra[:,1] = 10**(spectra[:,1] - 4)
    print("XYZ ",X,Y,Z)
    print("LAB ",round(L,1),round(a,1),round(b,1))
    print("Ch ",round(C,1),round(h,1))
    print("sRGB ",sRGB)
    print("shex ",shex)
    print("RGB ",RGB)
    print("hex ",hex)

    #print(CT.abtoCh(60.84 ,6.03))

    
    fig, ax = plt.subplots()
    for i in range(12):
        X,Y,Z = CT.spectraToXYZ(specW,specI,1,shift=i*10)
        sRGB = CT.XYZtosRGB(X,Y,Z)
        shex = CT.rgb_to_hex(sRGB)
        L,a,b = CT.XYZtoLab(X,Y,Z)
        C,h = CT.abtoCh(a,b)
        print(f"{i} : {h}")
        x, y = i % 4, -(i // 4)
        circle = plt.Circle(xy=(x, y*1.2), radius=0.4, fc=shex)
        ax.add_patch(circle)

    
    # Set the limits and background colour; remove the ticks
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(-3.2, 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('k')
    # Make sure our circles are circular!
    ax.set_aspect("equal")
    plt.show()
    
    
    """
    import matplotlib.pyplot as plt
    plt.plot(spectra[:,0],x_b)
    import numpy as np
    colorFuncs = np.loadtxt("CIEColourTools/CIE_xyz_1931_2deg.csv",delimiter=',')
    plt.plot(colorFuncs[:,0],colorFuncs[:,1])
    plt.show()
    """