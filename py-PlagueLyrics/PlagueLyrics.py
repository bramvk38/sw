import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.video import Video
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

import os

# Define global variables
global video_file
global video_path
global file
global last_path
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
video_file = "x"
video_path = "x"
file = "x"
last_path = "x"
selected = 0
Lyrics0 = ""
Lyrics1 = ""
Lyrics2 = ""
Lyrics3 = ""
Lyrics4 = ""
Lyrics5 = ""
Lyrics6 = ""
Lyrics7 = ""
PartitionColor = [[1,0,0,1],[0,1,0,1],[.1,.1,1,1],[1,1,0,1],[0,1,1,1],[1,0,1,1],[.5,.5,1,1],[1,.5,.5,1]]

class WelcomeDialog(FloatLayout):
    save_project_as = ObjectProperty(None)
    show_load = ObjectProperty(None)

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class LoadVideoDialog(FloatLayout):
    loadvideo = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    pre_save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)
        
class ContainerBox(BoxLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    def __init__(self, **kwargs):
        global PartitionColor
        global selected
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

    def try_export(self):
        global file
        if ".plague" in file: Generate(1)
        else: self.ids.lbl_msg.text = "Save project before export"

    def close_app(self):
        App.get_running_app().stop()

    def UpdatePartition(self):
        global selected
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
            
    def TestFunc(self):
        lines = self.ids.Lyrics.text.count('\n')
        self.ids.Lyrics.size_hint_y = 1 + 10 * lines
        self.ids.Lyrics2.pos_hint_y = 1 + lines * 10
        print(self.ids.Lyrics.text.count('\n'))

    def PlayVideo(self):
        self.ids.VideoPlayer.state = 'play'

    def StopVideo(self):
        self.ids.VideoPlayer.state = 'pause'

    def save_project_as(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def try_video(self):
        content = LoadVideoDialog(loadvideo=self.loadvideo, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def loadvideo(self, path, filename):
        global video_file
        global video_path
        if ".mp4" in filename:
            video_file = filename
            video_path = path
            self.ids.VideoPlayer.unload()
            self.ids.VideoPlayer.source = filename
        else:
            self.ids.lbl_msg.text = "No valid video, select a .mp4 file"
        self.dismiss_popup()

    def load(self, path, filename):
        global file
        global last_path
        global video_file
        global video_path
        global selected
        global Lyrics0
        global Lyrics1
        global Lyrics2
        global Lyrics3
        global Lyrics4
        global Lyrics5
        global Lyrics6
        global Lyrics7
        if ".plague" in filename[0]:
            file = filename[0]
            last_path = path
            with open(os.path.join(path, filename[0])) as file: filelines = file.readlines()
            video_path               = filelines[0].rstrip()
            video_file               = filelines[1].rstrip()
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
            self.loadvideo(video_path, video_file)
            self.ids.Lyrics.text = ""
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
        else:
            self.ids.lbl_msg.text = "No valid project-file, select a .plague file"
        self.dismiss_popup()

    def try_save(self):
        global file
        global last_path
        self.do_save(last_path, file)

    def save(self, path, filename):
        if ".plague" in filename:
            self.do_save(path, filename)
        else:
            self.do_save(path, filename + ".plague")

    def do_save(self, path, filename):
        global file
        global last_path
        global video_file
        global video_path
        if ".plague" in filename:
            file = filename
            last_path = path
            with open(os.path.join(path, filename), 'w') as stream:
                stream.write(video_path + "\n")
                stream.write(video_file + "\n")
                stream.write(self.ids.inp_start0.text + "\n")
                stream.write(self.ids.inp_start1.text + "\n")
                stream.write(self.ids.inp_start2.text + "\n")
                stream.write(self.ids.inp_start3.text + "\n")
                stream.write(self.ids.inp_start4.text + "\n")
                stream.write(self.ids.inp_start5.text + "\n")
                stream.write(self.ids.inp_start6.text + "\n")
                stream.write(self.ids.inp_start7.text + "\n")
                stream.write(self.ids.inp_bpm0.text + "\n")
                stream.write(self.ids.inp_bpm1.text + "\n")
                stream.write(self.ids.inp_bpm2.text + "\n")
                stream.write(self.ids.inp_bpm3.text + "\n")
                stream.write(self.ids.inp_bpm4.text + "\n")
                stream.write(self.ids.inp_bpm5.text + "\n")
                stream.write(self.ids.inp_bpm6.text + "\n")
                stream.write(self.ids.inp_bpm7.text + "\n")
                stream.write(self.ids.inp_beat0.text + "\n")
                stream.write(self.ids.inp_beat1.text + "\n")
                stream.write(self.ids.inp_beat2.text + "\n")
                stream.write(self.ids.inp_beat3.text + "\n")
                stream.write(self.ids.inp_beat4.text + "\n")
                stream.write(self.ids.inp_beat5.text + "\n")
                stream.write(self.ids.inp_beat6.text + "\n")
                stream.write(self.ids.inp_beat7.text + "\n")
                stream.write(Lyrics0 + "\nLYRICSKEY\n")
                stream.write(Lyrics1 + "\nLYRICSKEY\n")
                stream.write(Lyrics2 + "\nLYRICSKEY\n")
                stream.write(Lyrics3 + "\nLYRICSKEY\n")
                stream.write(Lyrics4 + "\nLYRICSKEY\n")
                stream.write(Lyrics5 + "\nLYRICSKEY\n")
                stream.write(Lyrics6 + "\nLYRICSKEY\n")
                stream.write(Lyrics7)
            self.dismiss_popup()
        else:
            self.save_project_as()
  
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

        # clear messages
        self.ids.lbl_msg.text = ""
        
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
        Lyrics = Lyrics0+"\n"+Lyrics1+"\n"+Lyrics2+"\n"+Lyrics3+"\n"+Lyrics4+"\n"+Lyrics5+"\n"+Lyrics6+"\n"+Lyrics7
        LyricsLines = Lyrics.split('\n')
        TimeStamp = list()
        for i in range(steps0):
          TimeStart = to_timestamp(start0/1000 + (i * incr0))
          TimeEnd = to_timestamp(start0/1000 + (i * incr0) + sub90_0)
          TimeStamp.append("%s --> %s" % (TimeStart,  TimeEnd))
          LyricsLines.append(" ")
        for i in range(steps1):
          TimeStart = to_timestamp(start1/1000 + (i * incr1))
          TimeEnd = to_timestamp(start1/1000 + (i * incr1) + sub90_1)
          TimeStamp.append("%s --> %s" % (TimeStart,  TimeEnd))
          LyricsLines.append(" ")
        
        # Print lists to preview
        LyricsOutList = list()
        for i in range(steps0+steps1):
          LyricsOutList.append("%s  %s\n" % (TimeStamp[i][3:16], LyricsLines[i]))

        self.ids.LyricsOutput.text = ''.join(LyricsOutList)
          
        if export == 1:
          name = ui.FileName.toPlainText()
          file = open('%s.srt' % (name), "w")
          for i in range(steps0+steps1+steps2+steps3):
            file.write("%s\n" % (i+1))
            file.write("%s\n" % (TimeStamp[i]))
            file.write("%s\n" % (LyricsLines[i]))
            file.write("\n")
          file.close() 
  
class PlagueLyrics_mainApp(App):
    def build(self):
        return ContainerBox() 

Factory.register('Root', cls=ContainerBox)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)

if __name__ == '__main__':
    PlagueLyrics_mainApp().run()
