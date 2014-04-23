# Orthographic Vietnamese
public_name='Orthographic Vietnamese'
default_data='orthographic_vietnamese.txt'
default_neighbor_lexicon='orthographic_vietnamese.txt'
default_word_lexicon='orthographic_vietnamese.txt'
default_lookup_lexicon='orthographic_vietnamese.txt'
from subsyllabic_common import *
import orth.vi as language
import segment
segment_function=segment.start_peak_end
def transform(input_sequence, frequency=1):
    return pre_transform(input_sequence, frequency=frequency, language=language)
