# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 10:58:20 2022

@author: bpresler-marshall
"""
import numpy as np
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import glob

"""
createArray
-----------------------------------------------------------------
This function takes the name of a file, a file location and a file of administrative
information on the entire array of poles and creates a new data frame for an individual pole
by matching serial numbers between the input file and the list of serial numbers 
in the administrative file

don't ask why a function that returns a data frame is called createArray

inputs:
    filename (string): the name of an individaul csv file exported from the hobo software. 
    don't rename files, just leave them the default manner, as this picks off parts
    of the name and uses that to match the serial number information
    pathName (string): the path name of where the files are stored
    polesInfo (np array): directly read in from the spreadsheet that contains the administrative
        information about the poles (deployment dates, transect number, location, serial number). 
        check the file itself for more information
    
outputs:
    panda (data frame): data frame that describes the deployment information
        and all recorded data from the four loggers on a pole in a single frame
    

"""

def createArray(filename,pathName, polesInfo):
    myFile=filename
  #  print("myFile", myFile)
    inPath=pathName
    np_poles=polesInfo
    #open individual file
   # df2=pd.read_csv(inPath+myFile, header=1)
    df2=pd.read_csv(inPath+myFile, header=2)
    

    #pull indices
    df3=df2.T
   # print(df3.index)

    #pull serial number, this gets matched between the two files
    #this is why to not change the file names
    df_headed=pd.read_csv(inPath+myFile)
    df_headed=df_headed.T
    serialNumber=(str(df_headed.index)[22:30])

    #reformat pandas info into numpy info
    b=df2.to_numpy()
    x,y=np.shape(b)  #dimensions of new numpy array, for personal reference (x--height, y--width)

    #split numpy array to get dates and temperatures of individual mesasurments
    dates=b[:,0]
    temperatures=b[:,1]
    temperatures=np.reshape(temperatures, (x,1))
  #  print("dates", dates)
    

    #match sensor info from data with sensor info from descriptive file
    myFavoriteIndex=np.where(np_poles==int(serialNumber))[0]
    mI=int(myFavoriteIndex[0])

    #create dummy array to populate with combined info on the data and poles
    master=np.zeros((x,14))

    poleInfo=np_poles[mI,:]
    #information about the monitors on the poles, being repopulated into other array
    master[:,0]=poleInfo[0]    #serial number
    master[:,1]=poleInfo[1]    #depth
    master[:,2]=poleInfo[2]    #pole number
    depTime=str(poleInfo[3])
    master[:,3]=int(depTime.split('/')[0])  #pole deployment month
    master[:,4]=int(depTime.split('/')[1])   #pole deployment day
    master[:,5]=int(depTime.split('/')[2])  #pole deployment year
    master[:,6]=poleInfo[4]  #latitude
    master[:,7]=poleInfo[5] #longitude
    master[:,8]=poleInfo[6] #transect number


    # date handling for individal data points
    for i in range(x):
        theDate=dates[i]
        master[i,9]=int(dates[i][0:4]) #year
        master[i,10]=int(dates[i][5:7]) #month
        master[i,11]=int(dates[i][8:10]) #day
        master[i,12]=int(dates[i][11:13]) #hour
        
        
        #temperature handling
        if temperatures[i] == ' ': #if temp is messed up, make number but a weird one
           # print("you're not in kansas anymore")
            temperatures[i]=-100
        #unit conversion and writing back into main array
        thisTemp=float(temperatures[i])
        master[i,13]= thisTemp#temperatures, in F


    #convert back into dataframe
    names=['SerialNumber', 'Height', 'PoleNumber', 'DeployYear', 'DeployMonth','DeployDat','latitude', 
     'longitude', 'TrasectNumber', 'DataYear', 'DataMonth', 'DataDay', 'DataHour', 'Temperature']
    panda=pd.DataFrame(master, columns=names)
    
    #return dataframe back to main file
    return panda


"""
polePlotter
-----------------------------------------------------------------
This function takes the name of a pole, a spreadsheet of daily averages for all
poles and a desired file destination and plots the temperature profile of that pole
at all four depths (or less, if there is data missing).

inputs:
    poleNumber (float): the pole for which you want information plotted
    dailyAverages (data frame): a pandas dataframe of daily averages that has been 
    built by the makeArray function
    pathName (string): where you want the files to be saved
outputs:
    this funtion does not return any values but saves two files to the desired path:
    -CSV file: has all the logger information (administrative and data) for the 
        desired pole
    -PNG file: the temperature profile as a function of time for all four
        loggers on that particular pole

"""



def polePlotter(poleNumber, dailyAverages, pathName):
    inPath=pathName
    #pull data from DF, separate into individual logger information
    #based on depth
    pole=dailyAverages.loc[dailyAverages['PoleNumber']==float(poleNumber)]
    a=pole.loc[[1],['DeployMonth', 'DeployDat', 'DeployYear']].to_numpy()
    m=a[0][0]
    d=a[0][1]
    y=a[0][2]
    a,b,c=pole.loc[[0],['DeployMonth', 'DeployDat', 'DeployYear']]
    meter025=pole.loc[pole['Height']==float(0.25)]
    meter05=pole.loc[pole['Height']==float(0.5)]
    meter1=pole.loc[pole['Height']==float(1)]
    meter2=pole.loc[pole['Height']==float(2)]
    
    #convert into NP arrays
    meter025=meter025.to_numpy()
    meter05=meter05.to_numpy()
    meter1=meter1.to_numpy()
    meter2=meter2.to_numpy()
    
    #make plots of temperature as a function of time
    plt.figure(poleNumber)
   # plt.plot(meter025[:,12], meter025[:,13],label='0.25 meters') #blue
   # plt.plot(meter05[:,12], meter05[:,13],label='0.5 meters') #orange
   # plt.plot(meter1[:,12], meter1[:,13],label='1 meter')#green
   # plt.plot(meter2[:,12], meter2[:,13],label='shield')#red
    
   
    cmap=plt.get_cmap("Oranges")
    colors=cmap([0.25,0.5,0.75,1])
    
    
    #cropping outthe first couple of data points for each pole because we turned on the loggers
    #while they were in the office and were recording room temp not outdoor air temp. YMMV
    plt.plot(meter2[10:,12], meter2[10:,13],label='Shield', color=colors[0])#red
    plt.plot(meter1[10:,12], meter1[10:,13],label='1 m', color=colors[1])#green
    plt.plot(meter05[10:,12], meter05[10:,13],label='0.5 m', color=colors[2]) #orange
    plt.plot(meter025[10:,12], meter025[10:,13],label='0.25 m', color=colors[3]) #blue
    #plt.xlabel("Days Since %d/%d/%d" %(m, d, y))
    plt.xlabel('Date')
    plt.ylabel("Temperature (F)")
    plt.xticks([0,100,200,300],['October 2020','January 2021','April 2021','August 2021'])
    #plt.title("Pole: %d" %poleNumber)
    plt.title("Daily Temperature at Pole %d" %poleNumber)
    plt.legend(title='Sensor Depth')
   # plt.legend()
    #save plot
    plt.savefig(inPath+'temperatureProfile'+str(poleNumber)+'.png')
    
  
    
    
    #make plots of snow/no snow as a function of time--we found this to not be super helpful but you're more than 
    #welcome to uncomment it if desired.
    """
    plt.figure(poleNumber+20)
    plt.plot(meter025[:,12], meter025[:,13], label='0.25 meter temp')
    plt.plot(meter025[:,12], meter025[:,14]*30, linestyle='', marker='1', label='0.25 meter code')
    plt.plot(meter05[:,12], meter05[:,14]*30, linestyle='', marker='1', label='0.5 meter code')
    plt.plot(meter1[:,12], meter1[:,14]*30, linestyle='', marker='1', label='1 meter code')
    plt.plot(meter2[:,12], meter2[:,14]*30, linestyle='', marker='1', label='shield code')
    plt.xlabel("Days Since %d / %d / %d" %(d, m, y))
    plt.ylabel("Snow Level")
    plt.title("Pole: %d" %poleNumber)
    plt.legend()
    """
    
    
    #make csv file for catted pole
    pole.to_csv(inPath+'pole'+str(poleNumber)+'.csv')
    









