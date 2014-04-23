# encoding: utf-8

from collections import *

class Error(Exception):
    """Base class for Exceptions in this module"""
    pass

class SegmentationError(Error):
    """Occurs when an input string cannot be segmented"""
    pass        


def onset_nucleus_coda(orthographic_syllable, lang=None):
    oncpattern=lang.oncpattern
    m=oncpattern.match(orthographic_syllable)
    try:
        return [m.group(1), m.group(2), m.group(3)]
    except AttributeError:
        raise SegmentationError('Input syllable could not be segmented')

def start_peak_end(orthographic_syllable, lang=None):
    oncpattern=lang.oncpattern
    m=oncpattern.match(orthographic_syllable)
    try:
        onset, nucleus, coda=m.group(1), m.group(2), m.group(3)
    except AttributeError:
        raise SegmentationError('Input syllable could not be segmented')
    peak=nucleus
    start=onset if onset!=u"" else u'>'+peak
    end=coda if coda!=u"" else u'<'+peak
    return [start, peak, end]

