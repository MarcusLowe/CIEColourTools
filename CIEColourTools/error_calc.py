import ColourTools as CT
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def calcError(spec1W,spec1I,spec2W,spec2I):
    X,Y,Z = CT.spectraToXYZ(spec1W,spec1I,1,shift=0)
    L1,a1,b1 = CT.XYZtoLab(X,Y,Z)
    X,Y,Z = CT.spectraToXYZ(spec2W,spec2I,1,shift=0)
    L2,a2,b2 = CT.XYZtoLab(X,Y,Z)

    error = np.sqrt((L2-L1)**2+(a2-a1)**2+ (b2-b1)**2)
    return error

if __name__ == '__main__':

    file1 = "CIEColourTools\\Spectra\\methyl yellow gaussian 50.txt"
    file2 = "C:\\Users\\axolo\\Downloads\\methyl yellow plot-data.csv"
    scale = 10

    specW1,specI1 = CT.ASCIIXYtoArr(file1,scale)
    
    expSpec = pd.read_csv(file2)
    specW = np.array(expSpec['x'])
    specI = np.array(expSpec[' y'])*scale
    order = specW.argsort()
    specW2 = specW[order]
    specI2 = specI[order]



    print(f"Error = {round(calcError(specW1,specI1,specW2,specI2),1)}")
    