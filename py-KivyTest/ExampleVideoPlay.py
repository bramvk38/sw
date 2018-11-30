import kivy

from kivy.app import App
from kivy.uix.video import Video


class MyApp(App):
    def build(self):
        video = Video(source='test_video.mp4')
        video.state='play'
        video.options = {'eos': 'loop'}
        video.allow_stretch=True
        return video

if __name__ == '__main__':
    MyApp().run()
