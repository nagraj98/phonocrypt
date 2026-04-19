# Complete corrected mapping + assembler

IPA_TO_DEVANAGARI = {
    # stress markers → strip
    'ˈ': '', 'ˌ': '',

    # affricates first (2-char)
    'dʒ': ('ज', 'C'),
    'tʃ': ('च', 'C'),

    # diphthongs first (2-char vowels)
    'aʊ': ('आउ', 'V', 'ाउ'),
    'aɪ': ('आइ', 'V', 'ाइ'),
    'oʊ': ('ओ',  'V', 'ो'),
    'eɪ': ('ए',  'V', 'े'),
    'ɔɪ': ('ओइ','V', 'ोइ'),

    # long vowels (2-char)
    'iː': ('ई', 'V', 'ी'),
    'ɑː': ('आ', 'V', 'ा'),
    'ɔː': ('ओ', 'V', 'ो'),
    'uː': ('ऊ', 'V', 'ू'),
    'ɜː': ('अर','V', 'अर'),  # British 'er' — no clean matra

    # single vowels
    'ɪ': ('इ', 'V', 'ि'),
    'æ': ('ए', 'V', 'े'),
    'ʌ': None,               # mid-central → inherent अ, write nothing as matra
    'ə': None,               # schwa → inherent अ, write nothing as matra
    'ɚ': ('अर','V', 'र'),    # r-colored schwa: consonant gets ् + र appended
    'ʊ': ('उ', 'V', 'ु'),
    'e': ('ए', 'V', 'े'),
    'i': ('ई', 'V', 'ी'),
    'u': ('ऊ', 'V', 'ू'),
    'a': ('आ', 'V', 'ा'),
    'o': ('ओ', 'V', 'ो'),

    'ɔ':  ('ऑ', 'V', 'ॉ'),   # American short-o (song, lot, hot)
    'ɒ': ('ऑ', 'V', 'ॉ'),   # British short-o (dog, fox, hot)

    # consonants → (standalone, type)  [no matra field needed]
    'ð': ('द', 'C'),
    'θ': ('थ', 'C'),
    'ŋ': ('ङ', 'C'),
    'ʃ': ('श', 'C'),
    'ʒ': ('ज़','C'),
    'ɹ': ('र', 'C'),
    'j': ('य', 'C'),
    'p': ('प', 'C'),
    'b': ('ब', 'C'),
    't': ('ट', 'C'),
    'd': ('ड', 'C'),
    'k': ('क', 'C'),
    'ɡ': ('ग', 'C'),
    'f': ('फ़','C'),
    'v': ('व', 'C'),
    's': ('स', 'C'),
    'z': ('ज़','C'),
    'h': ('ह', 'C'),
    'm': ('म', 'C'),
    'n': ('न', 'C'),
    'l': ('ल', 'C'),
    'r': ('र', 'C'),
    'w': ('व', 'C'),
}

HALANT = '्'  # Devanagari halant character to suppress inherent vowel