import time
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Frame, Style
import tkinter.font as tkFont
from random import randint

# Map size
sp = 0  # start point
fp = 5  # finish point

window = tk.Tk()
window.geometry('1000x800')
fontstyle = tkFont.Font(size=20)
node_price = [[None] * 5 for i in range(5)]
node_owner = [[0]*5 for i in range(5)]
player1 = None
player2 = None
player1_loc = 0
player2_loc = 0
player_cash = [50000, 50000]
player_property = [0, 0]
framemap = [[None] * 5 for i in range(5)]
btn_dice = None


def scoreboard():
    cash_output01 = "cash: "+str(player_cash[0])
    cash_output02 = "cash: "+str(player_cash[1])
    property_output01 = "property: "+str(player_property[0])
    property_output02 = "property: "+str(player_property[1])

    board1 = tk.Frame(window, bg='white', width=300, height=150)
    board1.grid(row=1, column=10, padx=10, pady=10)
    player01 = tk.Label(board1, text='Player 1', bg='dodgerblue',
                        fg='white', font=fontstyle).place(x=5, y=5)
    cash01 = tk.Label(board1, text=cash_output01, bg='white',
                      font=fontstyle).place(x=5, y=50)
    property01 = tk.Label(board1, text=property_output01,
                          bg='white', font=fontstyle).place(x=5, y=100)

    board2 = tk.Frame(window, bg='white', width=300, height=150)
    board2.grid(row=2, column=10, padx=10, pady=10)
    player02 = tk.Label(board2, text='Player 2', bg='limegreen',
                        fg='white', font=fontstyle).place(x=5, y=5)
    cash02 = tk.Label(board2, text=cash_output02, bg='white',
                      font=fontstyle).place(x=5, y=50)
    property02 = tk.Label(board2, text=property_output02,
                          bg='white', font=fontstyle).place(x=5, y=100)


def map():
    global framemap, player1, player2, btn_dice
    for i in range(sp, fp):
        for j in range(sp, fp):
            if(i == fp-1 and j == fp-1):  # Jail
                labelframe = tk.LabelFrame(
                    window, text='Jail', font=fontstyle, width=100, height=100)
                labelframe.grid(row=i, column=j, padx=1, pady=1)
                framemap[i][j] = tk.Frame(
                    labelframe, bg='white', width=100, height=100)
                framemap[i][j].grid(row=i, column=j, padx=10, pady=10)

            elif(i > sp and i < fp-1 and j > sp and j < fp-1):  # middle
                frame1 = tk.Frame(window, bg='lightsalmon',
                                  width=100, height=100)
                frame1.grid(row=i, column=j)

                if(i == 1 and j == 1):
                    outtext = tk.Label(frame1, text='大', bg='lightsalmon', font=tkFont.Font(
                        size=30), width=5, height=2).grid(row=i, column=j)
                if(i == 1 and j == 2):
                    outtext = tk.Label(frame1, text='富', bg='lightsalmon', font=tkFont.Font(
                        size=30), width=5, height=2).grid(row=i, column=j)
                if(i == 1 and j == 3):
                    outtext = tk.Label(frame1, text='翁', bg='lightsalmon', font=tkFont.Font(
                        size=30), width=5, height=2).grid(row=i, column=j)
            else:
                node_price[i][j] = randint(1, 100) * 100
                labelframe = tk.LabelFrame(
                    window, text='$' + str(node_price[i][j]), font=fontstyle, width=100, height=100)
                labelframe.grid(row=i, column=j, padx=1, pady=1)
                framemap[i][j] = tk.Frame(
                    labelframe, bg='white', width=100, height=100)
                framemap[i][j].grid(row=i, column=j, padx=10, pady=10)
    btn_dice = tk.Button(window, text='Dice', bg='orange',
                         command=dice, font=fontstyle, width=5, height=2)
    btn_dice.grid(row=3, column=10, padx=10, pady=10)
    player1 = update_player(1, player1, 0, 0)
    player2 = update_player(2, player2, 0, 0)


def dice():
    global player1, player1_loc, player2, player2_loc, btn_dice
    btn_dice['state'] = 'disabled'
    num = randint(1, 6)
    # TODO: add message box
    print("dice1: ", num)
    player1, player1_loc = move(1, player1, player1_loc, num)
    num = randint(1, 6)
    print("dice2: ", num)
    player2, player2_loc = move(2, player2, player2_loc, num)
    btn_dice['state'] = 'normal'


def move(player_id, player, player_loc, count):
    print("move start")
    for i in range(0, count):
        player_loc += 1
        player_loc %= 16
        if(player_loc <= 4):
            player = update_player(player_id, player, 0, player_loc)
            if i == count - 1:
                check_node(player_id, 0, player_loc)
        elif(player_loc <= 8):
            player = update_player(player_id, player, player_loc - 4, 4)
            if i == count - 1:
                check_node(player_id, player_loc - 4, 4)
        elif(player_loc <= 12):
            player = update_player(player_id, player, 4, 12 - player_loc)
            if i == count - 1:
                check_node(player_id, 4, 12 - player_loc)
        else:
            player = update_player(player_id, player, 16 - player_loc, 0)
            if i == count - 1:
                check_node(player_id, 16 - player_loc, 0)
        window.update()
        time.sleep(0.5)
    print("move stop")
    return player, player_loc


def update_player(player_id, player, i, j):
    print(i, j)
    if player is not None:
        player.destroy()
    if player_id == 1:
        player = tk.Label(framemap[i][j], text='Player 1',
                          bg='dodgerblue', fg='white', font=fontstyle)
        player.place(x=5, y=10)
    elif player_id == 2:
        player = tk.Label(framemap[i][j], text='Player 2',
                          bg='limegreen', fg='white', font=fontstyle)
        player.place(x=5, y=50)
    return player


def update_owner(player_id, i, j):
    node_owner[i][j] = player_id
    if player_id == 1:
        framemap[i][j].config(bg='lightblue')
    elif player_id == 2:
        framemap[i][j].config(bg='lightgreen')


def check_node(player_id, i, j):
    if not (i == fp - 1 and j == fp - 1):
        if node_owner[i][j] != 0:
            if node_owner[i][j] != player_id:
                tk.messagebox.showinfo(
                    '支付過路費', '你走到了' + str(node_owner[i][j]) + "號玩家的土地，需支付" + str(int(node_price[i][j] / 2)) + "元")
                player_cash[player_id - 1] -= int(node_price[i][j] / 2)
                player_cash[node_owner[i][j] - 1] += int(node_price[i][j] / 2)

        else:
            if tk.messagebox.askyesno('購買土地', '你要購買這塊地嗎?') == True:
                player_cash[player_id - 1] -= node_price[i][j]
                player_property[player_id - 1] += node_price[i][j]
                update_owner(player_id, i, j)
        scoreboard()


scoreboard()
map()

window.mainloop()
