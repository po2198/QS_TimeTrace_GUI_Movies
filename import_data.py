
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from pyqtgraph import PlotWidget, plot
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import glob
import numpy as np
import sys
import os
import time
import pandas as pd
import re
from re import search


def getfiles(self):

	self.importFilenames = QFileDialog.getOpenFileNames(self, "Open Data Files", "", "All Files (*.bin *py)")





def importRealTime(self, bin_file):
    """
    import binary file. Must have full, absolute path.
    
    """
    
    
    
    match = re.search('_Chan_[0-9]*_', bin_file)
    chan = int(match.group().strip('_').strip('.')[5:])
    measurement_datetime = re.search('[0-9]*-[0-9]*_', bin_file).group().strip('_')
    chip = re.search('Batch_[a-zA-Z0-9]*_Chip_[a-zA-Z0-9]*', bin_file).group().strip('Batch_')
    
    directory = os.path.split(bin_file)[0]
    
    param_file = glob.glob(os.path.join(directory, f'*.param'))[0]
    
    
    with open(param_file, 'r') as f:  
        for line in f:
            
            
            
            if "Measure" in line: # for measure time
                import_measure = float(line.split(' ')[-1])
            if "Gate" in line:
                vgs = float(line.split(' ')[-1])    
            if "Remark" in line:
                remark = line.split(' ')[-1].strip('\n\r')
            if "vset" in line:
                vset = float(line.split(' ')[-1])
            if "Electrolyte" in line:
                electrolyte = line.split(' ')[-1]
            if "Temperature" in line:
                temperature = float(line.split(' ')[-1])
                
            
            
            if str(chan) in line: 
                if "Resistor" in line:
                    dev_tmp = int(line.split(' ')[1])
                    if (dev_tmp < 10):
                        devs  = "0" + str(dev_tmp)
                    else:
                        devs = str(dev_tmp)
                    gain= float(line.split(' ')[-1])
                elif "ResX" in line:
                    resx = float(line.split(' ')[-1])
                elif "ResB" in line:
                    resb = float(line.split(' ')[-1])
                elif "ADC" in line:
                    offset = float(line.split(' ')[-1])
                elif "VDS" in line:
                    vds = float(line.split(' ')[-1])
                elif "HOLD" in line:
                    hold = float(line.split(' ')[-1])

                elif "Type" in line:
                    measureType = str(line.split(' ')[-1])
                elif "Min" in line:
                    import_min = float(line.split(' ')[-1])    
                elif "Max" in line:
                    import_max = float(line.split(' ')[-1])      
                elif "Step" in line:
                    import_step = float(line.split(' ')[-1])
                elif "Sweeps" in line:
                    import_numSweep = int(line.split(' ')[-1])  

                    
                    
    #file_path = r'C:\Users\Peijie\Downloads\20210524-121810_Batch__Chip_W1B2C6_IV_Experiment_InitIV_InitialIV-20210526T121829Z-001\20210524-121810_Batch__Chip_W1B2C6_IV_Experiment_InitIV_InitialIV\20210524-121810_Batch__Chip_W1B2C6_IV_Experiment_InitIV_InitialIV_Chan_15.bin'
    #file_path = r'C:\Users\Peijie\Downloads\20210524-125338_Batch__Chip_W1B2C6_RT_Experiment_Trials_rt2_p1V-20210601T153156Z-001\20210524-125338_Batch__Chip_W1B2C6_RT_Experiment_Trials_rt2_p1V\Chip_W1B2C6_RT_Experiment_Trials_rt2_p1V_Chan_15_1.bin'
    v_ref = 5
    
    data = np.fromfile(bin_file, dtype = 'uint16')    
                
    voltage = (np.array(data) * 5.0) / (2**14 - 1.0) + 2.5  
        
    current = (voltage - offset - vset - hold) / ( gain * resx * 1.0e6 + resb)
    
    current = current * 10**9
    
    samplingRate = int(25e3)
    num_points = len(data)
    time = np.linspace(0,import_measure, num_points)
    
    time_delta = time[1] - time[0]
    
    
    
    return time, time_delta, current, vgs, vds, electrolyte, temperature 