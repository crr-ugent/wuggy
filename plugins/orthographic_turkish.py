# orthographic Turkish
public_name='Orthographic Turkish'
default_data='orthographic_turkish.txt'
default_neighbor_lexicon='orthographic_turkish.txt'
default_word_lexicon='orthographic_turkish.txt'
default_lookup_lexicon='orthographic_turkish.txt'
from subsyllabic_common import *
import orth.tr as language
def transform(input_sequence, frequency=1):
    return pre_transform(input_sequence, frequency=frequency, language=language)
