#!/bin/bash

die() {
    printf '%s\n' "$1" >&2
    exit 1
}

show_help() {
    echo "Turn lights on or off on a cleware traffic light"
    echo "-g | --green   to turn on the green light"
    echo "-y | --yellow  to turn on the yellow light"
    echo "-r | --red     to turn on the red light"
    echo "not specifying an option will turn the light off"
}

# Initialize all the option variables.
# This ensures we are not contaminated by variables from the environment.
green=0
yellow=0
red=0

while :; do
    case $1 in
        -h|-\?|--help)
            show_help    # Display a usage synopsis.
            exit
            ;;
        -g|--green)
            green=1
            ;;
        -y|--yellow)
            yellow=1
            ;;
        -r|--red)
            red=1
            ;;
        --)              # End of all options.
            shift
            break
            ;;
        -?*)
            printf 'WARN: Unknown option (ignored): %s\n' "$1" >&2
            ;;
        *)               # Default case: No more options, so break out of the loop.
            break
    esac

    shift
done

clewarecontrol -c 1 -d 903327 -as 2 $green -as 1 $yellow -as 0 $red > /dev/null
