#!/usr/bin/python3

from colorama import Fore, Back, Style

import readchar

def printAllCharsUpTo(stop_char):


    for i in range(ord(' '), ord(stop_char)+1):
        print(chr(i))

def readAllUpTo(stop_key):


    pressed_keys = []

    while True:
        print('Type something (X to stop). ')
        pressed_key = readchar.readkey()

        if pressed_key == stop_key:
            print('You typed ' + Fore.RED + Style.BRIGHT + pressed_key + Style.RESET_ALL + '...' + ' terminating.')
            break
        else:
            print('Thank you for typing ' + pressed_key)
            pressed_keys.append(pressed_key)
    print('The keys you pressed are: ' + str(pressed_keys))

    #Analyze the list and count
    count_pressed_numbers = 0
    count_pressed_others = 0
    pressed_numbers = []
    pressed_others = []
    for pressed_key in pressed_keys:
        if str.isnumeric(pressed_key):
            count_pressed_numbers += 1
            pressed_numbers.append(pressed_key)
        else:
                count_pressed_others += 1
                pressed_others.append(pressed_key)

    print('You entered ' + str(count_pressed_numbers) + ' numbers: ' + str(pressed_numbers))
    print('You entered ' + str(count_pressed_others) + ' others: ' + str(pressed_others))


    text = ''
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN] * len(pressed_others)
    idx = 0
    for pressed_other in pressed_others:
        color = colors[idx]
        text += color + pressed_other + Style.RESET_ALL
        idx += 1

    print('Colored text:')
    print(text)

def main():

    #Ex4a
    #print('Give me the stop char...')
    #pressed_char = readchar.readchar()
    #printAllCharsUpTo(pressed_char)

    #Ex4b
    readAllUpTo('X')


if __name__ == '__main__':
    main()