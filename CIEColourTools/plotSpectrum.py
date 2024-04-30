import numpy as np
import matplotlib.pyplot as plt
import ColourTools as CT
import pandas as pd

#spectra = CT.spectrumToArr("CIEColourTools/Spectra/AQ-A_pbe0-631++g2d2p_esd-ahas2.spectrum",1e-5)
file1 = "CIEColourTools\\Spectra\\reactive blue 19 gaussian 30.txt"
file2 = "C:\\Users\\axolo\\Downloads\\reactive blue 19 plot-data.csv"
scale = 5

specW1,specI1 = CT.ASCIIXYtoArr(file1,scale)
specW1 += 65
expSpec = pd.read_csv(file2)
specW = np.array(expSpec['x'])
specI = np.array(expSpec[' y'])*scale
order = specW.argsort()
specW2 = specW[order]
specI2 = specI[order]


plt.plot(specW1,specI1,label="b3lyp")
plt.plot(specW2,specI2,label="Exp")
plt.legend()
plt.show()