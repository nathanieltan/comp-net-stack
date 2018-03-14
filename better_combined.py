#
## Introducton to Python breadboarding
#
from text_to_morse import sequence_to_morse
import time
import RPi.GPIO as GPIO
import sys

letter_dict = {".-": "a",
                "-...": "b",
                "-.-.": "c",
                "-..": "d",
                ".": "e",
                "..-.": "f",
                "--.": "g",
                "....": "h",
                "..": "i",
                ".---": "j",
                "-.-": "k",
                ".-..": "l",
                "--": "m",
                "-.": "n",
                "---": "o",
                ".--.": "p",
                "--.-": "q",
                ".-.": "r",
                "...": "s",
                "-": "t",
                "..-": "u",
                "...-": "v",
                ".--": "w",
                "-..-": "x",
                "-.--": "y",
                "--..": "z",
                ".----": "1",
                "..---": "2",
                "...--": "3",
                "....-": "4",
                ".....": "5",
                "-....": "6",
                "--...": "7",
                "---..": "8",
                "----.": "9",
                "-----": "0"}
#
## Introducton to Python breadboarding
#
import time
import RPi.GPIO as GPIO
dot = [1, 0]
dash = [1, 1, 1, 0]
let_brk = [0]*2
wor_brk = [0]*4
letter_dict = {"a": dot + dash,
                "b": dash + dot + dot + dot,
                "c": dash + dot + dash + dot,
                "d": dash + dot + dot,
                "e": dot,
                "f": dot + dot + dash + dot,
                "g": dash + dash + dot,
                "h": dot + dot + dot + dot,
                "i": dot + dot,
                "j": dot + dash + dash + dash,
                "k": dash + dot + dash,
                "l": dot + dash + dot + dot,
                "m": dash + dash,
                "n": dash + dot,
                "o": dash + dash + dash,
                "p": dot + dash + dash + dot,
                "q": dash + dash + dot + dash,
                "r": dot + dash + dot,
                "s": dot + dot + dot,
                "t": dash,
                "u": dot + dot + dash,
                "v": dot + dot + dot + dash,
                "w": dot + dash + dash,
                "x": dash + dot + dot + dash,
                "y": dash + dot + dash + dash,
                "z": dash + dash + dot + dot,
                "1": dot + dash + dash + dash + dash,
                "2": dot + dot + dash + dash + dash,
                "3": dot + dot + dot + dash + dash,
                "4": dot + dot + dot + dot + dash,
                "5": dot + dot + dot + dot + dot,
                "6": dash + dot + dot + dot + dot,
                "7": dash + dash + dot + dot + dot,
                "8": dash + dash + dash + dot + dot,
                "9": dash + dash + dash + dash + dot,
                "0": dash + dash + dash + dash + dash,
                " ": wor_brk}

def letter_to_morse(letter):

    return letter_dict[letter] + let_brk

def sequence_to_morse(sequence):
    sequence_in_morse = []
    for letter in sequence:
        sequence_in_morse += letter_to_morse(letter)
    return sequence_in_morse[:-2]
s=sequence_to_morse("acknowledged")

def prepare_spin(pin=17):
    GPIO.setmode(GPIO.BCM)  #use Broadcom (BCM) GPIO numbers on breakout pcb
    
    GPIO.setup(pin,GPIO.OUT) # allow pi to set 3.3v and 0v levels

def turn_shigh(pin):
    GPIO.output(pin,GPIO.HIGH)  # set 3.3V level on GPIO output

def turn_slow(pin):
    GPIO.output(pin,GPIO.LOW)   # set ground (0) level on GPIO output

def delays(duration):            # sleep for duration seconds where duration is a float.
    time.sleep(duration)



    
        
def blink(duration=1,pin=17):
    prepare_spin(pin)

    
    for i in range(len(s)):
        d=s[i]
        if d==1:
            turn_shigh(pin)
            delays(duration)
        elif d==0:
            turn_slow(pin)
            delays(duration)    
def letter(sequence):
    return letter_dict[sequence]

def word(sequence):
    seq = sequence.split("_")
    letter_seq = [letter(piece) for piece in seq]
    res = ""
    for item in letter_seq:
        res += item
    return res

def sequence(message):
    msg = message.split("/")
    msg_seq = [word(piece) for piece in msg]
    res = ""
    for item in msg_seq:
        res += item + " "
    return res[:-1]

def sequence_from_list(message):
    """ Use this function to convert a list of morse to a string. """

    msg = ""
    for item in message:
        msg += item
    return sequence(msg)

def interpret_sequence(s):
    i=0
    x=[]
    while i < len(s):
        d=s[i]

        if d==1:
            if len(s)>(i+1):
                m=s[i+1]
                if m==1:
                    print("dash")
                    x.append('-')
                    i=i+2
                else:
                    print("dot")
                    x.append('.')
        else:
            if len(s)>(i+4):
                m=s[i+1]
                f=s[i+3]
                e=s[i+2]
                #print(f)
                d=s[i+4]
                #print(d)
                #print(m)
                #print(e)
                if f==0 and d==0 and m==0:

                    print("word break")
                    x.append('/')
                    i=i+6
                elif m==0:

                    print("letter break")
                    i=i+2
                    x.append('_')
        i=i+1
    return sequence_from_list(x)


class Safeguards:
    def __enter__(self):
        return self
    def __exit__(self,*rabc):
        GPIO.cleanup()
        print("Safe exit succeeded")
        return not any(rabc)


def prepare_pin(pin=23):
    GPIO.setmode(GPIO.BCM)  #use Broadcom (BCM) GPIO numbers on breakout pcb

    GPIO.setup(pin,GPIO.IN) # allow pi to read levels

def read_pin(pin):
    return GPIO.input(pin)  # set 3.3V level on GPIO output

def delay(duration):            # sleep for duration seconds where duration is a float.
    time.sleep(duration)

def receive(blinks=200,duration=.25,pin=23):
    prepare_pin(pin)
    s=[]

    for i in range(blinks):
        if read_pin(pin):
            s.append(1)
        else:
            s.append(0)
        print("|{}".format("==" if read_pin(pin) else ""))
        if 1 in s:
            blink()
        delay(duration)
    return interpret_sequence(s)





if __name__ == "__main__":
    with Safeguards():
       receive()
