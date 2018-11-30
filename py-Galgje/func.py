def print_woord(woord):
    output=' '.join(woord)
    print(' ')
    print(' %s'%(output))
    print(' ')
    
def print_won(chosen_word):
    print("GERADEN !!!!!")
    print(chosen_word)

def print_lost(chosen_word):
    print("TE VEEL FOUTEN!")
    print("het woord was:")
    print(chosen_word)

def print_sticky(fouten):
    # Top
    print(' ')
    print(" 0000000000000      ")
    print(" 0           0      ")
    # Head
    if fouten < 1:
        print(" 0")
        print(" 0")
        print(" 0")
    else:
        print(" 0           1       ")
        print(" 0          1 1      ")
        print(" 0           1       ")
    # Body
    if fouten < 2:
        print(" 0")
        print(" 0")
        print(" 0")
        print(" 0")
    elif fouten < 3:
        print(" 0           2        ")
        print(" 0           2        ")
        print(" 0           2        ")
        print(" 0           2        ")
    elif fouten < 4:
        print(" 0          32        ")
        print(" 0         3 2        ")
        print(" 0        3  2        ")
        print(" 0        3  2        ")
    else:
        print(" 0          324      ")
        print(" 0         3 2 4     ")
        print(" 0        3  2  4    ")
        print(" 0        3  2  4    ")
    # Legs
    if fouten < 5:
        print(" 0")
        print(" 0")
        print(" 0")
        print(" 0")
    elif fouten < 6:
        print(" 0          5        ")
        print(" 0         5         ")
        print(" 0        5          ")
        print(" 0       5          ")
    else:
        print(" 0          5 6      ")
        print(" 0         5   6     ")
        print(" 0        5     6    ")
        print(" 0       5       6   ")
    # Bottom
    print(" 0                   ")
    
