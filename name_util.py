# -*- coding: utf-8 -*-
import re
#import Levenshtein #pip: python-levenshtein


_LONG_SHORT_VOWEL_PAIRS = tuple(
    zip(
        u'íóőúű',
        u'ioöuü'))


def weak_vowel_shorten(ustring):
    """ Replaces long hungarian vowels with their short pairs, weak because it
    ignores short variants with changing vowel quality (á->a, é->e) """
    for long, short in _LONG_SHORT_VOWEL_PAIRS:
        ustring = ustring.replace(long, short)
    return ustring.lower()

'''
def match_levenshtein(instring1, instring2):
    string1 = weak_vowel_shorten(instring1.lower())
    string2 = weak_vowel_shorten(instring2.lower())
    return (Levenshtein.jaro_winkler(string1, string2) > 0.9
            or Levenshtein.ratio(string1, string2) > 0.8
            or Levenshtein.distance(string1, string2) == 1)
'''

def clean_name(name):
    name = name.strip()
    match = re.match('\A[0-9\-]+\s+(.*)\Z', name)
    if match:
        name = match.group(1)
    match = re.match('\A(.*)\s+[0-9\-]+\Z', name)
    if match:
        name = match.group(1)
    return name.strip()


if __name__ == '__main__':
    assert(clean_name('12 Hello Bello') == 'Hello Bello')
    assert(clean_name('Hello Bello 12') == 'Hello Bello')
    assert(clean_name('-1   Bots Lászlóné') == 'Bots Lászlóné')
    assert(clean_name(' Bots Lászlóné  -1') == 'Bots Lászlóné')