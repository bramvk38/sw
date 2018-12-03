#!/usr/bin/python -d
 
import sys
from PyQt5 import QtWidgets
from ui.main import MainWindow
import tkinter as tk
from tkinter import filedialog
 
def CalcApp():
  
  def initButton():
    ui.Start.clicked.connect(on_click)
    ui.Export.clicked.connect(on_export)
    ui.Open.clicked.connect(on_open)
    ui.Save.clicked.connect(on_save)
  
  def on_save():
    root = tk.Tk()
    root.withdraw()
    file = filedialog.asksaveasfile(mode='w', defaultextension=".plague",  filetypes=[('Plague files','*.plague')])
    if file is None:
        return
    file.write(ui.S0.toPlainText()) 
    file.write("\n")
    file.write(ui.N0.toPlainText()) 
    file.write("\n")
    file.write(ui.BPM0.toPlainText()) 
    file.write("\n")
    file.write(ui.Beats0.toPlainText()) 
    file.write("\n")
    file.write(ui.S1.toPlainText()) 
    file.write("\n")
    file.write(ui.N1.toPlainText()) 
    file.write("\n")
    file.write(ui.BPM1.toPlainText()) 
    file.write("\n")
    file.write(ui.Beats1.toPlainText()) 
    file.write("\n")
    file.write(ui.S2.toPlainText()) 
    file.write("\n")
    file.write(ui.N2.toPlainText()) 
    file.write("\n")
    file.write(ui.BPM2.toPlainText()) 
    file.write("\n")
    file.write(ui.Beats2.toPlainText()) 
    file.write("\n")
    file.write(ui.S3.toPlainText()) 
    file.write("\n")
    file.write(ui.N3.toPlainText()) 
    file.write("\n")
    file.write(ui.BPM3.toPlainText()) 
    file.write("\n")
    file.write(ui.Beats3.toPlainText()) 
    file.write("\n")
    file.write(ui.FileName.toPlainText()) 
    file.write("\n")
    file.write(ui.LyricsList.toPlainText()) 
    file.close()
  
  def on_open():
    root = tk.Tk()
    root.withdraw()
    file = filedialog.askopenfile(filetypes=[('Plague files','*.plague')])
    if file is None:
        return
    filelines = file.readlines()
    ui.S0.setText(filelines[0].rstrip())
    ui.N0.setText(filelines[1].rstrip())
    ui.BPM0.setText(filelines[2].rstrip())
    ui.Beats0.setText(filelines[3].rstrip())
    ui.S1.setText(filelines[4].rstrip())
    ui.N1.setText(filelines[5].rstrip())
    ui.BPM1.setText(filelines[6].rstrip())
    ui.Beats1.setText(filelines[7].rstrip())
    ui.S2.setText(filelines[8].rstrip())
    ui.N2.setText(filelines[9].rstrip())
    ui.BPM2.setText(filelines[10].rstrip())
    ui.Beats2.setText(filelines[11].rstrip())
    ui.S3.setText(filelines[12].rstrip())
    ui.N3.setText(filelines[13].rstrip())
    ui.BPM3.setText(filelines[14].rstrip())
    ui.Beats3.setText(filelines[15].rstrip())
    ui.FileName.setText(filelines[16].rstrip())
    ui.LyricsList.setText("")
    Lyrics = filelines[17:]
    for x in Lyrics:
      ui.LyricsList.append(x.rstrip())
  
  def initText():
      ui.S0.setText("0")
      ui.N0.setText("60")
      ui.BPM0.setText("150")
      ui.Beats0.setText("4")
      ui.S1.setText("0")
      ui.N1.setText("0")
      ui.BPM1.setText("0")
      ui.Beats1.setText("0")
      ui.S2.setText("0")
      ui.N2.setText("0")
      ui.BPM2.setText("0")
      ui.Beats2.setText("0")
      ui.S3.setText("0")
      ui.N3.setText("0")
      ui.BPM3.setText("0")
      ui.Beats3.setText("0")
      ui.FileName.setText("Song title")
  
  def try_int(text):
      try:
          int(text)
          return int(text)
      except:
          return 0
          
  def try_float(text):
      try:
          float(text)
          return float(text)
      except:
          return 0
  
  def to_timestamp(val):
      TimeStr = str(format(val, '.3f')).zfill(10)
      TimeLow = TimeStr[-3:]
      TimeHigh = TimeStr[:-4]
      TimeHigh = '{0:02.0f}:{1:02.0f}'.format(*divmod(int(TimeHigh), 60))
      TimeStamp = ("00:%s,%s" % (TimeHigh, TimeLow))
      return TimeStamp
  
  def on_click(export):
      ui.OutList.clear()
      
      # Get parameters
      Lyrics = ui.LyricsList.toPlainText()
      
      start0 = try_float(ui.S0.toPlainText())
      steps0 = try_int(ui.N0.toPlainText())
      bpm0 = try_int(ui.BPM0.toPlainText())
      beats0 = try_int(ui.Beats0.toPlainText())
      start1 = try_float(ui.S1.toPlainText())
      steps1 = try_int(ui.N1.toPlainText())
      bpm1 = try_int(ui.BPM1.toPlainText())
      beats1 = try_int(ui.Beats1.toPlainText()) 
      start2 = try_float(ui.S2.toPlainText())
      steps2 = try_int(ui.N2.toPlainText())
      bpm2 = try_int(ui.BPM2.toPlainText())
      beats2 = try_int(ui.Beats2.toPlainText())
      start3 = try_float(ui.S3.toPlainText())
      steps3 = try_int(ui.N3.toPlainText())
      bpm3 = try_int(ui.BPM3.toPlainText())
      beats3 = try_int(ui.Beats3.toPlainText())
      
      if bpm0 > 0:
        incr0 = float((60 / bpm0) * beats0)
      else:
        incr0 = 0
      if bpm1 > 0:
        incr1 = float((60 / bpm1) * beats1)
      else:
        incr1 = 0
      if bpm2 > 0:
        incr2 = float((60 / bpm2) * beats2)
      else:
        incr2 = 0
      if bpm3 > 0:
        incr3 = float((60 / bpm3) * beats3)
      else:
        incr3 = 0
      
      sub90_0 = incr0 * 0.9
      sub90_1 = incr1 * 0.9
      sub90_2 = incr2 * 0.9
      sub90_3 = incr3 * 0.9
      
      # Make lists
      LyricsLines = Lyrics.split('\n')
      TimeStamp = list()
      for i in range(steps0):
        TimeStart = to_timestamp(start0 + (i * incr0))
        TimeEnd = to_timestamp(start0 + (i * incr0) + sub90_0)
        TimeStamp.append("%s --> %s" % (TimeStart,  TimeEnd))
        LyricsLines.append(" ")
      for i in range(steps1):
        TimeStart = to_timestamp(start1 + (i * incr1))
        TimeEnd = to_timestamp(start1 + (i * incr1) + sub90_1)
        TimeStamp.append("%s --> %s" % (TimeStart,  TimeEnd))
        LyricsLines.append(" ")
      for i in range(steps2):
        TimeStart = to_timestamp(start2 + (i * incr2))
        TimeEnd = to_timestamp(start2 + (i * incr2) + sub90_2)
        TimeStamp.append("%s --> %s" % (TimeStart,  TimeEnd))
        LyricsLines.append(" ")
      for i in range(steps3):
        TimeStart = to_timestamp(start3 + (i * incr3))
        TimeEnd = to_timestamp(start3 + (i * incr3) + sub90_3)
        TimeStamp.append("%s --> %s" % (TimeStart,  TimeEnd))
        LyricsLines.append(" ")
      
      # Print lists to preview
      for i in range(steps0+steps1+steps2+steps3):
        ui.OutList.addItem("%s  %s" % (TimeStamp[i], LyricsLines[i]))
        
      if export == 1:
        name = ui.FileName.toPlainText()
        file = open('%s.srt' % (name), "w")
        for i in range(steps0+steps1+steps2+steps3):
          file.write("%s\n" % (i+1))
          file.write("%s\n" % (TimeStamp[i]))
          file.write("%s\n" % (LyricsLines[i]))
          file.write("\n")
        file.close() 
  
  def on_export():
      on_click(1)
  
  initButton()
  initText()
  
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    ex = CalcApp()
    sys.exit(app.exec_())
