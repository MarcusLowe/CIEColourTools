import ColourTools as CT
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#spectra = CT.ASCIIXYtoArr("CIEColourTools/Spectra/1AAQ L30 Shift 0.txt",10)
#spectra = np.loadtxt("CIEColourTools/alazarinEXP.csv",delimiter=',')
#specW, specI = CT.spectrumToArr("CIEColourTools/Spectra/AQ-A_pbe0-631++g2d2p_esd-ahas2.spectrum",1e-5)
#spectra[:,1] = 10**(spectra[:,1] - 4)
#spectra = CT.spectrumToArr("CIEColourTools/AQ-A_pbe0-631++g2d2p_esd-ahas.spectrum",5e-5)
#print(spectra)

expSpec = pd.read_csv("CIEColourTools/Spectra/AQA_Exp_Graph.csv")

#plt.plot(spectra[:,0],spectra[:,1])
#plt.show()
specW = np.array(expSpec['x'])
specI = np.array(expSpec['y'])*0.6
#print(specW,specI)
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
print("LAB ",L,a,b)
print("Ch ",C,h)
print("sRGB ",sRGB)
print("shex ",shex)
print("RGB ",RGB)
print("hex ",hex)
"""
import matplotlib.pyplot as plt
plt.plot(spectra[:,0],x_b)
import numpy as np
colorFuncs = np.loadtxt("CIEColourTools/CIE_xyz_1931_2deg.csv",delimiter=',')
plt.plot(colorFuncs[:,0],colorFuncs[:,1])
plt.show()
"""