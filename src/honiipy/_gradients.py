"""gradient ramps and styles for the shading engine."""

# dark -> light, four ramps (finest to coarsest). the trailing double space is
# deliberate: the two brightest buckets both map to blank.
GRADIENTS = [
    list("@%8#$VYx*=+:~-.  "),
    list("8Oo:.  "),
    list("#+:  "),
    list("01  "),
]

STYLES = ("relative", "one_to_one")

# pillow "L" intensity is 0-255.
ONE_TO_ONE_MAX = 255
