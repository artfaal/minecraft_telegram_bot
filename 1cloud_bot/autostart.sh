#!bin/sh
DIR=$(dirname $0)
screen -dmS cloudbot $DIR/env/bin/python $DIR/app.py