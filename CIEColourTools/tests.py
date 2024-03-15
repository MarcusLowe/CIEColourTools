import ColourTools as CT
import numpy as np
import matplotlib.pyplot as plt

#spectra = CT.ASCIIXYtoArr("CIEColourTools/alizarinXY.txt")
#spectra = np.loadtxt("CIEColourTools/alazarinEXP.csv",delimiter=',')
#spectra[:,1] = 10**(spectra[:,1] - 4)
spectra = CT.spectrumToArr("CIEColourTools/AQ-A_pbe0-631++g2d2p_esd-ahas.spectrum",1e-5)
#print(spectra)

#plt.plot(spectra[:,0],spectra[:,1])
#plt.show()

X,Y,Z = CT.spectraToXYZ(spectra,50)
L,a,b = CT.XYZtoLab(X,Y,Z)
C,h = CT.abtoCh(a,b)
print(X,Y,Z)
print(L,a,b)
print(C,h)
"""
import matplotlib.pyplot as plt
plt.plot(spectra[:,0],x_b)
import numpy as np
colorFuncs = np.loadtxt("CIEColourTools/CIE_xyz_1931_2deg.csv",delimiter=',')
plt.plot(colorFuncs[:,0],colorFuncs[:,1])
plt.show()
"""