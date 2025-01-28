import re

from wuggy import BaseLanguagePlugin

class LanguagePlugin(BaseLanguagePlugin):
    default_data = 'orthographic_spanish.txt'
    default_neighbor_lexicon = 'orthographic_spanish.txt'
    default_word_lexicon = 'orthographic_spanish.txt'
    default_lookup_lexicon = 'orthographic_spanish.txt'

    double_letters_esp = set(['aa', 'au', 'ai', 'ea', 'ee', 'ia', 'ie', 'io',
                      'oo', 'oe', 'oi', 'ou', 'ui', 'ue', 'ei', 'eu', 'ae', 'oa'])
    
    double_letters_eng = set(['aa', 'ea', 'ee', 'ia', 'ie',
                      'io(?!u)', 'oo', 'oe', 'ou', '(?<!q)ui(?=.)', 'ei', 'eu', 'ae', 'ey(?=.)', 'oa'])

    double_letters = double_letters_esp.intersection(double_letters_eng)
    # Add extra double letters by hand, removing phonology
    double_letters.update(['io', 'ui'])
    double_letters = list(double_letters)

    single_letters = ['a', 'e', 'i', 'o', 'u', 'y']

    accented_letters_esp = set([u'á', u'à', u'ê', u'è', u'é',
                        u'í', u'ó', u'â', u'ô', u'ú', u'ü', u'ö'])
    accented_letters_eng = set([u'à', u'ê', u'è', u'é', u'â', u'ô', u'ü'])

    accented_letters = accented_letters_esp.intersection(accented_letters_eng)
    accented_letters = list(accented_letters)  

    double_letter_pattern = u'|'.join(double_letters)
    single_letter_pattern = u'|'.join(single_letters)
    accented_letter_pattern = u'|'.join(accented_letters)
    nucleuspattern = u'%s|%s|%s' % (
        double_letter_pattern, accented_letter_pattern, single_letter_pattern)
    oncpattern = re.compile(u'(.*?)(%s)(.*)' % nucleuspattern)

    def transform(self, input_sequence, frequency=1):
        return self.pre_transform(input_sequence, frequency=frequency, language=self)