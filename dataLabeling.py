from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
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


def addNewLabeledRegion(self):

	data_classification = self.DataLabels_comboBox.currentText()
	
	index = len(self.labeledData_df)
	
	self.labeledData_df.at[index, 'Data Classification'] = data_classification
	self.labeledData_df.at[index, 'Start Index'] = self.lo_ind
	self.labeledData_df.at[index, 'Stop Index'] = self.hi_ind
	self.labeledData_df.at[index, 'Start Time'] = self.time[self.lo_ind]
	self.labeledData_df.at[index, 'Stop Time'] = self.time[self.hi_ind]

	#sort all of the labeled regions by time.
	self.labeledData_df = self.labeledData_df.sort_values(by=['Start Index'])
	self.labeledData_df = self.labeledData_df.reset_index(drop=True)
	print('saved selected region')
	print(self.labeledData_df.head())
	self.selectionIndex = index 
	
	self.generateTable()
	
	#dataFrame = dataFrame.drop(index) to remove a row
	#dataFrame = dataFrame.reset_index(drop=True) to reset the index(the row labels)
	
def generateTable(self):
	self.selectionsDF_tableWidget.setRowCount(len(self.labeledData_df))
	columns = self.df_columns
	for j in range(len(self.labeledData_df)):
		for k in range(5):
			self.selectionsDF_tableWidget.setItem(j,k, QTableWidgetItem(f'{self.labeledData_df.at[j, columns[k]]}'))
			
	

def deleteLabeledRegion(self):
	if self.reviewingSelections == True and self.selectionIndex != -1:
	
		self.labeledData_df = self.labeledData_df.drop(self.selectionIndex)
		self.labeledData_df = self.labeledData_df.reset_index(drop=True)
		print(self.labeledData_df.head())
		self.generateTable()
		
		updated_classification = self.labeledData_df.at[self.selectionIndex - 1, 'Data Classification']
		self.selection_review_label.setText(f'{int(self.selectionIndex)}/{len(self.labeledData_df)} {updated_classification}')
		if len(self.labeledData_df) == 0:
			self.selectionIndex != -1
		# else:
			# self.prevLabeledSelection()
def resaveLabledRegion(self):
	if self.reviewingSelections == True and self.selectionIndex != -1:
		data_classification = self.DataLabels_comboBox.currentText()
		
		index = self.selectionIndex
		
		self.labeledData_df.at[index, 'Data Classification'] = data_classification
		self.labeledData_df.at[index, 'Start Index'] = self.lo_ind
		self.labeledData_df.at[index, 'Stop Index'] = self.hi_ind
		self.labeledData_df.at[index, 'Start Time'] = self.time[self.lo_ind]
		self.labeledData_df.at[index, 'Stop Time'] = self.time[self.hi_ind]
		
		#self.selection_review_label.setText(f'{int(self.sel_index + 1)}/{len(self.labeledData_df)} {data_classification}')
		
		print(self.labeledData_df.head())
		self.generateTable()
		
		self.updateSelectionInfo()
		self.plotSelection()

	#sort all of the labeled regions by time.
	#self.labeledData_df = self.labeledData_df.sort_values(by=['Start Index'])
	
def reviewLabeledSelection(self):
	self.reviewingSelections = not self.reviewingSelections
	
	if self.reviewingSelections == True and self.selectionIndex != -1:
		self.updateSelectionInfo()
		self.plotSelection()
		
	if self.reviewingSelections == False:
		self.plot_update()
		
def updateSelectionInfo(self):
	self.sel_index = self.selectionIndex
	self.sel_data_classification = self.labeledData_df.at[self.sel_index, 'Data Classification']
	self.sel_lo_ind = self.labeledData_df.at[self.sel_index, 'Start Index']
	self.sel_hi_ind = self.labeledData_df.at[self.sel_index, 'Stop Index'] 
	self.sel_time_lo_ind = self.labeledData_df.at[self.sel_index, 'Start Time']
	self.sel_time_hi_ind = self.labeledData_df.at[self.sel_index, 'Stop Time'] 

def plotSelection(self):
	self.cropPlot.setData(self.time[self.sel_lo_ind:self.sel_hi_ind], self.current[self.sel_lo_ind:self.sel_hi_ind], pen='r')
	
	self.zoomedViewWindow.setRegion([self.time[self.sel_lo_ind], self.time[self.sel_hi_ind - 1]])
	
	y, x = np.histogram(self.current[self.sel_lo_ind:self.sel_hi_ind],bins='fd')
	self.histPlot.setData(x, y, stepMode=True, fillLevel=50, pen='r')
	
	self.selection_review_label.setText(f'{int(self.sel_index + 1)}/{len(self.labeledData_df)} {self.sel_data_classification}')
	
def nextLabeledSelection(self):
	
	if self.reviewingSelections == True and self.selectionIndex != -1  and self.selectionIndex < len(self.labeledData_df) - 1 :
		self.selectionIndex = self.selectionIndex + 1

		self.updateSelectionInfo()
		self.plotSelection()
		# self.sel_index = self.selectionIndex
		# self.sel_data_classification = self.labeledData_df.at[index, 'Data Classification']
		# self.sel_lo_ind = self.labeledData_df.at[index, 'Start Index']
		# self.sel_hi_ind = self.labeledData_df.at[index, 'Stop Index'] 
		# self.sel_time_lo_ind = self.labeledData_df.at[index, 'Start Time']
		# self.sel_time_hi_ind = self.labeledData_df.at[index, 'Stop Time'] 
		



def prevLabeledSelection(self):

	if self.reviewingSelections == True and self.selectionIndex != -1 and self.selectionIndex > 0:
		
		self.selectionIndex = self.selectionIndex - 1
		
		self.updateSelectionInfo()
		self.plotSelection()
		# self.sel_index = self.selectionIndex
		# self.sel_data_classification = self.labeledData_df.at[index, 'Data Classification']
		# self.sel_lo_ind = self.labeledData_df.at[index, 'Start Index']
		# self.sel_hi_ind = self.labeledData_df.at[index, 'Stop Index'] 
		# self.sel_time_lo_ind = self.labeledData_df.at[index, 'Start Time']
		# self.sel_time_hi_ind = self.labeledData_df.at[index, 'Stop Time'] 
		
		
		
def selectedRegionPlot(self):
	
	self.labeled.setData(self.time[self.lo_ind:self.hi_ind], self.current[self.lo_ind:self.hi_ind], pen='r')
	
	
	
	
def saveSelection(self):
	if self.saveTimeStamsOnly_radioButton.isChecked() == True:
		dir = a = os.path.split(self.importFilename)[0]
		filename = f'{os.path.splitext(self.importFilename)[0]}_labeled.csv'
		
		self.labeledData_df.to_csv(filename, index = False)
		