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

from import_data import getfiles, importRealTime



def setFrameSize(self):

	
	self.frame_size = self.frameSizeSlider.value()
	self.frameSize_label.setText(f'{self.frame_size} sec')
	
	
	self.numFrames = np.ceil(self.time[-1] / self.frame_size)
	
	self.playbackPositionSlider.setMaximum(self.numFrames)
	self.frame_size = self.frameSizeSlider.value()

	
	
	
	self.playbackPositionSlider.setValue(self.ind + 1)
	self.playbackSliderPosition()
	
	self.frameNumber_label.setText(f'{self.ind + 1} / {int(self.numFrames)}')

	
	#self.plot_parameters()
	
	
	#print(self.numFrames)

def frame_boundaries(self):
	
	self.ind_per_frame = np.round(self.frame_size / self.time_delta)
	
	#print(self.ind_per_frame)
	self.start_ind = int(self.ind * self.ind_per_frame)
	
	self.stop_ind = int(self.start_ind + self.ind_per_frame )
	#print(self.start_ind, self.stop_ind)
	
	
def plot_initialization(self):
	print(self.importFilenames)
	self.time, self.time_delta, self.current, self.vgs, self.vds, self.electrolyte, self.temperature = self.importRealTime(self.importFilenames[0][0])
	
	self.filename_label.setText(os.path.split(self.importFilenames[0][0])[1])
	self.wholePlot.setData(self.time[::100], self.current[::100], pen='b') 
	
	

	
	# self.frame_size = self.frameSizeSlider.value()
	
	# self.numframes = np.ceil(self.time[-1] / self.frame_size)
	self.setFrameSize()
	
	self.frame_boundaries()

	self.cropPlot.setData(self.time[self.start_ind:self.stop_ind], self.current[self.start_ind:self.stop_ind], pen='b')
	
	# self.zoomedViewWindow = pg.LinearRegionItem([self.time[self.start_ind], self.time[self.stop_ind]])
	# self.zoomedViewWindow.setZValue(10)
	# self.ui.whole_plot.addItem(self.zoomedViewWindow)
	
	
	self.playbackPositionSlider.setMaximum(self.numFrames)

	self.frameNumber_label.setText(f'{self.ind} / {self.numFrames}')
	
	self.setPlaybackSpeed()
	
	
	self.zoomedViewWindow.setRegion([self.time[self.start_ind], self.time[self.stop_ind]])




def plot_parameters(self):
	
	self.setFrameSize()
	self.playbackPositionSlider.setMaximum(self.numFrames)
	self.frame_size = self.frameSizeSlider.value()

	
	
	
	self.playbackPositionSlider.setValue(self.ind + 1)
	self.playbackSliderPosition()
	
	self.frameNumber_label.setText(f'{self.ind + 1} / {int(self.numFrames)}')
	




def plot_update(self):
	#below is temporary until file handling is sorted out

	
	
	
	# y, x = np.histogram(data[:,1] * 1e9,bins='fd') # updated to use the Freedman Diconis estimator for # of bins. Alt is auto, which is max('fd', 'sturges')
	# self.CurrentHistogram_x[k] = x
	# self.CurrentHistogram_y[k] = y
	self.frame_boundaries()
	if self.ind < self.numFrames: 
		
		self.cropPlot.setData(self.time[self.start_ind:self.stop_ind], self.current[self.start_ind:self.stop_ind], pen='b')
		
		self.zoomedViewWindow.setRegion([self.time[self.start_ind], self.time[self.stop_ind - 1]])
		
		y, x = np.histogram(self.current[self.start_ind:self.stop_ind],bins='fd')
		
		self.histPlot.setData(x, y, stepMode=True, fillLevel=50, pen='b')
		
		
		
	else:
		self.cropPlot.setData(self.time[self.start_ind:], self.current[self.start_ind:], pen='b')
		self.zoomedViewWindow.setRegion([self.time[self.start_ind], self.time[-1]])
		
		y, x = np.histogram(self.current[self.start_ind:],bins='fd')	
		self.histPlot.setData(x, y, stepMode=True, fillLevel=50, pen='b')
	
	QtWidgets.QApplication.processEvents()   
		


def plot_playing(self):
	while self.ind < self.numFrames and self.playing == True:
	
		
		self.plot_update()
		self.plot_parameters()
		self.ind = self.ind + 1
		
		#time.sleep(3)
		time.sleep(self.pauseTime)
	
	if self.ind == self.numFrames:
		self.playing = False

def plotRestart(self):
	self.ind = 0
	self.playbackPositionSlider.setValue(self.ind + 1)
	self.playbackSliderPosition()
	self.plot_parameters()
	self.plot_update()
		
def playButtonHandler(self):
	
	self.playing = not self.playing
	
	#print(self.playing)
	
	if self.playing == True:
		self.plot_playing()

		
		
		
		
		
def stepForward(self):
	
	
	if self.playing == False:
	
		if self.ind  < self.numFrames:
			self.ind = self.ind + 1 
			self.plot_update()
			
			self.playbackPositionSlider.setValue(self.ind + 1)
			self.playbackSliderPosition()

			self.frameNumber_label.setText(f'{self.ind + 1} / {int(self.numFrames)}')
			# self.playbackPositionSlider.setValue(self.ind + 1)
			# self.playbackSliderPosition()

		
def stepBackward(self):

	if self.playing == False:
		if self.ind > 0:
			self.ind = self.ind - 1 
			self.plot_update()
			
			
			
			self.playbackPositionSlider.setValue(self.ind + 1)
			self.playbackSliderPosition()
			
			self.frameNumber_label.setText(f'{self.ind + 1} / {int(self.numFrames)}')
			
			#self.plot_parameters()
			# self.playbackPositionSlider.setValue(self.ind + 1)
			# self.playbackSliderPosition()

def playbackSliderPosition(self):

	self.ind = self.playbackPositionSlider.value() - 1
	self.frameNumber_label.setText(f'{self.ind + 1} / {int(self.numFrames)}')
	
	
	self.plot_update()
	#self.plot_parameters()
		
		
def setPlaybackSpeed(self):
	self.pauseTime = 1 - self.playbackSpeedSlider.value() * 0.1 + 0.1
	
	
	
def selectedRegionUpdated(self):
	self.lo, self.hi = self.zoomedViewWindow.getRegion()
	
	
	ind = int(np.round(self.lo / self.time_delta ))
	val = self.time[ind]
	
	print('default: ', self.lo, '; index: ', ind, '; index vlue:', val)
	self.startTime_lineEdit.setText(f'{self.lo:.3f}')
	self.stopTime_lineEdit.setText(f'{self.hi:.3f}')

