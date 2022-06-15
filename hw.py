import pickle
import select
import socket
import threading
import time
import tkinter as tk
import tkinter.font as tkFont
from random import randint
from tkinter import messagebox, simpledialog
from tkinter.ttk import Frame, Style

# Map size
sp = 0  # start point
fp = 5  # finish point

version_id = "2.0-rc1"
window = tk.Tk()
window.title("大富翁    版本:" + version_id + "  模式:單機模式")
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
frameprice = [[None] * 5 for i in range(5)]
btn_dice = None
server_socket = None
client_socket = None
my_playerid = 0
player_playing = 1
label_player1_playering = None
label_player2_playering = None
label_player1_you = None
label_player2_you = None
label_player1_cash = None
label_player2_cash = None
label_player1_property = None
label_player2_property = None
run_handler = True
socket_lock = False


def start_server():
    global client_socket, my_playerid
    rand_port = randint(10000, 60000)
    if tk.messagebox.askokcancel('啟動遊戲伺服器', '即將啟動遊戲伺服器,請於對方的遊戲輸入IP及Port(' + str(rand_port) + '),按下OK以啟動伺服器') == True:
        print("[start_server] tk.messagebox.showinfo")
        tk.messagebox.showinfo('等待對方連線', '伺服器正在等待對方連線,遊戲視窗可能會顯示沒有反應，請稍後...')
        print("[start_server] Creating socket...")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[start_server] setsockopt socket.SOL_SOCKET socket.SO_REUSEADDR 1")
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("[start_server] bind", rand_port)
        server_socket.bind(('', rand_port))
        print("[start_server] listen 10")
        server_socket.listen(10)
        print("[start_server] Wait for connection...")
        client_socket, addr = server_socket.accept()
        print("[start_server] Client (%s, %s) connected" % addr)
        print("[start_server] Call send_init")
        send_init()
        print("[start_server] Setting up my_playerid")
        my_playerid = 1
        print("[start_server] Place label_player1_you")
        label_player1_you.place(x=100, y=5)
        print("[start_server] tk.messagebox.showinfo")
        tk.messagebox.showinfo('連線成功', '玩家' + str(addr) + '已加入遊戲')
        print("[start_server] set window.title")
        window.title("大富翁    版本:" + version_id + "  模式:連線模式  角色:伺服端  Port:" + str(rand_port))
        print("[start_server] Finished.")


def start_client():
    global client_socket, my_playerid
    if (host := tk.simpledialog.askstring('連線至伺服器', 'IP位置:')) is not None:
        if (port := tk.simpledialog.askinteger('連線至伺服器', 'Port:')) is not None:
            print("[start_client] Get Host =", host, "Port =", port)
            try:
                print("[start_client] Creating socket...")
                client_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                print("[start_client] Socket connect")
                client_socket.connect((host, port))
                print("[start_client] Call receive_init")
                receive_init()
                print("[start_client] Setting up my_playerid")
                my_playerid = 2
                print("[start_client] Place label_player2_you")
                label_player2_you.place(x=100, y=5)
                print("[start_client] Disable Dice button")
                btn_dice['state'] = 'disabled'
                print("[start_client] tk.messagebox.showinfo")
                tk.messagebox.showinfo('連線成功', '已成功連線至遊戲伺服器')
                print("[start_client] set window.title")
                window.title("大富翁    版本:" + version_id + "  模式:連線模式  角色:客戶端  伺服端位置:" + host + ":" + str(port))
                print("[start_client] Finished.")
            except:
                print('Unable to connect')


def send_init():
    # server send node_price to client
    client_socket.send(pickle.dumps(node_price))
    if not t.is_alive():
        t.start()
    reset_game()


def receive_init():
    global node_price
    data = client_socket.recv(4096)
    node_price = pickle.loads(data)
    for i in range(sp, fp):
        for j in range(sp, fp):
            if not (i == fp-1 and j == fp-1) and not (i > sp and i < fp-1 and j > sp and j < fp-1):
                frameprice[i][j].configure(text='$' + str(node_price[i][j]))
    if not t.is_alive():
        t.start()
    reset_game()


def socket_handler():
    global socket_lock, player1, player2, player_cash, player_property
    while run_handler:
        ready_to_read, ready_to_write, in_error = select.select(
            [client_socket], [], [], 0)
        if len(ready_to_read) == 1:
            data = client_socket.recv(4096)
            if data:
                data = data.decode().split()
                if data[0] == "ACK":
                    print("[socket_handler] socket_lock unlocked")
                    socket_lock = False
                else:
                    if data[0] == "update_player":
                        print("[socket_handler] Command: update_player")
                        if int(data[1]) == 1:
                            player1 = update_player(
                                1, player1, int(data[2]), int(data[3]), False)
                        else:
                            player2 = update_player(
                                2, player2, int(data[2]), int(data[3]), False)
                    elif data[0] == "update_owner":
                        print("[socket_handler] Command: update_owner")
                        update_owner(int(data[1]), int(
                            data[2]), int(data[3]), False)
                    elif data[0] == "player_poll":
                        print("[socket_handler] Command: player_poll")
                        player_poll(False)
                    elif data[0] == "update_scoreboard":
                        print("[socket_handler] Command: update_scoreboard")
                        player_cash = [int(data[1]), int(data[2])]
                        player_property = [int(data[3]), int(data[4])]
                        update_scoreboard(False)
                    else:
                        print("[socket_handler] Received unknown command:", data)
                    client_socket.send('ACK'.encode())
            else:
                print('[socket_handler] server disconnect!')
                break


t = threading.Thread(target=socket_handler)


def send_peer(data):
    global socket_lock
    while socket_lock == True:
        continue
    if client_socket is not None:
        socket_lock = True
        client_socket.send(data.encode())


def reset_game():
    global player1, player2, player1_loc, player2_loc, player_cash, player_property, player_playing
    player1_loc = 0
    player1 = update_player(1, player1, 0, 0, False)
    player2_loc = 0
    player2 = update_player(2, player2, 0, 0, False)
    player_cash = [50000, 50000]
    player_property = [0, 0]
    update_scoreboard()
    player_playing = 1
    for i in range(sp, fp):
        for j in range(sp, fp):
            if not (i == fp-1 and j == fp-1) and not (i > sp and i < fp-1 and j > sp and j < fp-1):
                update_owner(0, i, j, False)


def build_scoreboard():
    global label_player1_playering, label_player2_playering, label_player1_you, label_player2_you, label_player1_cash, label_player2_cash, label_player1_property, label_player2_property
    cash_output01 = "cash: "+str(player_cash[0])
    cash_output02 = "cash: "+str(player_cash[1])
    property_output01 = "property: "+str(player_property[0])
    property_output02 = "property: "+str(player_property[1])

    board1 = tk.Frame(window, bg='white', width=300, height=150)
    board1.grid(row=1, column=10, padx=10, pady=10)
    player01 = tk.Label(board1, text='Player 1', bg='dodgerblue',
                        fg='white', font=fontstyle).place(x=5, y=5)
    label_player1_playering = tk.Label(board1, text='Playing', bg='red',
                                       fg='white', font=fontstyle)
    label_player1_playering.place(x=200, y=5)
    label_player1_you = tk.Label(board1, text='You', bg='white',
                                 fg='red', font=fontstyle)
    label_player1_cash = tk.Label(board1, text=cash_output01, bg='white',
                                  font=fontstyle)
    label_player1_cash.place(x=5, y=50)
    label_player1_property = tk.Label(board1, text=property_output01,
                                      bg='white', font=fontstyle)
    label_player1_property.place(x=5, y=100)

    board2 = tk.Frame(window, bg='white', width=300, height=150)
    board2.grid(row=2, column=10, padx=10, pady=10)
    player02 = tk.Label(board2, text='Player 2', bg='limegreen',
                        fg='white', font=fontstyle).place(x=5, y=5)
    label_player2_playering = tk.Label(board2, text='Playing', bg='red',
                                       fg='white', font=fontstyle)
    label_player2_you = tk.Label(board2, text='You', bg='white',
                                 fg='red', font=fontstyle)
    label_player2_cash = tk.Label(board2, text=cash_output02, bg='white',
                                  font=fontstyle)
    label_player2_cash.place(x=5, y=50)
    label_player2_property = tk.Label(board2, text=property_output02,
                                      bg='white', font=fontstyle)
    label_player2_property.place(x=5, y=100)


def update_scoreboard(b_send_peer=True):
    print("[update_scoreboard]", b_send_peer)
    if b_send_peer == True:
        send_peer("update_scoreboard " + str(player_cash[0]) + " " + str(
            player_cash[1]) + " " + str(player_property[0]) + " " + str(player_property[1]))
    label_player1_cash.configure(text="cash: " + str(player_cash[0]))
    label_player2_cash.configure(text="cash: " + str(player_cash[1]))
    label_player1_property.configure(text="property: "+str(player_property[0]))
    label_player2_property.configure(text="property: "+str(player_property[1]))


def map():
    global framemap, player1, player2, btn_dice, frameprice
    for i in range(sp, fp):
        for j in range(sp, fp):
            if(i == fp-1 and j == fp-1):  # Jail
                frameprice[i][j] = tk.LabelFrame(
                    window, text='Jail', font=fontstyle, width=100, height=100)
                frameprice[i][j].grid(row=i, column=j, padx=1, pady=1)
                framemap[i][j] = tk.Frame(
                    frameprice[i][j], bg='white', width=100, height=100)
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
                frameprice[i][j] = tk.LabelFrame(
                    window, text='$' + str(node_price[i][j]), font=fontstyle, width=100, height=100)
                frameprice[i][j].grid(row=i, column=j, padx=1, pady=1)
                framemap[i][j] = tk.Frame(
                    frameprice[i][j], bg='white', width=100, height=100)
                framemap[i][j].grid(row=i, column=j, padx=10, pady=10)
    btn_dice = tk.Button(window, text='Dice', bg='orange',
                         command=dice, font=fontstyle, width=5, height=2)
    btn_dice.grid(row=3, column=10, padx=10, pady=10)
    player1 = update_player(1, player1, 0, 0)
    player2 = update_player(2, player2, 0, 0)
    tk.Button(window, text='start server', bg='orange', command=start_server).grid(
        row=0, column=10, padx=10, pady=10)
    tk.Button(window, text='Connect to server', bg='orange', command=start_client).grid(
        row=4, column=10, padx=10, pady=10)


def player_poll(b_send_peer=True):
    print("[player_poll]", b_send_peer)
    if b_send_peer == True:
        send_peer("player_poll")
    global player_playing
    if player_playing == 1:
        player_playing = 2
        label_player1_playering.place_forget()
        label_player2_playering.place(x=200, y=5)
    else:
        player_playing = 1
        label_player1_playering.place(x=200, y=5)
        label_player2_playering.place_forget()
    if my_playerid == 0 or my_playerid == player_playing:
        btn_dice['state'] = 'normal'
    else:
        btn_dice['state'] = 'disabled'


def dice():
    global player1, player1_loc, player2, player2_loc, btn_dice
    btn_dice['state'] = 'disabled'
    num = randint(1, 6)
    print("dice: ", num)
    if player_playing == 1:
        player1, player1_loc = move(1, player1, player1_loc, num)
    else:
        player2, player2_loc = move(2, player2, player2_loc, num)
    player_poll()


def move(player_id, player, player_loc, count):
    for i in range(0, count):
        btn_dice.configure(text=str(count - i - 1))
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
    btn_dice.configure(text='Dice')
    return player, player_loc


def update_player(player_id, player, i, j, b_send_peer=True):
    print("[update_player]", player_id, i, j, b_send_peer)
    if b_send_peer == True:
        send_peer("update_player " + str(player_id) +
                  " " + str(i) + " " + str(j))
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


def update_owner(player_id, i, j, b_send_peer=True):
    print("[update_owner]", player_id, i, j, b_send_peer)
    if b_send_peer == True:
        send_peer("update_owner " + str(player_id) +
                  " " + str(i) + " " + str(j))
    node_owner[i][j] = player_id
    if player_id == 1:
        framemap[i][j].config(bg='lightblue')
    elif player_id == 2:
        framemap[i][j].config(bg='lightgreen')
    else:
        framemap[i][j].config(bg='white')


def check_node(player_id, i, j):
    print("[check_node]", player_id, i, j)
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
        update_scoreboard()


build_scoreboard()
map()

window.mainloop()
run_handler = False
