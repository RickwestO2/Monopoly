import tkinter as tk
from tkinter.ttk import Frame, Style
import tkinter.font as tkFont
from random import randint

window = tk.Tk()
window.geometry('1000x800')
fontstyle=tkFont.Font(size=20)
node=[1000,2000,3000]
node_owner= [[0]*5 for i in range(5)]
player_loc01=[0,0]

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
    sp=0 #start point
    fp=5 #finish point
    for i in range(sp,fp):
        for j in range(sp,fp):
            if(i==fp-1 and j==fp-1):#Jail
                labelframe = tk.LabelFrame(window, text='Jail',font=fontstyle, width=100, height=100)
                labelframe.grid(row=i,column=j,padx=1,pady=1)
                frame = tk.Frame(labelframe, bg='white', width=100, height=100)
                frame.grid(row=i,column=j,padx=10,pady=10)

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
                frame = tk.Frame(labelframe, bg='white', width=100, height=100)
                frame.grid(row=i,column=j,padx=10,pady=10)



def move():
    num = randint(1,6)#dice
    print("dice: ",num)
    dice=tk.Button(window, text='Dice',bg='orange',command=lambda: dice.config(text=num),font=fontstyle, width=5, height=2)
    dice.grid(row=3,column=10,padx=10,pady=10)
    tmp=(player_loc01[0]+player_loc01[1]+num)%16
    if(tmp<=4):
        player_loc01[0]=0
        player_loc01[1]=tmp
    elif(tmp<=8):
        player_loc01[0]=tmp-4
        player_loc01[1]=4
    elif(tmp<=12):
        player_loc01[0]=4
        player_loc01[1]=12-tmp
    else:
        player_loc01[0]=16-tmp
        player_loc01[1]=0

    

#test
node_owner[0][0]=1
node_owner[4][4]=1
node_owner[0][1]=2

def check():
    sp=0 #start point
    fp=5 #finish point
    for i in range(sp,fp):
        for j in range(sp,fp):
            if(node_owner[i][j]==1):#node_owner player1 
                labelframe = tk.LabelFrame(window, text=node[i%3],font=fontstyle, width=100, height=100)
                labelframe.grid(row=i,column=j,padx=1,pady=1)
                frame = tk.Frame(labelframe, bg='lightblue', width=100, height=100)
                frame.grid(row=i,column=j,padx=10,pady=10)
            if(node_owner[i][j]==2):#node_owner player2
                labelframe = tk.LabelFrame(window, text=node[i%3],font=fontstyle, width=100, height=100)
                labelframe.grid(row=i,column=j,padx=1,pady=1)
                frame = tk.Frame(labelframe, bg='lightgreen', width=100, height=100)
                frame.grid(row=i,column=j,padx=10,pady=10)

            if(i==player_loc01[0] and j==player_loc01[1]):#player1 location
                labelframe = tk.LabelFrame(window, text=node[i%3],font=fontstyle, width=100, height=100)
                labelframe.grid(row=i,column=j,padx=1,pady=1)
                if(node_owner[i][j]==1):
                    frame = tk.Frame(labelframe, bg='lightblue', width=100, height=100)
                elif(node_owner[i][j]==2):
                    frame = tk.Frame(labelframe, bg='lightgreen', width=100, height=100)
                else:
                    frame = tk.Frame(labelframe, bg='white', width=100, height=100)
                frame.grid(row=i,column=j,padx=10,pady=10)
                player1=tk.Label(frame, text='Player 1',bg='dodgerblue',fg='white',font=fontstyle).place(x=5, y=10)
            
            if(i==4 and j==4):#player2 location
                labelframe = tk.LabelFrame(window, text=node[i%3],font=fontstyle, width=100, height=100)
                labelframe.grid(row=i,column=j,padx=1,pady=1)
                if(node_owner[i][j]==2):
                    frame = tk.Frame(labelframe, bg='lightgreen', width=100, height=100)
                elif(node_owner[i][j]==1):
                    frame = tk.Frame(labelframe, bg='lightblue', width=100, height=100)
                else:
                    frame = tk.Frame(labelframe, bg='white', width=100, height=100)
                frame.grid(row=i,column=j,padx=10,pady=10)
                player2=tk.Label(frame, text='Player 2',bg='limegreen',fg='white',font=fontstyle).place(x=5, y=50)

round=5
scoreboard()
map()
for x in range(0,round):
    move()
    check()


window.mainloop()