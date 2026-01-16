"""
PhonoCrypt Core Phonetic Engine
===============================

This module provides the foundational phonetic conversion functionality for PhonoCrypt.
It converts text to International Phonetic Alphabet (IPA) representation and back.

Milestone 1 Deliverables:
- text_to_phonemes(text: str) -> List[str]: Convert text to phoneme list
- phonemes_to_text(phonemes: List[str]) -> str: Convert phonemes back to text

Target accuracy: 95%+ for English text
"""

from typing import List, Optional, Dict
import re
import os
from dataclasses import dataclass

# Set espeak-ng library path for macOS Homebrew installations
# phonemizer needs to find the espeak-ng shared library
if not os.environ.get('PHONEMIZER_ESPEAK_LIBRARY'):
    # Common paths for espeak-ng library
    common_lib_paths = [
        '/opt/homebrew/lib/libespeak-ng.dylib',  # macOS Homebrew (Apple Silicon)
        '/usr/local/lib/libespeak-ng.dylib',      # macOS Homebrew (Intel)
        '/usr/lib/x86_64-linux-gnu/libespeak-ng.so',  # Linux (x86_64)
        '/usr/lib/aarch64-linux-gnu/libespeak-ng.so',  # Linux (ARM64)
        '/usr/lib/libespeak-ng.so',              # Linux (generic)
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
                print(f"Warning: Could not initialize epitran: {e}")
        
        # Create reverse mapping for phoneme-to-text conversion
        self._build_reverse_mapping()
    
    def _build_reverse_mapping(self):
        """
        Build a reverse mapping from common IPA phonemes to English letters.
        This is approximate and used for basic reconstruction.
        """
        # Common English phoneme to letter mappings
        # These are approximations for demonstration purposes
        self.phoneme_to_letter: Dict[str, str] = {
            # Consonants
            'p': 'p', 'b': 'b', 't': 't', 'd': 'd', 'k': 'k', 'g': 'g',
            'f': 'f', 'v': 'v', 'θ': 'th', 'ð': 'th', 's': 's', 'z': 'z',
            'ʃ': 'sh', 'ʒ': 'zh', 'h': 'h', 'm': 'm', 'n': 'n', 'ŋ': 'ng',
            'l': 'l', 'r': 'r', 'w': 'w', 'j': 'y',
            'tʃ': 'ch', 'dʒ': 'j',
            
            # Vowels (monophthongs)
            'i': 'ee', 'ɪ': 'i', 'e': 'e', 'ɛ': 'e', 'æ': 'a',
            'ɑ': 'a', 'ɒ': 'o', 'ɔ': 'o', 'ʊ': 'u', 'u': 'oo',
            'ʌ': 'u', 'ə': 'a', 'ɜ': 'er', 'ɚ': 'er',
            
            # Diphthongs
            'eɪ': 'ay', 'aɪ': 'i', 'ɔɪ': 'oy', 'aʊ': 'ow', 'oʊ': 'o',
            'ɪə': 'ear', 'ɛə': 'air', 'ʊə': 'oor',
            
            # Common symbols
            ' ': ' ', '.': '.', ',': ',', '!': '!', '?': '?',
            ':': '', 'ː': '', 'ˈ': '', 'ˌ': '',  # Stress markers (ignored)
        }
    
    def text_to_phonemes(self, text: str) -> List[str]:
        """
        Convert text to a list of phonemes (IPA representation).
        
        This function:
        1. Normalizes the input text (lowercase, basic cleanup)
        2. Converts to IPA using espeak-ng backend
        3. Splits into individual phoneme units
        4. Returns as a list for further processing
        
        Args:
            text: Input text to convert to phonemes
            
        Returns:
            List of phoneme strings representing the input text
            
        Examples:
            >>> engine = PhoneticEngine()
            >>> engine.text_to_phonemes("Hello")
            ['h', 'ə', 'l', 'oʊ']
            >>> engine.text_to_phonemes("world")
            ['w', 'ɜː', 'l', 'd']
        """
        if not text:
            return []
        
        # Normalize text
        normalized_text = self._normalize_text(text)
        
        # Convert using primary backend (phonemizer)
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
                
                # Parse IPA into phoneme list
                phonemes = self._parse_ipa_to_phonemes(ipa)
                return phonemes
                
            except Exception as e:
                print(f"Warning: phonemizer failed: {e}, trying fallback")
        
        # Fallback to epitran
        if self.epitran_translator:
            try:
                ipa = self.epitran_translator.transliterate(normalized_text)
                phonemes = self._parse_ipa_to_phonemes(ipa)
                return phonemes
            except Exception as e:
                print(f"Warning: epitran failed: {e}")
        
        # Ultimate fallback: character-level representation
        print("Warning: Using character-level fallback (no phonetic backend available)")
        return list(normalized_text)
    
    def _normalize_text(self, text: str) -> str:
        """
        Normalize text before phonetic conversion.
        
        Args:
            text: Raw input text
            
        Returns:
            Normalized text ready for phonetic conversion
        """
        # Convert to lowercase for consistent processing
        text = text.lower()
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def _parse_ipa_to_phonemes(self, ipa: str) -> List[str]:
        """
        Parse IPA string into individual phoneme units.
        
        This handles:
        - Multi-character phonemes (tʃ, dʒ, etc.)
        - Diphthongs (eɪ, aɪ, etc.)
        - Stress markers (ˈ, ˌ)
        - Length markers (ː)
        
        Args:
            ipa: IPA string from phonemizer
            
        Returns:
            List of phoneme units
        """
        phonemes = []
        i = 0
        
        # Multi-character phonemes to check first
        multi_char_phonemes = [
            'tʃ', 'dʒ', 'eɪ', 'aɪ', 'ɔɪ', 'aʊ', 'oʊ', 'ɪə', 'ɛə', 'ʊə',
            'ɜː', 'iː', 'uː', 'ɑː', 'ɔː'
        ]
        
        while i < len(ipa):
            # Check for multi-character phonemes
            matched = False
            for mc_phoneme in multi_char_phonemes:
                if ipa[i:i+len(mc_phoneme)] == mc_phoneme:
                    phonemes.append(mc_phoneme)
                    i += len(mc_phoneme)
                    matched = True
                    break
            
            if not matched:
                # Single character phoneme or symbol
                char = ipa[i]
                
                # Skip stress markers if configured
                if self.config.strip_stress and char in ['ˈ', 'ˌ']:
                    i += 1
                    continue
                
                # Handle length marker (combine with previous phoneme)
                if char == 'ː' and phonemes:
                    phonemes[-1] = phonemes[-1] + 'ː'
                else:
                    phonemes.append(char)
                
                i += 1
        
        return phonemes
    
    def phonemes_to_text(self, phonemes: List[str]) -> str:
        """
        Convert a list of phonemes back to approximate text representation.
        
        Note: This is an approximation and may not perfectly reconstruct
        the original text, especially for homophones. The accuracy depends
        on the phoneme-to-letter mapping quality.
        
        Args:
            phonemes: List of IPA phonemes
            
        Returns:
            Reconstructed text string
            
        Examples:
            >>> engine = PhoneticEngine()
            >>> engine.phonemes_to_text(['h', 'ə', 'l', 'oʊ'])
            'halo'
            >>> engine.phonemes_to_text(['w', 'ɜː', 'l', 'd'])
            'werld'
        """
        if not phonemes:
            return ""
        
        # Convert each phoneme to its letter representation
        text_parts = []
        for phoneme in phonemes:
            # Clean phoneme (remove stress/length markers for lookup)
            clean_phoneme = phoneme.replace('ˈ', '').replace('ˌ', '').replace('ː', '')
            
            # Look up in mapping
            if clean_phoneme in self.phoneme_to_letter:
                text_parts.append(self.phoneme_to_letter[clean_phoneme])
            else:
                # Unknown phoneme - use as-is or placeholder
                text_parts.append(phoneme)
        
        # Join and return
        reconstructed = ''.join(text_parts)
        return reconstructed


# Convenience functions for module-level access
_default_engine: Optional[PhoneticEngine] = None


def get_default_engine() -> PhoneticEngine:
    """Get or create the default phonetic engine instance."""
    global _default_engine
    if _default_engine is None:
        _default_engine = PhoneticEngine()
    return _default_engine


def text_to_phonemes(text: str) -> List[str]:
    """
    Convert text to phonemes using the default engine.
    
    Args:
        text: Input text
        
    Returns:
        List of phoneme strings
    """
    engine = get_default_engine()
    return engine.text_to_phonemes(text)


def phonemes_to_text(phonemes: List[str]) -> str:
    """
    Convert phonemes to text using the default engine.
    
    Args:
        phonemes: List of phoneme strings
        
    Returns:
        Reconstructed text
    """
    engine = get_default_engine()
    return engine.phonemes_to_text(phonemes)


if __name__ == "__main__":
    # Quick test
    engine = PhoneticEngine()
    
    test_words = [
        "Hello",
        "world",
        "The quick brown fox",
        "jumps over the lazy dog"
    ]
    
    print("PhonoCrypt Phonetic Engine - Quick Test\n")
    print("=" * 60)
    
    for word in test_words:
        phonemes = engine.text_to_phonemes(word)
        reconstructed = engine.phonemes_to_text(phonemes)
        
        print(f"\nOriginal:      {word}")
        print(f"Phonemes:      {phonemes}")
        print(f"Reconstructed: {reconstructed}")
        print("-" * 60)
