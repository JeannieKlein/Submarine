#!/usr/bin/env python

#first part of script to remove all but two columns of interest 

InFileName ='/ufrc/zoo6927/kleinje/pcfb/examples/ctd.txt'
OutFileName = '/ufrc/zoo6927/kleinje/submarine/maxdepth.out'

InFile= open(InFileName,'r')

OutFile= open(OutFileName,'w')

# initialize the counter used to keep track of line numbers
LineNumber = 0

for Line in InFile:
    if LineNumber>0:
        Line = Line.strip()
        ElementList = Line.split(",")
        OutputString = "%s %s" % (ElementList[1], ElementList[4])
        OutFile.write(OutputString+"\n")
    LineNumber = LineNumber + 1

InFile.close()
OutFile.close()

#############
#script to remove date column from dataset so only time and depth remain

InFileName ='/ufrc/zoo6927/kleinje/submarine/maxdepth.out'
OutFileName = '/ufrc/zoo6927/kleinje/submarine/TimeDepth'

InFile= open(InFileName,'r')

OutFile= open(OutFileName,'w')

LineValue = 1

for Line in InFile:
    Line = Line.strip()
    ElementList = Line.split(" ")
    OutputString = "%s %s %s" % (LineValue, ElementList[1], ElementList[2])
    OutFile.write(OutputString+"\n")
    LineValue += 1

InFile.close()
OutFile.close()

###########################
#script to calculate how long it takes to go from the first recording to a depth of 800 meters
  #calculate and print how long the submarine was below 800 meters
    #and writes a file that has the maximum depth for the dive

InFileName ='/ufrc/zoo6927/kleinje/submarine/TimeDepth'
OutFileName = '/ufrc/zoo6927/kleinje/submarine/TimeDepthDiff'
SecondOutFileName = '/ufrc/zoo6927/kleinje/submarine/Below800'
ThirdOutFileName = '/ufrc/zoo6927/kleinje/submarine/Resurface'
FourthOutFileName = '/ufrc/zoo6927/kleinje/submarine/DepthList'
FifthOutFileName = '/ufrc/zoo6927/kleinje/submarine/MaximumDepthOfDive'

InFile= open(InFileName,'r') #read file

OutFile= open(OutFileName,'w') #write to file

SecondOutFile= open(SecondOutFileName,'w') #write to file

ThirdOutFile= open(ThirdOutFileName,'w') #write to file

FourthOutFile= open(FourthOutFileName,'w') #write to a file

Diving = 1 #when descending. Control variable
MaxDepth = 0 #Control variable. Will redefine in loop below

for Line in InFile: #work with data from first file defined
    Line = Line.strip()
    ElementList = Line.split(" ")
    if (float(ElementList[2]) <= 800) and (Diving == 1): #depth column, work with if value less than or equal to 800
			#diving equals 1 until it is redefined in the next loop
        StartTime= int(ElementList[0])/4 #using line numbers, divide by 4 (minutes)
        OutputString = "%s %s" % (StartTime, ElementList[2]) #output start time and depth as strings
        OutFile.write(OutputString+"\n") #write outfile with line breaks
    elif float(ElementList[2]) > 800: #when depth column above 800..
        Diving=0 #redefine diving variable so no longer equal to 1, so can work with in next loop
        Below= int(ElementList[0])/4 #new variable 'Below', define as line number divided by 4 to give minutes
        OutputString = "%s %s" % (Below, ElementList[2]) #output Below variable and depth
        SecondOutFile.write(OutputString+"\n") #write outfile with line breaks
        if float(ElementList[2]) > MaxDepth: #redefines every time it goes through loop, only if deeper than before
            MaxDepth= float(ElementList[2]) #redefines MaxDepth each time through so comparing with prior loop value
				#keeps largest MaxDepth value
            OutputString = "%s" % (MaxDepth)
            FourthOutFile.write(OutputString+"\n")
			#FourthOutFile.close() #could also use this line to close file after use instead of write last line of file later, 
				#so then it would overwrite the value each time it is larger and ultimately just have one value instead of a list
		#first 'if' statement is false now because global variable defined 'diving' as = 0.
		#once we've gone below 800, 'diving' variable is always going to be = 0 (local variable)
    elif (float(ElementList[2]) <= 800) and (Diving == 0): #diving was redefined as 0 (local variable)
			#Work with data from depth less than 800 (submarine coming back up)
        AfterDiveTime= int(ElementList[0])/4 #using line numbers (integers), divide by 4 (minutes)
        OutputString = "%s %s" % (AfterDiveTime, ElementList[2]) #output AfterDiveTime variable and depth
        ThirdOutFile.write(OutputString+"\n") #write outfile with line breaks

OutFile.close() #TimeDepthDiff file
OutFile= open(OutFileName,'r') #now open for reading. Can only have one open at time (reading, writing, or appending)

SecondOutFile.close() #Below800 file
SecondOutFile= open(SecondOutFileName,'r') #now open for reading

ThirdOutFile.close() #Resurface file
ThirdOutFile= open(ThirdOutFileName,'r') #now open for reading

FourthOutFile.close() #MaximumDepthOfDive file
FourthOutFile= open(FourthOutFileName,'r') #now open for reading

FifthOutFile= open(FifthOutFileName,'w') #open for writing

for Line in OutFile:
    pass #burn through file
Last = Line #on last line of file, call this value "Last"
LastTimeElement= Last.split(" ") #separate columns based on spacing
LastTime= int(LastTimeElement[0]) #LastTime variable equals minutes column
print "Time at which submarine reached 800 meters in depth was %s minutes" % (LastTime) #print this last column 1 line of OutFile

for Line in SecondOutFile:
    pass #burn through file
SecondLast = Line #on last line of file, call this value "Last"
SecondLastElement= SecondLast.split(" ") #separate columns based on spacing
SecondLastTime= int(SecondLastElement[0]) #SecondLastTime variable equals minutes column
print "Time at which submarine resurfaced above 800 meters was %s minutes" % (SecondLastTime) #print this last column 1 line of SecondOutFile

TotalBelow= SecondLastTime - LastTime #subtracts last time above 800 from last time below 800, before resurfacing
print "Total time below 800 meters was %d minutes" % (TotalBelow) #print this line

for Line in FourthOutFile:
    pass #burn through file
Last = Line #on last line of file, call this value "Last"
MaxDepth= Last
OutputString = "The maximum depth for the dive was %s meters" % (MaxDepth)
FifthOutFile.write(OutputString+"\n")

InFile.close()
OutFile.close()
SecondOutFile.close()
ThirdOutFile.close()
FourthOutFile.close()
FifthOutFile.close()