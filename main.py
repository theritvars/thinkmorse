#!/usr/bin/python

from time import sleep

text_string = "MM7XRT"

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...', 
                    'C':'-.-.', 'D':'-..', 'E':'.', 
                    'F':'..-.', 'G':'--.', 'H':'....', 
                    'I':'..', 'J':'.---', 'K':'-.-', 
                    'L':'.-..', 'M':'--', 'N':'-.', 
                    'O':'---', 'P':'.--.', 'Q':'--.-', 
                    'R':'.-.', 'S':'...', 'T':'-', 
                    'U':'..-', 'V':'...-', 'W':'.--', 
                    'X':'-..-', 'Y':'-.--', 'Z':'--..', 
                    '1':'.----', '2':'..---', '3':'...--', 
                    '4':'....-', '5':'.....', '6':'-....', 
                    '7':'--...', '8':'---..', '9':'----.', 
                    '0':'-----', ', ':'--..--', '.':'.-.-.-', 
                    '?':'..--..', '/':'-..-.', '-':'-....-', 
                    '(':'-.--.', ')':'-.--.-'} 

multiplier = 0.15

# International Morse code is composed of five elements:
# - short mark, dot or "dit" (.): "dot duration" is one time unit long
# - longer mark, dash or "dah" (-): three time units long
# - inter-element gap between the dots and dashes within a character: one dot duration or one unit long
# - short gap (between letters): three time units long
# - medium gap (between words): seven time units long

DOT_LENGTH = 1
DASH_LENGTH = 3
INNER_ELE_GAP = 1
LETTER_GAP = 3
WORD_GAP = 7
LOOP_GAP = 10

def text_to_morse(txt):
    cipher = ""
    for letter in txt.upper():
        if letter != " ":
            cipher += MORSE_CODE_DICT[letter] + " "
        else:
            cipher += "/"
    return cipher


def led(state):
    if state:
        led = open("/sys/kernel/debug/ec/ec0/io", "wb")
        led.seek(12)
        led.write(b"\x8a")
        led.flush()
    else:
        led = open("/sys/kernel/debug/ec/ec0/io", "wb")
        led.seek(12)
        led.write(b"\x0a")
        led.flush()

if __name__ == "__main__":
    while True:
        led(False)
        morse_string = text_to_morse(text_string)
        for ind,ch in enumerate(morse_string[:-1]):
            if ch == ".":
                led(True)
                sleep(multiplier * DOT_LENGTH)
                led(False)

                if morse_string[ind+1] != " " or morse_string[ind+1] != "/":
                    sleep(multiplier * INNER_ELE_GAP)

            elif ch == "-":
                led(True)
                sleep(multiplier * DASH_LENGTH)
                led(False)

                if morse_string[ind+1] != " " or morse_string[ind+1] != "/":
                    sleep(multiplier * INNER_ELE_GAP)

            elif ch == " ":
                if morse_string[ind+1] != "/" or morse_string[ind-1] != "/":
                    sleep(multiplier * LETTER_GAP)

            elif ch == "/":
                sleep(multiplier * WORD_GAP)

        sleep(multiplier * LOOP_GAP)
