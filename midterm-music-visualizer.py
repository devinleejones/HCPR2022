import board
import neopixel
import time
import audiobusio
import math
import array
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import (
    PURPLE,
    WHITE,
    AMBER,
    JADE,
    TEAL,
    PINK,
    MAGENTA,
    ORANGE,
)

# variable for neopixel input
strip_pin = board.A1

# variable for number of NeoPixels
num_pixels = 30

# variable for the order of the pixel colors
ORDER = neopixel.RGBW

# variable for NeoPixels output
pixels = neopixel.NeoPixel(
    strip_pin, num_pixels, brightness=.1, auto_write=False,
)

# variable for animation
amber_comet = Comet(pixels, speed=0.01, color=AMBER, tail_length=30)
purple_comet = Comet(pixels, speed=0.01, color=PURPLE, tail_length=30)
teal_comet = Comet(pixels, speed=0.01, color=TEAL, tail_length=30)
pink_comet = Comet(pixels, speed=0.01, color=PINK, tail_length=30)
magenta_comet = Comet(pixels, speed=0.01, color=MAGENTA, tail_length=30)
jade_comet = Comet(pixels, speed=0.01, color=JADE, tail_length=30)
white_comet = Comet(pixels, speed=0.01, color=WHITE, tail_length=30)



# mic configuration
SAMPLERATE = 16000
SAMPLES = 1024
THRESHOLD = 100
MIN_DELTAS = 5
DELAY = 0.01

# variable for audio data input
mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, sample_rate=SAMPLERATE, bit_depth=16)

# variable to create a buffer to record into
samples = array.array('H', [0] * SAMPLES)

# frequency ranges
sub_base = 100
base = 200
lower_midrange = 300
midrange = 400
higher_midrange = 500
presence = 600
brilliance = 700

# remove DC bias before computing RMS.
def mean(values):
    return sum(values) / len(values)


def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )

    return math.sqrt(samples_sum / len(values))

def animation_selector(frequency):
    if freq > brilliance:
        return white_comet.animate()
    elif freq > presence:
        return amber_comet.animate()
    elif freq > higher_midrange:
        return jade_comet.animate()
    elif freq > midrange:
        return teal_comet.animate()
    elif freq > lower_midrange:
        return pink_comet.animate()
    elif freq > base:
        return purple_comet.animate()
    elif freq > sub_base:
        return magenta_comet.animate()


while True:
    # Get raw mic data
    mic.record(samples, SAMPLES)

    # Compute DC offset (mean) and threshold level
    mean = int(sum(samples) / len(samples) + 0.5)
    threshold = mean + THRESHOLD

    # Compute deltas between mean crossing points
    # (this bit by Dan Halbert)
    deltas = []
    last_xing_point = None
    crossed_threshold = False
    for i in range(SAMPLES-1):
        sample = samples[i]
        if sample > threshold:
            crossed_threshold = True
        if crossed_threshold and sample < mean:
            if last_xing_point:
                deltas.append(i - last_xing_point)
            last_xing_point = i
            crossed_threshold = False

    # Try again if not enough deltas
    if len(deltas) < MIN_DELTAS:
        continue

    # Average the deltas
    mean = sum(deltas) / len(deltas)

    # Compute frequency
    freq = SAMPLERATE / mean

    print("crossings: {}  mean: {}  freq: {} ".format(len(deltas), mean, freq))


    if freq > brilliance:
        if not white_comet.animate():
            white_comet.animate()
            print("white_comet")
    elif freq > presence:
        if not amber_comet.animate():
            amber_comet.animate()
            print("amber_comet")
    elif freq > higher_midrange:
        if not jade_comet.animate():
            jade_comet.animate()
            print("jade_comet")
    elif freq > midrange:
        if not teal_comet.animate():
            teal_comet.animate()
            print("teal_comet")
    elif freq > lower_midrange:
        if not pink_comet.animate():
            pink_comet.animate()
            print("pink_comet")
    elif freq > base:
        if not purple_comet.animate():
            purple_comet.animate()
            print("purple_comet")
    elif freq > sub_base:
        if not magenta_comet.animate():
            magenta_comet.animate()
            print("magenta_comet")
