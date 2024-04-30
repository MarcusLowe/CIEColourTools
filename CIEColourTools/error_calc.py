import ColourTools as CT
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def calcError(L1,a1,b1,L2,a2,b2):

    error = np.sqrt((L2-L1)**2+(a2-a1)**2+ (b2-b1)**2)
    return error

if __name__ == '__main__':

    name = "disperse red 60"
    file1 = f"CIEColourTools\\Spectra\\{name} gaussian 50.txt"
    file2 = f"CIEColourTools\\Spectra\\experimental\\{name} plot-data.csv"
    scale = 2.5

    specW1,specI1 = CT.ASCIIXYtoArr(file1,scale)
    
    expSpec = pd.read_csv(file2)
    specW = np.array(expSpec['x'])
    specI = np.array(expSpec[' y'])*scale
    order = specW.argsort()
    specW2 = specW[order]
    specI2 = specI[order]

    X1,Y1,Z1 = CT.spectraToXYZ(specW1,specI1,1,shift=50)
    L1,a1,b1 = CT.XYZtoLab(X1,Y1,Z1)
    C1,h1 = CT.abtoCh(a1,b1)
    X2,Y2,Z2 = CT.spectraToXYZ(specW2,specI2,1,shift=0)
    L2,a2,b2 = CT.XYZtoLab(X2,Y2,Z2)
    C2,h2 = CT.abtoCh(a2,b2)
    sRGB1 = CT.XYZtosRGB(X1,Y1,Z1)
    sRGB2 = CT.XYZtosRGB(X2,Y2,Z2)
    hex1 = CT.rgb_to_hex(sRGB1)
    hex2 = CT.rgb_to_hex(sRGB2)

    print(f"1 LabCh {round(L1,1),round(a1,1),round(b1,1),round(C1,1),round(h1,1)}\nHex: {hex1}")
          
    print(f"2 LabCh {round(L2,1),round(a2,1),round(b2,1),round(C2,1),round(h2,1)}\nHex: {hex2}")

    print(f"Error = {round(calcError(L1,a1,b1,L2,a2,b2),1)}")

    fig, ax = plt.subplots()
    
    circle = plt.Circle(xy=(0.25, -1.2), radius=0.4, fc=hex1)
    ax.add_patch(circle)
    circle = plt.Circle(xy=(1.75, -1.2), radius=0.4, fc=hex2)
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
    
    