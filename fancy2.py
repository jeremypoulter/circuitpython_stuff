import board
import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy

pixel_pin = board.NEOPIXEL
num_pixels = 10

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False)

pixels.auto_write = False  # Update only when we say
pixels.brightness = 0.25   # make less blinding

palette = [fancy.CRGB(255, 255, 255),  # White
           fancy.CRGB(255, 255, 0),    # Yellow
           fancy.CRGB(255, 0, 0),      # Red
           fancy.CRGB(0,0,0)]          # Black

offset = 0  # Position offset into palette to make it "spin"
levels = (0.95, 1, 0.85)

while True:
    for i in range(10):
        color = fancy.palette_lookup(palette, offset + i / 9)
        color = fancy.gamma_adjust(color, brightness=levels)
        pixels[i] = color.pack()
    pixels.show()

    offset += 0.033  # Bigger number = faster spin