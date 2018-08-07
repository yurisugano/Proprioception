# -*- coding: utf-8 -*-
"""
Created on Tue Aug 07 05:15:18 2018

@author: Yuri Sugano
"""

# Get directory and files to be processed
directory = raw_input('Where are the files stored?')
First_trial_number = input('ID of first subject to be analyzed: ')
Last_trial_number = input('ID of last subject to be analyzed: ')

# Manually change optional settings
Zones_to_display = 20   # Only if zones are displayed as list
Zone_radius = .5       # Radius of concentric circle

# Import needed packages
import os
import csv
import numpy as np
import pandas as pd
from collections import OrderedDict

os.chdir(directory)

# Create output files
Output_ID = {}
Stats_ID = {}
Zone_ID = {}
Conditions = ['Open','Closed']


# Loop through all the selected trials
for x in xrange(First_trial_number,Last_trial_number+1):

    # Create subject dictionaries, reset them before next loop
    SubectID = df.iloc[30,1]
    Output_subject = {}
    Stats_subject = {}
    Zone_subject = {}
    
    #Analyze both conditions for each subject            
    for condition in Conditions:
        # Load .csv file from subject
        which_file = Conditions.index(condition) + 1
        df = pd.read_csv('{}_{}.csv'.format(x,which_file))
        
        # Process Ethovision outputs to correct for subject center
        length = df.shape[0]
        temp = df.iloc[37:length, [0,2,3]]
        temp.columns = ['Time','X','Y']
        temp = temp[temp.X != '-']
        Xpos = np.array(pd.to_numeric(temp.X))
        Xpos = Xpos - Xpos[0]
        Ypos = np.array(pd.to_numeric(temp.Y))
        Ypos = Ypos - Ypos[0]
        time = np.array(pd.to_numeric(temp.Time))
        
        # Get movement from previous frame
        Xdiff = np.diff(Xpos)
        Ydiff = np.diff(Ypos)
        vector_length = np.sqrt(Ydiff ** 2 + Xdiff ** 2)
        
        # Calculate relevant metrics
        Max_up = max(Ypos)
        Max_down = min(Ypos)
        Max_right = min(Xpos)
        Max_left = max(Xpos)
        
        Range_y = np.absolute(Max_up - Max_down)
        Range_x = np.absolute(Max_right - Max_left)
        
        Total_excursion = np.sum(vector_length)
        Mean_difference_x = np.mean(Xpos)
        Mean_difference_y = np.mean(Ypos)
        distance_to_center = np.sqrt(Xpos ** 2 + Ypos ** 2)
        Mean_distance_to_center = np.mean(distance_to_center)
        
        Final_x_excursion = np.sum(Xdiff)
        Final_y_excursion = np.sum(Ydiff)
        Final_excursion = np.sqrt(Final_x_excursion ** 2 + \
                                  Final_y_excursion ** 2)
        
        Final_angle_rad = np.arctan(Final_y_excursion / Final_x_excursion)
        Final_angle_deg = np.degrees(Final_angle_rad)
        
        X_variance = np.var(Xpos)
        Y_variance = np.var(Ypos)
        
        # Calculate percentage of time in quadrants
        Q1 = sum((Xpos > 0) & (Ypos >= 0)) / float(len(Xpos))
        Q2 = sum((Xpos <= 0) & (Ypos > 0)) / float(len(Xpos))
        Q3 = sum((Xpos < 0) & (Ypos <= 0)) / float(len(Xpos)) 
        Q4 = sum((Xpos >= 0) & (Ypos < 0)) / float(len(Xpos))
        
        # Store outputs
        Output = np.column_stack((time,Xpos,Ypos))
        Output_stats = np.array([Total_excursion, Mean_difference_x, 
                                   Mean_difference_y, Mean_distance_to_center,
                                   Max_up, Max_down, Max_right, Max_left,
                                   Range_x, Range_y,
                                   Final_x_excursion, Final_y_excursion,
                                   Final_excursion, Final_angle_rad,
                                   Final_angle_deg, X_variance, Y_variance,
                                   Q1, Q2, Q3, Q4])
        
        # Calculate percentage of time in concentric zones
        # (define radius of the zones on Zone_radius on line 16)
        Zone_percentage = list()    
        for i in range (0,int(20/Zone_radius)):
            pct = sum((distance_to_center < float(i) * Zone_radius) / \
                      float(len(distance_to_center)))
            Zone_percentage.append(pct)
           
        # Organize output of raw data      
        Output_fieldnames = ['time', 'X1', 'Y1']    
        Output = {key: None for key in Output_fieldnames}
        Output['time'] = time
        Output['X1'] = Xpos
        Output['Y1'] = Ypos
  
        Output_subject[condition] = Output                 
        Output_ID['%s' %x] = Output_subject
        
        # Organize statistical outputs
        statistics = ['Excursion', 'MeanDiffX', 'MeanDiffY', 'MeanDiffCenter',
                      'MaxUp', 'MaxDown', 'MaxRight', 'MaxLeft', 'RangeX', 
                      'RangeY', 'FinalX','FinalY','FinalPos','FinalAngleRad',
                      'FinalAngleDeg', 'Xvar','Yvar','Q1','Q2','Q3','Q4']
        
        Stats = {}
        for index in range(0,15):
            Stats[statistics[index]] = round(Output_stats[index],2)
        Stats_subject[condition] = Stats
        Stats_ID[x] = Stats_subject
        
#        # Organize zone output (IF LIST)    
#        Zone = []
#        for index in range(0,len(Zone_percentage)):
#            next_zone = round(Zone_percentage[index],3)
#            Zone.append(next_zone)
#        Zone_subject[condition] = Zone[1:Zones_to_display]
#        Zone_ID[x] = Zone_subject

        # Organize zone output    
        Zone = {}
        for index in range(0,len(Zone_percentage)):
            Zone[index] = round(Zone_percentage[index],3)
        Zone_subject[condition] = Zone
        Zone_ID[x] = Zone_subject

