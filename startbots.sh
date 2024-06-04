#!/bin/bash
cd discord-bots
source colebot/bin/activate
cd octobot
python3 app.py &
disown
cd ..
cd rufus
python3 app.py &
disown
cd ..
cd colebot
python3 app.py &
disown
cd ~
python3 ytapi.py &
disown