"""
PhonoCrypt Core Phonetic Engine
===============================

This module provides the foundational phonetic conversion functionality for PhonoCrypt.
It converts text to International Phonetic Alphabet (IPA) representation.

Milestone 1 Deliverables:
- text_to_ipa(text: str) -> str: Convert text to raw IPA string
- text_to_words(text: str) -> List[str]: Split text into words
- text_to_phonemes(text: str) -> List[str]: Convert text to phoneme list

Target accuracy: 95%+ for English text
"""

from enum import Enum
from typing import List, Optional, Dict
import re
import os
import re
from dataclasses import dataclass

from core.mappings import IPA_TO_DEVANAGARI, HALANT

# Set espeak-ng library path for macOS Homebrew installations
# phonemizer needs to find the espeak-ng shared library
if not os.environ.get('PHONEMIZER_ESPEAK_LIBRARY'):
    common_lib_paths = [
        '/opt/homebrew/lib/libespeak-ng.dylib',  # macOS Homebrew (Apple Silicon)
        '/usr/local/lib/libespeak-ng.dylib',      # macOS Homebrew (Intel)
        '/usr/lib/x86_64-linux-gnu/libespeak-ng.so',  # Linux (x86_64)
        '/usr/lib/aarch64-linux-gnu/libespeak-ng.so',  # Linux (ARM64)
        '/usr/lib/libespeak-ng.so',               # Linux (generic)
    ]
    for path in common_lib_paths:
        if os.path.exists(path):
            os.environ['PHONEMIZER_ESPEAK_LIBRARY'] = path
            break

try:
    from phonemizer import phonemize
    from phonemizer.backend import EspeakBackend
    PHONEMIZER_AVAILABLE = True
except ImportError:
    PHONEMIZER_AVAILABLE = False
    print("Warning: phonemizer not available. Install with: pip install phonemizer")

try:
    import epitran
    EPITRAN_AVAILABLE = True
except ImportError:
    EPITRAN_AVAILABLE = False
    print("Warning: epitran not available. Install with: pip install epitran")


@dataclass
class PhoneticConfig:
    """Configuration for phonetic conversion"""
    language: str = "en-us"
    backend: str = "espeak"  # or "epitran"
    preserve_punctuation: bool = True
    strip_stress: bool = False
    with_stress: bool = True


class Script(Enum):
    SANSKRIT = "sanskrit"
    HINDI    = "hindi"
    MARATHI  = "marathi"  # same as hindi for this purpose


class PhoneticEngine:
    """
    Core engine for converting text to phonetic representation and back.

    Uses espeak-ng backend via phonemizer library for IPA conversion.
    Provides fallback mechanisms for robustness.
    """

    def __init__(self, config: Optional[PhoneticConfig] = None):
        """
        Initialize the phonetic engine.

        Args:
            config: Optional configuration for phonetic processing
        """
        self.config = config or PhoneticConfig()

        # Initialize backend
        if PHONEMIZER_AVAILABLE and self.config.backend == "espeak":
            try:
                self.backend = EspeakBackend(
                    self.config.language,
                    with_stress=self.config.with_stress
                )
                self.backend_available = True
            except Exception as e:
                print(f"Warning: Could not initialize espeak backend: {e}")
                self.backend_available = False
        else:
            self.backend_available = False

        # Initialize epitran as fallback
        self.epitran_translator = None
        if EPITRAN_AVAILABLE:
            try:
                self.epitran_translator = epitran.Epitran('eng-Latn')
            except Exception as e:
                print(f"Warning: Could not initialize epitran translator: {e}")

        # Phoneme-to-approximate-letter mapping for reverse conversion
        self.phoneme_to_letter: Dict[str, str] = {
            # Vowels
            'iː': 'ee', 'ɪ': 'i', 'e': 'e', 'ɛ': 'e', 'æ': 'a',
            'ɑː': 'ah', 'ɒ': 'o', 'ɔː': 'aw', 'ʊ': 'oo', 'uː': 'oo',
            'ʌ': 'u', 'ɜː': 'er', 'ə': 'e',
            # Diphthongs
            'eɪ': 'ay', 'aɪ': 'i', 'ɔɪ': 'oy', 'aʊ': 'ow', 'oʊ': 'o',
            'ɪə': 'ear', 'ɛə': 'air', 'ʊə': 'oor',
            # Consonants - plosives
            'p': 'p', 'b': 'b', 't': 't', 'd': 'd', 'k': 'k', 'g': 'g',
            # Consonants - affricates
            'tʃ': 'ch', 'dʒ': 'j',
            # Consonants - fricatives
            'f': 'f', 'v': 'v', 'θ': 'th', 'ð': 'th',
            's': 's', 'z': 'z', 'ʃ': 'sh', 'ʒ': 'zh', 'h': 'h',
            # Consonants - nasals and approximants
            'm': 'm', 'n': 'n', 'ŋ': 'ng',
            'l': 'l', 'r': 'r', 'j': 'y', 'w': 'w',
        }

    def text_to_ipa(self, text: str) -> str:
        """
        Convert text to raw IPA string (step 1).

        This is the first step in the conversion pipeline. It converts
        normalized text directly to IPA representation without parsing.

        Args:
            text: Input text to convert

        Returns:
            IPA string representation

        Examples:
            >>> engine = PhoneticEngine()
            >>> engine.text_to_ipa("hello")
            'həˈloʊ'
        """
        if not text:
            return ""

        normalized_text = self._normalize_text(text)

        if self.backend_available:
            try:
                ipa = phonemize(
                    normalized_text,
                    language=self.config.language,
                    backend='espeak',
                    strip=True,
                    preserve_punctuation=self.config.preserve_punctuation,
                    with_stress=self.config.with_stress
                )
                return ipa
            except Exception as e:
                print(f"Warning: phonemizer failed: {e}, trying fallback")

        if self.epitran_translator:
            try:
                ipa = self.epitran_translator.transliterate(normalized_text)
                return ipa
            except Exception as e:
                print(f"Warning: epitran failed: {e}")

        print("Warning: Using fallback (no phonetic backend available)")
        return normalized_text

    def text_to_words(self, text: str) -> List[str]:
        """
        Split text into words (step 2).

        This preserves punctuation as separate tokens.

        Args:
            text: Input text

        Returns:
            List of words and punctuation tokens

        Examples:
            >>> engine = PhoneticEngine()
            >>> engine.text_to_words("Hello, world!")
            ['Hello', ',', 'world', '!']
        """
        if not text:
            return []
        tokens = re.findall(r'\w+|[^\w\s]', text)
        return tokens

    def text_to_phonemes(self, text: str) -> List[str]:
        """
        Convert text to a list of phonemes (step 3 - complete pipeline).

        This function:
        1. Normalizes the input text (lowercase, basic cleanup)
        2. Converts to IPA using espeak-ng backend
        3. Parses IPA into individual phoneme units
        4. Returns as a list for further processing

        Args:
            text: Input text to convert to phonemes

        Returns:
            List of phoneme strings representing the input text

        Examples:
            >>> engine = PhoneticEngine()
            >>> engine.text_to_phonemes("Hello")
            ['h', 'ə', 'ˈ', 'l', 'oʊ']
            >>> engine.text_to_phonemes("world")
            ['w', 'ˈ', 'ɜː', 'l', 'd']
        """
        if not text:
            return []
        ipa = self.text_to_ipa(text)
        return self._parse_ipa_to_phonemes(ipa)

    def _parse_ipa_to_phonemes(self, ipa: str) -> List[str]:
        """
        Parse an IPA string into a list of individual phoneme units.

        Handles multi-character phonemes (diphthongs, long vowels, affricates)
        before falling back to single characters.

        Args:
            ipa: IPA string from phonemizer

        Returns:
            List of phoneme units
        """
        phonemes = []
        i = 0

        # Multi-character phonemes checked first (longest-match priority)
        multi_char_phonemes = [
            'tʃ', 'dʒ', 'eɪ', 'aɪ', 'ɔɪ', 'aʊ', 'oʊ',
            'ɪə', 'ɛə', 'ʊə',
            'ɜː', 'iː', 'uː', 'ɑː', 'ɔː'
        ]

        while i < len(ipa):
            matched = False
            for mc in multi_char_phonemes:
                if ipa[i:i + len(mc)] == mc:
                    phonemes.append(mc)
                    i += len(mc)
                    matched = True
                    break
            if not matched:
                char = ipa[i]
                if self.config.strip_stress and char in ('ˈ', 'ˌ'):
                    i += 1
                else:
                    phonemes.append(char)
                    i += 1

        return phonemes

    def _normalize_text(self, text: str) -> str:
        """
        Normalize input text for consistent phonetic conversion.

        Converts to lowercase and normalizes whitespace.

        Args:
            text: Raw input text

        Returns:
            Normalized text string
        """
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def phonemes_to_text(self, phonemes: List[str]) -> str:
        """
        Convert a list of phonemes back to approximate text (reverse conversion).

        Uses a phoneme-to-letter mapping to reconstruct approximate spelling.
        Note: This is a lossy approximation; perfect reconstruction is not possible.

        Args:
            phonemes: List of IPA phoneme strings

        Returns:
            Reconstructed approximate text
        """
        parts = []
        for phoneme in phonemes:
            clean = phoneme.replace('ˈ', '').replace('ˌ', '').replace('ː', '')
            if clean in self.phoneme_to_letter:
                parts.append(self.phoneme_to_letter[clean])
            else:
                parts.append(phoneme)
        return ''.join(parts)
    

    def ipa_word_to_devanagari_sanskrit(ipa_word: str) -> str:
        """
        Sanskrit logic:
        - Every consonant is written with halant by default
        - Halant is removed (replaced by matra) only when an explicit vowel follows
        - ə / ʌ are EXPLICIT vowels — they produce the 'a' matra (ा) or inherent form
        """
        HALANT = '्'
        
        tokens = []
        i = 0
        while i < len(ipa_word):
            matched = False
            for length in (2, 1):
                chunk = ipa_word[i:i+length]
                if chunk in IPA_TO_DEVANAGARI:
                    entry = IPA_TO_DEVANAGARI[chunk]
                    if entry != '':
                        tokens.append((chunk, entry))
                    i += length
                    matched = True
                    break
            if not matched:
                i += 1

        result = []

        for idx, (ipa_char, entry) in enumerate(tokens):

            # Look ahead: is the next token a vowel?
            next_entry = tokens[idx + 1][1] if idx + 1 < len(tokens) else None
            next_is_vowel = next_entry is not None and (
                next_entry is None or  # won't hit
                (isinstance(next_entry, tuple) and next_entry[1] == 'V')
                or next_entry is None  # inherent schwa
            )
            # cleaner lookahead
            if idx + 1 < len(tokens):
                ne = tokens[idx + 1][1]
                next_is_vowel = (ne is None) or (isinstance(ne, tuple) and ne[1] == 'V')
            else:
                next_is_vowel = False

            if entry is None:
                # ə or ʌ — explicit 'a' vowel
                # Previous consonant already written with halant — replace it with inherent a
                # i.e. just remove the last halant from result
                if result and result[-1] == HALANT:
                    result.pop()   # remove halant → consonant now has inherent 'a'
                else:
                    result.append('अ')  # vowel-initial or after another vowel
            
            elif entry[1] == 'C':
                char = entry[0]
                result.append(char)
                result.append(HALANT)  # always add halant — vowel will remove it if needed

            elif entry[1] == 'V':
                standalone = entry[0]
                matra = entry[2]
                if result and result[-1] == HALANT:
                    result.pop()        # remove halant from preceding consonant
                    result.append(matra)  # attach matra instead
                else:
                    result.append(standalone)  # word-initial vowel, no preceding consonant

            print(f"Token: {ipa_char} → {entry}, Result so far: {''.join(result)}")

        return ''.join(result)


    
    def ipa_word_to_devanagari(self, ipa_word: str, script: Script = Script.SANSKRIT, verbose: bool = False) -> str:
        HALANT = '्'

        tokens = []
        i = 0
        while i < len(ipa_word):
            matched = False
            for length in (2, 1):
                chunk = ipa_word[i:i+length]
                if chunk in IPA_TO_DEVANAGARI:
                    entry = IPA_TO_DEVANAGARI[chunk]
                    if entry != '':
                        tokens.append((chunk, entry))
                    i += length
                    matched = True
                    break
            if not matched:
                if verbose:
                    print(f"Warning: Unrecognized IPA symbol '{ipa_word[i]}' at position {i} in '{ipa_word}'")
                i += 1

        result = []

        for idx, (ipa_char, entry) in enumerate(tokens):

            if entry is None:
                # ə or ʌ — explicit 'a' vowel
                if result and result[-1] == HALANT:
                    result.pop()   # remove halant → inherent a
                else:
                    result.append('अ')

            elif entry[1] == 'C':
                result.append(entry[0])
                result.append(HALANT)  # always halant — vowel will pop it if needed

            elif entry[1] == 'V':
                if result and result[-1] == HALANT:
                    result.pop()
                    result.append(entry[2])   # matra
                else:
                    result.append(entry[0])   # standalone

            if verbose:
                print(f"Token: {ipa_char} → {entry}, Result so far: {''.join(result)}")

        # ── The one difference between scripts ──────────────────────────────
        # Sanskrit: word-final halant stays   → क्विक्
        # Hindi/Marathi: word-final halant dropped → क्विक
        if script in (Script.HINDI, Script.MARATHI):
            if result and result[-1] == HALANT:
                result.pop()

        return ''.join(result)
                

    def english_word_to_devanagari(self, word: str, script: Script = Script.SANSKRIT, verbose: bool = False) -> str:
        """Convert English word to Devanagari script via IPA."""
        ipa = self.text_to_ipa(word)
        ipa = self.normalize_ipa(ipa)
        return self.ipa_word_to_devanagari(ipa, script=script, verbose=verbose)
    

    def english_to_devanagari(self, text: str, script: Script = Script.SANSKRIT, verbose: bool = False) -> str:
        """Convert English text to Devanagari script via IPA."""
        words = self.text_to_words(text)
        devanagari_words = [self.english_word_to_devanagari(w, script=script, verbose=verbose) for w in words]
        return ' '.join(devanagari_words)


    def normalize_ipa(self, ipa_string: str) -> str:
        """
        Normalize IPA string for consistent processing.

        Specifically, convert final 'ŋ' to 'ŋɡ' when it appears at the end of a word. for example for 'song'
        This is to handle cases where espeak-ng may produce 'ŋ' for the 'ng' sound.
        """

        ipa_string = re.sub(r'ŋ(\s|$)', r'ŋɡ\1', ipa_string)
        return ipa_string


# Convenience functions for module-level access
_default_engine: Optional[PhoneticEngine] = None


def get_default_engine() -> PhoneticEngine:
    """Get or create the default phonetic engine instance."""
    global _default_engine
    if _default_engine is None:
        _default_engine = PhoneticEngine()
    return _default_engine


def text_to_ipa(text: str) -> str:
    """Convert text to raw IPA using the default engine."""
    return get_default_engine().text_to_ipa(text)


def text_to_words(text: str) -> List[str]:
    """Split text into words using the default engine."""
    return get_default_engine().text_to_words(text)


def text_to_phonemes(text: str) -> List[str]:
    """Convert text to phonemes using the default engine."""
    return get_default_engine().text_to_phonemes(text)


def phonemes_to_text(phonemes: List[str]) -> str:
    """Convert phonemes back to approximate text using the default engine."""
    return get_default_engine().phonemes_to_text(phonemes)
