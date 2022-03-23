# -*- coding: utf-8 -*-
"""
Created on March 17, 2022
"""

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog,  QListWidgetItem
from pyqtgraph import PlotWidget, plot
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import sys
import os
import time
import pandas as pd
import re
from re import search










class MainWindow(QtWidgets.QMainWindow):
	from import_data import getfiles, importRealTime
	from plotting import plot_update, stepBackward, stepForward, plotRestart, plot_initialization, playButtonHandler, \
	setFrameSize, setPlaybackSpeed, playbackSliderPosition, plot_parameters, frame_boundaries, plot_playing, selectedRegionUpdated, \
	selectedRegionPlot, typedRegionRange
	from dataLabeling import addNewLabeledRegion, deleteLabeledRegion, resaveLabledRegion, prevLabeledSelection, nextLabeledSelection, \
	reviewLabeledSelection, plotSelection, updateSelectionInfo, updateSelectionInfo, generateTable, saveSelection
	
	def __init__(self, *args, **kwargs):
        
        #QtWidgets.QMainWindow.__init__(self, parent)
		super(MainWindow,self).__init__(*args, **kwargs)
        
        
        #app.aboutToQuit.connect(self.Exit)
        

		self.playing = False
		self.ind = 0
		self.ui = uic.loadUi('GUI.ui',self)
		
		
		
		
		
		self.loadDataButton.clicked.connect(self.getfiles)   
		
		self.plotButton.clicked.connect(self.plot_initialization)  
		
		
		
		"""
		Plotting windows
		"""
		self.wholePlot = self.ui.whole_plot.plot()
		self.whole_plot.setBackground('w')
		
		
		#whole plot linear region item for (i) showing cropped view and (ii) selecting regions for labeling data sections
		self.zoomedViewWindow = pg.LinearRegionItem()
		self.zoomedViewWindow.setZValue(10)
		self.ui.whole_plot.addItem(self.zoomedViewWindow)		
		
		self.zoomedViewWindow.sigRegionChanged.connect(self.selectedRegionUpdated)
		
		
		self.cropPlot = self.ui.crop_plot.plot()
		self.crop_plot.setBackground('w')
		
		
		self.histPlot = self.ui.histogram_plot.plot()
		self.histogram_plot.setBackground('w')
		self.ui.histogram_plot.rotate(90)
		
		
		self.labeledPlot = self.ui.labeledWholePlot.plot()
		self.labeledWholePlot.setBackground('w')
		
		
		
		
		
		
		
		
		self.stepBackButton.clicked.connect(self.stepBackward)
		self.stepFwdButton.clicked.connect(self.stepForward)
		self.restartPlayButton.clicked.connect(self.plotRestart)
		self.playPauseButton.clicked.connect(self.playButtonHandler)
		
		
		
		
		self.typedEntry_pushButton.clicked.connect(self.typedRegionRange)
		
		self.selectedRegionPlot_pushButton.clicked.connect(self.selectedRegionPlot)

		self.playbackPositionSlider.valueChanged.connect(self.playbackSliderPosition)
		
		
		
		self.playbackSpeedSlider.valueChanged.connect(self.setPlaybackSpeed)
		self.frameSizeSlider.valueChanged.connect(self.setFrameSize)

		
		
		self.DataLabels_comboBox.addItems(['Baseline Noise', 'NonBio RTN', 'Bio RTN', 'Wandering Baseline', 'Unusual Noise'  ])
		          
        #self.DataLabels_comboBox.activated.connect(self.)
		
		self.df_columns = ['Data Classification', 'Start Index', 'Stop Index', 'Start Time', 'Stop Time']
		self.labeledData_df = pd.DataFrame(columns=self.df_columns)
       
		self.labelDataRange_pushButton.clicked.connect(self.addNewLabeledRegion)
	   
		self.labeledData_df_selectionIndex = -1
		self.deleteLabeledRegion_pushButton.clicked.connect(self.deleteLabeledRegion)
		
		
		self.resaveLabeledRegion_pushButton.clicked.connect(self.resaveLabledRegion)
		
		
		self.reviewLabeledSelection_pushButton.clicked.connect(self.reviewLabeledSelection)
		self.nextLabeledSelection_pushButton.clicked.connect(self.nextLabeledSelection)
		self.previousLabeledSelection_pushButton.clicked.connect(self.prevLabeledSelection)
		
		self.selectionIndex = -1
		self.reviewingSelections = False
 
        

        
		self.exportLabels_pushButton.clicked.connect(self.saveSelection)
        




        
        
        
# def main():
    
    
#     app = QtWidgets.QApplication(sys.argv)
#     #app.aboutToQuit.connect(Exit)
    
#     main = MainWindow()
    
    
#     main.show()
    
#     app.aboutToQuit.connect(MainWindow.Exit(main))
#     sys.exit(app.exec_())
    
    
    
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    #app.aboutToQuit.connect(Exit)
    
    main = MainWindow()
    
    
    main.show()
    
    #app.aboutToQuit.connect(MainWindow.Exit(main))
    sys.exit(app.exec_())
