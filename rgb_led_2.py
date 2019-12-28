#from adafruit_circuitplayground.express import cpx
import board
import neopixel
import adafruit_irremote
import pulseio
import time

import gc

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=False)

savedColour = (255, 255, 255)
mode = 0
display = 0

def fill(colour):
  pixels.fill(colour[mode])
  global savedColour
  savedColour = colour[mode]

def brightness(brightness):
  pixels.brightness = brightness

def setMode():
  global mode
  mode = mode + 1
  if mode > 1:
    mode = 0
  pixels.fill((0,0,0))
  pixels[mode] = (0,0,255)
  pixels.show()
  time.sleep(0.3)
  pixels.fill(savedColour)

def setAuto():
  global display
  display = display + 1
  if display > 1:
    display = 0

pulsein = pulseio.PulseIn(board.IR_RX, maxlen=120, idle_state=True)
decoder = adafruit_irremote.GenericDecode()

pixels.fill(savedColour)

command_table = {
  0xff008778: lambda : pixels.fill((0, 0, 0)),
  0xff0007f8: lambda : pixels.fill(savedColour),

  0xff00e718:  lambda : fill(((255, 0, 0),     (252, savedColour[1], savedColour[2]))),
  0xff00df20:  lambda : fill(((255, 40, 0),    (189, savedColour[1], savedColour[2]))),
  0xff00ef10:  lambda : fill(((255, 80, 0),    (126, savedColour[1], savedColour[2]))),
  0xff00cf30:  lambda : fill(((255, 120, 0),   (63, savedColour[1], savedColour[2]))),
  0xff00f708:   lambda : fill(((255, 160, 0),   (0, savedColour[1], savedColour[2]))),

  0xff006798: lambda : fill(((0, 255, 0),     (savedColour[0], 252, savedColour[2]))),
  0xff005fa0:  lambda : fill(((0, 200, 50),    (savedColour[0], 189, savedColour[2]))),
  0xff006f90: lambda : fill(((0, 150, 100),   (savedColour[0], 126, savedColour[2]))),
  0xff004fb0:  lambda : fill(((0, 100, 150),   (savedColour[0], 63, savedColour[2]))),
  0xff007788: lambda : fill(((0, 50, 200),    (savedColour[0], 0, savedColour[2]))),

  0xff00a758:  lambda : fill(((0, 0, 255),     (savedColour[0], savedColour[1], 252))),
  0xff009f60:  lambda : fill(((40, 0, 255),    (savedColour[0], savedColour[1], 189))),
  0xff00af50:  lambda : fill(((80, 0, 255),    (savedColour[0], savedColour[1], 126))),
  0xff008f70: lambda : fill(((120, 0, 250),   (savedColour[0], savedColour[1], 63))),
  0xff00b748:  lambda : fill(((250, 0, 120),   (savedColour[0], savedColour[1], 0))),

  0xff00d728:  lambda : fill(((255, 255, 255), (0, 0, 0))),

  0xff0027d8:  lambda : brightness(1),
  0xff001fe0:  lambda : brightness(0.8),
  0xff002fd0:  lambda : brightness(0.6),
  0xff000ff0:  lambda : brightness(0.4),
  0xff0037c8:  lambda : brightness(0.2),

  0xff0017e8:  lambda : setMode(),
}

def dummy():
  return

def decodeIr(pulses):
  try:
    received_code = decoder.decode_bits(pulses, debug=False)
  except adafruit_irremote.IRNECRepeatException:
    return
  except adafruit_irremote.IRDecodeException:
    return

  if 4 != len(received_code):
    return

  code = (received_code[0] << 24) + (received_code[1] << 16) + (received_code[2] << 8) + received_code[3]

  command_table.get(code, dummy)()
  print(hex(code), savedColour, gc.mem_free())

while True:
  print(gc.mem_free())
  pulses = decoder.read_pulses(pulsein, blocking = False)
  if(None != pulses):
    decodeIr(pulses)

  pixels.show()