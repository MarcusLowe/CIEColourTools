import numpy as np
import matplotlib.pyplot as plt
import ColourTools as CT
import pandas as pd

#spectra = CT.spectrumToArr("CIEColourTools/Spectra/AQ-A_pbe0-631++g2d2p_esd-ahas2.spectrum",1e-5)
name = "disperse orange 1"
file1 = f"CIEColourTools\\Spectra\\{name} gaussian 50.txt"
file2 = f"CIEColourTools\\Spectra\\experimental\\{name} plot-data.csv"
scale = 1

specW1,specI1 = CT.ASCIIXYtoArr(file1,scale)
specW1 += 0
expSpec = pd.read_csv(file2)
specW = np.array(expSpec['x'])
specI = np.array(expSpec[' y'])*scale
order = specW.argsort()
specW2 = specW[order]
specI2 = specI[order]

fig, ax = plt.subplots()
ax.plot(specW1,specI1,label="B3LYP",linewidth=2,color='orange')
ax.plot(specW2,specI2,label="Exp",linestyle='--',linewidth=2,color='r')
ax.legend()
ax.set_xlabel("Wavelength (nm)")
ax.set_ylabel("Absorption Intensity")
ax.set_xlim(300, 800)
#ax.set_ylim(0, 1)
#ax.set_aspect("equal")
plt.show()