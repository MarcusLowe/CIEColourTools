import numpy as np
import matplotlib.pyplot as plt
import ColourTools as CT

spectra = CT.spectrumToArr("CIEColourTools/Spectra/AQ-A_pbe0-631++g2d2p_esd-ahas2.spectrum",1e-5)
plt.plot(spectra[:,0],spectra[:,1])
plt.show()