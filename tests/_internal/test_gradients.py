"""the gradient ramps and styles the shading engine indexes into."""

from honiipy._internal.gradients import GRADIENTS, ONE_TO_ONE_MAX, STYLES


def test_four_ramps_ordered_finest_to_coarsest():
    assert len(GRADIENTS) == 4
    lengths = [len(ramp) for ramp in GRADIENTS]
    assert lengths == sorted(lengths, reverse=True)  # gradient 0 is the finest


def test_every_ramp_runs_dark_to_light_ending_in_two_blanks():
    for ramp in GRADIENTS:
        # the trailing double space is deliberate: the two brightest buckets
        # both map to blank, so the lightest end of an image reads as empty.
        assert ramp[-2:] == [" ", " "]
        assert ramp[0] != " "


def test_styles_are_the_two_the_engine_accepts():
    assert STYLES == ("relative", "one_to_one")


def test_one_to_one_max_is_pillow_l_range():
    assert ONE_TO_ONE_MAX == 255
