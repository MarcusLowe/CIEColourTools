import ColourTools as CT
import numpy as np

#spectra = CT.ASCIIXYtoArr("CIEColourTools/alizarinXY.txt")
#spectra = CT.ASCIIXYtoArr("CIEColourTools/Alizarin_LHW17_Shift25.txt")
spectra = CT.ASCIIXYtoArr("CIEColourTools/alizarin_shifted_big.txt")
spectra[:,1] *= 10
#spectra = np.loadtxt("CIEColourTools/alazarinEXP.csv",delimiter=',')
#spectra[:,1] = 10**(spectra[:,1] - 4)
X,Y,Z = CT.spectraToXYZ(spectra,1)
print(X,Y,Z)
"""
import matplotlib.pyplot as plt
plt.plot(spectra[:,0],x_b)
import numpy as np
colorFuncs = np.loadtxt("CIEColourTools/CIE_xyz_1931_2deg.csv",delimiter=',')
plt.plot(colorFuncs[:,0],colorFuncs[:,1])
plt.show()
"""