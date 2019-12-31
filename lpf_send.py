#from adafruit_circuitplayground.express import cpx
import board
import adafruit_irremote
import pulseio
from digitalio import DigitalInOut, Direction, Pull

import neopixel

pixel_pin = board.NEOPIXEL
num_pixels = 10

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

## Create a 'pulseio' output, to send infrared signals on the IR transmitter @ 38KHz
pwm = pulseio.PWMOut(board.IR_TX, frequency=38000, duty_cycle=2 ** 15)
pulseout = pulseio.PulseOut(pwm)
# Create an encoder that will take numbers and turn them into NEC IR pulses
encoder = adafruit_irremote.GenericTransmit(header=[156, 1014], one=[156, 546],
                                            zero=[156, 260], trail=0)
 
channel = 0
address = 0
output = 0
toggle = 0
pwm = 0

MIN_PWM = -7
MAX_PWM = 7

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
BLACK = (0, 0, 0)

button_a = DigitalInOut(board.BUTTON_A)
button_a.direction = Direction.INPUT
button_a.pull = Pull.DOWN

button_a_last = False

button_b = DigitalInOut(board.BUTTON_B)
button_b.direction = Direction.INPUT
button_b.pull = Pull.DOWN

button_b_last = False

def setPwm(pwm):
    global toggle
    print("Set pwm %d" % pwm)

    print("toggle = %d, channel = %d, output = %d, address = %d" % (toggle, channel, output, address))

    nibble1 = (toggle << 3) | channel 
    nibble2 = (address << 3) | (1 << 2) | output

    if 0 == pwm:
        nibble3 = 1 << 3
    elif pwm < 0:
        nibble3 = (1 << 3) | (8 + pwm)
    else:
        nibble3 = pwm

    nibble4 = 0xF ^ nibble1 ^ nibble2 ^ nibble3

    print("Nibbles: ", nibble1, nibble2, nibble3, nibble4)

    byte1 = (nibble1 << 4) | nibble2
    byte2 = (nibble3 << 4) | nibble4

    colour = GREEN if pwm >= 0 else BLUE
    pwm = abs(pwm)
    #print (pwm, colour)

    for i in range(num_pixels):
        pixels[i] = colour if i < pwm else BLACK
    
    pixels.show()

    print("Sending code: %s %s" % ('{:08b}'.format(byte1), '{:08b}'.format(byte2)))
    encoder.transmit(pulseout, [byte1, byte2])

    toggle = (toggle + 1) % 2

while True:
    if button_a_last != button_a.value:
        button_a_last = button_a.value
        if button_a.value:
            if pwm < MAX_PWM:
                pwm = pwm + 1
                setPwm(pwm)
    if button_b_last != button_b.value:
        button_b_last = button_b.value
        if button_b.value:
            if pwm > MIN_PWM:
                pwm = pwm - 1
                setPwm(pwm)
