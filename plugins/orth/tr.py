#encoding: utf-8

import re

single_letters=['a', 'e', 'i', 'o', 'u']
accented_letters=[u'â', u'ü', u'ö', u'ı', u'î']
single_letter_pattern='|'.join(single_letters)
accented_letter_pattern='|'.join(accented_letters)
nucleuspattern = '%s|%s' % (accented_letter_pattern, single_letter_pattern)
oncpattern=re.compile('(.*?)(%s)(.*)' % nucleuspattern)
    