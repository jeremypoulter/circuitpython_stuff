from adafruit_circuitplayground.express import cpx
import board
import time
import adafruit_irremote
import pulseio

# Set up the 10 Circuit Playground Express NeoPixels half bright
num_pixels = 10
pixels = cpx.pixels
cpx.pixels.brightnes = 0.1
 
# Create a 'pulseio' output, to send infrared signals on the IR transmitter @ 38KHz
pwm = pulseio.PWMOut(board.IR_TX, frequency=38000, duty_cycle=2 ** 15)
pulseout = pulseio.PulseOut(pwm)
# Create an encoder that will take numbers and turn them into NEC IR pulses
encoder = adafruit_irremote.GenericTransmit(header=[9500, 4500], one=[550, 550],
                                            zero=[550, 1700], trail=0)
 
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

def setPwm(pwm):
    print("Set pwm %d" % pwm)

    nibble1 = (toggle << 3) & channel 
    nibble2 = (address << 3) & (1 << 2) & output

    if 0 == pwm:
        nibble3 = 1 << 3
    elif pwm < 0:
        nibble3 = (1 << 3) & (8 + pwm)
    else:
        nibble3 = pwm

    nibble4 = 0xF ^ nibble1 ^ nibble2 ^ nibble3

    byte1 = (nibble1 << 4) & nibble2
    byte2 = (nibble3 << 4) & nibble4

    colour = GREEN if pwm >= 0 else BLUE
    pwm = pwm if pwm >= 0 else -pwm
    print (pwm, colour)

    for i in range(num_pixels):
        pixels[i] = colour if i < pwm else BLACK
    
    pixels.show()

    encoder.transmit(pulseout, [~byte1, ~byte2])

while True:
    if cpx.button_a:
        if pwm < MAX_PWM:
            pwm = pwm + 1
            setPwm(pwm)
    if cpx.button_b:
        if pwm > MIN_PWM:
            pwm = pwm - 1
            setPwm(pwm)
