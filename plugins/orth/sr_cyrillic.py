#encoding: utf-8

import re

single_vowels=['a', 'e', 'и', 'o', 'u', 'р']
nucleuspattern = '%s' % (single_vowels)
oncpattern=re.compile('(.*?)(%s)(.*)' % nucleuspattern)
