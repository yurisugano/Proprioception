# -*- coding: utf-8 -*-
"""
Created on Tue Aug 07 04:01:30 2018

@author: Yuri Sugano
"""


directory = raw_input('Where are the files stored?')
First_trial_number = input('ID of first subject to be analyzed: ')
Last_trial_number = input('ID of last subject to be analyzed: ')


import os
import csv


os.chdir(directory)

import numpy as np
import pandas as pd

# Create output files

Output_ID = {}
Stats_ID = {}
Zone_ID = {}

# Loop through all the selected trials

for x in xrange(First_trial_number,Last_trial_number+1):
    
    df_1 = pd.read_csv('{}_1.csv'.format(x))
    df_2 = pd.read_csv('{}_2.csv'.format(x))
    SubectID = df_1.iloc[30,1]
    
    # Create output for eyes open
    Condition_1 = 'Eyes Open'
    length_1 = df_1.shape[0]
    temp = df_1.iloc[37:length_1, [0,2,3]]
    temp.columns = ['Time','X','Y']
    temp = temp[temp.X != '-']
    Xpos_1 = np.array(pd.to_numeric(temp.X))
    Xpos_1 = Xpos_1 - Xpos_1[0]
    Ypos_1 = np.array(pd.to_numeric(temp.Y))
    Ypos_1 = Ypos_1 - Ypos_1[0]
    time_1 = np.array(pd.to_numeric(temp.Time))
    Xdiff_1 = np.diff(Xpos_1)
    Ydiff_1 = np.diff(Ypos_1)
    vector_length_1 = np.sqrt(Ydiff_1 ** 2 + Xdiff_1 ** 2)
    
    Max_up_1 = max(Ypos_1)
    Max_down_1 = min(Ypos_1)
    Max_right_1 = min(Xpos_1)
    Max_left_1 = max(Xpos_1)
    
    Range_y_1 = np.absolute(Max_up_1 - Max_down_1)
    Range_x_1 = np.absolute(Max_right_1 - Max_left_1)
    
    Total_excursion_1 = np.sum(vector_length_1)
    Mean_difference_x_1 = np.mean(Xpos_1)
    Mean_difference_y_1 = np.mean(Ypos_1)
    distance_to_center_1 = np.sqrt(Xpos_1 ** 2 + Ypos_1 ** 2)
    Mean_distance_to_center_1 = np.mean(distance_to_center_1)
    
    Final_x_excursion_1 = np.sum(Xdiff_1)
    Final_y_excursion_1 = np.sum(Ydiff_1)
    Final_excursion_1 = np.sqrt(Final_x_excursion_1 ** 2 + Final_y_excursion_1 ** 2)
    
    Final_angle_rad_1 = np.arctan(Final_y_excursion_1 / Final_x_excursion_1)
    Final_angle_deg_1 = np.degrees(Final_angle_rad_1)
    
    X_variance_1 = np.var(Xpos_1)
    Y_variance_1 = np.var(Ypos_1)
    
    Q1_1 = sum((Xpos_1 > 0) & (Ypos_1 >= 0)) / float(len(Xpos_1))
    Q2_1 = sum((Xpos_1 <= 0) & (Ypos_1 > 0)) / float(len(Xpos_1))
    Q3_1 = sum((Xpos_1 < 0) & (Ypos_1 <= 0)) / float(len(Xpos_1)) 
    Q4_1 = sum((Xpos_1 >= 0) & (Ypos_1 < 0)) / float(len(Xpos_1))
    
    Output_1 = np.column_stack((time_1,Xpos_1,Ypos_1))
    Output_stats_1 = np.array([Total_excursion_1, Mean_difference_x_1, 
                               Mean_difference_y_1, Mean_distance_to_center_1,
                               Max_up_1, Max_down_1, Max_right_1, Max_left_1,
                               Range_x_1, Range_y_1,
                               Final_x_excursion_1, Final_y_excursion_1,
                               Final_excursion_1, Final_angle_rad_1,
                               Final_angle_deg_1, X_variance_1, Y_variance_1,
                               Q1_1, Q2_1, Q3_1, Q4_1])
    
    Zone_percentage_5mm_1 = list()
    for i in range (0,40):
        pct = sum((distance_to_center_1 < float(i) / 2) / float(len(distance_to_center_1)))
        Zone_percentage_5mm_1.append(pct)
    
    Zone_percentage_10mm_1 = list()    
    for i in range (0,20):
        pct = sum((distance_to_center_1 < float(i)) / float(len(distance_to_center_1)))
        Zone_percentage_10mm_1.append(pct)
    
    
    
    # Create output for eyes closed
    Condition_2 = 'Eyes Closed'
    length_2 = df_2.shape[0]
    temp = df_2.iloc[37:length_2, [0,2,3]]
    temp.columns = ['Time','X','Y']
    temp = temp[temp.X != '-']
    Xpos_2 = np.array(pd.to_numeric(temp.X))
    Xpos_2 = Xpos_2 - Xpos_2[0]
    Ypos_2 = np.array(pd.to_numeric(temp.Y))
    Ypos_2 = Ypos_2 - Ypos_2[0]
    time_2 = np.array(pd.to_numeric(temp.Time))
    Xdiff_2 = np.diff(Xpos_2)
    Ydiff_2 = np.diff(Ypos_2)
    vector_length_2 = np.sqrt(Ydiff_2 ** 2 + Xdiff_2 ** 2)
    
    Max_up_2 = max(Ypos_2)
    Max_down_2 = min(Ypos_2)
    Max_right_2 = min(Xpos_2)
    Max_left_2 = max(Xpos_2)
    
    Range_y_2 = np.absolute(Max_up_2 - Max_down_2)
    Range_x_2 = np.absolute(Max_right_2 - Max_left_2)
    
    Total_excursion_2 = np.sum(vector_length_2)
    Mean_difference_x_2 = np.mean(Xpos_2)
    Mean_difference_y_2 = np.mean(Ypos_2)
    distance_to_center_2 = np.sqrt(Xpos_2 ** 2 + Ypos_2 ** 2)
    Mean_distance_to_center_2 = np.mean(distance_to_center_2)
    
    Final_x_excursion_2 = np.sum(Xdiff_2)
    Final_y_excursion_2 = np.sum(Ydiff_2)
    Final_excursion_2 = np.sqrt(Final_x_excursion_2 ** 2 + Final_y_excursion_2 ** 2)
    
    Final_angle_rad_2 = np.arctan(Final_y_excursion_2 / Final_x_excursion_2)
    Final_angle_deg_2 = np.degrees(Final_angle_rad_2)
    
    X_variance_2 = np.var(Xpos_2)
    Y_variance_2 = np.var(Ypos_2)
    
    Q1_2 = sum((Xpos_2 > 0) & (Ypos_2 >= 0)) / float(len(Xpos_2))
    Q2_2 = sum((Xpos_2 <= 0) & (Ypos_2 > 0)) / float(len(Xpos_2))
    Q3_2 = sum((Xpos_2 < 0) & (Ypos_2 <= 0)) / float(len(Xpos_2)) 
    Q4_2 = sum((Xpos_2 >= 0) & (Ypos_2 < 0)) / float(len(Xpos_2))
    Zone_percentage_5mm_2 = list()
    for i in range (0,40):
        pct = sum((distance_to_center_2 < float(i) / 2) / float(len(distance_to_center_2)))
        Zone_percentage_5mm_2.append(pct)
    
    Zone_percentage_10mm_2 = list()    
    for i in range (0,20):
        pct = sum((distance_to_center_2 < float(i)) / float(len(distance_to_center_2)))
        Zone_percentage_10mm_2.append(pct)
    
    
    Output_stats_2 = np.array([Total_excursion_2, Mean_difference_x_2, 
                               Mean_difference_y_2, Mean_distance_to_center_2,
                               Max_up_2, Max_down_2, Max_right_2, Max_left_2,
                               Range_x_2, Range_y_2,
                               Final_x_excursion_2, Final_y_excursion_2,
                               Final_excursion_2, Final_angle_rad_2,
                               Final_angle_deg_2, X_variance_2, Y_variance_2,
                               Q1_2, Q2_2, Q3_2, Q4_2])
    
    
    
    ### Organize output of raw data      
    Output_fieldnames = ['time', 'X1', 'Y1']    
    Output_open = {key: None for key in Output_fieldnames}
    Output_open['time'] = time_1
    Output_open['X1'] = Xpos_1
    Output_open['Y1'] = Ypos_1
    
    Output_closed = {key: None for key in Output_fieldnames}
    Output_closed['time'] = time_2
    Output_closed['X1'] = Xpos_2
    Output_closed['Y1'] = Ypos_2
    
    Output_subject = {'Open':Output_open, 'Closed':Output_closed}                        
    Output_ID['%s' %x] = Output_subject
    
    ### Organize statistical outputs
    statistics =['Excursion', 'MeanDiffX', 'MeanDiffY', 'MeanDiffCenter',
                 'MaxUp', 'MaxDown', 'MaxRight', 'MaxLeft', 'RangeX', 'RangeY',
                 'FinalX','FinalY','FinalPos','FinalAngleRad','FinalAngleDeg',
                 'Xvar','Yvar','Q1','Q2','Q3','Q4']
    
    Stats_open = {}
    Stats_closed = {}
    
    for index in range(0,15):
        Stats_open[statistics[index]] = round(Output_stats_1[index],2)
        Stats_closed[statistics[index]] = round(Output_stats_2[index],2)
    
    Stats_subject = {'Open': Stats_open, 'Closed': Stats_closed}
    Stats_ID['%s' %x] = Stats_subject
    
    ### Organize zone output    
    Zone_open = {}
    Zone_closed = {}
    
    for index in range(0,40):
        Zone_open['Z%s' %index] = round(Zone_percentage_5mm_1[index],3)
        Zone_closed['Z%s' %index] = round(Zone_percentage_5mm_2[index],3)
    
    Zone_5mm_subject = {'Open': Zone_open, 'Closed': Zone_closed}
    Zone_ID['%s' %x] = Zone_5mm_subject
