ffmpeg.exe -loop 1 -i cover.jpg -i in.mp3 -c:a copy -c:v libx264 -shortest -vf subtitles=subs.srt:force_style='Fontsize=38' out.mp4
exit