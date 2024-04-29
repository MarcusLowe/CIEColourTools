import ColourTools as CT
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def calcError(spec1W,spec1I,spec2W,spec2I):
    X,Y,Z = CT.spectraToXYZ(spec1W,spec1I,1,shift=0)
    L1,a1,b1 = CT.XYZtoLab(X,Y,Z)
    X,Y,Z = CT.spectraToXYZ(spec2W,spec2I,1,shift=0)
    L2,a2,b2 = CT.XYZtoLab(X,Y,Z)
    print(L1,a1,b1,L2,a2,b2)
    error = np.sqrt((L2-L1)**2+(a2-a1)**2+ (b2-b1)**2)
    return error

if __name__ == '__main__':

    specW1,specI1 = CT.ASCIIXYtoArr("CIEColourTools\\Spectra\\methyl red gaussian 50.txt",10)
    
    expSpec = pd.read_csv("C:\\Marcus Stuff\\Quantum Dyes Project\\Experimental Spectra\\Methyl Red Exp.csv")
    specW = np.array(expSpec['x'])
    specI = np.array(expSpec[' y'])*10
    order = specW.argsort()
    specW2 = specW[order]
    specI2 = specI[order]

    print(f"Error = {round(calcError(specW1,specI1,specW2,specI2),1)}")
    