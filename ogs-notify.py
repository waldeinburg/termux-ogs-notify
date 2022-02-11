#!/data/data/com.termux/files/usr/bin/python3

# Thanks to https://github.com/flovo/ogs_api and
# https://forums.online-go.com/t/api-for-notifications-about-new-moves/20264/7

import os

import socketio

game_move_numbers = {}
auth_file = "~/.ogs-notify"


def get_auth():
    try:
        with open(os.path.expanduser(auth_file)) as f:
            lines = f.read().splitlines()  # without newlines
            if len(lines) != 2:
                raise ValueError("Not 2 lines in {}".format(auth_file))
            return [int(lines[0]),
                    lines[1]]
    except Exception as e:
        print(e)
        print("Cannot read authentication. To fix:")
        print("1. Log in to OGS and visit: https://online-go.com/api/v1/ui/config")
        print("2. Create {} with exactly two lines containing the contents of the following fields from that page:"
              .format(auth_file))
        print("user.id")
        print("notification_auth")
        exit(1)


[player_id, auth] = get_auth()
print("Read auth player_id '{}', notification_auth '{}'".format(player_id, auth))

sio = socketio.Client()


def connect():
    if not sio.connected:
        print("Connecting ...")
        sio.connect("https://online-go.com/socket.io/?EIO=3", transports='websocket')
    else:
        print("Already connected")


def notification_connect():
    print("notification/connect")
    sio.emit("notification/connect", {"player_id": player_id,
                                      "auth": auth})


def reconnect():
    print("Reconnecting ...")
    sio.disconnect()
    sio.sleep(1)
    connect()


def keep_alive():
    while True:
        sio.emit("net/ping")
        sio.sleep(20)


def notification_handler(game):
    gid = game['id']
    mn = game['move_number']
    if gid not in game_move_numbers or game_move_numbers[gid] != mn:
        game_move_numbers[gid] = mn
        print("Game id {}, new move number {}".format(gid, mn))
        if game['player_to_move'] == player_id:
            print("Notify my turn!")
            open_game = "termux-open-url 'https://online-go.com/game/{}'".format(gid)
            os.system("termux-notification -t 'Your turn!' -c 'Game: {}' --action '{}'"
                      .format(game['name'], open_game))
    else:
        print("Game id {} unchanged".format(gid))


sio.on("HUP", reconnect)
sio.on("active_game", notification_handler)
sio.on("connect", notification_connect)

connect()

# Avoid constant "packet queue is empty, aborting" errro
sio.start_background_task(keep_alive)

print("Running ...")
