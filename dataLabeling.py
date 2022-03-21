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
	print('saved selected region')
	print(self.labeledData_df.head())
	
	#dataFrame = dataFrame.drop(index) to remove a row
	#dataFrame = dataFrame.reset_index(drop=True) to reset the index(the row labels)
	
	
def deleteLabeledRegion(self):
	if self.labeledData_df_selectionIndex != -1:
	
		self.labeledData_df = self.labeledData_df.drop(self.labeledData_df_selectionIndex)
		self.labeledData_df = self.labeledData_df.reset_index(drop=True)
		
		
def resaveLabledRegion(self):

	data_classification = self.DataLabels_comboBox.currentText()
	
	index = self.labelRegionSelectionIndex
	
	self.labeledData_df.at[index, 'Data Classification'] = data_classification
	self.labeledData_df.at[index, 'Start Index'] = self.lo_ind
	self.labeledData_df.at[index, 'Stop Index'] = self.hi_i
	self.labeledData_df.at[index, 'Start Time'] = self.time[self.lo_ind]
	self.labeledData_df.at[index, 'Stop Time'] = self.time[self.hi_i]

	#sort all of the labeled regions by time.
	#self.labeledData_df = self.labeledData_df.sort_values(by=['Start Index'])
	
	
	
	
def nextLabeledSelection(self):
	
	if self.selectionIndex != -1:
		self.selectionIndex = self.selectionIndex + 1
		
		index = self.selectionIndex
		data_classification = self.labeledData_df.at[index, 'Data Classification']
		lo_ind = self.labeledData_df.at[index, 'Start Index']
		hi_ind = self.labeledData_df.at[index, 'Stop Index'] 
		time_lo_ind = self.labeledData_df.at[index, 'Start Time']
		time_hi_ind = self.labeledData_df.at[index, 'Stop Time'] 
		



def prevLabeledSelection(self):

	if self.selectionIndex != -1:
		self.selectionIndex = self.selectionIndex - 1
		
		index = self.selectionIndex
		data_classification = self.labeledData_df.at[index, 'Data Classification']
		lo_ind = self.labeledData_df.at[index, 'Start Index']
		hi_ind = self.labeledData_df.at[index, 'Stop Index'] 
		time_lo_ind = self.labeledData_df.at[index, 'Start Time']
		time_hi_ind = self.labeledData_df.at[index, 'Stop Time'] 
		