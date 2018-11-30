# Import the modules
import sys
import random
import func
from tkinter import *

class Window(Frame):
  
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.master.title("Lines")        
        self.pack(fill=BOTH, expand=1)
        canvas = Canvas(self)
        canvas.pack(fill=BOTH, expand=1)
        
    def draw_0():
        canvas.create_line(15, 25, 200, 25)
    def draw_1():
        canvas.create_line(300, 35, 300, 200, dash=(4, 2))
    def draw_2():
        canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)

def input(letters):
    
    # Wacht op input
    question = input("Voer een letter in?!")
	
    # Check input
    letters_geraden=0
    fout=1
    for x in range(0, letters):
        if question == answer[x]:
            letters_goed[x]="1"
            fout=0
        if letters_goed[x] == "1":
            letters_geraden=letters_geraden+1
            woord_goed[x]=answer[x]

    if fout == 1:
        fouten=fouten+1
	
    # Update galgje
    func.print_sticky(fouten)
    func.print_woord(woord_goed)
	
    # end game
    if letters_geraden == letters or question == chosen_word:
        func.print_won(chosen_word)
        sys.exit()
    elif fouten == max_fouten:
        func.print_lost(chosen_word)
        sys.exit()

# Define global variables
global answer
global letters_goed
global woord_goed
global max_fouten
global fouten
global chosen_word
answer=[]
letters_goed=[]
woord_goed=[]
max_fouten = 6
fouten = 0
root = Tk()
root.geometry("400x250+300+300")
win = Window()
restart = Button(root, text="OK", command=win.draw_0)
restart.place(x = 50,y = 50)

# Pick a word from maarten_wordlist.txt
lines = open("wordlist.txt").readlines()
nr_of_lines = len(lines) - 1
chosen_word = lines[random.randint(0,nr_of_lines)]
chosen_word = chosen_word[:-1] #remove end-of-line character (\n)
letters = len(chosen_word)

# Fill variables
for x in range(0, letters):
    answer.append(chosen_word[x])
for x in range(0, letters):
    letters_goed.append("0")
for x in range(0, letters):
    woord_goed.append("_")

# print(start game
func.print_sticky(0)
func.print_woord(woord_goed)

# Loop
root.mainloop()  
