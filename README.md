# disdox.py
Discord Doxxing Python (Recommended 3.11+) script based on WebHooks and Pastebin for Windows

The script provides the user with the target's location, entire network configuration, PC and account names.

In the future, it will support WiFi Password Sniffer (Made by me, still unpublished)

# Running
You can embed script in e.g. Python / Ren'py games, just integrate the script running into part of a code and make sure you install the requests package, you can do this with commands like this: ```pip install requests && python disdox.py ipconf_on "Test message"```, this won't work if python isn't installed on the machine so you will need to use portable python which I will not get into.

# Arguments
You can disable the function for attaching ```ipconfig /all``` output in the webhook message by adding the ```ipconf_off``` argument.
You can add custom messages to webhook messages by adding a second argument in double quotation marks e.g. ```"Test message"```

# Setting up
Before the script will be usable you need to fill role ID to ping inside of a message (you can also remove it) and link to Pastebin hosting raw webhook link.

# Why Pastebin?
If your webhook gets nuked you can edit your paste without editing the script itself after deployment, especially useful when using the same webhook on multiple targets.
