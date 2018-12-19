#from adafruit_circuitplayground.express import cpx
import board
import neopixel
import adafruit_irremote
import pulseio

# Set up the 10 Circuit Playground Express NeoPixels half bright
#num_pixels = 10
#pixels = cpx.pixels
#cpx.pixels.brightnes = 0.1

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.2)

savedColour = 0

def fill(colour):
  pixels.fill(colour)
  global savedColour
  savedColour = colour

def off():
  pixels.fill((0, 0, 0))

def on():
  pixels.fill(savedColour)

def brightness(brightness):
  pixels.brightness = brightness

# Create a 'pulseio' input, to listen to infrared signals on the IR receiver
pulsein = pulseio.PulseIn(board.IR_RX, maxlen=120, idle_state=True)
# Create a decoder that will take pulses and turn them into numbers
decoder = adafruit_irremote.GenericDecode()

fill((255, 255, 255))

command_table = [
  { "code": [255, 0, 135, 120], "action": lambda : off() },
  { "code": [255, 0, 7, 248],   "action": lambda : on() },

  { "code": [255, 0, 231, 24],  "action": lambda : fill((255, 0, 0)) },
  { "code": [255, 0, 223, 32],  "action": lambda : fill((255, 40, 0)) },
  { "code": [255, 0, 239, 16],  "action": lambda : fill((255, 80, 0)) },
  { "code": [255, 0, 207, 48],  "action": lambda : fill((255, 120, 0)) },
  { "code": [255, 0, 247, 8],   "action": lambda : fill((255, 160, 0)) },
  
  { "code": [255, 0, 103, 152], "action": lambda : fill((0, 255, 0)) },
  { "code": [255, 0, 95, 160],  "action": lambda : fill((0, 200, 50)) },
  { "code": [255, 0, 111, 144], "action": lambda : fill((0, 150, 100)) },
  { "code": [255, 0, 79, 176],  "action": lambda : fill((0, 100, 150)) },
  { "code": [255, 0, 119, 136], "action": lambda : fill((0, 50, 200)) },

  { "code": [255, 0, 167, 88],  "action": lambda : fill((0, 0, 255)) },
  { "code": [255, 0, 159, 96],  "action": lambda : fill((40, 0, 255)) },
  { "code": [255, 0, 175, 80],  "action": lambda : fill((80, 0, 255)) },
  { "code": [255, 0, 143, 112], "action": lambda : fill((120, 0, 250)) },
  { "code": [255, 0, 183, 72],  "action": lambda : fill((250, 0, 120)) },

  { "code": [255, 0, 215, 40],  "action": lambda : fill((255, 255, 255)) },

  { "code": [255, 0, 39, 216],  "action": lambda : brightness(1) },
  { "code": [255, 0, 31, 224],  "action": lambda : brightness(0.8) },
  { "code": [255, 0, 47, 208],  "action": lambda : brightness(0.6) },
  { "code": [255, 0, 15, 240],  "action": lambda : brightness(0.4) },
  { "code": [255, 0, 55, 200],  "action": lambda : brightness(0.2) },
]

while True:
  pulses = decoder.read_pulses(pulsein)
  try:
    # Attempt to convert received pulses into numbers
    received_code = decoder.decode_bits(pulses, debug=False)
  except adafruit_irremote.IRNECRepeatException:
    # We got an unusual short code, probably a 'repeat' signal
    # print("NEC repeat!")
    continue
  except adafruit_irremote.IRDecodeException as e:
    # Something got distorted or maybe its not an NEC-type remote?
    # print("Failed to decode: ", e.args)
    continue

  print("NEC Infrared code received: ", received_code)
  for command in command_table:
    if command['code'] == received_code:
      command['action']()
  print(savedColour)