# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 09:31:46 2022

@author: bpresler-marshall

This work is licensed under a Creative Commons Attribution-NonCommercial-
ShareAlike 4.0 International License.


~~~~~~~~~~~~~~~~~ READ ME ~~~~~~~~~~~~~~~~~ 
Welcome to the python processing set up for the minimalist snowpack monitoring
array currently (as of May 2022) deployed in Hoonah. This is set up to take 
files directly exported from the HOBO Pendant MX Temp loggers used on our
monitoring poles and turn that data into a variety of plots. 

In order for this to work, some user changes are required and your data needs 
to be set up correctly. Lines that must be changed are commented with a 
#CHANGE ME. They mostly describe file naming conventions, your particular file
names and date ranges of interest. 

Inputs
    CSV Files
        *This is set up to work with the file structure directly exported from 
        the HOBO app. It can be adjusted, but please do so at your own risk
        *Please do not rename files that have exported from the HOBO app--
        parts of the file name are used to match the data with that sensor's 
            biographical information (elevation, lat, long, deployment date, etc). 

        *You must have a pole information csv file (refered to as Poles.csv in 
        this document) that contains the following information in order: 
            Serial Number	Height	PoleNumber	DeployDate	latitude	
            longitude	TrasectNumber	Elevation
            If you are missing any of that information, enter 0 or 01/01/2020 
            if it's the date category
            It doesn't damage anything to add additional notes to the right of 
            those columns; they're ignored by the script. We have a column 
            indicating which poles/sensors
            have been damaged by bears or other environmental factors, but feel 
            free to change that to suit your needs.
        *Check the file structure before you begin and make sure that your 
        files are where the program wants them to be. 
            You should have the two .py files and the Poles Information (.csv) 
            in your main working directory. In a subdirectory, you should have 
            all of your data files exported directly from the HOBO loggers. 
            You can export HOBO data into various kinds of excel files, please
            choose the standard .csv and not one of the .xlsx file types (or be
            prepared to edit the line that tells the program which file types
            to read).

    Python Files
        *You should have two .py files in order to run this code: 
            PoleProcessing.py (this file) as well as a functions.py file. They
            must be kept in the same directory (one level up from the collection)
            of data files.


Outputs
This creates a variety of plots (.png) and tables(.csv) files to help you better 
understand your data. Below is a brief description of each file it makes and 
the contents therein. Please feel free to rename the files however you please, 
csv files are all created on lines that read 
someArrayName.to_csv(inPath+'FILENAMEHERE.csv'). Plots are saved with the line 
plt.savefig(inPath +'FILENAME'+'.png'). For those unfamiliar with Python, leave 
the quotation marks in there.

Biographical Information in this context refers to the information contained 
in the Poles.csv files that describes where the poles are and which sensors 
are on each pole.


combinedData.csv: This is the master file that has all of the data for all 
    of the poles on all the dates (hence why it is referred to as LargeFrame as a 
    variable name).
    It has the biographical information of the pole 
    (lat, long, deployment info, etc), the date and hour on which a particular
    data point was recorded and the temperature. This file is created BEFORE 
    the snow/no snow coding.It's just raw data in a different format before
    any of the math is inflicted on it.

dailyAverages.csv: This file is a direct product of the combinedData.csv file 
    but with a few notable changes.
    The temperature is now referring to the average over a 24 hour period.
    The variance is calculated through the numpy package, it is a measure of how 
    much the temperature varies over a 24 hour period (lower variance = smaller 
    daily change).
    The snowNoSnow column is an indicator of no (0) or yes (1) for the presence 
    or absence of snow at that sensor depth on the particular pole. More 
    information about how the snow-no-snow determination and several options
    for the calculations are given in Section Three. More information about the 
    choices we made in the coding and why is available from the literature 
    references. 
    
poleXXXX.csv: a subset of the dailyAverages array for each pole number
     The XXXX indicates the pole number and is set automatically. The column 
     names and contents are the same as the dailyAverages.csv file
    
depths.csv: File that indicates the presence or absence of snow at each sensor 
    for each date that there was data recorded. The majority of the columns 
    follow previous convention, with the exception of the last four 
    (025mYN, 05N, 1mYN and 2mYN) Those columns are yes (1) or no (0) snow 
    recorded at that sensor depth for the indicated pole on every date
    
summary.csv: Summary file displays the snow coverage information for each pole 
    on a given winter.
    Pole Number
    Deployment Day, Month and Year: three columns, one for each part of the date
    Latitude, Longitude: pair of floats pulled from the pole biographical 
        information csv file
    Transect Number: float pulled from the pole biographical information csv file
    firstYMD025, lastYMD025, duration025: the first date snow appears at 0.25 
        meters for a particular pole, the last date there is snow present, and 
        the length of time between those dates
    firstYMD05, lastYMD05, duration05: same as above but for 0.5 meter sensor
    firstYMD1, lastYMD1, duration1: same as above but for 1 meter sensor
    firstYMDshield, lastYMDshield, durationshield: same as above but for the 
        sensor at the shield depth
    
temperatureProfileXXXX.png: the temperature profile in Fahrenheit for each of 
the four sensors on a pole for the duration of their deployment
    the XXXX is automatically set to be the pole number
    The axis labels must be set manually based on the range of your data
    
snowCoverageProfileXXXX.png: the snow coverage profile in meters for each pole.
    As above, the XXXX is automatically set to be the pole number and axis 
    labels must be set manually
       
snowCoverageSummary.png: bar chart that describes the duration of snow coverage 
    for each pole and each of the four sensors on it.
    It does not account for thawing during the season. 
    snowCoverageSummaryBinned.png is a similar version of the plot that just 
    the 0.25 meter data (or whatever your lowest sensor depth is).
    

    




Literature References: These are the sources used to design the poles in the 
    first place and to provide context for our methodology. 
    PDFs are available upon request from the HIA Environmental Office.
    
    Evaluation of Miniature Temperature-loggers to Monitor Snowpack
    Evolution at Mountain Permafrost Sites, Northwestern Canada (2008)
    by Antoni G. Lewkowicz

    Responses of white spruce (Picea Glauca) to experimental warming 
    at a subarctic alpine treeline (2007)
    by Ryan Danby and David Hik
    
    Analysis of continuous snow temperature profiles from automatic weather 
    stations in Aosta Valley (NW Italy):
    Uncertainties and applications
    by G. Filippa et al. (2012)

Python Things that May be Useful: you shouldn't technically need any of this 
    to make the program run, but may be useful if you wish to make changes:
        
    Anaconda downloader to run python if you don't already have it set up:
    https://anaconda.org/anaconda/python
    
    datetime data type documentation
    https://docs.python.org/3/library/datetime.html

    matplotlib (how the plots are made) cheat sheet
    https://matplotlib.org/cheatsheets/
    
    Pandas Info (this is how the dataframes work)
    https://pythonbasics.org/pandas-dataframe/
    
    A couple of numpy links--this handles the math and many of the data formatting tasks. 
    variance: https://numpy.org/doc/stable/reference/generated/numpy.var.html
    arrays: https://www.w3schools.com/python/numpy/numpy_intro.asp
"""




"""
Section One: Imports, Path Names, Docs and other Administrative Tasks
"""

#import various packages--not all of these are technically used and some are just along for the ride
import numpy as np
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import glob
from functions import *
from matplotlib import cm
from mpl_toolkits import mplot3d
import scipy as sp
from datetime import date
print("All packages loaded. You are cleared to proceed.")
print("If the IDE complains about unimported packages, check the functions.py file; they might be in there.")


#CHANGE ME: define path name--this is the path to the subdirectory where your csv datafiles (the ones directly exported from HOBO) live
inPath = r'C:\Users\bpresler-marshall\OneDrive - Hoonah Indian Association\SnowPack Things\Data_2021\CSVFiles'




"""
Section Two: Making the master dataFrame/spreadsheet that has all of the raw data concatinated together
"""
print("Loading Files. Please be patient.")
#these names will be used in the master Pandas dataframe
names=['SerialNumber', 'Height', 'PoleNumber', 'DeployYear', 'DeployMonth','DeployDat','latitude', 
 'longitude', 'TrasectNumber', 'DataYear', 'DataMonth', 'DataDay', 'DataHour', 'Temperature']


#set up poles data frame
#this has serial number, depth, pole number, location and deployment date in that order
#requires transposing to make Pandas happy about how the data is being read

#CHANGE ME--poleFile should be whatever you've named your .csv file that has the pole biographical inforamtion. Keep the quotes around it. 
poleFile='Poles.csv'
poles_df = pd.read_csv(poleFile)
p2=poles_df.T
indexes=p2.index
#reformat to numpy  from pandas
np_poles=poles_df.to_numpy()

#set up list of files to look in
fileList=[]
#make set of files to loop through--for each .csv file in your collection, add it to the list
for file in glob.glob(inPath+'\*.csv', recursive=True):
    fileList.append(file)
    
#create the big cheese of data frames (this will eventually become the combinedData.csv file described in the README file)
#the myDF line is why you shouldn't rename the files after exporting them from HOBO. The [-42:] cuts the sensor number and is expecting that number to be in a particular location.
largeFrame=pd.DataFrame(columns=names)  
for i in range(len(fileList)): #for each file in your list
    myFile=fileList[i] 
    myDF=createArray(myFile[-42:], inPath, np_poles) 
    largeFrame=largeFrame.append(myDF)



#save all of the combined data and the information about the pole/sensor it came from into one massive csv file
#if you'd like to rename this, feel free to do so, a different name won't break anything (or shouldn't anyway)
#more information about the contents of the CombinedData file can be found in the README section of this file
largeFrame.to_csv(inPath+'CombinedData.csv')
print("CombinedData.csv has been created.")



"""
Section Three: Making daily averages and adding initial coding of the snow/no snow parameter
"""

#new names for daily averages data frame
averageNames=['SerialNumber', 'Height', 'PoleNumber',  'DeployMonth','DeployDat','DeployYear','latitude', 
 'longitude', 'TrasectNumber', 'DataYear', 'DataMonth', 'DataDay', 'DaySince','Temperature','snowNoSnow', 'dailyVariance', 'Datayyyymmdd']

#initialize empty frame-- this will eventually become the dailyAverages.csv file described in the README section above
dailyAverages=pd.DataFrame(columns=averageNames)
#make daily averages for each sensor and code snow no snow
#for i in range(2):                     #version for testing
for i in range(len(fileList)):        #version for working--loop over each of the csv files in your collection
    thisSensor=fileList[i][-38:-30] #cut out serial number
    thisSensorData=largeFrame.loc[largeFrame['SerialNumber']==float(thisSensor)] #find the data that corrolates with your sensor of interest by matching serial numbers
    #thisSensorData.to_csv(inPath+'thisSensorData.csv')
    thisSensorData=thisSensorData.to_numpy()
    a,b=np.shape(thisSensorData) #shape of the array, for later reference
    
    myArray=np.zeros(((int(a/24))+1,len(averageNames))) #set up array that is (number of days+1) by (number of columns/names)
    day=0
    dailyTemp=0
    tempsRun=[]
    
    #for each hour of data, get the temp and add to the running total for the day
    for j in range(a):
        hour=thisSensorData[j][12]
        temp=thisSensorData[j][13]
        dailyTemp+=temp
        tempsRun.append(temp)
        
        if np.mod(j,24)==0: #every 24 hours, cutting at midnight
            #pull dates
            yyyy=str(int(thisSensorData[j,9]))
            mm=int(thisSensorData[j,10])
            dd=int(thisSensorData[j,11])
            
          #  print('yyyy', yyyy)
          #  print('mm', mm)
          #  print('dd', dd)
            
            #if the day or month is in the single digits, add a leading zero to make the date formatter happy later on
            if mm <= 9:
                mm="0"+str(mm)
            if dd <= 9:
                dd="0"+str(dd)
            
            #create the yyyymmdd format and add to array
            ymd=yyyy+str(mm)+str(dd)
            myArray[day][16]=ymd
            
            
           #calculate daily average temperature
            aveTemp=dailyTemp/24
            myArray[day][13]=aveTemp
            myArray[day,0:12]=thisSensorData[j,0:12] #copy most of the contents of the df to carry along the records
            myArray[day][12]=day
           # print('day',day)
            #calculate variance for the day
            variance=np.var(tempsRun)
            myArray[day][15]=variance
            
              
              
            #coding for the snow versus no snow column
            # you've got some options here, so feel free to change which line is uncommented depending on how you want to estimate the snow coverage
            #the first version is the most conservative, and is probably an over estimate of the amount of snow
            #the second version is the recommended one
            #the third version has the tightest restrictions on what counts as snow coverage
            
            #if variance <1.5 and variance >0 and aveTemp<=35.6 and aveTemp>=28.4:  #most conservative version +pm 2 C
            if variance <1 and variance >0 and aveTemp<=33 and aveTemp>=29.3:
           # if variance <1 and variance >0 and aveTemp<=33 and aveTemp>=30:
               
                myArray[day][14]=1
            else:
                myArray[day][14]=0
                  
        
            #over write variables to prepare them for use the next day
            dailyTemp=0
            day=day+1
            tempsRun=[]
            
            
                        
    
    #convert array into df (just unit conversion between numpy and pandas)
    thisAverage=pd.DataFrame(myArray, columns=averageNames)
    #append to daily averages frame
    dailyAverages=dailyAverages.append(thisAverage)
    
    
#make gigantic csv file
#more information about the contents of the DailyAverages file can be found in the README section of this file
dailyAverages.to_csv(inPath+'DailyAverages.csv')
print("DailyAverages.csv has been created.")

#plot that stuff up: this makes the temperature profile for each pole (all four sensors) as a function of time. 
#the dates on the axises must be manually set in the functions.py file. 
polePlotter(14,dailyAverages,inPath)
print("The temperature profiles for each pole have been created.")

"""
Section Four: calculate depth for each day at each of the poles and make that into one
large csv and dataframe
"""

#list of pole numbers, omiting pole 2 which has vanished 
poleList=[1,3,4,5,6,7,8,9,10,11,12,13,14]

#hardcoded in version, technically this should be in the poleInformation file as well
elevations=[424,380,238,270,294,493,390,293,248,287,357,267,382,321]

#new names for data frame that will describe snow depth on each date for each pole
snowCoverNames=['PoleNumber',  'DeployMonth','DeployDat','DeployYear','latitude', 
 'longitude', 'TrasectNumber', 'DataYear', 'DataMonth', 'DataDay', 'depth', 'YYYYMMDD', 'elevation']

a,b=np.shape(dailyAverages)
#initalize empty frame and some blank variables
#setting each of the snow codes to zero means the default is to assume no snow and must later be proven otherwise
snow=pd.DataFrame(columns=snowCoverNames)
snow['025mYN']=0
snow['05N']=0
snow['1mYN']=0
snow['2mYN']=0

#for each of the poles in your array
for i in range(len(poleList)):

    #get the data for the pole you're talking about
    thisPole=poleList[i]
    thisPoleData=dailyAverages.loc[dailyAverages['PoleNumber']==float(thisPole)]
    thisElevation=elevations[i]
    
   # break a pole's worth of information apart into its constituent sensors
   #there's a lot of unit conversion here to make numpy happy as well
    pole=thisPoleData
    meter025=pole.loc[pole['Height']==float(0.25)]
    meter05=pole.loc[pole['Height']==float(0.5)]
    meter1=pole.loc[pole['Height']==float(1)]
    meter2=pole.loc[pole['Height']==float(2)]

    meter025=meter025.to_numpy()
    meter05=meter05.to_numpy()
    meter1=meter1.to_numpy()
    meter2=meter2.to_numpy()
   
    
    a,b=np.shape(meter025)
    c,d=np.shape(meter05)
    e,f=np.shape(meter1)
    g,h=np.shape(meter2)
    
   
   #force sizes of sensor read outs to be the same for each sensor on a pole--this deals with missing or damaged data from one or more sensors on a pole.
    maxLength=np.max([a,c,e,g]) #find the maximum data range of any sensor on a particular pole
   
    if a!=maxLength:                            #if array for 025 meter is too small
        diff=np.abs(maxLength-a)
        pads=np.zeros((diff,b))
        meter025=np.concatenate((meter025,pads))
    if c!=maxLength:                             #if array for 05 meter is too small
        diff=np.abs(maxLength-c)
        pads=np.zeros((diff,b))
        meter05=np.concatenate((meter05,pads))
    if e!=maxLength:                             #if array for 1 meter is too small
        diff=np.abs(maxLength-e)
        pads=np.zeros((diff,b))
        meter1=np.concatenate((meter1,pads))
    if g!= maxLength:                            #if array for the shield is too small
        diff=np.abs(maxLength-g)
        pads=np.zeros((diff,b))
        meter2=np.concatenate((meter2,pads))
    
    #this will eventually be populated with the depths for each date for an individual pole
    snowCoverArray=np.zeros((maxLength,len(snow.columns)))
    
    thisPoleData=thisPoleData.to_numpy()
    #loop over each date of data
    depth=0 #assume no snow until prove otherwise
    for j in range(np.max([a,c,e,g])): #for each date on each pole:
    #for j in range(10):
        #copy and paste most information from the daily averages pole into this frame. It's lat, long, obs days, pole number etc
        #all the sort of header stuff
        snowCoverArray[j,0:10]=thisPoleData[j,2:12]
        depth=0
        snowCoverArray[j,13]=0
        
        
        #calculate snow depth by elif-fing over each potential depth to see if they've thrown a YES snow code
        if meter025[j,14]==1:
            depth=0.25
            snowCoverArray[j,13]=1 #through code for 25 meter
            
        if meter05[j,14]==1 and meter025[j,14]==1:
            depth=0.5
           # snowCoverArray[j,13]=1
            snowCoverArray[j,14]=1  #code of 25 and 05 meter being covered
        if meter1[j,14]==1 and meter025[j,14]==1 and meter05[j,14]==1:
            depth=1
           # snowCoverArray[j,13]=1 #code for 1 meter, 0.5 and 0.25 being covered
           # snowCoverArray[j,14]=1
            snowCoverArray[j,15]=1
            
            
        if meter2[j,14]==1 and meter1[j,14]==1 and meter025[j,14]==1 and meter05[j,14]:
            depth=2
          #  snowCoverArray[j,13]=1 #throw codes for all four sensors being covered
          #  snowCoverArray[j,14]=1
           # snowCoverArray[j,15]=1            
            snowCoverArray[j,16]=1
        
        
        #record said depth
        snowCoverArray[j,10]=depth
        
        
        #date formatting to make datetime happy later on
        #is it pretty? no. does it work? I hope so.
        YYYY=str(int(thisPoleData[j,9]))
        MM=int(thisPoleData[j,10])
        DD=int(thisPoleData[j,11])
        
        if MM <= 9:
            MM="0"+str(MM)
        if DD <= 9:
            DD="0"+str(DD)
        
        YYYYMMDD=YYYY+str(MM)+str(DD)
        snowCoverArray[j,11]=YYYYMMDD
        snowCoverArray[j,12]=thisElevation
        
        
    #append this poles depth to the large array and do some unit conversion between numpy and pandas
    cover=pd.DataFrame(snowCoverArray, columns=snow.columns)
    snow=snow.append(cover)
    
#make gigantic csv file
depths=snow
snow=snow.to_numpy()
depths.to_csv(inPath+'depths.csv')
print("depths.csv has been created.")









"""
Section Five Make a little summary table of when the snow appeared at each depth at each pole
this does nothing to address any thawing and refreezing events throughout the winter

This is also the bit that makes the snow duration plots
"""

#CHANGE ME: select your own date range of which winter of data you want to look at. Date format should be YYYYMMDD.
#select dates before what you think the first snow is and after when you think the spring melt off is for your region of interest.
winterStart=20201001     # dates defining the winter of 2020-2021
winterEnd=20210631

#winterStart=20191001    #dates definining the winter of 2019-2020
#winterEnd=20200631




#function to get the number of days between two dates
#inputs: ymd1 and ymd2 must be floats in the yyyymmdd format (so that December 4, 2020 would be 20201204, for example)
#outputs: a duration in days between ymd1 and ymd2 that accounts for the different lengths of months and things like that
#returns: an integer number of days
def numOfDays(ymd1,ymd2):
    #if there are in fact non zero dates
    if ymd1!=0 and ymd2!=0:
        date1=date(int(str(ymd1)[0:4]), int(str(ymd1)[4:6]), int(str(ymd1)[6:8]))
        date2=date(int(str(ymd2)[0:4]), int(str(ymd2)[4:6]), int(str(ymd2)[6:8]))
    #if the dates are messed up (for example, if the poles didn't freeze over or the data is just missing), hardcode the dates to be january 1, 2020 
    #this is just so that the formatting is alright so that it can return a duration of zero days without panic
    else:
        date1=date(2020,1,1)
        date2=date(2020,1,1)
    return (date2-date1).days



#list of pole numbers, omiting pole 2 which has vanished 
#pole 15 removed from analysis because we don't actually know where it is
#CHANGE ME: this is a hardcoded way to omit certain poles from your analysis if there is something wrong with the data or if it's missing
#for example, we chose to omit pole 2 because the data on it was not retrieved during the last field season
#and pole 15 because we have the data but the location information was inaccurate. 
#which poles you choose to include in your processing is completely up to you--it could be the whole list or just a partial set.
poleList=[1,3,4,5,6,7,8,9,10,11,12,13,14]    #complete-sh version
#poleList=[1,3,4,5,6,7,8,9]                  #deployed in 2019 version

#this makes the temperature profiles for each pole as well as a .csv file that has the dailyAverages information but only for that one pole
#your computer may complain about polePlotter not existing, it's alive and well in the functions.py file.
for i in poleList:
    polePlotter(i, dailyAverages,inPath)
print("The temperature profiles for each pole have been created.")


#new names for summary data frame
summaryNames=['PoleNumber',  'DeployMonth','DeployDat','DeployYear','latitude', 
 'longitude', 'TrasectNumber', 'firstYMD025','lastYMD025','duration025', 
                                 'firstYMD05','lastYMD05','duration05'
                                 , 'firstYMD1','lastYMD1','duration1', 
                                 'firstYMDshield','lastYMDshield','durationshield', 'Elevation']

#initialize empty frame--this will later have all of the information described by summaryNames in it
summaryArray=np.zeros((len(poleList), len(summaryNames)))
#loop over each logger to find when it detected snow
for i in range(len(poleList)):
    #set up data frame--pull the info you want out of daily averages by SN
    thisPoleData=depths.loc[depths['PoleNumber']==float(poleList[i])]
    #thisSensorData=thisSensorData.loc[thisSensorData['DataYear']!=2019]
    
    
    #unit conversion
    thisPoleData=thisPoleData.to_numpy()
    a,b=np.shape(thisPoleData)
    averages=dailyAverages.to_numpy()
    
    
    summaryArray[i,0:7]=thisPoleData[i,0:7] #copy biographic information about pole (latitude, longitude, etc)
    summaryArray[i,19]=thisPoleData[i,12] #elevation gets moved over separately because this script was written by an idiot
    
    #loop over every data point for a particular pole, all sensors
    for j in range(a):

        t=np.where(thisPoleData[:,13]==1) #IS THERE SNOW AT 0.25 METERS
        b=t[0]  #this is just to handle nonsense with tuples
        chillDatesWithSnow025=[]
        for k in range(len(t[0])): #for each date where there is snow
            #see if the date for the yeah snow code is within the desired range
            thisDate=thisPoleData[b[k],11]
            if winterStart <=thisDate and thisDate <= winterEnd: #if the date is in the desired range
                chillDatesWithSnow025.append(thisDate)
                
        
        
        #first day of snow, last day of snow, duration of snow depth
        #dates in the yyyymmdd format (floats)
        summaryArray[i][7]=chillDatesWithSnow025[0]
        summaryArray[i][8]=chillDatesWithSnow025[-1]
        summaryArray[i][9]=numOfDays(chillDatesWithSnow025[0],chillDatesWithSnow025[-1])
        
 
        t=np.where(thisPoleData[:,14]==1) #IS THERE SNOW AT 0.5 METERS
        b=t[0]  #this is just to handle nonsense with tuples
        chillDatesWithSnowHalf=[]
        for k in range(len(t[0])): #for each date where there is snow
            #see if the date for the yeah snow code is within the desired range
            thisDate=thisPoleData[b[k],11]
            if winterStart <=thisDate and thisDate <= winterEnd:
              
                chillDatesWithSnowHalf.append(thisDate)
                
        #if the pole never froze over or the data is just missing--hard code in zeros
        if len(chillDatesWithSnowHalf) !=0:
            summaryArray[i][10]=chillDatesWithSnowHalf[0]
            summaryArray[i][11]=chillDatesWithSnowHalf[-1]
            summaryArray[i][12]=numOfDays(chillDatesWithSnowHalf[0],chillDatesWithSnowHalf[-1])
        else:
            summaryArray[i][10]=0
            summaryArray[i][11]=0
            summaryArray[i][12]=0
        

        t=np.where(thisPoleData[:,15]==1) #IS THERE SNOW AT ONE METER
        b=t[0]  #this is just to handle nonsense with tuples
        chillDatesWithSnowOne=[]
        for k in range(len(t[0])): #for each date where there is snow
            #see if the date for the yeah snow code is within the desired range
            thisDate=thisPoleData[b[k],11]
            if winterStart <=thisDate and thisDate <= winterEnd:
              #  print("thisDate: ", thisDate)
                chillDatesWithSnowOne.append(thisDate)
                
        
        #if the pole never froze over or the data is just missing--hard code in zeros
        if len(chillDatesWithSnowOne)!=0:
            summaryArray[i][13]=chillDatesWithSnowOne[0]
            summaryArray[i][14]=chillDatesWithSnowOne[-1]
            summaryArray[i][15]=numOfDays(chillDatesWithSnowOne[0],chillDatesWithSnowOne[-1])
        else: 
            summaryArray[i][13]=0
            summaryArray[i][14]=0
            summaryArray[i][15]=0
        
      
        t=np.where(thisPoleData[:,16]==1) #IS THERE SNOW AT THE SHIELD DEPTH
        b=t[0]  #this is just to handle nonsense with tuples
        chillDatesWithSnowShield=[]
        for k in range(len(t[0])): #for each date where there is snow
            #see if the date for the yeah snow code is within the desired range
            thisDate=thisPoleData[b[k],11]
            if winterStart <=thisDate and thisDate <= winterEnd:
               # print("thisDate: ", thisDate)
                chillDatesWithSnowShield.append(thisDate)
                
        
        #if the pole never froze over or the data is just missing--hard code in zeros
        if len(chillDatesWithSnowShield) !=0:
            summaryArray[i][16]=chillDatesWithSnowShield[0]
            summaryArray[i][17]=chillDatesWithSnowShield[-1]
            summaryArray[i][18]=numOfDays(chillDatesWithSnowShield[0],chillDatesWithSnowShield[-1])
        else:
            summaryArray[i][16]=0
            summaryArray[i][17]=0
            summaryArray[i][18]=0
            
            
        
#make gigantic csv file that has the summary info in it
summary=pd.DataFrame(summaryArray, columns=summaryNames)
summary.to_csv(inPath+'summary.csv')
print("summary.csv has been created.")
      




#function that gets a yyyymmdd into a python datetime variable
#theFloatandtheFurious must be a float of the date in question with four digits for the year
#two digits for the month and two digits for the day
#if you've got single digit numbers (it Jan 1, it must be 0101 and not 11)
#returns date1, which is a datetime variable (more info on those for the curiously-minded is available in the Python resources of the README section)

def mrSandManMakeMeSomeSand(theFloatandtheFurious):
    
        date1=date(int(str(theFloatandtheFurious)[0:4]), int(str(theFloatandtheFurious)[4:6]), int(str(theFloatandtheFurious)[6:8]))
        return date1

miniA, miniB, miniC, miniD =np.min(summaryArray[:,7]), np.min(summaryArray[:,10]), np.min(summaryArray[:,13]),np.min(summaryArray[:,16]) #first date that there is snow anywhere on the ground
elevations025, elevations05, elevations1, elevationsS = [],[],[],[] #itialize blanks to later be filled
maxiA=np.max(summaryArray[:,8]) #the last day that there was snow at 025 meters anywhere in the basin
startDates025=[] #more initialization
#for each pole in the pole list, figure out the range based on the start date and duration, this is just cutting them up to get it right for plotting
for i in range(len(poleList)):
    elevations025.append(numOfDays(miniA, summaryArray[i,7]))
    elevations05.append(numOfDays(miniA, summaryArray[i,10]))
    elevations1.append(numOfDays(miniA, summaryArray[i,13]))
    elevationsS.append(numOfDays(miniA, summaryArray[i,16]))
    
    #get dates in the right order and convert from floats to python datetimes
    startDates025.append(mrSandManMakeMeSomeSand(summaryArray[i,7]))




#this stuff is how you change the axis on the plot
poleList=np.array(poleList)
#xtick=[1,2,3,5,7,9,11,13] #this determines where the labels go on the x axis
xtick=np.linspace(1,13,13)
#xlabels=["Pole 1", 'Pole 4', 'Pole 6','Pole 8','Pole 10','Pole 12','Pole 14'] # this determines what the labels ARE on the x axis
xlabels=["Pole 4", "Pole 10",'Pole 13','Pole 5', 'Pole 11','Pole 9','Pole 6','Pole 12','Pole 3','Pole 14','Pole 8','Pole 1','Pole 7']
ytick=[0,60,120,180,240] #locations for y axis labels
ylabels=['Oct. 2020', 'Dec. 2020','Feb. 2021','Apr. 2021', 'Jun. 2021'] #what the y axis labels are

cmap=plt.get_cmap("Oranges") #set color range and scale
colors=cmap([0.25,0.5,0.75,1])

#CHANGE ME: make this count up to n, where n is the number of poles you're interested in (we had 15 poles but omitted two from analysis, so it counts to 13)
xs=np.array([1,2,3,4,5,6,7,8,9,10,11,12,13]) #hard-coded version of where to put the bars 
#xs=np.array([1,2,3,4,5,6,7,8]) #this version is for the winter of 2019 when there were fewer poles

#depth at each sensor for the 2020 winter
plt.figure(99)
summaryArray=summary.sort_values(by=['Elevation']).to_numpy() #sort by elevation
plt.bar(xs,summaryArray[:,9], bottom=elevations025, width=0.2,color=colors[0], label='0.25 m')      #this one is the lightest orange
plt.bar(xs+0.2,summaryArray[:,12], bottom=elevations05, width=0.2,color=colors[1],label='0.5 m')
plt.bar(xs+0.4,summaryArray[:,15], bottom=elevations05, width=0.2 ,color=colors[2],label='1 m')
plt.bar(xs+0.6,summaryArray[:,18], bottom=elevations05, width=0.2,color=colors[3],label='Shield')   #this one is the darkest orange
plt.xticks(xtick, xlabels, rotation=45)
plt.yticks(ytick,ylabels)
plt.legend(title='Sensor Depth',loc='lower right', fontsize=7, title_fontsize=7.5)
plt.title("Snow Coverage Throughout the Year as a Function of Elevation")
plt.savefig(inPath+'snowCoverageSummary.png')
print("snowCoverageSummary.png has been created.")




#just minimum snow depth plot--ie just the 025 meter data but with wider bars so it doesn't look so weird
#this is the monochrome version
#xs=np.array([1,2,3,4,5,6,7,8,9,10,11,12,13])
plt.figure(100)
summaryArray=summary.sort_values(by=['Elevation']).to_numpy()
plt.bar(xs,summaryArray[:,9], bottom=elevations025, width=0.8,color=colors[2], label='0.25 m')
plt.xticks(xtick, xlabels)
plt.yticks(ytick,ylabels)
plt.title("Snow Coverage Throughout the Year")
plt.savefig(inPath+'snowCoverageSummaryBinned.png')







'''
FOR PERSONAL USE
'''


#plot of 2019-2020 winter


#this stuff is how you change the axis on the plot
poleList=np.array(poleList)
xtick=[1,2,3,4,5,6,7,8] #this determines where the labels go on the x axis
xlabels=["Pole 4", 'Pole 5', 'Pole 9','Pole 6','Pole 3','Pole 8','Pole 1','Pole 7'] # this determines what the labels ARE on the x axis
ytick=np.linspace(0,7,8)*(160/7) #locations for y axis labels
ylabels=['Nov. 2019', 'Dec. 2019','Jan. 2020','Feb. 2020','Mar. 2020', 'Apr. 2020', 'May 2020','Jun. 2020'] #what the y axis labels are

cmap=plt.get_cmap("Oranges") #set color range and scale
colors=cmap([0.25,0.5,0.75,1])

#CHANGE ME: make this count up to n, where n is the number of poles you're interested in (we had 15 poles but omitted two from analysis, so it counts to 13)
#xs=np.array([1,2,3,4,5,6,7,8,9,10,11,12,13]) #hard-coded version of where to put the bars 
xs=np.array([1,2,3,4,5,6,7,8])

#depth at each sensor for the 2020 winter
plt.figure(100)
summaryArray=summary.sort_values(by=['Elevation']).to_numpy() #sort by elevation
plt.bar(xs,summaryArray[:,9], bottom=elevations025, width=0.2,color=colors[0], label='0.25 m')      #this one is the lightest orange
plt.bar(xs+0.2,summaryArray[:,12], bottom=elevations05, width=0.2,color=colors[1],label='0.5 m')
plt.bar(xs+0.4,summaryArray[:,15], bottom=elevations05, width=0.2 ,color=colors[2],label='1 m')
plt.bar(xs+0.6,summaryArray[:,18], bottom=elevations05, width=0.2,color=colors[3],label='Shield')   #this one is the darkest orange
plt.xticks(xtick, xlabels)
plt.yticks(ytick,ylabels)
plt.legend(title='Sensor Depth',loc='lower right', fontsize=7, title_fontsize=7.5)
plt.annotate

plt.title("Snow Coverage Throughout the Year as a Function of Elevation")
#plt.savefig(inPath+'snowCoverageSummary.png')
print("snowCoverageSummary.png has been created.")



#just minimum snow depth plot--ie just the 025 meter data but with wider bars so it doesn't look so weird
#this is the monochrome version
#xs=np.array([1,2,3,4,5,6,7,8,9,10,11,12,13])
plt.figure(100)
summaryArray=summary.sort_values(by=['Elevation']).to_numpy()
plt.bar(xs,summaryArray[:,9], bottom=elevations025, width=0.8,color=colors[2], label='0.25 m')
plt.xticks(xtick, xlabels)
plt.yticks(ytick,ylabels)
plt.title("Snow Coverage Throughout the Year")
plt.savefig(inPath+'snowCoverageSummaryBinned.png')









'''
Personal reference zone: can we ascertain anything about the temperature profile as a function of depth
'''


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

    xa=50
    xb=150
    #cropping outthe first couple of data points for each pole because we turned on the loggers
    #while they were in the office and were recording room temp not outdoor air temp. YMMV
    plt.plot(meter2[xa:xb,12], meter2[xa:xb,13],label='Shield', color=colors[0])#red
    plt.plot(meter1[xa:xb,12], meter1[xa:xb,13],label='1 m', color=colors[1])#green
    plt.plot(meter05[xa:xb,12], meter05[xa:xb,13],label='0.5 m', color=colors[2]) #orange
    plt.plot(meter025[xa:xb,12], meter025[xa:xb,13],label='0.25 m', color=colors[3]) #blue
    #plt.xlabel("Days Since %d/%d/%d" %(m, d, y))
    plt.xlabel('Date')
    plt.ylabel("Temperature (F)")
    plt.ylim(30,35)
   # plt.xticks([0,100,200,300],['October 2020','January 2021','April 2021','August 2021'])
    #plt.title("Pole: %d" %poleNumber)
    plt.title("Daily Temperature at Pole %d" %poleNumber)
    plt.legend(title='Sensor Depth')
   # plt.legend()
    #save plot
    plt.savefig(inPath+'temperatureProfile'+str(poleNumber)+'.png')

polePlotter(6,dailyAverages,inPath)































"""
Section Six: Misc. Plots

We didn't consider any of these plots essential for our work, however no good deed goes unpunished, so here are some code fragments that make other 
plots that may or may not be useful when trying to visualize your data.

All of them require at least a little bit of user input to match your data. 

"""

#CHANGE ME: this is the date that you want to look at.
todaysDay=16
todaysMonth=12
todaysYear=2020

#pull the information on the desired day from the depths array
#pole number line excludes any info where the pole was damaged (in this case it was pole 2 and my error
#exclusion stuff results in a zero in the PN for that)
today=depths.loc[(depths['DataYear']==float(todaysYear)) & (depths['DataMonth']==float(todaysMonth)) 
                      & (depths['DataDay']==float(todaysDay)) &(depths['PoleNumber']!=float(0))]
todaysData=today.to_numpy()



#this plot is the snow depth on a particular date (the one you define above) as a function of latitude and longitude
#the color indicates the snow depth
plt.figure(60)
plt.scatter(todaysData[:,4],todaysData[:,5],c=todaysData[:,10], cmap='Oranges') #this plots lat on the x axis, long on the y and the color (c) is depth
plt.xlabel("latitude")
plt.ylabel("longitude")
plt.title("snow depth on %d\%d\%d" %(todaysMonth, todaysDay, todaysYear))
plt.xlim(58.047, 58.06) #these are the relevent latitudes for our data, your milage will vary
plt.ylim(-135.38, -135.475)
plt.colorbar()

#snow depth for a single day as a function of elevation--makes a 3d plot with lat on x axis, long on y and elevation on z
fig = plt.figure(figsize=(8,6))
ax = plt.axes(projection="3d")
ax.set_xlabel('lat')
ax.set_ylabel('long')
ax.set_zlabel("ele")
im=ax.scatter(todaysData[:,4],todaysData[:,5],todaysData[:,12], c=todaysData[:,10], cmap='Oranges') #plt. scatter in 3d does (x,y,z) position followed by the color variable
ax.view_init(10, 45)
plt.xlim(58.047, 58.06)
plt.ylim(-135.38, -135.43)
plt.title("snow depth on %d\%d\%d" %(todaysMonth, todaysDay, todaysYear))
fig.colorbar(im, ax=ax)
plt.show()









#depth as a function of time for an individal pole
#CHANGE ME: desiredPole is the pole number of whichever pole you want to look at
desiredPole=12
thisPoleData=depths.loc[depths['PoleNumber']==float(desiredPole)]
pole1=thisPoleData.to_numpy()
plt.figure(61)
plt.plot(pole1[:,10], linestyle='', marker='1', color=colors[2])
plt.xlabel("logger day")
plt.ylabel("snow depth (meters)")
plt.title('snow depth as a function of time')






#depth as a function of time for all poles

poleList=[1,3,4,5,6,7,8,9,10,11,12,13,14] #poles of interest
for i in range(len(poleList)):
    
    thisPole=poleList[i] #crop data to just be an individual pole for the moment
    today=depths.loc[depths['PoleNumber']==float(thisPole)]
    todaysData=today.to_numpy()
    
  
    d=todaysData[:,10] #cut out depth row
    for j in range(len(d)):
        if d[j]>1.5:
            d[j]=1.4
    
    #colormap information, this makes it orange
    #the only logical color for snow
    cmap=plt.get_cmap("Oranges")
    colors=cmap([0.25,0.5,0.75,1])
    
    
    plt.figure(thisPole+60)
    plt.plot(d, linestyle='',marker='1', color=colors[2])
    plt.xlabel("Date")
    plt.ylabel("Sensor Coverage (meters)")
    plt.title("Snow Coverage as a function of time for Pole %d" %thisPole)
    xtick=[0,75,150,225,300]
    xlabels=['Oct. 2020', 'Dec. 2020','Feb. 2021','Apr. 2021', 'Jun. 2021']
    plt.xticks(xtick,xlabels)
    plt.savefig(inPath+'snowCoverageProfile'+str(thisPole)+'.png')
    
    

m=np.array([4,10,13,5,11,9,6,12,3,14,8,1,7])
va=[]
for i in range(len(m)):
    thisPole=m[i]
    today=depths.loc[depths['PoleNumber']==float(thisPole)]
    todaysData=today.to_numpy()
    
  
    d=todaysData[:,10]
    for j in range(len(d)):
        if d[j]>1.5:
            d[j]=1.4

    v=np.var(d)
    va.append(v)
















#other ways of looking at the summary file data: this makes plots of the first date
#last date and duration of snow fall/coverage (in that order) on individual plots
#run each plotting segment individually in the terminal

q=[]
asd=[]
for i in range(len(poleList)):
    qwerty=mrSandManMakeMeSomeSand(summaryArray[i,7])
    asdf=mrSandManMakeMeSomeSand(summaryArray[i,8])
    q.append(qwerty)
    asd.append(asdf)

#looking at the date of first snow as a fucntion of elevation
#no super strong relationship
plt.figure(40)
plt.plot(summaryArray[:,19], q, linestyle='', marker='1',color=colors[1], label='first')
plt.xlabel('Elevation (Feet)')
plt.ylabel('Date')
plt.title('Date of First Snow in the Fall')

#looking at last date that there was at least 025 meters of snow on the ground
#generally speaking, the higher the elevation, the later the snow melts off, as one would expect
plt.figure(41)
plt.plot(summaryArray[:,19], asd, linestyle='', marker='1',color=colors[2], label='last')
plt.xlabel('Elevation (Feet)')
plt.ylabel('Date')
plt.title('Date of Final Snow Melt in the Spring')

#duration of snow coverage increases in elevation
plt.figure(42)
plt.plot(summaryArray[:,19], summaryArray[:,9], linestyle='', marker='1',color=colors[2], label='duration')
plt.xlabel('Elevation (Feet)')
plt.ylabel('Duration (Days)')
plt.title('Snow Duration as a Function of Elevation')



plt.figure(43)
for i in range(np.shape(summaryArray)[0]):
    if summaryArray[i,6]>1:
        print('3 and below')
        plt.plot(summaryArray[i,19], q[i], linestyle='', marker='1',color=colors[0], label='duration')
    else:
        print('four')
        plt.plot(summaryArray[i,19], q[i], linestyle='', marker='1',color=colors[3], label='duration')

            