import board
import adafruit_irremote
import pulseio

# Create a 'pulseio' input, to listen to infrared signals on the IR receiver
pulsein = pulseio.PulseIn(board.IR_RX, maxlen=120, idle_state=True)
# Create a decoder that will take pulses and turn them into numbers
decoder = adafruit_irremote.GenericDecode()

toggleSave = -1
 
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
 
    #print("Code received: %s %s" % ('{:08b}'.format(~received_code[0]), '{:08b}'.format(~received_code[1])))

    toggle = received_code[0] >> 7
    escape = (~received_code[0] >> 6) & 1
    channel = (~received_code[0] >> 4) & 3
    address = (~received_code[0] >> 3) & 1
    mode = ~received_code[0] & 7
    data = (~received_code[1] >> 4) & 15
    lrc = ~received_code[1] & 15

    nibble1 = (~received_code[0] >> 4) & 15
    nibble2 = ~received_code[0] & 15
    nibble3 = (~received_code[1] >> 4) & 15

    check = 0xF ^ nibble1 ^ nibble2 ^ nibble3

    if check == lrc and toggle != toggleSave:
        print("toggle = %d, escape = %d, channel = %d, address = %d, mode = %s, data = %s" % (toggle, escape, channel, address, '{:03b}'.format(mode), '{:04b}'.format(data)))
        toggleSave = toggle
