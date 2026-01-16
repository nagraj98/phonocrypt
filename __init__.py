"""PhonoCrypt - Phonetic Encryption Engine"""

__version__ = "0.1.0"
__author__ = "Nagraj Deshmukh"
__description__ = "A novel encryption engine leveraging phonetic script consistency"

from core import (
    PhoneticEngine,
    PhoneticConfig,
    text_to_phonemes,
    phonemes_to_text
)

__all__ = [
    'PhoneticEngine',
    'PhoneticConfig',
    'text_to_phonemes',
    'phonemes_to_text',
]
