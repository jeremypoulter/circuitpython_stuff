from adafruit_circuitplayground.express import cpx
import adafruit_fancyled.adafruit_fancyled as fancy

cpx.pixels.auto_write = False  # Update only when we say
cpx.pixels.brightness = 0.25   # make less blinding

palette = [fancy.CRGB(255, 255, 255),  # White
           fancy.CRGB(255, 255, 0),    # Yellow
           fancy.CRGB(255, 0, 0),      # Red
           fancy.CRGB(0,0,0)]          # Black

offset = 0  # Position offset into palette to make it "spin"

while True:
    for i in range(10):
        color = fancy.palette_lookup(palette, offset + i / 9)
        cpx.pixels[i] = color.pack()
    cpx.pixels.show()

    offset += 0.033  # Bigger number = faster spin