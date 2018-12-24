import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.garden.graph import Graph, MeshLinePlot
from shutil import copyfile
import time

# Define global variables
global Promile
global DataTime
global DataBAC
global Weight
global Gender
global PercentageVal
global UnitsizeVal
Promile = float(0)
DataTime = list()
DataBAC = list()
Weight = 70000
Gender = "Male"
PercentageVal = float(0)
UnitsizeVal = float(0)
        
class ContainerBox(BoxLayout):

    # Init
    def __init__(self, **kwargs):
        super(ContainerBox, self).__init__(**kwargs)
        Clock.schedule_interval(self.Refresh, 1)
    def close_app(self):
        App.get_running_app().stop()
    
    # Update text
    def Refresh(self, *args):
        global Promile
        self.UpdatePromile()
        self.ids.lbl_promile.text = "%s" % (format(Promile,'.3f'))

    # Add unit
    def Add(self, ml, percentage, minutes_past):
        global DataTime
        global DataBAC
        if Gender == "Male": GenderVal = 0.68
        else:                GenderVal = 0.55
        Dose = (ml * percentage) / 100 * 0.789
        BAC = Dose / (Weight * GenderVal)
        DataBAC.append(int(BAC * 1000000))
        DataTime.append(int(time.time()) - minutes_past * 60)
        self.UpdatePromile()

    # Data processing
    def UpdatePromile(self):
        global Promile
        Promile = 0.0
        Stamps = list()
        timenow = int(time.time())
        Stamps.append(0)
        for j in range(96):
            if Stamps[j] > 38: Stamps.append(Stamps[j] - 38)
            else:              Stamps.append(0.0)
            for i in range(len(DataBAC)):
                if int((timenow - DataTime[i]) / 900) == 95 - j:
                    Stamps[j+1] += DataBAC[i]
        Promile = float(Stamps[96]) / 1000
        # Update graph
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x, Stamps[x]/1000) for x in range(1, 97)]
        for old in self.ids.plotter.plots:
            self.ids.plotter.remove_plot(old)
        self.ids.plotter.add_plot(plot)
  
class Promilator_mainApp(App):
    def build(self):
        return ContainerBox()

if __name__ == '__main__':
    Promilator_mainApp().run()
