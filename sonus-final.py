import board
import neopixel
import time
import audiobusio
import math
import array
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import (
    PURPLE,
    WHITE,
    AMBER,
    JADE,
    TEAL,
    BLUE,
    PINK,
    GOLD,
    YELLOW,
    MAGENTA,
    CYAN,
    AQUA,
    OLD_LACE,
    ORANGE,
)


# variable for neopixel input
strip1 = board.A1
strip2 = board.A2
strip3 = board.A3
strip4 = board.A4
strip5 = board.A5
strip6 = board.A6


# variable for number of NeoPixels
num_pixels = 30


# variable for the order of the pixel colors
ORDER = neopixel.RGBW

# variable for NeoPixels output
pixels = neopixel.NeoPixel(
    strip1, num_pixels, brightness=1, auto_write=False,
)

pixels2 = neopixel.NeoPixel(
    strip2, num_pixels, brightness=1, auto_write=False,
)

pixels3 = neopixel.NeoPixel(
    strip3, num_pixels, brightness=1, auto_write=False,
)

pixels4 = neopixel.NeoPixel(
    strip4, num_pixels, brightness=1, auto_write=False,
)

pixels5 = neopixel.NeoPixel(
    strip5, num_pixels, brightness=1, auto_write=False,
)

pixels6 = neopixel.NeoPixel(
    strip6, num_pixels, brightness=1, auto_write=False,
)


# variable for animation
aqua_comet = Sparkle(pixels, speed=0.01, color=AQUA, num_sparkles=10)
pink_comet = Sparkle(pixels2, speed=0.05, color=PINK, num_sparkles=10)
white_comet = Sparkle(pixels3, speed=0.05, color=WHITE, num_sparkles=10)
aqua_comet2 = Sparkle(pixels4, speed=0.05, color=AQUA, num_sparkles=10)
pink_comet2 = Sparkle(pixels5, speed=0.05, color=PINK, num_sparkles=10)
aqua_comet3 = Sparkle(pixels6, speed=0.05, color=AQUA, num_sparkles=10)

# mic configuration
SAMPLERATE = 16000
SAMPLES = 1024
THRESHOLD = 100
MIN_DELTAS = 10
DELAY = 0.01

# variable for audio data input
mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, sample_rate=SAMPLERATE, bit_depth=16)

# variable to create a buffer to record into
samples = array.array('H', [0] * SAMPLES)

# frequency ranges
sub_base = 100
midrange = 400
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
        white_comet.animate()


    elif freq > midrange:
        aqua_comet.animate()
        aqua_comet2.animate()
        aqua_comet3.animate()

    elif freq > sub_base:
        pink_comet.animate()
        pink_comet2.animate()

