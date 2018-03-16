#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

class Listener():
    def __init__(self, verbose=False):
        self.verbose = verbose
        pass


    def main(self):
        """ Main loop that runs as long as object is listening. """
        pass


    def read_to_buffer(self, pin=23, read_rate=20.0, write_rate=5.0):
        """ Listens to GPIO and interprets bits that are sent on the line.
        After end of message is detected, returns the message as a string. """

        self.prepare_pin(pin)
        bit_buffer = []
        cur_bit = []
        end_detected = False
        delay_amt = 1.0/read_rate
        write_time = 1.0/write_rate
        rpw = read_rate/write_rate  #   Read bits per write bit

        #   Reads from the pin until a nonzero value is read, meaning msg start.
        while not (1 in bit_buffer):
            cur_bit = []
            self.delay(delay_amt)
            cur_bit.append(self.read_pin(pin))
        self.print_v("Detected start of message.")

        t_last = time.time()    #   time of last buffer write
        while not end_detected:
            read = self.read_pin(pin)
            cur_bit.append(read)
            self.delay(delay_amt)

            #   If the next bit should have been broadcast, clear cur_bit and
            #   append bit value to bit_buffer.
            t_cur = time.time()
            if t_cur - t_last >= write_time:
                avg = float(sum(cur_bit))/len(cur_bit)
                bit_buffer.append(avg)
                cur_bit = []
                t_last = t_cur

        #TODO finish implementation


    def print_v(self, msg):
        """ Prints the message only if self.verbose is true. """
        if self.verbose:
            print(msg)


    def prepare_pin(pin=23):
        """ Prepares a RasPi pin to be read. Only needs to be done once
        per pin used. """
        GPIO.setmode(GPIO.BCM)  #use Broadcom (BCM) GPIO numbers on breakout pcb
        GPIO.setup(pin,GPIO.IN) # allow pi to read levels


    def read_pin(pin):
        """ Reads the value of the given pin. """
        return GPIO.input(pin)  # set 3.3V level on GPIO output


    def delay(duration):
        """ Sleep for duration seconds where duration is a float. """
        time.sleep(duration)


    def receive(blinks=200,duration=.25,pin=23):
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
