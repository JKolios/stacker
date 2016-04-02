#!/usr/bin/env bash

cmd=""
cdto="$PWD"
args="$@"
if [ -d "$1" ]; then
    cdto=`cd "$1"; pwd`
    args="${@:2}"
fi
if [ -n "$args" ]; then
    cmd="; $args"
fi

osascript -e 'tell application "iTerm" to activate'

osascript &>/dev/null <<EOF
    tell application "iTerm"
        tell current terminal
            launch session "Default Session"
            tell the last session
                write text "cd \"$cdto\"$cmd"
            end tell
        end tell
    end tell
EOF