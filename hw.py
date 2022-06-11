import time
import tkinter as tk
from tkinter.ttk import Frame, Style
import tkinter.font as tkFont
from random import randint

# Map size
sp=0 #start point
fp=5 #finish point

window = tk.Tk()
window.geometry('1000x800')
fontstyle=tkFont.Font(size=20)
node=[1000,2000,3000]
node_owner= [[0]*5 for i in range(5)]
player1=None
player2=None
player1_loc=0
player_loc02=[0,0]
framemap = [[None] * 5 for i in range(5)]

def scoreboard():
    cash_output01="cash: "+str(1000)
    cash_output02="cash: "+str(2000)
    property_output01="property: "+str(3000)
    property_output02="property: "+str(4000)

    board1 = tk.Frame(window, bg='white', width=300, height=150)
    board1.grid(row=1,column=10,padx=10,pady=10)
    player01=tk.Label(board1, text='Player 1',bg='dodgerblue',fg='white',font=fontstyle).place(x=5, y=5)
    cash01=tk.Label(board1, text=cash_output01,bg='white',font=fontstyle).place(x=5, y=50)
    property01=tk.Label(board1, text=property_output01,bg='white',font=fontstyle).place(x=5, y=100)

    board2 = tk.Frame(window, bg='white', width=300, height=150)
    board2.grid(row=2,column=10,padx=10,pady=10)
    player02=tk.Label(board2, text='Player 2',bg='limegreen',fg='white',font=fontstyle).place(x=5, y=5)
    cash02=tk.Label(board2, text=cash_output02,bg='white',font=fontstyle).place(x=5, y=50)
    property02=tk.Label(board2, text=property_output02,bg='white',font=fontstyle).place(x=5, y=100)

def map():
    global framemap, player1, player2
    for i in range(sp,fp):
        for j in range(sp,fp):
            if(i==fp-1 and j==fp-1):#Jail
                labelframe = tk.LabelFrame(window, text='Jail',font=fontstyle, width=100, height=100)
                labelframe.grid(row=i,column=j,padx=1,pady=1)
                framemap[i][j] = tk.Frame(labelframe, bg='white', width=100, height=100)
                framemap[i][j].grid(row=i,column=j,padx=10,pady=10)

            elif(i>sp and i<fp-1 and j>sp and j<fp-1):#middle
                frame1 = tk.Frame(window, bg='lightsalmon', width=100, height=100)
                frame1.grid(row=i,column=j)
                
                if(i==1 and j==1):
                    outtext=tk.Label(frame1, text='大',bg='lightsalmon',font=tkFont.Font(size=30), width=5, height=2).grid(row=i,column=j)
                if(i==1 and j==2):
                    outtext=tk.Label(frame1, text='富',bg='lightsalmon',font=tkFont.Font(size=30), width=5, height=2).grid(row=i,column=j)
                if(i==1 and j==3):
                    outtext=tk.Label(frame1, text='翁',bg='lightsalmon',font=tkFont.Font(size=30), width=5, height=2).grid(row=i,column=j)
            else:
                labelframe = tk.LabelFrame(window, text=node[i%3],font=fontstyle, width=100, height=100)
                labelframe.grid(row=i,column=j,padx=1,pady=1)
                framemap[i][j] = tk.Frame(labelframe, bg='white', width=100, height=100)
                framemap[i][j].grid(row=i,column=j,padx=10,pady=10)
    tk.Button(window, text='Dice',bg='orange',command=dice,font=fontstyle, width=5, height=2).grid(row=3,column=10,padx=10,pady=10)
    player1=tk.Label(framemap[0][0], text='Player 1',bg='dodgerblue',fg='white',font=fontstyle)
    player1.place(x=5, y=10)
    #update_player(player1, 0, 0)
    player2=tk.Label(framemap[0][0], text='Player 2',bg='limegreen',fg='white',font=fontstyle)
    player2.place(x=5, y=50)
    #update_player(player2, 0, 0)

def d_test(player):
    player.destroy()

def dice():
    global player1, player1_loc
    num = randint(1,6)
    # TODO: add message box
    print("dice: ",num)
    player1, player1_loc = move(player1, player1_loc, num)

def move(player, player_loc, count):
    print("move start")
    for i in range(0, count):
        player_loc+=1
        player_loc%=16
        if(player_loc<=4):
            player = update_player(player, 0, player_loc)
        elif(player_loc<=8):
            player = update_player(player, player_loc - 4, 4)
        elif(player_loc<=12):
            player = update_player(player, 4, 12 - player_loc)
        else:
            player = update_player(player, 16 - player_loc, 0)
        window.update()
        time.sleep(0.5)
    print("move stop")
    return player, player_loc

def update_player(player, i, j):
    print(i, j)
    player.destroy()
    # TODO: different color when defferent player
    player = tk.Label(framemap[i][j], text='Player 1',bg='dodgerblue',fg='white',font=fontstyle)
    player.place(x=5, y=10)
    return player

def update_owner(player_id, i, j):
    node_owner[i][j] = player_id
    # TODO: different color when defferent player
    framemap[i][j].config(bg = 'lightblue')

def test():
    update_owner(1, 0, 0)
    update_owner(1, 4, 4)
    update_owner(2, 0, 1)

round=5
scoreboard()
map()
test()
"""
for x in range(0,round):
    move()
    check()
"""

window.mainloop()