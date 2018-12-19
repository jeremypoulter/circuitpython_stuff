# for delay
import time

# for mouse emulation
from adafruit_hid.mouse import Mouse

# the cpx
import board

# buttons
from digitalio import DigitalInOut, Direction, Pull

# accelerometer
import adafruit_lis3dh

# i2c
import busio

# set up the on-board LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# right button
rbutton = DigitalInOut(board.BUTTON_A)
rbutton.direction = Direction.INPUT
rbutton.pull = Pull.DOWN

# left button
lbutton = DigitalInOut(board.BUTTON_B)
lbutton.direction = Direction.INPUT
lbutton.pull = Pull.DOWN

# mouse
mouse = Mouse()

# accelerometer
i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)
lis3dh.range = adafruit_lis3dh.RANGE_8_G

# infinite loop
while True:

    # if either button is pressed, light up the LED
    if (rbutton.value) or (lbutton.value):  # button is pushed
        led.value = True

        # if it is the right button, emulate right-click
        if rbutton.value:
            mouse.click(Mouse.RIGHT_BUTTON)

        # if left, left-click
        if lbutton.value:
            mouse.click(Mouse.LEFT_BUTTON)
    # otherwise, LED off
    else:
        led.value = False

    # get the acceleration
    x, y, z = lis3dh.acceleration

    # log to plotter
    print((x, y, z))

    # if tilted right, move right
    if (x > 1):
        mouse.move(x=x)

    # ... move left
    elif (x < 0):
        mouse.move(x=x)

    # up
    if (y > 1):
        mouse.move(y=y)

    # down
    elif (y < 0):
        mouse.move(y=y)

    # otherwise blank
    else:
        print()

    # tiny delay then loop!
    time.sleep(0.1)
