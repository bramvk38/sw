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
video_file = "Dead.mp4"
video_path = "x"
file = "x"
last_path = "x"

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
        super(ContainerBox, self).__init__(**kwargs)

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
            self.ids.Lyrics.text = "No valid video, select a .mp4 file"
        self.dismiss_popup()

    def load(self, path, filename):
        global file
        global last_path
        global video_file
        global video_path
        if ".plague" in filename[0]:
            file = filename[0]
            last_path = path
            with open(os.path.join(path, filename[0])) as file: filelines = file.readlines()
            video_path = filelines[0].rstrip()
            video_file = filelines[1].rstrip()
            self.loadvideo(video_path, video_file)
            self.ids.Lyrics.text = ""
            Lyrics = ''.join(filelines[2:])
            self.ids.Lyrics.text = Lyrics
        else:
            self.ids.Lyrics.text = "No valid project-file, select a .plague file"
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
                stream.write(video_path)
                stream.write("\n")
                stream.write(video_file)
                stream.write("\n")
                stream.write(self.ids.Lyrics.text)
            self.dismiss_popup()
        else:
            self.save_project_as()
  
    def Generate(self, export):

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
      
        # Get parameters
        Lyrics = self.ids.Lyrics.text
        start0 = try_int(self.ids.inp_start0.text)
        steps0 = self.ids.Lyrics.text.count('\n')
        bpm0 = try_int(self.ids.inp_bpm0.text)
        beats0 = try_int(self.ids.inp_beat0.text)
        start1 = 200
        steps1 = 10
        bpm1 = 120
        beats1 = 4
        
        if bpm0 > 0:
          incr0 = float((60 / bpm0) * beats0)
        else:
          incr0 = 0
        if bpm1 > 0:
          incr1 = float((60 / bpm1) * beats1)
        else:
          incr1 = 0

        sub90_0 = incr0 * 0.9
        sub90_1 = incr1 * 0.9
        
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
        
        # Print lists to preview
        LyricsOutList = list()
        for i in range(steps0+steps1):
          LyricsOutList.append("%s  %s\n" % (TimeStamp[i], LyricsLines[i]))

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
