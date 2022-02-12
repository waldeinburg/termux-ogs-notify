OGS notifier for Termux
=======================

Simple script to run in Termux to get a notification on your phone when it's your turn in a
correspondence game on [OGS](https://online-go.com).

## Installation

Install [Termux](https://play.google.com/store/apps/details?id=com.termux) and open a Termux
terminal.

Install `python3`, `python-socketio` and `websocket-client`. You will also need `wget` or `curl` for
downloading the script:

    apt update
    apt install python wget
    pip install python-socketio websocket-client

Download script and make it executable.

    wget https://github.com/waldeinburg/termux-ogs-notify/blob/main/ogs-notify.py
    chmod +x ogs-notify.py

In a browser, log in to [OGS](https://online-go.com) and visit
[https://online-go.com/api/v1/ui/config]. This will display a JSON file. You will need the `user.id`
and `notification_auth` keys:

    ...
    "user": {
        ...
        "id": SOMEVALUE,
        ...
    },
    ...
    "notification_auth": "SOMEVALUE",
    ...

In Termux, create a file, `~/.ogs-notify`, with exactly two lines. In the first line, put the value
of `user.id`, in the next line put the value `notification_auth` (without the quotes!):

    nano .ogs-notify

Now you're ready!

## Usage

Open Termux and run:

    ./ogs-notify.py

If you have game running, and it's your turn, a notification should show up. Tap the notification to
open the game in your default browser.

## Known issues

If you know that you have game running and that it's your turn and a notification does not show up,
the most likely reason is wrong credentials. It doesn't seem to be documented how to get error
feedback from the OGS real time API.

## License

Copyright © 2021 Daniel Lundsgaard Skovenborg

Distributed under the Eclipse Public License either version 1.0 or (at your option) any later
version.
