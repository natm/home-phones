#!/usr/bin/env python

# https://en.wikipedia.org/wiki/Telephone_numbers_in_the_United_Kingdom#Format


def evalute_number(dialed):
    """Create a full number from what the user entered."""
    if (len(dialed) == 11 or len(dialed) == 10) and str(dialed).startswith("0"):
        # UK Number
        return "+44%s" % (dialed[1:])
    elif len(dialed) == 6:
        return "+441348%s" % (dialed)
    return ""


class DialHelperEvaluationError(Exception):
    pass
