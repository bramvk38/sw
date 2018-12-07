import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.clock import Clock

import ntpath

import tkinter as tk
from tkinter import filedialog

# Define global variables
global audio_file
global project_file
global selected
global Lyrics0
global Lyrics1
global Lyrics2
global Lyrics3
global Lyrics4
global Lyrics5
global Lyrics6
global Lyrics7
global PartitionColor
global TimeStartList
global TimeEndList
global TimeLyricsList
global Audio
global SliderVal
audio_file = 'unknown.mp3'
project_file = ""
selected = 0
Lyrics0 = ""
Lyrics1 = ""
Lyrics2 = ""
Lyrics3 = ""
Lyrics4 = ""
Lyrics5 = ""
Lyrics6 = ""
Lyrics7 = ""
TimeStartList = list()
TimeEndList = list()
TimeLyricsList = list()
PartitionColor = [[1,0,0,1],[0,1,0,1],[.1,.1,1,1],[1,1,0,1],[0,1,1,1],[1,0,1,1],[.5,.5,1,1],[1,.5,.5,1]]
Audio = SoundLoader.load(audio_file)
SliderVal = float(0)
        
class ContainerBox(BoxLayout):

    # Init
    def __init__(self, **kwargs):
        super(ContainerBox, self).__init__(**kwargs)
        self.ids.lbl_0.color = PartitionColor[0]
        self.ids.lbl_1.color = PartitionColor[1]
        self.ids.lbl_2.color = PartitionColor[2]
        self.ids.lbl_3.color = PartitionColor[3]
        self.ids.lbl_4.color = PartitionColor[4]
        self.ids.lbl_5.color = PartitionColor[5]
        self.ids.lbl_6.color = PartitionColor[6]
        self.ids.lbl_7.color = PartitionColor[7]
        self.ids.lbl_selected.color = PartitionColor[selected]
        self.ids.lbl_selected.text = "%s" % (selected+1)
        Clock.schedule_interval(self.Refresh, 0.1)
        self.ids.lbl_msg.text = "Welcome to PlagueLyrics"
    def close_app(self):
        App.get_running_app().stop()
    
    # Update text
    def Refresh(self, *args):
        hit = 0
        if Audio.state == 'play':
            self.ids.lbl_msg.text = "Audio: %s sec" % (format(Audio.get_pos(),'.3f'))
        for i in range(len(TimeStartList)):
            if Audio.get_pos() >= TimeStartList[i] and Audio.get_pos() <= TimeEndList[i]:
                self.ids.lbl_subs.text = "%s" % (TimeLyricsList[i])
                hit = 1
        if hit == 0: self.ids.lbl_subs.text = ""
    def SubSize(self, up):
        if up == 1: self.ids.lbl_subs.font_size += 1
        if up == 0: self.ids.lbl_subs.font_size -= 1
    def LyricsSize(self, up):
        if up == 1: self.ids.Lyrics.font_size += 1
        if up == 0: self.ids.Lyrics.font_size -= 1
        if up == 1: self.ids.LyricsOutput.font_size += 1
        if up == 0: self.ids.LyricsOutput.font_size -= 1

    # Lyrics Partition Functions
    def UpdatePartition(self):
        self.ids.lbl_selected.color = PartitionColor[selected]
        self.ids.lbl_selected.text = "%s" % (selected+1)
        if selected == 0: self.ids.Lyrics.text = Lyrics0
        if selected == 1: self.ids.Lyrics.text = Lyrics1
        if selected == 2: self.ids.Lyrics.text = Lyrics2
        if selected == 3: self.ids.Lyrics.text = Lyrics3
        if selected == 4: self.ids.Lyrics.text = Lyrics4
        if selected == 5: self.ids.Lyrics.text = Lyrics5
        if selected == 6: self.ids.Lyrics.text = Lyrics6
        if selected == 7: self.ids.Lyrics.text = Lyrics7
    def PrevPartition(self):
        global selected
        if selected > 0:
            selected = selected - 1
            self.UpdatePartition()
    def NextPartition(self):
        global selected
        if selected < 7:
            selected = selected + 1
            self.UpdatePartition()

    # audio Functions
    def PlayAudio(self):
        global Audio
        Audio = SoundLoader.load(ntpath.dirname(project_file)+"/"+audio_file)
        Audio.play()
    def StopAudio(self):
        global Audio
        Audio.stop()
    def AudioVolume(self, up):
        global Audio
        if up == 1 and Audio.volume < 1: Audio.volume += 0.05
        if up == 0 and Audio.volume > 0: Audio.volume -= 0.05
    def ChangeAudioPos(self):
        global Audio
        global SliderVal
        if SliderVal != self.ids.AudioSlider.value and audio_file != "":
            SliderVal = self.ids.AudioSlider.value
            Audio.seek(SliderVal * Audio.length)

    # File Functions
    def save(self, save_as):
        global project_file
        if save_as == 1 or ".plague" not in project_file:
            root = tk.Tk()
            root.withdraw()
            file = filedialog.asksaveasfile(mode='w', defaultextension=".plague",  filetypes=[('Plague files','*.plague')])
            if file is None:
                self.ids.lbl_msg.text = "Not saved!"
                return
            project_file = file.name
            file.write(self.save_data())
            file.close()
            self.ids.lbl_msg.text = "Project saved!"
        else:
            file = open(project_file, "w")
            if file is None:
                self.ids.lbl_msg.text = "Not saved!"
                return
            file.write(self.save_data())
            file.close()
            self.ids.lbl_msg.text = "Project saved!"
            
    def loadAudio(self):
        global audio_file
        if ".plague" not in project_file:
            self.ids.lbl_msg.text = "Save project first!"
            return
        root = tk.Tk()
        root.withdraw()
        file = filedialog.askopenfile(filetypes=[('Audio files','*.mp3'),('Audio files','*.wav')])
        if file is None:
            self.ids.lbl_msg.text = "No audio file selected"
            return
        if ntpath.dirname(file.name) != ntpath.dirname(project_file):
            self.ids.lbl_msg.text = "Put audio file in project-folder!"
            return
        audio_file = ntpath.basename(file.name)
        Audio.unload()
        Audio.source = ntpath.dirname(project_file)+"/"+audio_file
        self.ids.lbl_msg.text = "%s loaded" % (audio_file)

    def load(self):
        global project_file
        global audio_file
        global selected
        global Lyrics0
        global Lyrics1
        global Lyrics2
        global Lyrics3
        global Lyrics4
        global Lyrics5
        global Lyrics6
        global Lyrics7
        global Audio
        root = tk.Tk()
        root.withdraw()
        file = filedialog.askopenfile(filetypes=[('Plague files','*.plague')])
        if file is None:
            return
        project_file = file.name
        filelines = file.readlines()
        file.close()
        audio_file               = filelines[1].rstrip()
        self.ids.inp_start0.text = filelines[2].rstrip()
        self.ids.inp_start1.text = filelines[3].rstrip()
        self.ids.inp_start2.text = filelines[4].rstrip()
        self.ids.inp_start3.text = filelines[5].rstrip()
        self.ids.inp_start4.text = filelines[6].rstrip()
        self.ids.inp_start5.text = filelines[7].rstrip()
        self.ids.inp_start6.text = filelines[8].rstrip()
        self.ids.inp_start7.text = filelines[9].rstrip()
        self.ids.inp_bpm0.text   = filelines[10].rstrip()
        self.ids.inp_bpm1.text   = filelines[11].rstrip()
        self.ids.inp_bpm2.text   = filelines[12].rstrip()
        self.ids.inp_bpm3.text   = filelines[13].rstrip()
        self.ids.inp_bpm4.text   = filelines[14].rstrip()
        self.ids.inp_bpm5.text   = filelines[15].rstrip()
        self.ids.inp_bpm6.text   = filelines[16].rstrip()
        self.ids.inp_bpm7.text   = filelines[17].rstrip()
        self.ids.inp_beat0.text  = filelines[18].rstrip()
        self.ids.inp_beat1.text  = filelines[19].rstrip()
        self.ids.inp_beat2.text  = filelines[20].rstrip()
        self.ids.inp_beat3.text  = filelines[21].rstrip()
        self.ids.inp_beat4.text  = filelines[22].rstrip()
        self.ids.inp_beat5.text  = filelines[23].rstrip()
        self.ids.inp_beat6.text  = filelines[24].rstrip()
        self.ids.inp_beat7.text  = filelines[25].rstrip()
        i = 26
        p0 = 26
        while filelines[i] != 'LYRICSKEY\n': i = i + 1
        p1 = i
        i = i + 1
        while filelines[i] != 'LYRICSKEY\n': i = i + 1
        p2 = i
        i = i + 1
        while filelines[i] != 'LYRICSKEY\n': i = i + 1
        p3 = i
        i = i + 1
        while filelines[i] != 'LYRICSKEY\n': i = i + 1
        p4 = i
        i = i + 1
        while filelines[i] != 'LYRICSKEY\n': i = i + 1
        p5 = i
        i = i + 1
        while filelines[i] != 'LYRICSKEY\n': i = i + 1
        p6 = i
        i = i + 1
        while filelines[i] != 'LYRICSKEY\n': i = i + 1
        p7 = i
        Audio = SoundLoader.load(ntpath.dirname(project_file)+"/"+audio_file)
        Lyrics0 = ''.join(filelines[p0:p1])
        Lyrics1 = ''.join(filelines[p1+1:p2])
        Lyrics2 = ''.join(filelines[p2+1:p3])
        Lyrics3 = ''.join(filelines[p3+1:p4])
        Lyrics4 = ''.join(filelines[p4+1:p5])
        Lyrics5 = ''.join(filelines[p5+1:p6])
        Lyrics6 = ''.join(filelines[p6+1:p7])
        Lyrics7 = ''.join(filelines[p7+1:])
        Lyrics0 = Lyrics0.rstrip()
        Lyrics1 = Lyrics1.rstrip()
        Lyrics2 = Lyrics2.rstrip()
        Lyrics3 = Lyrics3.rstrip()
        Lyrics4 = Lyrics4.rstrip()
        Lyrics5 = Lyrics5.rstrip()
        Lyrics6 = Lyrics6.rstrip()
        Lyrics7 = Lyrics7.rstrip()
        selected = 0
        self.ids.Lyrics.text = Lyrics0
        self.ids.lbl_msg.text = "%s loaded" % (ntpath.basename(project_file))

    def save_data(self):
        s = ""
        s+=(ntpath.basename(project_file) + "\n")
        s+=(audio_file + "\n")
        s+=(self.ids.inp_start0.text + "\n")
        s+=(self.ids.inp_start1.text + "\n")
        s+=(self.ids.inp_start2.text + "\n")
        s+=(self.ids.inp_start3.text + "\n")
        s+=(self.ids.inp_start4.text + "\n")
        s+=(self.ids.inp_start5.text + "\n")
        s+=(self.ids.inp_start6.text + "\n")
        s+=(self.ids.inp_start7.text + "\n")
        s+=(self.ids.inp_bpm0.text + "\n")
        s+=(self.ids.inp_bpm1.text + "\n")
        s+=(self.ids.inp_bpm2.text + "\n")
        s+=(self.ids.inp_bpm3.text + "\n")
        s+=(self.ids.inp_bpm4.text + "\n")
        s+=(self.ids.inp_bpm5.text + "\n")
        s+=(self.ids.inp_bpm6.text + "\n")
        s+=(self.ids.inp_bpm7.text + "\n")
        s+=(self.ids.inp_beat0.text + "\n")
        s+=(self.ids.inp_beat1.text + "\n")
        s+=(self.ids.inp_beat2.text + "\n")
        s+=(self.ids.inp_beat3.text + "\n")
        s+=(self.ids.inp_beat4.text + "\n")
        s+=(self.ids.inp_beat5.text + "\n")
        s+=(self.ids.inp_beat6.text + "\n")
        s+=(self.ids.inp_beat7.text + "\n")
        s+=(Lyrics0 + "\nLYRICSKEY\n")
        s+=(Lyrics1 + "\nLYRICSKEY\n")
        s+=(Lyrics2 + "\nLYRICSKEY\n")
        s+=(Lyrics3 + "\nLYRICSKEY\n")
        s+=(Lyrics4 + "\nLYRICSKEY\n")
        s+=(Lyrics5 + "\nLYRICSKEY\n")
        s+=(Lyrics6 + "\nLYRICSKEY\n")
        s+=(Lyrics7)
        return s

    def try_export(self):
        if ".plague" in project_file: self.Generate(1)
        else: self.ids.lbl_msg.text = "Save project before export"
  
    # Data processing
    def Generate(self, export):

        # use global variables
        global selected
        global Lyrics0
        global Lyrics1
        global Lyrics2
        global Lyrics3
        global Lyrics4
        global Lyrics5
        global Lyrics6
        global Lyrics7
        global TimeStartList
        global TimeEndList
        global TimeLyricsList

        # load text-input to variables
        if selected == 0: Lyrics0 = self.ids.Lyrics.text
        if selected == 1: Lyrics1 = self.ids.Lyrics.text
        if selected == 2: Lyrics2 = self.ids.Lyrics.text
        if selected == 3: Lyrics3 = self.ids.Lyrics.text
        if selected == 4: Lyrics4 = self.ids.Lyrics.text
        if selected == 5: Lyrics5 = self.ids.Lyrics.text
        if selected == 6: Lyrics6 = self.ids.Lyrics.text
        if selected == 7: Lyrics7 = self.ids.Lyrics.text

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
      
        # Get timing paramters
        start0 = try_int(self.ids.inp_start0.text)
        bpm0   = try_int(self.ids.inp_bpm0.text)
        beats0 = try_int(self.ids.inp_beat0.text)
        start1 = try_int(self.ids.inp_start1.text)
        bpm1   = try_int(self.ids.inp_bpm1.text)
        beats1 = try_int(self.ids.inp_beat1.text)
        start2 = try_int(self.ids.inp_start2.text)
        bpm2   = try_int(self.ids.inp_bpm2.text)
        beats2 = try_int(self.ids.inp_beat2.text)
        start3 = try_int(self.ids.inp_start3.text)
        bpm3   = try_int(self.ids.inp_bpm3.text)
        beats3 = try_int(self.ids.inp_beat3.text)
        start4 = try_int(self.ids.inp_start4.text)
        bpm4   = try_int(self.ids.inp_bpm4.text)
        beats4 = try_int(self.ids.inp_beat4.text)
        start5 = try_int(self.ids.inp_start5.text)
        bpm5   = try_int(self.ids.inp_bpm5.text)
        beats5 = try_int(self.ids.inp_beat5.text)
        start6 = try_int(self.ids.inp_start6.text)
        bpm6   = try_int(self.ids.inp_bpm6.text)
        beats6 = try_int(self.ids.inp_beat6.text)
        start7 = try_int(self.ids.inp_start7.text)
        bpm7   = try_int(self.ids.inp_bpm7.text)
        beats7 = try_int(self.ids.inp_beat7.text)

        # Get lyrics parameters
        if Lyrics0 == "": steps0 = 0
        else: steps0 = Lyrics0.count('\n') + 1
        if Lyrics1 == "": steps1 = 0
        else: steps1 = Lyrics1.count('\n') + 1
        if Lyrics2 == "": steps2 = 0
        else: steps2 = Lyrics2.count('\n') + 1
        if Lyrics3 == "": steps3 = 0
        else: steps3 = Lyrics3.count('\n') + 1
        if Lyrics4 == "": steps4 = 0
        else: steps4 = Lyrics4.count('\n') + 1
        if Lyrics5 == "": steps5 = 0
        else: steps5 = Lyrics5.count('\n') + 1
        if Lyrics6 == "": steps6 = 0
        else: steps6 = Lyrics6.count('\n') + 1
        if Lyrics7 == "": steps7 = 0
        else: steps7 = Lyrics7.count('\n') + 1
        
        if bpm0 > 0: incr0 = float((60 / bpm0) * beats0)
        else:        incr0 = 0
        if bpm1 > 0: incr1 = float((60 / bpm1) * beats1)
        else:        incr1 = 0
        if bpm2 > 0: incr2 = float((60 / bpm2) * beats2)
        else:        incr2 = 0
        if bpm3 > 0: incr3 = float((60 / bpm3) * beats3)
        else:        incr3 = 0
        if bpm4 > 0: incr4 = float((60 / bpm4) * beats4)
        else:        incr4 = 0
        if bpm5 > 0: incr5 = float((60 / bpm5) * beats5)
        else:        incr5 = 0
        if bpm6 > 0: incr6 = float((60 / bpm6) * beats6)
        else:        incr6 = 0
        if bpm7 > 0: incr7 = float((60 / bpm7) * beats7)
        else:        incr7 = 0

        sub90_0 = incr0 * 0.9
        sub90_1 = incr1 * 0.9
        sub90_2 = incr2 * 0.9
        sub90_3 = incr3 * 0.9
        sub90_4 = incr4 * 0.9
        sub90_5 = incr5 * 0.9
        sub90_6 = incr6 * 0.9
        sub90_7 = incr7 * 0.9
        
        # Make lists
        Lyrics = ""
        if steps0 > 0: Lyrics += (Lyrics0+"\n")
        if steps1 > 0: Lyrics += (Lyrics1+"\n")
        if steps2 > 0: Lyrics += (Lyrics2+"\n")
        if steps3 > 0: Lyrics += (Lyrics3+"\n")
        if steps4 > 0: Lyrics += (Lyrics4+"\n")
        if steps5 > 0: Lyrics += (Lyrics5+"\n")
        if steps6 > 0: Lyrics += (Lyrics6+"\n")
        if steps7 > 0: Lyrics += (Lyrics7+"\n")
        LyricsLines = Lyrics.split('\n')
        TimeStamp = list()
        TimeStartList.clear()
        TimeEndList.clear()
        TimeLyricsList.clear()
        for i in range(steps0):
          TimeStart = (start0/1000 + (i * incr0))
          TimeEnd = (start0/1000 + (i * incr0) + sub90_0)
          TimeStamp.append("%s --> %s" % (to_timestamp(TimeStart),to_timestamp(TimeEnd)))
          TimeStartList.append(TimeStart)
          TimeEndList.append(TimeEnd)
        for i in range(steps1):
          TimeStart = (start1/1000 + (i * incr1))
          TimeEnd = (start1/1000 + (i * incr1) + sub90_1)
          TimeStamp.append("%s --> %s" % (to_timestamp(TimeStart),to_timestamp(TimeEnd)))
          TimeStartList.append(TimeStart)
          TimeEndList.append(TimeEnd)
        for i in range(steps2):
          TimeStart = (start2/1000 + (i * incr2))
          TimeEnd = (start2/1000 + (i * incr2) + sub90_2)
          TimeStamp.append("%s --> %s" % (to_timestamp(TimeStart),to_timestamp(TimeEnd)))
          TimeStartList.append(TimeStart)
          TimeEndList.append(TimeEnd)
        for i in range(steps3):
          TimeStart = (start3/1000 + (i * incr3))
          TimeEnd = (start3/1000 + (i * incr3) + sub90_3)
          TimeStamp.append("%s --> %s" % (to_timestamp(TimeStart),to_timestamp(TimeEnd)))
          TimeStartList.append(TimeStart)
          TimeEndList.append(TimeEnd)
        for i in range(steps4):
          TimeStart = (start4/1000 + (i * incr4))
          TimeEnd = (start4/1000 + (i * incr4) + sub90_4)
          TimeStamp.append("%s --> %s" % (to_timestamp(TimeStart),to_timestamp(TimeEnd)))
          TimeStartList.append(TimeStart)
          TimeEndList.append(TimeEnd)
          LyricsLines.append(" ")
        for i in range(steps5):
          TimeStart = (start5/1000 + (i * incr5))
          TimeEnd = (start5/1000 + (i * incr5) + sub90_5)
          TimeStamp.append("%s --> %s" % (to_timestamp(TimeStart),to_timestamp(TimeEnd)))
          TimeStartList.append(TimeStart)
          TimeEndList.append(TimeEnd)
        for i in range(steps6):
          TimeStart = (start6/1000 + (i * incr6))
          TimeEnd = (start6/1000 + (i * incr6) + sub90_6)
          TimeStamp.append("%s --> %s" % (to_timestamp(TimeStart),to_timestamp(TimeEnd)))
          TimeStartList.append(TimeStart)
          TimeEndList.append(TimeEnd)
        for i in range(steps7):
          TimeStart = (start7/1000 + (i * incr7))
          TimeEnd = (start7/1000 + (i * incr7) + sub90_7)
          TimeStamp.append("%s --> %s" % (to_timestamp(TimeStart),to_timestamp(TimeEnd)))
          TimeStartList.append(TimeStart)
          TimeEndList.append(TimeEnd)
        
        # Print lists to preview
        LyricsOutList = list()
        for i in range(steps0+steps1+steps2+steps3+steps4+steps5+steps6+steps7):
          LyricsOutList.append("%s  %s\n" % (TimeStamp[i][3:16], LyricsLines[i]))
          TimeLyricsList.append(LyricsLines[i])

        self.ids.LyricsOutput.text = ''.join(LyricsOutList)
          
        # Export to .srt
        if export == 1:
          srtfile = project_file.replace(".plague", ".srt")
          file = open(srtfile, "w")
          for i in range(steps0+steps1+steps2+steps3+steps4+steps5+steps6+steps7):
            file.write("%s\n" % (i+1))
            file.write("%s\n" % (TimeStamp[i]))
            file.write("%s\n" % (LyricsLines[i]))
            file.write("\n")
          file.close()
          self.ids.lbl_msg.text = "%s exported!" % (ntpath.basename(srtfile))
  
class PlagueLyrics_mainApp(App):
    def build(self):
        return ContainerBox()

if __name__ == '__main__':
    PlagueLyrics_mainApp().run()
