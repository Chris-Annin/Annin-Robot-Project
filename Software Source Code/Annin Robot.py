##########################################################################
##########################################################################
""" Annin Robot - Stepper motor robot control software
    Copyright (C) 2016  Chris Annin

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    chris.annin@gmail.com
"""
##########################################################################
##########################################################################


from Tkinter import *
import pickle
import serial
import time
import threading
import Queue

root = Tk()
root.wm_title("Annin Robot 1.0")
root.iconbitmap(r'ARbot.ico')
root.resizable(width=True, height=True)
root.geometry('{}x{}'.format(1024,700))
root.runTrue = 0


###DEFS###################################################################
##########################################################################


def setCom():
  global ser  
  port = "COM" + comPortEntryField.get()  
  baud = 9600 
  ser = serial.Serial(port, baud)

def deleteitem():
  selRow = root.progView.curselection()[0]
  selection = root.progView.curselection()  
  root.progView.delete(selection[0])
  root.progView.select_set(selRow)  
  value=root.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
    

def executeRow():
  selRow = root.progView.curselection()[0]
  root.progView.see(selRow+2)
  data = map(int, root.progView.curselection())
  command=root.progView.get(data[0])
  cmdType=command[:6]
  ##Call Program##
  if (cmdType == "Call P"):
    root.lastRow = root.progView.curselection()[0]
    root.lastProg = ProgEntryField.get()
    programIndex = command.find("Program -")
    progNum = str(command[programIndex+10:])
    ProgEntryField.delete(0, 'end')
    ProgEntryField.insert(0,progNum)
    loadProg()
    time.sleep(.2)    
    index = 0
    root.progView.selection_clear(0, END)
    root.progView.select_set(index) 
  ##Return Program##
  if (cmdType == "Return"):
    lastRow = root.lastRow
    lastProg = root.lastProg
    ProgEntryField.delete(0, 'end')
    ProgEntryField.insert(0,lastProg)
    loadProg()
    time.sleep(.2)    
    index = 0
    root.progView.selection_clear(0, END)
    root.progView.select_set(lastRow)  
  ##Servo Command##
  if (cmdType == "Servo "):
    servoIndex = command.find("number ")
    posIndex = command.find("position: ")
    servoNum = str(command[servoIndex+7:posIndex-4])
    servoPos = str(command[posIndex+10:])
    command = "SV"+servoNum+"P"+servoPos
    ser.write(command +"\n")
    ser.flushInput()
    time.sleep(.1)  
    ser.read() 
  ##If Input On Jump to Tab##
  if (cmdType == "If On "):
    inputIndex = command.find("Input-")
    tabIndex = command.find("Tab-")
    inputNum = str(command[inputIndex+6:tabIndex-9])
    tabNum = str(command[tabIndex+4:])
    command = "JFX"+inputNum+"T"+tabNum   
    ser.write(command +"\n")
    ser.flushInput()
    value = ser.readline()
    #value = str(value[3:])
    manEntryField.delete(0, 'end')
    manEntryField.insert(0,value)
    if (value == "True\n"):
      index = root.progView.get(0, "end").index("Tab Number " + tabNum)
      index = index-1
      root.progView.selection_clear(0, END)
      root.progView.select_set(index)
  ##If Input Off Jump to Tab##
  if (cmdType == "If Off"):
    inputIndex = command.find("Input-")
    tabIndex = command.find("Tab-")
    inputNum = str(command[inputIndex+6:tabIndex-9])
    tabNum = str(command[tabIndex+4:])
    command = "JFX"+inputNum+"T"+tabNum   
    ser.write(command +"\n")
    ser.flushInput()
    value = ser.readline()
    #value = str(value[3:])
    manEntryField.delete(0, 'end')
    manEntryField.insert(0,value)
    if (value == "False\n"):
      index = root.progView.get(0, "end").index("Tab Number " + tabNum)
      index = index-1
      root.progView.selection_clear(0, END)
      root.progView.select_set(index)
  ##Jump to Row##
  if (cmdType == "Jump T"):
    tabIndex = command.find("Tab-")
    tabNum = str(command[tabIndex+4:])
    index = root.progView.get(0, "end").index("Tab Number " + tabNum)
    root.progView.selection_clear(0, END)
    root.progView.select_set(index)  
  ##Set Output ON Command##
  if (cmdType == "Out On"):
    outputIndex = command.find("Output-")
    outputNum = str(command[outputIndex+7:])
    command = "ONX"+outputNum
    ser.write(command +"\n")
    ser.flushInput()
    time.sleep(.1)  
    ser.read() 
  ##Set Output OFF Command##
  if (cmdType == "Out Of"):
    outputIndex = command.find("Output-")
    outputNum = str(command[outputIndex+7:])
    command = "OFX"+outputNum
    ser.write(command +"\n")
    ser.flushInput()
    time.sleep(.1)  
    ser.read() 
  ##Wait Input ON Command##
  if (cmdType == "Wait I"):
    inputIndex = command.find("Input-")
    inputNum = str(command[inputIndex+6:])
    command = "WIN"+inputNum
    ser.write(command +"\n")
    ser.flushInput()
    time.sleep(.1)  
    ser.read() 
  ##Wait Input OFF Command##
  if (cmdType == "Wait O"):
    inputIndex = command.find("Input-")
    inputNum = str(command[inputIndex+6:])
    command = "WON"+inputNum
    ser.write(command +"\n")
    ser.flushInput()
    time.sleep(.1)  
    ser.read() 
  ##Wait Time Command##
  if (cmdType == "Wait T"):
    timeIndex = command.find("Seconds-")
    timeSeconds = str(command[timeIndex+8:])
    command = "WTS"+timeSeconds
    ser.write(command +"\n")
    ser.flushInput()
    time.sleep(.1)  
    ser.read() 
  ##Move Command##  
  if (cmdType == "Move J"):  
    J1curAng = J1curAngEntryField.get()
    J2curAng = J2curAngEntryField.get()
    J3curAng = J3curAngEntryField.get()
    J4curAng = J4curAngEntryField.get()
    J5curAng = J5curAngEntryField.get()
    J6curAng = J6curAngEntryField.get()
    J1newIndex = command.find("J1-")
    J2newIndex = command.find("J2-")
    J3newIndex = command.find("J3-")
    J4newIndex = command.find("J4-")
    J5newIndex = command.find("J5-")
    J6newIndex = command.find("J6-")
    SpeedIndex = command.find("Speed-")
    J1newAng = command[J1newIndex+3:J2newIndex-1]
    J2newAng = command[J2newIndex+3:J3newIndex-1]
    J3newAng = command[J3newIndex+3:J4newIndex-1]
    J4newAng = command[J4newIndex+3:J5newIndex-1]
    J5newAng = command[J5newIndex+3:J6newIndex-1]
    J6newAng = command[J6newIndex+3:SpeedIndex-1]
    newSpeed = str(command[SpeedIndex+6:])
    ##J1 calc##
    J1degStep = float(J1degPerStepEntryField.get())
    J1curStep = int(J1curStepEntryField.get())
    if (float(J1newAng) >= float(J1curAng)):
      ####SET DIRECTION
      J1dir = "1"
      J1calcAng = float(J1newAng) - float(J1curAng)
      J1steps = int(J1calcAng / J1degStep)
      J1newSteps = J1curStep + J1steps
      J1curStepEntryField.delete(0, 'end')
      J1curStepEntryField.insert(0,str(J1newSteps))       
      J1writeAng = float(J1curAng) + J1calcAng
      J1curAngEntryField.delete(0, 'end')
      J1curAngEntryField.insert(0,str(J1writeAng))    
      J1steps = str(J1steps) 
    elif(float(J1newAng) < float(J1curAng)): 
      J1dir = "0"
      J1calcAng = float(J1curAng) - float(J1newAng)
      J1steps = int(J1calcAng / J1degStep)
      J1newSteps = J1curStep - J1steps
      J1curStepEntryField.delete(0, 'end')
      J1curStepEntryField.insert(0,str(J1newSteps))
      J1writeAng = float(J1curAng) - J1calcAng
      J1curAngEntryField.delete(0, 'end')
      J1curAngEntryField.insert(0,str(J1writeAng))     
      J1steps = str(J1steps)
    ##J2 calc##
    J2degStep = float(J2degPerStepEntryField.get())
    J2curStep = int(J2curStepEntryField.get())
    if (float(J2newAng) >= float(J2curAng)):
      ####SET DIRECTION
      J2dir = "0"
      J2calcAng = float(J2newAng) - float(J2curAng)
      J2steps = int(J2calcAng / J2degStep)
      J2newSteps = J2curStep + J2steps
      J2curStepEntryField.delete(0, 'end')
      J2curStepEntryField.insert(0,str(J2newSteps))       
      J2writeAng = float(J2curAng) +J2calcAng
      J2curAngEntryField.delete(0, 'end')
      J2curAngEntryField.insert(0,str(J2writeAng))    
      J2steps = str(J2steps) 
    elif(float(J2newAng) < float(J2curAng)): 
      J2dir = "1"
      J2calcAng = float(J2curAng) - float(J2newAng)
      J2steps = int(J2calcAng / J2degStep)
      J2newSteps = J2curStep - J2steps
      J2curStepEntryField.delete(0, 'end')
      J2curStepEntryField.insert(0,str(J2newSteps))
      J2writeAng = float(J2curAng) - J2calcAng
      J2curAngEntryField.delete(0, 'end')
      J2curAngEntryField.insert(0,str(J2writeAng))     
      J2steps = str(J2steps)
    ##J3 calc##
    J3degStep = float(J3degPerStepEntryField.get())
    J3curStep = int(J3curStepEntryField.get())
    if (float(J3newAng) >= float(J3curAng)):
      ####SET DIRECTION
      J3dir = "0"
      J3calcAng = float(J3newAng) - float(J3curAng)
      J3steps = int(J3calcAng / J3degStep)
      J3newSteps = J3curStep + J3steps
      J3curStepEntryField.delete(0, 'end')
      J3curStepEntryField.insert(0,str(J3newSteps))       
      J3writeAng = float(J3curAng) + J3calcAng
      J3curAngEntryField.delete(0, 'end')
      J3curAngEntryField.insert(0,str(J3writeAng))    
      J3steps = str(J3steps) 
    elif(float(J3newAng) < float(J3curAng)): 
      J3dir = "1"
      J3calcAng = float(J3curAng) - float(J3newAng)
      J3steps = int(J3calcAng / J3degStep)
      J3newSteps = J3curStep - J3steps
      J3curStepEntryField.delete(0, 'end')
      J3curStepEntryField.insert(0,str(J3newSteps))
      J3writeAng = float(J3curAng) - J3calcAng
      J3curAngEntryField.delete(0, 'end')
      J3curAngEntryField.insert(0,str(J3writeAng))     
      J3steps = str(J3steps)  
    ##J4 calc##
    J4degStep = float(J4degPerStepEntryField.get())
    J4curStep = int(J4curStepEntryField.get())
    if (float(J4newAng) >= float(J4curAng)):
      ####SET DIRECTION
      J4dir = "0"
      J4calcAng = float(J4newAng) - float(J4curAng)
      J4steps = int(J4calcAng / J4degStep)
      J4newSteps = J4curStep + J4steps
      J4curStepEntryField.delete(0, 'end')
      J4curStepEntryField.insert(0,str(J4newSteps))       
      J4writeAng = float(J4curAng) + J4calcAng
      J4curAngEntryField.delete(0, 'end')
      J4curAngEntryField.insert(0,str(J4writeAng))    
      J4steps = str(J4steps) 
    elif(float(J4newAng) < float(J4curAng)): 
      J4dir = "1"
      J4calcAng = float(J4curAng) - float(J4newAng)
      J4steps = int(J4calcAng / J4degStep)
      J4newSteps = J4curStep - J4steps
      J4curStepEntryField.delete(0, 'end')
      J4curStepEntryField.insert(0,str(J4newSteps))
      J4writeAng = float(J4curAng) - J4calcAng
      J4curAngEntryField.delete(0, 'end')
      J4curAngEntryField.insert(0,str(J4writeAng))     
      J4steps = str(J4steps)
    ##J5 calc##
    J5degStep = float(J5degPerStepEntryField.get())
    J5curStep = int(J5curStepEntryField.get())
    if (float(J5newAng) >= float(J5curAng)):
      ####SET DIRECTION
      J5dir = "1"
      J5calcAng = float(J5newAng) - float(J5curAng)
      J5steps = int(J5calcAng / J5degStep)
      J5newSteps = J5curStep + J5steps
      J5curStepEntryField.delete(0, 'end')
      J5curStepEntryField.insert(0,str(J5newSteps))       
      J5writeAng = float(J5curAng) + J5calcAng
      J5curAngEntryField.delete(0, 'end')
      J5curAngEntryField.insert(0,str(J5writeAng))    
      J5steps = str(J5steps) 
    elif(float(J5newAng) < float(J5curAng)): 
      J5dir = "0"
      J5calcAng = float(J5curAng) - float(J5newAng)
      J5steps = int(J5calcAng / J5degStep)
      J5newSteps = J5curStep - J5steps
      J5curStepEntryField.delete(0, 'end')
      J5curStepEntryField.insert(0,str(J5newSteps))
      J5writeAng = float(J5curAng) - J5calcAng
      J5curAngEntryField.delete(0, 'end')
      J5curAngEntryField.insert(0,str(J5writeAng))     
      J5steps = str(J5steps)
    ##J6 calc##
    J6degStep = float(J6degPerStepEntryField.get())
    J6curStep = int(J6curStepEntryField.get())
    if (float(J6newAng) >= float(J6curAng)):
      ####SET DIRECTION
      J6dir = "0"
      J6calcAng = float(J6newAng) - float(J6curAng)
      J6steps = int(J6calcAng / J6degStep)
      J6newSteps = J6curStep + J6steps
      J6curStepEntryField.delete(0, 'end')
      J6curStepEntryField.insert(0,str(J6newSteps))       
      J6writeAng = float(J6curAng) + J6calcAng
      J6curAngEntryField.delete(0, 'end')
      J6curAngEntryField.insert(0,str(J6writeAng))    
      J6steps = str(J6steps) 
    elif(float(J6newAng) < float(J6curAng)): 
      J6dir = "1"
      J6calcAng = float(J6curAng) - float(J6newAng)
      J6steps = int(J6calcAng / J6degStep)
      J6newSteps = J6curStep - J6steps
      J6curStepEntryField.delete(0, 'end')
      J6curStepEntryField.insert(0,str(J6newSteps))
      J6writeAng = float(J6curAng) - J6calcAng
      J6curAngEntryField.delete(0, 'end')
      J6curAngEntryField.insert(0,str(J6writeAng))     
      J6steps = str(J6steps)            
    commandCalc = "MJA"+J1dir+J1steps+"B"+J2dir+J2steps+"C"+J3dir+J3steps+"D"+J4dir+J4steps+"E"+J5dir+J5steps+"F"+J6dir+J6steps+"S"+newSpeed
    ser.write(commandCalc +"\n")
    ser.flushInput()
    time.sleep(.1)  
    ser.read() 
    savePosData()    


  
def stepFwd():
    executeRow() 
    selRow = root.progView.curselection()[0]
    root.progView.selection_clear(0, END)
    selRow += 1
    root.progView.select_set(selRow)
    time.sleep(.1)
    try:
      selRow = root.progView.curselection()[0]
      curRowEntryField.delete(0, 'end')
      curRowEntryField.insert(0,selRow)
    except:
      curRowEntryField.delete(0, 'end')
      curRowEntryField.insert(0,"---")
 

def stepRev():
    executeRow()  
    selRow = root.progView.curselection()[0]
    root.progView.selection_clear(0, END)
    selRow -= 1
    root.progView.select_set(selRow)
    time.sleep(.1)
    try:
      selRow = root.progView.curselection()[0]
      curRowEntryField.delete(0, 'end')
      curRowEntryField.insert(0,selRow)
    except:
      curRowEntryField.delete(0, 'end')
      curRowEntryField.insert(0,"---")
 

def runProg():
  def threadProg():
    try:
      curRow = root.progView.curselection()[0]
      if (curRow == 0):
        curRow=1
    except:
      curRow=1
      root.progView.selection_clear(0, END)
      root.progView.select_set(curRow)
    root.runTrue = 1
    while root.runTrue == 1:
      if (root.runTrue == 0):
        runStatusLab.config(text='PROGRAM STOPPED', bg = "red")
      else:
        runStatusLab.config(text='PROGRAM RUNNING', bg = "green")
      executeRow()  
      selRow = root.progView.curselection()[0]
      root.progView.selection_clear(0, END)
      selRow += 1
      root.progView.select_set(selRow)
      curRow += 1
      time.sleep(.1)
      try:
        selRow = root.progView.curselection()[0]
        curRowEntryField.delete(0, 'end')
        curRowEntryField.insert(0,selRow)
      except:
        curRowEntryField.delete(0, 'end')
        curRowEntryField.insert(0,"---") 
        root.runTrue = 0
        runStatusLab.config(text='PROGRAM STOPPED', bg = "red")
  t = threading.Thread(target=threadProg)
  t.start()


def stopProg():
  root.runTrue = 0 
  if (root.runTrue == 0):
    runStatusLab.config(text='PROGRAM STOPPED', bg = "red")
  else:
    runStatusLab.config(text='PROGRAM RUNNING', bg = "green")

def calRobot():
  calibration.delete(0, END)
  ##J1##
  J1stepLimNeg = float(J1stepLimNegEntryField.get())
  J1stepLimPos = float(J1stepLimPosEntryField.get())
  J1angLimNeg = float(J1angLimNegEntryField.get())
  J1angLimPos = float(J1angLimPosEntryField.get())
  J1stepDelta = J1stepLimPos - J1stepLimNeg
  J1angDelta = J1angLimPos - J1angLimNeg
  J1degPerStep = J1angDelta / J1stepDelta
  J1degPerStepEntryField.delete(0, 'end')
  J1degPerStepEntryField.insert(0,str(J1degPerStep))
  J1calAng = float(J1calAngleEntryField.get())
  J1curStep = int((J1calAng-J1angLimNeg) / J1degPerStep)
  J1curStepEntryField.delete(0, 'end')
  J1curStepEntryField.insert(0,str(J1curStep))
  J1curAngEntryField.delete(0, 'end')
  J1curAngEntryField.insert(0,str(J1calAng))
  ###########
  calibration.insert(END, J1stepLimNegEntryField.get())
  calibration.insert(END, J1stepLimPosEntryField.get())
  calibration.insert(END, J1angLimNegEntryField.get())
  calibration.insert(END, J1angLimPosEntryField.get())
  calibration.insert(END, J1degPerStepEntryField.get())
  calibration.insert(END, J1calAngleEntryField.get())
  calibration.insert(END, J1curStepEntryField.get())
  calibration.insert(END, J1curAngEntryField.get())
  calibration.insert(END, J1jogStepsEntryField.get()) 
  ###########
  ##J2##
  J2stepLimNeg = float(J2stepLimNegEntryField.get())
  J2stepLimPos = float(J2stepLimPosEntryField.get())
  J2angLimNeg = float(J2angLimNegEntryField.get())
  J2angLimPos = float(J2angLimPosEntryField.get())
  J2stepDelta = J2stepLimPos - J2stepLimNeg
  J2angDelta = J2angLimPos - J2angLimNeg
  J2degPerStep = J2angDelta / J2stepDelta
  J2degPerStepEntryField.delete(0, 'end')
  J2degPerStepEntryField.insert(0,str(J2degPerStep))
  J2calAng = float(J2calAngleEntryField.get())
  J2curStep = int((J2calAng-J2angLimNeg) / J2degPerStep)
  J2curStepEntryField.delete(0, 'end')
  J2curStepEntryField.insert(0,str(J2curStep))
  J2curAngEntryField.delete(0, 'end')
  J2curAngEntryField.insert(0,str(J2calAng))
  ###########
  calibration.insert(END, J2stepLimNegEntryField.get())
  calibration.insert(END, J2stepLimPosEntryField.get())
  calibration.insert(END, J2angLimNegEntryField.get())
  calibration.insert(END, J2angLimPosEntryField.get())
  calibration.insert(END, J2degPerStepEntryField.get())
  calibration.insert(END, J2calAngleEntryField.get())
  calibration.insert(END, J2curStepEntryField.get())
  calibration.insert(END, J2curAngEntryField.get())
  calibration.insert(END, J2jogStepsEntryField.get()) 
  ###########
  ##J3##
  J3stepLimNeg = float(J3stepLimNegEntryField.get())
  J3stepLimPos = float(J3stepLimPosEntryField.get())
  J3angLimNeg = float(J3angLimNegEntryField.get())
  J3angLimPos = float(J3angLimPosEntryField.get())
  J3stepDelta = J3stepLimPos - J3stepLimNeg
  J3angDelta = J3angLimPos - J3angLimNeg
  J3degPerStep = J3angDelta / J3stepDelta
  J3degPerStepEntryField.delete(0, 'end')
  J3degPerStepEntryField.insert(0,str(J3degPerStep))
  J3calAng = float(J3calAngleEntryField.get())
  J3curStep = int((J3calAng-J3angLimNeg) / J3degPerStep)
  J3curStepEntryField.delete(0, 'end')
  J3curStepEntryField.insert(0,str(J3curStep))
  J3curAngEntryField.delete(0, 'end')
  J3curAngEntryField.insert(0,str(J3calAng))
  ###########
  calibration.insert(END, J3stepLimNegEntryField.get())
  calibration.insert(END, J3stepLimPosEntryField.get())
  calibration.insert(END, J3angLimNegEntryField.get())
  calibration.insert(END, J3angLimPosEntryField.get())
  calibration.insert(END, J3degPerStepEntryField.get())
  calibration.insert(END, J3calAngleEntryField.get())
  calibration.insert(END, J3curStepEntryField.get())
  calibration.insert(END, J3curAngEntryField.get())
  calibration.insert(END, J3jogStepsEntryField.get()) 
  ###########
  ##J4##
  J4stepLimNeg = float(J4stepLimNegEntryField.get())
  J4stepLimPos = float(J4stepLimPosEntryField.get())
  J4angLimNeg = float(J4angLimNegEntryField.get())
  J4angLimPos = float(J4angLimPosEntryField.get())
  J4stepDelta = J4stepLimPos - J4stepLimNeg
  J4angDelta = J4angLimPos - J4angLimNeg
  J4degPerStep = J4angDelta / J4stepDelta
  J4degPerStepEntryField.delete(0, 'end')
  J4degPerStepEntryField.insert(0,str(J4degPerStep))
  J4calAng = float(J4calAngleEntryField.get())
  J4curStep = int((J4calAng-J4angLimNeg) / J4degPerStep)
  J4curStepEntryField.delete(0, 'end')
  J4curStepEntryField.insert(0,str(J4curStep))
  J4curAngEntryField.delete(0, 'end')
  J4curAngEntryField.insert(0,str(J4calAng))
  ###########
  calibration.insert(END, J4stepLimNegEntryField.get())
  calibration.insert(END, J4stepLimPosEntryField.get())
  calibration.insert(END, J4angLimNegEntryField.get())
  calibration.insert(END, J4angLimPosEntryField.get())
  calibration.insert(END, J4degPerStepEntryField.get())
  calibration.insert(END, J4calAngleEntryField.get())
  calibration.insert(END, J4curStepEntryField.get())
  calibration.insert(END, J4curAngEntryField.get())
  calibration.insert(END, J4jogStepsEntryField.get()) 
  ###########
  ##J5##
  J5stepLimNeg = float(J5stepLimNegEntryField.get())
  J5stepLimPos = float(J5stepLimPosEntryField.get())
  J5angLimNeg = float(J5angLimNegEntryField.get())
  J5angLimPos = float(J5angLimPosEntryField.get())
  J5stepDelta = J5stepLimPos - J5stepLimNeg
  J5angDelta = J5angLimPos - J5angLimNeg
  J5degPerStep = J5angDelta / J5stepDelta
  J5degPerStepEntryField.delete(0, 'end')
  J5degPerStepEntryField.insert(0,str(J5degPerStep))
  J5calAng = float(J5calAngleEntryField.get())
  J5curStep = int((J5calAng-J5angLimNeg) / J5degPerStep)
  J5curStepEntryField.delete(0, 'end')
  J5curStepEntryField.insert(0,str(J5curStep))
  J5curAngEntryField.delete(0, 'end')
  J5curAngEntryField.insert(0,str(J5calAng))
  ###########
  calibration.insert(END, J5stepLimNegEntryField.get())
  calibration.insert(END, J5stepLimPosEntryField.get())
  calibration.insert(END, J5angLimNegEntryField.get())
  calibration.insert(END, J5angLimPosEntryField.get())
  calibration.insert(END, J5degPerStepEntryField.get())
  calibration.insert(END, J5calAngleEntryField.get())
  calibration.insert(END, J5curStepEntryField.get())
  calibration.insert(END, J5curAngEntryField.get())
  calibration.insert(END, J5jogStepsEntryField.get()) 
  ###########
  ##J6##
  J6stepLimNeg = float(J6stepLimNegEntryField.get())
  J6stepLimPos = float(J6stepLimPosEntryField.get())
  J6angLimNeg = float(J6angLimNegEntryField.get())
  J6angLimPos = float(J6angLimPosEntryField.get())
  J6stepDelta = J6stepLimPos - J6stepLimNeg
  J6angDelta = J6angLimPos - J6angLimNeg
  J6degPerStep = J6angDelta / J6stepDelta
  J6degPerStepEntryField.delete(0, 'end')
  J6degPerStepEntryField.insert(0,str(J6degPerStep))
  J6calAng = float(J6calAngleEntryField.get())
  J6curStep = int((J6calAng-J6angLimNeg) / J6degPerStep)
  J6curStepEntryField.delete(0, 'end')
  J6curStepEntryField.insert(0,str(J6curStep))
  J6curAngEntryField.delete(0, 'end')
  J6curAngEntryField.insert(0,str(J6calAng))
  ###########
  calibration.insert(END, J6stepLimNegEntryField.get())
  calibration.insert(END, J6stepLimPosEntryField.get())
  calibration.insert(END, J6angLimNegEntryField.get())
  calibration.insert(END, J6angLimPosEntryField.get())
  calibration.insert(END, J6degPerStepEntryField.get())
  calibration.insert(END, J6calAngleEntryField.get())
  calibration.insert(END, J6curStepEntryField.get())
  calibration.insert(END, J6curAngEntryField.get())
  calibration.insert(END, J6jogStepsEntryField.get()) 
  ###########
  calibration.insert(END, comPortEntryField.get()) 
  ###########
  value=calibration.get(0,END)
  pickle.dump(value,open("ARbot.cal","wb"))

def savePosData():
  calibration.delete(0, END)
  calibration.insert(END, J1stepLimNegEntryField.get())
  calibration.insert(END, J1stepLimPosEntryField.get())
  calibration.insert(END, J1angLimNegEntryField.get())
  calibration.insert(END, J1angLimPosEntryField.get())
  calibration.insert(END, J1degPerStepEntryField.get())
  calibration.insert(END, J1calAngleEntryField.get())
  calibration.insert(END, J1curStepEntryField.get())
  calibration.insert(END, J1curAngEntryField.get())
  calibration.insert(END, J1jogStepsEntryField.get())
  calibration.insert(END, J2stepLimNegEntryField.get())
  calibration.insert(END, J2stepLimPosEntryField.get())
  calibration.insert(END, J2angLimNegEntryField.get())
  calibration.insert(END, J2angLimPosEntryField.get())
  calibration.insert(END, J2degPerStepEntryField.get())
  calibration.insert(END, J2calAngleEntryField.get())
  calibration.insert(END, J2curStepEntryField.get())
  calibration.insert(END, J2curAngEntryField.get())
  calibration.insert(END, J2jogStepsEntryField.get())
  calibration.insert(END, J3stepLimNegEntryField.get())
  calibration.insert(END, J3stepLimPosEntryField.get())
  calibration.insert(END, J3angLimNegEntryField.get())
  calibration.insert(END, J3angLimPosEntryField.get())
  calibration.insert(END, J3degPerStepEntryField.get())
  calibration.insert(END, J3calAngleEntryField.get())
  calibration.insert(END, J3curStepEntryField.get())
  calibration.insert(END, J3curAngEntryField.get())
  calibration.insert(END, J3jogStepsEntryField.get())
  calibration.insert(END, J4stepLimNegEntryField.get())
  calibration.insert(END, J4stepLimPosEntryField.get())
  calibration.insert(END, J4angLimNegEntryField.get())
  calibration.insert(END, J4angLimPosEntryField.get())
  calibration.insert(END, J4degPerStepEntryField.get())
  calibration.insert(END, J4calAngleEntryField.get())
  calibration.insert(END, J4curStepEntryField.get())
  calibration.insert(END, J4curAngEntryField.get())
  calibration.insert(END, J4jogStepsEntryField.get())
  calibration.insert(END, J5stepLimNegEntryField.get())
  calibration.insert(END, J5stepLimPosEntryField.get())
  calibration.insert(END, J5angLimNegEntryField.get())
  calibration.insert(END, J5angLimPosEntryField.get())
  calibration.insert(END, J5degPerStepEntryField.get())
  calibration.insert(END, J5calAngleEntryField.get())
  calibration.insert(END, J5curStepEntryField.get())
  calibration.insert(END, J5curAngEntryField.get())
  calibration.insert(END, J5jogStepsEntryField.get())
  calibration.insert(END, J6stepLimNegEntryField.get())
  calibration.insert(END, J6stepLimPosEntryField.get())
  calibration.insert(END, J6angLimNegEntryField.get())
  calibration.insert(END, J6angLimPosEntryField.get())
  calibration.insert(END, J6degPerStepEntryField.get())
  calibration.insert(END, J6calAngleEntryField.get())
  calibration.insert(END, J6curStepEntryField.get())
  calibration.insert(END, J6curAngEntryField.get())
  calibration.insert(END, J6jogStepsEntryField.get())
  calibration.insert(END, comPortEntryField.get())  
  calibration.insert(END, ProgEntryField.get())
  calibration.insert(END, servo0onEntryField.get())
  calibration.insert(END, servo0offEntryField.get())
  calibration.insert(END, servo1onEntryField.get())
  calibration.insert(END, servo1offEntryField.get())
  calibration.insert(END, servo2onEntryField.get())
  calibration.insert(END, servo2offEntryField.get())
  calibration.insert(END, servo3onEntryField.get())
  calibration.insert(END, servo3offEntryField.get())     
  ###########
  value=calibration.get(0,END)
  pickle.dump(value,open("ARbot.cal","wb"))


def J1jogNeg():
  Speed = speedEntryField.get()
  J1jogSteps = J1jogStepsEntryField.get()
  J1curStep = int(J1curStepEntryField.get())
  J1curAng = float(J1curAngEntryField.get())  
  if (J1curStep >= int(J1jogSteps)):
    ser.write("MJA0"+J1jogSteps+"S"+Speed+"\n")    
    ser.flushInput()
    time.sleep(.1)  
    ser.read()  
    J1curStep = J1curStep - int(J1jogSteps)
    J1curStepEntryField.delete(0, 'end')
    J1curStepEntryField.insert(0,str(J1curStep))
    DegPerStep = float(J1degPerStepEntryField.get())
    J1totAng = DegPerStep * float(J1jogSteps)
    J1newAng = J1curAng - J1totAng
    J1curAngEntryField.delete(0, 'end')
    J1curAngEntryField.insert(0,str(J1newAng))
    savePosData()


def J1jogPos():
  Speed = speedEntryField.get()
  J1jogSteps = J1jogStepsEntryField.get()
  J1curStep = int(J1curStepEntryField.get())
  J1curAng = float(J1curAngEntryField.get())  
  J1posLim = int(J1stepLimPosEntryField.get())
  J1stepsRem = J1posLim - int(J1curStep)
  if (int(J1jogSteps) <= J1stepsRem):
    ser.write("MJA1"+J1jogSteps+"S"+Speed+"\n")    
    ser.flushInput()
    time.sleep(.1)  
    ser.read()  
    J1curStep = J1curStep + int(J1jogSteps)
    J1curStepEntryField.delete(0, 'end')
    J1curStepEntryField.insert(0,str(J1curStep))
    DegPerStep = float(J1degPerStepEntryField.get())
    J1totAng = DegPerStep * float(J1jogSteps)
    J1newAng = J1curAng + J1totAng
    J1curAngEntryField.delete(0, 'end')
    J1curAngEntryField.insert(0,str(J1newAng))
    savePosData()

def J2jogNeg():
  Speed = speedEntryField.get()
  J2jogSteps = J2jogStepsEntryField.get()
  J2curStep = int(J2curStepEntryField.get())
  J2curAng = float(J2curAngEntryField.get())  
  if (J2curStep >= int(J2jogSteps)):
    ser.write("MJB1"+J2jogSteps+"S"+Speed+"\n")    
    ser.flushInput()
    time.sleep(.1)  
    ser.read()  
    J2curStep = J2curStep - int(J2jogSteps)
    J2curStepEntryField.delete(0, 'end')
    J2curStepEntryField.insert(0,str(J2curStep))
    DegPerStep = float(J2degPerStepEntryField.get())
    J2totAng = DegPerStep * float(J2jogSteps)
    J2newAng = J2curAng - J2totAng
    J2curAngEntryField.delete(0, 'end')
    J2curAngEntryField.insert(0,str(J2newAng))
    savePosData()


def J2jogPos():
  Speed = speedEntryField.get()
  J2jogSteps = J2jogStepsEntryField.get()
  J2curStep = int(J2curStepEntryField.get())
  J2curAng = float(J2curAngEntryField.get())  
  J2posLim = int(J2stepLimPosEntryField.get())
  J2stepsRem = J2posLim - int(J2curStep)
  if (int(J2jogSteps) <= J2stepsRem):
    ser.write("MJB0"+J2jogSteps+"S"+Speed+"\n")    
    ser.flushInput()
    time.sleep(.1)  
    ser.read()  
    J2curStep = J2curStep +int(J2jogSteps)
    J2curStepEntryField.delete(0, 'end')
    J2curStepEntryField.insert(0,str(J2curStep))
    DegPerStep = float(J2degPerStepEntryField.get())
    J2totAng = DegPerStep * float(J2jogSteps)
    J2newAng = J2curAng +J2totAng
    J2curAngEntryField.delete(0, 'end')
    J2curAngEntryField.insert(0,str(J2newAng))
    savePosData()

def J3jogNeg():
  Speed = speedEntryField.get()
  J3jogSteps = J3jogStepsEntryField.get()
  J3curStep = int(J3curStepEntryField.get())
  J3curAng = float(J3curAngEntryField.get())  
  if (J3curStep >= int(J3jogSteps)):
    ser.write("MJC1"+J3jogSteps+"S"+Speed+"\n")    
    ser.flushInput()
    time.sleep(.1)  
    ser.read()  
    J3curStep = J3curStep - int(J3jogSteps)
    J3curStepEntryField.delete(0, 'end')
    J3curStepEntryField.insert(0,str(J3curStep))
    DegPerStep = float(J3degPerStepEntryField.get())
    J3totAng = DegPerStep * float(J3jogSteps)
    J3newAng = J3curAng - J3totAng
    J3curAngEntryField.delete(0, 'end')
    J3curAngEntryField.insert(0,str(J3newAng))
    savePosData()


def J3jogPos():
  Speed = speedEntryField.get()
  J3jogSteps = J3jogStepsEntryField.get()
  J3curStep = int(J3curStepEntryField.get())
  J3curAng = float(J3curAngEntryField.get())  
  J3posLim = int(J3stepLimPosEntryField.get())
  J3stepsRem = J3posLim - int(J3curStep)
  if (int(J3jogSteps) <= J3stepsRem):
    ser.write("MJC0"+J3jogSteps+"S"+Speed+"\n")    
    ser.flushInput()
    time.sleep(.1)  
    ser.read()  
    J3curStep = J3curStep + int(J3jogSteps)
    J3curStepEntryField.delete(0, 'end')
    J3curStepEntryField.insert(0,str(J3curStep))
    DegPerStep = float(J3degPerStepEntryField.get())
    J3totAng = DegPerStep * float(J3jogSteps)
    J3newAng = J3curAng + J3totAng
    J3curAngEntryField.delete(0, 'end')
    J3curAngEntryField.insert(0,str(J3newAng))
    savePosData()


def J4jogNeg():
  Speed = speedEntryField.get()
  J4jogSteps = J4jogStepsEntryField.get()
  J4curStep = int(J4curStepEntryField.get())
  J4curAng = float(J4curAngEntryField.get())  
  if (J4curStep >= int(J4jogSteps)):
    ser.write("MJD1"+J4jogSteps+"S"+Speed+"\n")    
    ser.flushInput()
    time.sleep(.1)  
    ser.read()  
    J4curStep = J4curStep - int(J4jogSteps)
    J4curStepEntryField.delete(0, 'end')
    J4curStepEntryField.insert(0,str(J4curStep))
    DegPerStep = float(J4degPerStepEntryField.get())
    J4totAng = DegPerStep * float(J4jogSteps)
    J4newAng = J4curAng - J4totAng
    J4curAngEntryField.delete(0, 'end')
    J4curAngEntryField.insert(0,str(J4newAng))
    savePosData()


def J4jogPos():
  Speed = speedEntryField.get()
  J4jogSteps = J4jogStepsEntryField.get()
  J4curStep = int(J4curStepEntryField.get())
  J4curAng = float(J4curAngEntryField.get())  
  J4posLim = int(J4stepLimPosEntryField.get())
  J4stepsRem = J4posLim - int(J4curStep)
  if (int(J4jogSteps) <= J4stepsRem):
    ser.write("MJD0"+J4jogSteps+"S"+Speed+"\n")    
    ser.flushInput()
    time.sleep(.1)  
    ser.read()  
    J4curStep = J4curStep + int(J4jogSteps)
    J4curStepEntryField.delete(0, 'end')
    J4curStepEntryField.insert(0,str(J4curStep))
    DegPerStep = float(J4degPerStepEntryField.get())
    J4totAng = DegPerStep * float(J4jogSteps)
    J4newAng = J4curAng + J4totAng
    J4curAngEntryField.delete(0, 'end')
    J4curAngEntryField.insert(0,str(J4newAng))
    savePosData()

def J5jogNeg():
  Speed = speedEntryField.get()
  J5jogSteps = J5jogStepsEntryField.get()
  J5curStep = int(J5curStepEntryField.get())
  J5curAng = float(J5curAngEntryField.get())  
  if (J5curStep >= int(J5jogSteps)):
    ser.write("MJE0"+J5jogSteps+"S"+Speed+"\n")    
    ser.flushInput()
    time.sleep(.1)  
    ser.read()  
    J5curStep = J5curStep - int(J5jogSteps)
    J5curStepEntryField.delete(0, 'end')
    J5curStepEntryField.insert(0,str(J5curStep))
    DegPerStep = float(J5degPerStepEntryField.get())
    J5totAng = DegPerStep * float(J5jogSteps)
    J5newAng = J5curAng - J5totAng
    J5curAngEntryField.delete(0, 'end')
    J5curAngEntryField.insert(0,str(J5newAng))
    savePosData()


def J5jogPos():
  Speed = speedEntryField.get()
  J5jogSteps = J5jogStepsEntryField.get()
  J5curStep = int(J5curStepEntryField.get())
  J5curAng = float(J5curAngEntryField.get())  
  J5posLim = int(J5stepLimPosEntryField.get())
  J5stepsRem = J5posLim - int(J5curStep)
  if (int(J5jogSteps) <= J5stepsRem):
    ser.write("MJE1"+J5jogSteps+"S"+Speed+"\n")    
    ser.flushInput()
    time.sleep(.1)  
    ser.read()  
    J5curStep = J5curStep + int(J5jogSteps)
    J5curStepEntryField.delete(0, 'end')
    J5curStepEntryField.insert(0,str(J5curStep))
    DegPerStep = float(J5degPerStepEntryField.get())
    J5totAng = DegPerStep * float(J5jogSteps)
    J5newAng = J5curAng + J5totAng
    J5curAngEntryField.delete(0, 'end')
    J5curAngEntryField.insert(0,str(J5newAng))
    savePosData()

def J6jogNeg():
  Speed = speedEntryField.get()
  J6jogSteps = J6jogStepsEntryField.get()
  J6curStep = int(J6curStepEntryField.get())
  J6curAng = float(J6curAngEntryField.get())  
  if (J6curStep >= int(J6jogSteps)):
    ser.write("MJF1"+J6jogSteps+"S"+Speed+"\n")    
    ser.flushInput()
    time.sleep(.1)  
    ser.read()  
    J6curStep = J6curStep - int(J6jogSteps)
    J6curStepEntryField.delete(0, 'end')
    J6curStepEntryField.insert(0,str(J6curStep))
    DegPerStep = float(J6degPerStepEntryField.get())
    J6totAng = DegPerStep * float(J6jogSteps)
    J6newAng = J6curAng - J6totAng
    J6curAngEntryField.delete(0, 'end')
    J6curAngEntryField.insert(0,str(J6newAng))
    savePosData()


def J6jogPos():
  Speed = speedEntryField.get()
  J6jogSteps = J6jogStepsEntryField.get()
  J6curStep = int(J6curStepEntryField.get())
  J6curAng = float(J6curAngEntryField.get())  
  J6posLim = int(J6stepLimPosEntryField.get())
  J6stepsRem = J6posLim - int(J6curStep)
  if (int(J6jogSteps) <= J6stepsRem):
    ser.write("MJF0"+J6jogSteps+"S"+Speed+"\n")    
    ser.flushInput()
    time.sleep(.1)  
    ser.read()  
    J6curStep = J6curStep + int(J6jogSteps)
    J6curStepEntryField.delete(0, 'end')
    J6curStepEntryField.insert(0,str(J6curStep))
    DegPerStep = float(J6degPerStepEntryField.get())
    J6totAng = DegPerStep * float(J6jogSteps)
    J6newAng = J6curAng + J6totAng
    J6curAngEntryField.delete(0, 'end')
    J6curAngEntryField.insert(0,str(J6newAng))
    savePosData()


def teachInsertEnd():
  Speed = speedEntryField.get()
  J1curAng = J1curAngEntryField.get()
  J2curAng = J2curAngEntryField.get()
  J3curAng = J3curAngEntryField.get()
  J4curAng = J4curAngEntryField.get()
  J5curAng = J5curAngEntryField.get()
  J6curAng = J6curAngEntryField.get()
  newPos = "Move J  J1-"+J1curAng+"  J2-"+J2curAng+"  J3-"+J3curAng+"  J4-"+J4curAng+"  J5-"+J5curAng+"  J6-"+J6curAng+"  Speed-"+Speed               
  root.progView.insert(END, newPos) 
  value=root.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def teachInsertBelSelected():
  selRow = root.progView.curselection()[0]
  selRow += 1
  Speed = speedEntryField.get()
  J1curAng = J1curAngEntryField.get()
  J2curAng = J2curAngEntryField.get()
  J3curAng = J3curAngEntryField.get()
  J4curAng = J4curAngEntryField.get()
  J5curAng = J5curAngEntryField.get()
  J6curAng = J6curAngEntryField.get()
  newPos = "Move J  J1-"+J1curAng+"  J2-"+J2curAng+"  J3-"+J3curAng+"  J4-"+J4curAng+"  J5-"+J5curAng+"  J6-"+J6curAng+"  Speed-"+Speed               
  root.progView.insert(selRow, newPos) 
  root.progView.selection_clear(0, END)
  root.progView.select_set(selRow)
  value=root.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def teachReplaceSelected():
  selRow = root.progView.curselection()[0]
  Speed = speedEntryField.get()
  J1curAng = J1curAngEntryField.get()
  J2curAng = J2curAngEntryField.get()
  J3curAng = J3curAngEntryField.get()
  J4curAng = J4curAngEntryField.get()
  J5curAng = J5curAngEntryField.get()
  J6curAng = J6curAngEntryField.get()
  newPos = "Move J  J1-"+J1curAng+"  J2-"+J2curAng+"  J3-"+J3curAng+"  J4-"+J4curAng+"  J5-"+J5curAng+"  J6-"+J6curAng+"  Speed-"+Speed               
  root.progView.insert(selRow, newPos)
  selection = root.progView.curselection()
  root.progView.delete(selection[0]) 
  root.progView.select_set(selRow)
  value=root.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))


def manAdditem():
  selRow = root.progView.curselection()[0]
  selRow += 1
  root.progView.insert(selRow, manEntryField.get())
  root.progView.selection_clear(0, END)
  root.progView.select_set(selRow) 
  value=root.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))



def teachHome():
  selRow = root.progView.curselection()[0]
  selRow += 5
  header = "### MOVE HOME START ###"
  root.progView.insert(selRow, header)
  J1curAng = float(J1calAngleEntryField.get())+(float(J1degPerStepEntryField.get())*15)
  J2curAng = float(J2calAngleEntryField.get())+(float(J2degPerStepEntryField.get())*60)
  J3curAng = float(J3calAngleEntryField.get())+(float(J3degPerStepEntryField.get())*480)
  J4curAng = float(J4calAngleEntryField.get())
  J5curAng = float(J5calAngleEntryField.get())-(float(J5degPerStepEntryField.get())*50)
  J6curAng = float(J6calAngleEntryField.get())
  Speed = speedEntryField.get()
  newPos = "Move J  J1-"+str(J1curAng)+"  J2-"+str(J2curAng)+"  J3-"+str(J3curAng)+"  J4-"+str(J4curAng)+"  J5-"+str(J5curAng)+"  J6-"+str(J6curAng)+"  Speed-"+Speed               
  root.progView.insert(selRow, newPos)
  ###
  J1curAng = float(J1calAngleEntryField.get())+(float(J1degPerStepEntryField.get())*15)
  J2curAng = float(J2calAngleEntryField.get())
  J3curAng = float(J3calAngleEntryField.get())
  J4curAng = float(J4calAngleEntryField.get())
  J5curAng = float(J5calAngleEntryField.get())
  J6curAng = float(J6calAngleEntryField.get())
  Speed = speedEntryField.get()
  newPos = "Move J  J1-"+str(J1curAng)+"  J2-"+str(J2curAng)+"  J3-"+str(J3curAng)+"  J4-"+str(J4curAng)+"  J5-"+str(J5curAng)+"  J6-"+str(J6curAng)+"  Speed-"+Speed               
  root.progView.insert(selRow, newPos)
  ###
  J1curAng = int(J1calAngleEntryField.get())
  J2curAng = int(J2calAngleEntryField.get())
  J3curAng = int(J3calAngleEntryField.get())
  J4curAng = int(J4calAngleEntryField.get())
  J5curAng = int(J5calAngleEntryField.get())
  J6curAng = int(J6calAngleEntryField.get())
  Speed = speedEntryField.get()
  newPos = "Move J  J1-"+str(J1curAng)+"  J2-"+str(J2curAng)+"  J3-"+str(J3curAng)+"  J4-"+str(J4curAng)+"  J5-"+str(J5curAng)+"  J6-"+str(J6curAng)+"  Speed-"+Speed               
  root.progView.insert(selRow, newPos)
  ###
  footer = "### MOVE HOME END ###"
  root.progView.insert(selRow, footer)
  root.progView.selection_clear(0, END)  
  root.progView.select_set(selRow)
  value=root.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def exitHome():
  selRow = root.progView.curselection()[0]
  selRow += 5
  header = "### EXIT HOME START ###"
  root.progView.insert(selRow, header)
  J1curAng = int(J1calAngleEntryField.get())
  J2curAng = int(J2calAngleEntryField.get())
  J3curAng = int(J3calAngleEntryField.get())
  J4curAng = int(J4calAngleEntryField.get())
  J5curAng = int(J5calAngleEntryField.get())
  J6curAng = int(J6calAngleEntryField.get())
  Speed = speedEntryField.get()
  newPos = "Move J  J1-"+str(J1curAng)+"  J2-"+str(J2curAng)+"  J3-"+str(J3curAng)+"  J4-"+str(J4curAng)+"  J5-"+str(J5curAng)+"  J6-"+str(J6curAng)+"  Speed-"+Speed               
  root.progView.insert(selRow, newPos)
  ###
  J1curAng = float(J1calAngleEntryField.get())+(float(J1degPerStepEntryField.get())*15)
  J2curAng = float(J2calAngleEntryField.get())
  J3curAng = float(J3calAngleEntryField.get())
  J4curAng = float(J4calAngleEntryField.get())
  J5curAng = float(J5calAngleEntryField.get())
  J6curAng = float(J6calAngleEntryField.get())
  Speed = speedEntryField.get()
  newPos = "Move J  J1-"+str(J1curAng)+"  J2-"+str(J2curAng)+"  J3-"+str(J3curAng)+"  J4-"+str(J4curAng)+"  J5-"+str(J5curAng)+"  J6-"+str(J6curAng)+"  Speed-"+Speed               
  root.progView.insert(selRow, newPos)
  ###
  J1curAng = float(J1calAngleEntryField.get())+(float(J1degPerStepEntryField.get())*15)
  J2curAng = float(J2calAngleEntryField.get())+(float(J2degPerStepEntryField.get())*60)
  J3curAng = float(J3calAngleEntryField.get())+(float(J3degPerStepEntryField.get())*480)
  J4curAng = float(J4calAngleEntryField.get())
  J5curAng = float(J5calAngleEntryField.get())-(float(J5degPerStepEntryField.get())*50)
  J6curAng = float(J6calAngleEntryField.get())
  Speed = speedEntryField.get()
  newPos = "Move J  J1-"+str(J1curAng)+"  J2-"+str(J2curAng)+"  J3-"+str(J3curAng)+"  J4-"+str(J4curAng)+"  J5-"+str(J5curAng)+"  J6-"+str(J6curAng)+"  Speed-"+Speed               
  root.progView.insert(selRow, newPos)
  ###
  footer = "### EXIT HOME END ###"
  root.progView.insert(selRow, footer)
  root.progView.selection_clear(0, END)  
  root.progView.select_set(selRow)
  value=root.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))



def waitTime():
  selRow = root.progView.curselection()[0]
  selRow += 1
  seconds = waitTimeEntryField.get()
  newTime = "Wait T - wait time - Seconds-"+seconds               
  root.progView.insert(selRow, newTime)
  root.progView.selection_clear(0, END) 
  root.progView.select_set(selRow) 
  value=root.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))


def waitInputOn():
  selRow = root.progView.curselection()[0]
  selRow += 1
  input = waitInputEntryField.get()
  newInput = "Wait I - wait input ON - Input-"+input              
  root.progView.insert(selRow, newInput)
  root.progView.selection_clear(0, END) 
  root.progView.select_set(selRow) 
  value=root.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def waitInputOff():
  selRow = root.progView.curselection()[0]
  selRow += 1
  input = waitInputOffEntryField.get()
  newInput = "Wait Off - wait input OFF - Input-"+input              
  root.progView.insert(selRow, newInput)
  root.progView.selection_clear(0, END) 
  root.progView.select_set(selRow) 
  value=root.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def setOutputOn():
  selRow = root.progView.curselection()[0]
  selRow += 1
  output = outputOnEntryField.get()
  newOutput = "Out On - set output ON - Output-"+output              
  root.progView.insert(selRow, newOutput)
  root.progView.selection_clear(0, END) 
  root.progView.select_set(selRow) 
  value=root.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def setOutputOff():
  selRow = root.progView.curselection()[0]
  selRow += 1
  output = outputOffEntryField.get()
  newOutput = "Out Off - set output OFF - Output-"+output              
  root.progView.insert(selRow, newOutput)
  root.progView.selection_clear(0, END) 
  root.progView.select_set(selRow) 
  value=root.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def tabNumber():
  selRow = root.progView.curselection()[0]
  selRow += 1
  tabNum = tabNumEntryField.get()
  tabins = "Tab Number "+tabNum              
  root.progView.insert(selRow, tabins) 
  value=root.progView.get(0,END)
  root.progView.selection_clear(0, END) 
  root.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')

def jumpTab():
  selRow = root.progView.curselection()[0]
  selRow += 1
  tabNum = jumpTabEntryField.get()
  tabjmp = "Jump Tab-"+tabNum              
  root.progView.insert(selRow, tabjmp) 
  value=root.progView.get(0,END)
  root.progView.selection_clear(0, END)
  root.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')

def IfOnjumpTab():
  selRow = root.progView.curselection()[0]
  selRow += 1
  inpNum = IfOnjumpInputTabEntryField.get()
  tabNum = IfOnjumpNumberTabEntryField.get()
  tabjmp = "If On Jump - Input-"+inpNum+" Jump to Tab-"+tabNum             
  root.progView.insert(selRow, tabjmp)   
  value=root.progView.get(0,END)
  root.progView.selection_clear(0, END) 
  root.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')

def IfOffjumpTab():
  selRow = root.progView.curselection()[0]
  selRow += 1
  inpNum = IfOffjumpInputTabEntryField.get()
  tabNum = IfOffjumpNumberTabEntryField.get()
  tabjmp = "If Off Jump - Input-"+inpNum+" Jump to Tab-"+tabNum             
  root.progView.insert(selRow, tabjmp) 
  value=root.progView.get(0,END)
  root.progView.selection_clear(0, END) 
  root.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')


def Servo():
  selRow = root.progView.curselection()[0]
  selRow += 1
  servoNum = servoNumEntryField.get()
  servoPos = servoPosEntryField.get()
  servoins = "Servo number "+servoNum+" to position: "+servoPos              
  root.progView.insert(selRow, servoins)
  root.progView.selection_clear(0, END) 
  root.progView.select_set(selRow) 
  value=root.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def loadProg():
  progframe=Frame(root)
  progframe.place(x=20,y=172)
  #progframe.pack(side=RIGHT, fill=Y)
  scrollbar = Scrollbar(progframe) 
  scrollbar.pack(side=RIGHT, fill=Y)
  root.progView = Listbox(progframe,width=48,height=31, yscrollcommand=scrollbar.set)
  root.progView.bind('<<ListboxSelect>>', progViewselect)
  try:
    Prog = pickle.load(open(ProgEntryField.get(),"rb"))
  except:
    try:
      Prog = ['##BEGINNING OF PROGRAM##','Tab Number 1']
      pickle.dump(Prog,open(ProgEntryField.get(),"wb"))    
    except:
      Prog = ['##BEGINNING OF PROGRAM##','Tab Number 1']
      pickle.dump(Prog,open("new","wb"))
      ProgEntryField.insert(0,"new")
  time.sleep(.1)
  for item in Prog:
    root.progView.insert(END,item) 
  root.progView.pack()
  scrollbar.config(command=root.progView.yview)
  savePosData()

def insertCallProg():  
  selRow = root.progView.curselection()[0]
  selRow += 1
  newProg = changeProgEntryField.get()
  changeProg = "Call Program - "+newProg            
  root.progView.insert(selRow, changeProg)
  root.progView.selection_clear(0, END) 
  root.progView.select_set(selRow)  
  value=root.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def insertReturn():  
  selRow = root.progView.curselection()[0]
  selRow += 1
  value = "Return"           
  root.progView.insert(selRow, value)
  root.progView.selection_clear(0, END) 
  root.progView.select_set(selRow)  
  value=root.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))


def progViewselect(e):
  selRow = root.progView.curselection()[0]
  curRowEntryField.delete(0, 'end')
  curRowEntryField.insert(0,selRow)


def Servo0on():
  savePosData() 
  servoPos = servo0onEntryField.get()
  command = "SV0P"+servoPos
  ser.write(command +"\n")
  ser.flushInput()
  time.sleep(.1)  
  ser.read()


def Servo0off():
  savePosData() 
  servoPos = servo0offEntryField.get()
  command = "SV0P"+servoPos
  ser.write(command +"\n")
  ser.flushInput()
  time.sleep(.1)  
  ser.read()


def Servo1on():
  savePosData() 
  servoPos = servo1onEntryField.get()
  command = "SV1P"+servoPos
  ser.write(command +"\n")
  ser.flushInput()
  time.sleep(.1)  
  ser.read() 


def Servo1off():
  savePosData() 
  servoPos = servo1offEntryField.get()
  command = "SV1P"+servoPos
  ser.write(command +"\n")
  ser.flushInput()
  time.sleep(.1)  
  ser.read()
 

def Servo2on():
  savePosData() 
  servoPos = servo2onEntryField.get()
  command = "SV2P"+servoPos
  ser.write(command +"\n")
  ser.flushInput()
  time.sleep(.1)  
  ser.read()


def Servo2off():
  savePosData() 
  servoPos = servo2offEntryField.get()
  command = "SV2P"+servoPos
  ser.write(command +"\n")
  ser.flushInput()
  time.sleep(.1)  
  ser.read()
 

def Servo3on():
  savePosData() 
  servoPos = servo3onEntryField.get()
  command = "SV3P"+servoPos
  ser.write(command +"\n")
  ser.flushInput()
  time.sleep(.1)  
  ser.read()
 

def Servo3off():
  savePosData() 
  servoPos = servo3offEntryField.get()
  command = "SV3P"+servoPos
  ser.write(command +"\n")
  ser.flushInput()
  time.sleep(.1)  
  ser.read() 
  

###LABELS#################################################################
##########################################################################

curRowLab = Label(root, text = "Current Row  = ")
curRowLab.place(x=200, y=150)


runStatusLab = Label(root, text = "PROGRAM STOPPED", bg = "red")
runStatusLab.place(x=20, y=150)

inoutavailLab = Label(root, text = "INPUTS 22-37  /  OUTPUTS 38-53  /  SERVOS A0-A7")
inoutavailLab.place(x=10, y=675)

manEntLab = Label(root, text = "Manual Program Entry")
manEntLab.place(x=665, y=643)

ifOnLab = Label(root,font=("Arial", 6), text = "Input           Tab")
ifOnLab.place(x=892, y=428)

ifOffLab = Label(root,font=("Arial", 6), text = "Input           Tab")
ifOffLab.place(x=892, y=468)

servoLab = Label(root,font=("Arial", 6), text = "Number      Position")
servoLab.place(x=892, y=508)

StepLimLab = Label(root,fg = "dark blue", text = "Step Limits (-,+)")
StepLimLab.place(x=340, y=58)

AngLimLab = Label(root,fg = "dark blue", text = "Angle Limits (-,+)")
AngLimLab.place(x=340, y=83)

ComPortLab = Label(root, text = "COM PORT:")
ComPortLab.place(x=10, y=10)

ProgLab = Label(root, text = "Program:")
ProgLab.place(x=10, y=45)

speedLab = Label(root, text = "Robot Speed (%)")
speedLab.place(x=375, y=320)


J1Lab = Label(root, font=("Arial", 22), text = "J1")
J1Lab.place(x=460, y=20)

J2Lab = Label(root, font=("Arial", 22), text = "J2")
J2Lab.place(x=550, y=20)

J3Lab = Label(root, font=("Arial", 22), text = "J3")
J3Lab.place(x=640, y=20)

J4Lab = Label(root, font=("Arial", 22), text = "J4")
J4Lab.place(x=730, y=20)

J5Lab = Label(root, font=("Arial", 22), text = "J5")
J5Lab.place(x=820, y=20)

J6Lab = Label(root, font=("Arial", 22), text = "J6")
J6Lab.place(x=910, y=20)

J1degPerStepLab = Label(root, text = "Degrees per Step")
J1degPerStepLab.place(x=340, y=108)

J1calAngLab = Label(root,fg = "dark blue", text = "Calibration Angle")
J1calAngLab.place(x=340, y=133)

J1curStepLab = Label(root, text = "Current Step")
J1curStepLab.place(x=340, y=158)

J1curAngLab = Label(root, text = "Current Angle")
J1curAngLab.place(x=340, y=183)

J1jogStepsLab = Label(root,fg = "dark blue", text = "Steps to Jog")
J1jogStepsLab.place(x=340, y=208)

J1jogRobotLab = Label(root, text = "JOG ROBOT")
J1jogRobotLab.place(x=340, y=250)

waitTequalsLab = Label(root, text = "=")
waitTequalsLab.place(x=655, y=360)

waitIequalsLab = Label(root, text = "=")
waitIequalsLab.place(x=655, y=400)

waitIoffequalsLab = Label(root, text = "=")
waitIoffequalsLab.place(x=655, y=440)

outputOnequalsLab = Label(root, text = "=")
outputOnequalsLab.place(x=655, y=480)

outputOffequalsLab = Label(root, text = "=")
outputOffequalsLab.place(x=655, y=520)

tabequalsLab = Label(root, text = "=")
tabequalsLab.place(x=875, y=360)

jumpequalsLab = Label(root, text = "=")
jumpequalsLab.place(x=875, y=400)

jumpIfOnequalsLab = Label(root, text = "=")
jumpIfOnequalsLab.place(x=875, y=440)

jumpIfOffequalsLab = Label(root, text = "=")
jumpIfOffequalsLab.place(x=875, y=480)

servoequalsLab = Label(root, text = "=")
servoequalsLab.place(x=875, y=520)

changeProgequalsLab = Label(root, text = "=")
changeProgequalsLab.place(x=875, y=560)

servo0onequalsLab = Label(root, text = "=")
servo0onequalsLab.place(x=395, y=575)

servo0offequalsLab = Label(root, text = "=")
servo0offequalsLab.place(x=395, y=605)

servo1onequalsLab = Label(root, text = "=")
servo1onequalsLab.place(x=395, y=635)

servo1offequalsLab = Label(root, text = "=")
servo1offequalsLab.place(x=395, y=665)

servo2onequalsLab = Label(root, text = "=")
servo2onequalsLab.place(x=535, y=575)

servo2offequalsLab = Label(root, text = "=")
servo2offequalsLab.place(x=535, y=605)

servo3onequalsLab = Label(root, text = "=")
servo3onequalsLab.place(x=535, y=635)

servo3offequalsLab = Label(root, text = "=")
servo3offequalsLab.place(x=535, y=665)

servoManLab = Label(root, text = "Manual Servo toggle buttons")
servoManLab.place(x=340, y=555)



###BUTTONS################################################################
##########################################################################

servo0onBut = Button(root, text="Servo 0", height=1, width=6, command = Servo0on)
servo0onBut.place(x=340, y=575)

servo0offBut = Button(root, text="Servo 0", height=1, width=6, command = Servo0off)
servo0offBut.place(x=340, y=605)

servo1onBut = Button(root, text="Servo 1", height=1, width=6, command = Servo1on)
servo1onBut.place(x=340, y=635)

servo1offBut = Button(root, text="Servo 1", height=1, width=6, command = Servo1off)
servo1offBut.place(x=340, y=665)

servo2onBut = Button(root, text="Servo 2", height=1, width=6, command = Servo2on)
servo2onBut.place(x=480, y=575)

servo2offBut = Button(root, text="Servo 2", height=1, width=6, command = Servo2off)
servo2offBut.place(x=480, y=605)

servo3onBut = Button(root, text="Servo 3", height=1, width=6, command = Servo3on)
servo3onBut.place(x=480, y=635)

servo4offBut = Button(root, text="Servo 3", height=1, width=6, command = Servo3off)
servo4offBut.place(x=480, y=665)

manEntBut = Button(root, text="Enter", height=1, width=10, command = manAdditem)
manEntBut.place(x=920, y=654)

#teachNewBut = Button(root, text="Teach - Insert Last", height=1, width=20, command = teachInsertEnd)
#teachNewBut.place(x=340, y=360)

teachInsBut = Button(root, text="Teach New Position", height=1, width=20, command = teachInsertBelSelected)
teachInsBut.place(x=340, y=360)

teachReplaceBut = Button(root, text="Teach Replace Selected", height=1, width=20, command = teachReplaceSelected)
teachReplaceBut.place(x=340, y=400)

teachHomeBut = Button(root, text="Move Home - calibrate", height=1, width=20, command = teachHome)
teachHomeBut.place(x=340, y=440)

exitHomeBut = Button(root, text="Exit Home", height=1, width=20, command = exitHome)
exitHomeBut.place(x=340, y=480)

waitTimeBut = Button(root, text="Wait Time (seconds)", height=1, width=20, command = waitTime)
waitTimeBut.place(x=500, y=360)

waitInputOnBut = Button(root, text="Wait Input ON", height=1, width=20, command = waitInputOn)
waitInputOnBut.place(x=500, y=400)

waitInputOffBut = Button(root, text="Wait Input OFF", height=1, width=20, command = waitInputOff)
waitInputOffBut.place(x=500, y=440)

setOutputOnBut = Button(root, text="Set Output On", height=1, width=20, command = setOutputOn)
setOutputOnBut.place(x=500, y=480)

setOutputOffBut = Button(root, text="Set Output OFF", height=1, width=20, command = setOutputOff)
setOutputOffBut.place(x=500, y=520)

tabNumBut = Button(root, text="Create Tab Number", height=1, width=20, command = tabNumber)
tabNumBut.place(x=720, y=360)

jumpTabBut = Button(root, text="Jump to Tab", height=1, width=20, command = jumpTab)
jumpTabBut.place(x=720, y=400)

IfOnjumpTabBut = Button(root, text="If On Jump", height=1, width=20, command = IfOnjumpTab)
IfOnjumpTabBut.place(x=720, y=440)

IfOffjumpTabBut = Button(root, text="If Off Jump", height=1, width=20, command = IfOffjumpTab)
IfOffjumpTabBut.place(x=720, y=480)

servoBut = Button(root, text="Servo", height=1, width=20, command = Servo)
servoBut.place(x=720, y=520)

callBut = Button(root, text="Call Program", height=1, width=20, command = insertCallProg)
callBut.place(x=720, y=560)

returnBut = Button(root, text="Return", height=1, width=20, command = insertReturn)
returnBut.place(x=720, y=600)

comPortBut = Button(root, text="Set Com", height=0, width=7, command = setCom)
comPortBut.place(x=103, y=7)

ProgBut = Button(root, text="Load Program", height=0, width=12, command = loadProg)
ProgBut.place(x=202, y=42)


calibrateBut = Button(root, text="Calibrate Robot", height=1, width=12, command = calRobot)
calibrateBut.place(x=910, y=300)

deleteBut = Button(root, text="Delete", height=1, width=20, command = deleteitem)
deleteBut.place(x=340, y=520)

runProgBut = Button(root, height=60, width=60, command = runProg)
playPhoto=PhotoImage(file="play-icon.gif")
runProgBut.config(image=playPhoto,width="60",height="60")
runProgBut.place(x=20, y=80)

stopProgBut = Button(root, height=60, width=60, command = stopProg)
stopPhoto=PhotoImage(file="stop-icon.gif")
stopProgBut.config(image=stopPhoto,width="60",height="60")
stopProgBut.place(x=200, y=80)

fwdBut = Button(root,text="FWD", height=3, width=4, command = stepFwd)
fwdBut.place(x=100, y=80)

revBut = Button(root,text="REV", height=3, width=4, command = stepRev)
revBut.place(x=150, y=80)

J1jogNegBut = Button(root,text="-", height=2, width=3, command = J1jogNeg)
J1jogNegBut.place(x=442, y=240)

J1jogPosBut = Button(root,text="+", height=2, width=3, command = J1jogPos)
J1jogPosBut.place(x=480, y=240)

J2jogNegBut = Button(root,text="-", height=2, width=3, command = J2jogNeg)
J2jogNegBut.place(x=532, y=240)

J2jogPosBut = Button(root,text="+", height=2, width=3, command = J2jogPos)
J2jogPosBut.place(x=570, y=240)

J3jogNegBut = Button(root,text="-", height=2, width=3, command = J3jogNeg)
J3jogNegBut.place(x=622, y=240)

J3jogPosBut = Button(root,text="+", height=2, width=3, command = J3jogPos)
J3jogPosBut.place(x=660, y=240)

J4jogNegBut = Button(root,text="-", height=2, width=3, command = J4jogNeg)
J4jogNegBut.place(x=712, y=240)

J4jogPosBut = Button(root,text="+", height=2, width=3, command = J4jogPos)
J4jogPosBut.place(x=750, y=240)

J5jogNegBut = Button(root,text="-", height=2, width=3, command = J5jogNeg)
J5jogNegBut.place(x=802, y=240)

J5jogPosBut = Button(root,text="+", height=2, width=3, command = J5jogPos)
J5jogPosBut.place(x=840, y=240)

J6jogNegBut = Button(root,text="-", height=2, width=3, command = J6jogNeg)
J6jogNegBut.place(x=892, y=240)

J6jogPosBut = Button(root,text="+", height=2, width=3, command = J6jogPos)
J6jogPosBut.place(x=930, y=240)








####ENTRY FIELDS##########################################################
##########################################################################

servo0onEntryField = Entry(root,width=5)
servo0onEntryField.place(x=412, y=577)

servo0offEntryField = Entry(root,width=5)
servo0offEntryField.place(x=412, y=607)

servo1onEntryField = Entry(root,width=5)
servo1onEntryField.place(x=412, y=637)

servo1offEntryField = Entry(root,width=5)
servo1offEntryField.place(x=412, y=667)

servo2onEntryField = Entry(root,width=5)
servo2onEntryField.place(x=552, y=577)

servo2offEntryField = Entry(root,width=5)
servo2offEntryField.place(x=552, y=607)

servo3onEntryField = Entry(root,width=5)
servo3onEntryField.place(x=552, y=637)

servo3offEntryField = Entry(root,width=5)
servo3offEntryField.place(x=552, y=667)

curRowEntryField = Entry(root,width=5)
curRowEntryField.place(x=290, y=150)

manEntryField = Entry(root,width=40)
manEntryField.place(x=665, y=660)

ProgEntryField = Entry(root,width=20)
ProgEntryField.place(x=70, y=45)

comPortEntryField = Entry(root,width=2)
comPortEntryField.place(x=80, y=10)

speedEntryField = Entry(root,width=5)
speedEntryField.place(x=340, y=320)

waitTimeEntryField = Entry(root,width=5)
waitTimeEntryField.place(x=672, y=363)

waitInputEntryField = Entry(root,width=5)
waitInputEntryField.place(x=672, y=403)

waitInputOffEntryField = Entry(root,width=5)
waitInputOffEntryField.place(x=672, y=443)

outputOnEntryField = Entry(root,width=5)
outputOnEntryField.place(x=672, y=483)

outputOffEntryField = Entry(root,width=5)
outputOffEntryField.place(x=672, y=523)

tabNumEntryField = Entry(root,width=5)
tabNumEntryField.place(x=892, y=363)

jumpTabEntryField = Entry(root,width=5)
jumpTabEntryField.place(x=892, y=403)

IfOnjumpInputTabEntryField = Entry(root,width=5)
IfOnjumpInputTabEntryField.place(x=892, y=443)

IfOnjumpNumberTabEntryField = Entry(root,width=5)
IfOnjumpNumberTabEntryField.place(x=932, y=443)

IfOffjumpInputTabEntryField = Entry(root,width=5)
IfOffjumpInputTabEntryField.place(x=892, y=483)

IfOffjumpNumberTabEntryField = Entry(root,width=5)
IfOffjumpNumberTabEntryField.place(x=932, y=483)

servoNumEntryField = Entry(root,width=5)
servoNumEntryField.place(x=892, y=523)

servoPosEntryField = Entry(root,width=5)
servoPosEntryField.place(x=932, y=523)

changeProgEntryField = Entry(root,width=12)
changeProgEntryField.place(x=892, y=563)


  ### J1 ###

J1stepLimNegEntryField = Entry(root,width=5)
J1stepLimNegEntryField.place(x=442, y=60)

J1stepLimPosEntryField = Entry(root,width=5)
J1stepLimPosEntryField.place(x=480, y=60)

J1angLimNegEntryField = Entry(root,width=5)
J1angLimNegEntryField.place(x=442, y=85)

J1angLimPosEntryField = Entry(root,width=5)
J1angLimPosEntryField.place(x=480, y=85)

J1degPerStepEntryField = Entry(root,width=5)
J1degPerStepEntryField.place(x=460, y=110)

J1calAngleEntryField = Entry(root,width=5)
J1calAngleEntryField.place(x=460, y=135)

J1curStepEntryField = Entry(root,width=5)
J1curStepEntryField.place(x=460, y=160)

J1curAngEntryField = Entry(root,width=5)
J1curAngEntryField.place(x=460, y=185)

J1jogStepsEntryField = Entry(root,width=5)
J1jogStepsEntryField.place(x=460, y=210)


   ### J2 ###

J2stepLimNegEntryField = Entry(root,width=5)
J2stepLimNegEntryField.place(x=532, y=60)

J2stepLimPosEntryField = Entry(root,width=5)
J2stepLimPosEntryField.place(x=570, y=60)

J2angLimNegEntryField = Entry(root,width=5)
J2angLimNegEntryField.place(x=532, y=85)

J2angLimPosEntryField = Entry(root,width=5)
J2angLimPosEntryField.place(x=570, y=85)

J2degPerStepEntryField = Entry(root,width=5)
J2degPerStepEntryField.place(x=550, y=110)

J2calAngleEntryField = Entry(root,width=5)
J2calAngleEntryField.place(x=550, y=135)

J2curStepEntryField = Entry(root,width=5)
J2curStepEntryField.place(x=550, y=160)

J2curAngEntryField = Entry(root,width=5)
J2curAngEntryField.place(x=550, y=185)

J2jogStepsEntryField = Entry(root,width=5)
J2jogStepsEntryField.place(x=550, y=210)


   ### J3 ###

J3stepLimNegEntryField = Entry(root,width=5)
J3stepLimNegEntryField.place(x=622, y=60)

J3stepLimPosEntryField = Entry(root,width=5)
J3stepLimPosEntryField.place(x=660, y=60)

J3angLimNegEntryField = Entry(root,width=5)
J3angLimNegEntryField.place(x=622, y=85)

J3angLimPosEntryField = Entry(root,width=5)
J3angLimPosEntryField.place(x=660, y=85)

J3degPerStepEntryField = Entry(root,width=5)
J3degPerStepEntryField.place(x=640, y=110)

J3calAngleEntryField = Entry(root,width=5)
J3calAngleEntryField.place(x=640, y=135)

J3curStepEntryField = Entry(root,width=5)
J3curStepEntryField.place(x=640, y=160)

J3curAngEntryField = Entry(root,width=5)
J3curAngEntryField.place(x=640, y=185)

J3jogStepsEntryField = Entry(root,width=5)
J3jogStepsEntryField.place(x=640, y=210)


   ### J4 ###

J4stepLimNegEntryField = Entry(root,width=5)
J4stepLimNegEntryField.place(x=712, y=60)

J4stepLimPosEntryField = Entry(root,width=5)
J4stepLimPosEntryField.place(x=750, y=60)

J4angLimNegEntryField = Entry(root,width=5)
J4angLimNegEntryField.place(x=712, y=85)

J4angLimPosEntryField = Entry(root,width=5)
J4angLimPosEntryField.place(x=750, y=85)

J4degPerStepEntryField = Entry(root,width=5)
J4degPerStepEntryField.place(x=730, y=110)

J4calAngleEntryField = Entry(root,width=5)
J4calAngleEntryField.place(x=730, y=135)

J4curStepEntryField = Entry(root,width=5)
J4curStepEntryField.place(x=730, y=160)

J4curAngEntryField = Entry(root,width=5)
J4curAngEntryField.place(x=730, y=185)

J4jogStepsEntryField = Entry(root,width=5)
J4jogStepsEntryField.place(x=730, y=210)


   ### J5 ###

J5stepLimNegEntryField = Entry(root,width=5)
J5stepLimNegEntryField.place(x=802, y=60)

J5stepLimPosEntryField = Entry(root,width=5)
J5stepLimPosEntryField.place(x=840, y=60)

J5angLimNegEntryField = Entry(root,width=5)
J5angLimNegEntryField.place(x=802, y=85)

J5angLimPosEntryField = Entry(root,width=5)
J5angLimPosEntryField.place(x=840, y=85)

J5degPerStepEntryField = Entry(root,width=5)
J5degPerStepEntryField.place(x=820, y=110)

J5calAngleEntryField = Entry(root,width=5)
J5calAngleEntryField.place(x=820, y=135)

J5curStepEntryField = Entry(root,width=5)
J5curStepEntryField.place(x=820, y=160)

J5curAngEntryField = Entry(root,width=5)
J5curAngEntryField.place(x=820, y=185)

J5jogStepsEntryField = Entry(root,width=5)
J5jogStepsEntryField.place(x=820, y=210)


   ### J6 ###

J6stepLimNegEntryField = Entry(root,width=5)
J6stepLimNegEntryField.place(x=892, y=60)

J6stepLimPosEntryField = Entry(root,width=5)
J6stepLimPosEntryField.place(x=930, y=60)

J6angLimNegEntryField = Entry(root,width=5)
J6angLimNegEntryField.place(x=892, y=85)

J6angLimPosEntryField = Entry(root,width=5)
J6angLimPosEntryField.place(x=930, y=85)

J6degPerStepEntryField = Entry(root,width=5)
J6degPerStepEntryField.place(x=910, y=110)

J6calAngleEntryField = Entry(root,width=5)
J6calAngleEntryField.place(x=910, y=135)

J6curStepEntryField = Entry(root,width=5)
J6curStepEntryField.place(x=910, y=160)

J6curAngEntryField = Entry(root,width=5)
J6curAngEntryField.place(x=910, y=185)

J6jogStepsEntryField = Entry(root,width=5)
J6jogStepsEntryField.place(x=910, y=210)


###OPEN CALIBRATION AND PROG FILE AND LOAD LISTS##########################
##########################################################################












###OPEN CAL FILE AND LOAD LIST###########################################
##########################################################################

calibration = Listbox(root,width=20,height=60)
#calibration.place(x=160,y=170)

try:
  Cal = pickle.load(open("ARbot.cal","rb"))
except:
  Cal = "0"
  pickle.dump(Cal,open("ARbot.cal","wb"))
for item in Cal:
  calibration.insert(END,item)
J1stepLimNeg=calibration.get("0")
J1stepLimPos=calibration.get("1")
J1angLimNeg =calibration.get("2")
J1angLimPos =calibration.get("3")
J1degPerStep=calibration.get("4")
J1calAngle  =calibration.get("5")
J1curStep   =calibration.get("6")
J1curAng    =calibration.get("7")
J1jogSteps  =calibration.get("8")
J2stepLimNeg=calibration.get("9")
J2stepLimPos=calibration.get("10")
J2angLimNeg =calibration.get("11")
J2angLimPos =calibration.get("12")
J2degPerStep=calibration.get("13")
J2calAngle  =calibration.get("14")
J2curStep   =calibration.get("15")
J2curAng    =calibration.get("16")
J2jogSteps  =calibration.get("17")
J3stepLimNeg=calibration.get("18")
J3stepLimPos=calibration.get("19")
J3angLimNeg =calibration.get("20")
J3angLimPos =calibration.get("21")
J3degPerStep=calibration.get("22")
J3calAngle  =calibration.get("23")
J3curStep   =calibration.get("24")
J3curAng    =calibration.get("25")
J3jogSteps  =calibration.get("26")
J4stepLimNeg=calibration.get("27")
J4stepLimPos=calibration.get("28")
J4angLimNeg =calibration.get("29")
J4angLimPos =calibration.get("30")
J4degPerStep=calibration.get("31")
J4calAngle  =calibration.get("32")
J4curStep   =calibration.get("33")
J4curAng    =calibration.get("34")
J4jogSteps  =calibration.get("35")
J5stepLimNeg=calibration.get("36")
J5stepLimPos=calibration.get("37")
J5angLimNeg =calibration.get("38")
J5angLimPos =calibration.get("39")
J5degPerStep=calibration.get("40")
J5calAngle  =calibration.get("41")
J5curStep   =calibration.get("42")
J5curAng    =calibration.get("43")
J5jogSteps  =calibration.get("44")
J6stepLimNeg=calibration.get("45")
J6stepLimPos=calibration.get("46")
J6angLimNeg =calibration.get("47")
J6angLimPos =calibration.get("48")
J6degPerStep=calibration.get("49")
J6calAngle  =calibration.get("50")
J6curStep   =calibration.get("51")
J6curAng    =calibration.get("52")
J6jogSteps  =calibration.get("53")
comPort     =calibration.get("54")
Prog        =calibration.get("55")
Servo0on    =calibration.get("56")
Servo0off   =calibration.get("57")
Servo1on    =calibration.get("58")
Servo1off   =calibration.get("59")
Servo2on    =calibration.get("60")
Servo2off   =calibration.get("61")
Servo3on    =calibration.get("62")
Servo3off   =calibration.get("63")

####
J1stepLimNegEntryField.insert(0,str(J1stepLimNeg))
J1stepLimPosEntryField.insert(0,str(J1stepLimPos))
J1angLimNegEntryField.insert(0,str(J1angLimNeg))
J1angLimPosEntryField.insert(0,str(J1angLimPos))
J1degPerStepEntryField.insert(0,str(J1degPerStep))
J1calAngleEntryField.insert(0,str(J1calAngle))
J1curStepEntryField.insert(0,str(J1curStep))
J1curAngEntryField.insert(0,str(J1curAng))
J1jogStepsEntryField.insert(0,str(J1jogSteps))
J2stepLimNegEntryField.insert(0,str(J2stepLimNeg))
J2stepLimPosEntryField.insert(0,str(J2stepLimPos))
J2angLimNegEntryField.insert(0,str(J2angLimNeg))
J2angLimPosEntryField.insert(0,str(J2angLimPos))
J2degPerStepEntryField.insert(0,str(J2degPerStep))
J2calAngleEntryField.insert(0,str(J2calAngle))
J2curStepEntryField.insert(0,str(J2curStep))
J2curAngEntryField.insert(0,str(J2curAng))
J2jogStepsEntryField.insert(0,str(J2jogSteps))
J3stepLimNegEntryField.insert(0,str(J3stepLimNeg))
J3stepLimPosEntryField.insert(0,str(J3stepLimPos))
J3angLimNegEntryField.insert(0,str(J3angLimNeg))
J3angLimPosEntryField.insert(0,str(J3angLimPos))
J3degPerStepEntryField.insert(0,str(J3degPerStep))
J3calAngleEntryField.insert(0,str(J3calAngle))
J3curStepEntryField.insert(0,str(J3curStep))
J3curAngEntryField.insert(0,str(J3curAng))
J3jogStepsEntryField.insert(0,str(J3jogSteps))
J4stepLimNegEntryField.insert(0,str(J4stepLimNeg))
J4stepLimPosEntryField.insert(0,str(J4stepLimPos))
J4angLimNegEntryField.insert(0,str(J4angLimNeg))
J4angLimPosEntryField.insert(0,str(J4angLimPos))
J4degPerStepEntryField.insert(0,str(J4degPerStep))
J4calAngleEntryField.insert(0,str(J4calAngle))
J4curStepEntryField.insert(0,str(J4curStep))
J4curAngEntryField.insert(0,str(J4curAng))
J4jogStepsEntryField.insert(0,str(J4jogSteps))
J5stepLimNegEntryField.insert(0,str(J5stepLimNeg))
J5stepLimPosEntryField.insert(0,str(J5stepLimPos))
J5angLimNegEntryField.insert(0,str(J5angLimNeg))
J5angLimPosEntryField.insert(0,str(J5angLimPos))
J5degPerStepEntryField.insert(0,str(J5degPerStep))
J5calAngleEntryField.insert(0,str(J5calAngle))
J5curStepEntryField.insert(0,str(J5curStep))
J5curAngEntryField.insert(0,str(J5curAng))
J5jogStepsEntryField.insert(0,str(J5jogSteps))
J6stepLimNegEntryField.insert(0,str(J6stepLimNeg))
J6stepLimPosEntryField.insert(0,str(J6stepLimPos))
J6angLimNegEntryField.insert(0,str(J6angLimNeg))
J6angLimPosEntryField.insert(0,str(J6angLimPos))
J6degPerStepEntryField.insert(0,str(J6degPerStep))
J6calAngleEntryField.insert(0,str(J6calAngle))
J6curStepEntryField.insert(0,str(J6curStep))
J6curAngEntryField.insert(0,str(J6curAng))
J6jogStepsEntryField.insert(0,str(J6jogSteps))
comPortEntryField.insert(0,str(comPort))
speedEntryField.insert(0,"100")
ProgEntryField.insert(0,(Prog))
servo0onEntryField.insert(0,str(Servo0on))
servo0offEntryField.insert(0,str(Servo0off))
servo1onEntryField.insert(0,str(Servo1on))
servo1offEntryField.insert(0,str(Servo1off))
servo2onEntryField.insert(0,str(Servo2on))
servo2offEntryField.insert(0,str(Servo2off))
servo3onEntryField.insert(0,str(Servo3on))
servo3offEntryField.insert(0,str(Servo3off))

try:
  setCom()
except:
  print ""

loadProg()

root.mainloop()