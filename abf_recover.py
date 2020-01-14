import pyabf
import matplotlib.pyplot as plt
import numpy as np

filepath = 'C:\\Users\\msbak\\Desktop\\새 폴더\\20200103 vcr c3.abf'
file1_abf = pyabf.ABF(filepath)

file1_abf.setSweep(0)
#
#plt.plot(file1_abf.sweepY)
#plt.plot(file1_abf.sweepC) # sweep command (DAC)
plt.plot(file1_abf.sweepX, file1_abf.sweepY, linewidth=0.1)

sampleRateHz = file1_abf.sweepX.shape[0]/file1_abf.sweepX[-1]

msdata = np.array(file1_abf.sweepY)
msdata = np.reshape(msdata, (1,msdata.shape[0]))

pyabf.abfWriter.writeABF1(msdata, filepath + '_recover.abf', sampleRateHz)
