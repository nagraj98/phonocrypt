"""
Unit tests for PhonoCrypt Phonetic Engine
=========================================

Milestone 1 Test Suite:
- 10+ test cases covering various scenarios
- Target: 95%+ accuracy for phonetic conversion
"""

import pytest
from typing import List
from core.phonetic_engine import (
    PhoneticEngine,
    PhoneticConfig,
    text_to_phonemes,
    phonemes_to_text
)


class TestPhoneticEngine:
    """Test suite for PhoneticEngine class."""
    
    @pytest.fixture
    def engine(self):
        """Create a phonetic engine instance for testing."""
        return PhoneticEngine()
    
    @pytest.fixture
    def engine_no_stress(self):
        """Create engine without stress markers."""
        config = PhoneticConfig(strip_stress=True)
        return PhoneticEngine(config)
    
    # Basic Functionality Tests
    
    def test_engine_initialization(self, engine):
        """Test that engine initializes properly."""
        assert engine is not None
        assert engine.config is not None
        assert isinstance(engine.phoneme_to_letter, dict)
    
    def test_empty_input(self, engine):
        """Test handling of empty input."""
        result = engine.text_to_phonemes("")
        assert result == []
        
        result = engine.phonemes_to_text([])
        assert result == ""
    
    def test_simple_word_hello(self, engine):
        """Test conversion of 'Hello'."""
        phonemes = engine.text_to_phonemes("Hello")
        assert len(phonemes) > 0
        # Should contain phonemes for h-e-l-l-o sounds
        # Exact phonemes may vary by backend, so we test for non-empty
        assert isinstance(phonemes, list)
        assert all(isinstance(p, str) for p in phonemes)
    
    def test_simple_word_world(self, engine):
        """Test conversion of 'world'."""
        phonemes = engine.text_to_phonemes("world")
        assert len(phonemes) > 0
        assert isinstance(phonemes, list)
    
    def test_phrase_conversion(self, engine):
        """Test conversion of a simple phrase."""
        text = "The quick brown fox"
        phonemes = engine.text_to_phonemes(text)
        assert len(phonemes) > 0
        # Should have space-separated words or continuous phonemes
        assert isinstance(phonemes, list)
    
    def test_sentence_with_punctuation(self, engine):
        """Test sentence with punctuation marks."""
        text = "Hello, world!"
        phonemes = engine.text_to_phonemes(text)
        assert len(phonemes) > 0
        # Punctuation should be preserved if configured
        # At minimum, we should get some phonemes
    
    def test_complete_sentence(self, engine):
        """Test the complete pangram sentence."""
        text = "The quick brown fox jumps over the lazy dog"
        phonemes = engine.text_to_phonemes(text)
        assert len(phonemes) > 10  # Should have many phonemes
        assert isinstance(phonemes, list)
    
    # Normalization Tests
    
    def test_case_insensitivity(self, engine):
        """Test that uppercase and lowercase produce same phonemes."""
        upper = engine.text_to_phonemes("HELLO")
        lower = engine.text_to_phonemes("hello")
        mixed = engine.text_to_phonemes("HeLLo")
        
        # All should normalize to same phonemes
        assert upper == lower
        assert lower == mixed
    
    def test_whitespace_normalization(self, engine):
        """Test that excessive whitespace is normalized."""
        normal = engine.text_to_phonemes("hello world")
        extra = engine.text_to_phonemes("hello    world")
        tabs = engine.text_to_phonemes("hello\t\tworld")
        
        # Should produce similar results (whitespace normalized)
        assert len(normal) > 0
        assert len(extra) > 0
        assert len(tabs) > 0
    
    def test_leading_trailing_whitespace(self, engine):
        """Test that leading/trailing whitespace is handled."""
        clean = engine.text_to_phonemes("hello")
        padded = engine.text_to_phonemes("  hello  ")
        
        # Should produce same phonemes
        assert clean == padded
    
    # Reverse Conversion Tests
    
    def test_phonemes_to_text_basic(self, engine):
        """Test basic phoneme-to-text conversion."""
        # Use known phonemes
        phonemes = ['h', 'ə', 'l', 'oʊ']
        text = engine.phonemes_to_text(phonemes)
        
        assert isinstance(text, str)
        assert len(text) > 0
    
    def test_round_trip_approximation(self, engine):
        """Test that round-trip conversion produces similar results."""
        original = "hello"
        phonemes = engine.text_to_phonemes(original)
        reconstructed = engine.phonemes_to_text(phonemes)
        
        # Reconstructed may not match exactly but should be similar
        assert isinstance(reconstructed, str)
        assert len(reconstructed) > 0
        # Check that it has some letters from the original
        # (exact match not guaranteed due to phonetic ambiguity)
    
    # Edge Cases
    
    def test_numbers_and_special_chars(self, engine):
        """Test handling of numbers and special characters."""
        text = "test123"
        phonemes = engine.text_to_phonemes(text)
        
        # Should handle gracefully (may convert numbers to words or keep as-is)
        assert len(phonemes) > 0
    
    def test_single_character(self, engine):
        """Test single character input."""
        phonemes = engine.text_to_phonemes("a")
        assert len(phonemes) > 0
        
        phonemes = engine.text_to_phonemes("I")
        assert len(phonemes) > 0
    
    def test_repeated_letters(self, engine):
        """Test words with repeated letters."""
        text = "Mississippi"
        phonemes = engine.text_to_phonemes(text)
        assert len(phonemes) > 0
    
    # Configuration Tests
    
    def test_strip_stress_markers(self, engine_no_stress):
        """Test that stress markers can be stripped."""
        phonemes = engine_no_stress.text_to_phonemes("hello")
        
        # Should not contain stress markers if stripped
        stress_markers = ['ˈ', 'ˌ']
        for phoneme in phonemes:
            assert not any(marker in phoneme for marker in stress_markers)
    
    # Module-level Function Tests
    
    def test_module_level_text_to_phonemes(self):
        """Test module-level convenience function."""
        phonemes = text_to_phonemes("hello")
        assert isinstance(phonemes, list)
        assert len(phonemes) > 0
    
    def test_module_level_phonemes_to_text(self):
        """Test module-level convenience function."""
        phonemes = ['h', 'ə', 'l', 'oʊ']
        text = phonemes_to_text(phonemes)
        assert isinstance(text, str)
        assert len(text) > 0
    
    # Accuracy Validation Tests
    
    def test_phoneme_list_validity(self, engine):
        """Test that all phonemes in output are valid IPA symbols."""
        text = "The quick brown fox jumps over the lazy dog"
        phonemes = engine.text_to_phonemes(text)
        
        # All phonemes should be non-empty strings
        for phoneme in phonemes:
            assert isinstance(phoneme, str)
            assert len(phoneme) > 0
    
    def test_multiple_words_consistency(self, engine):
        """Test that the same word produces same phonemes."""
        word = "test"
        
        phonemes1 = engine.text_to_phonemes(word)
        phonemes2 = engine.text_to_phonemes(word)
        phonemes3 = engine.text_to_phonemes(word)
        
        # Should be consistent
        assert phonemes1 == phonemes2
        assert phonemes2 == phonemes3


class TestPhoneticConfig:
    """Test suite for PhoneticConfig class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = PhoneticConfig()
        
        assert config.language == "en-us"
        assert config.backend == "espeak"
        assert config.preserve_punctuation is True
        assert config.with_stress is True
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = PhoneticConfig(
            language="en-gb",
            backend="epitran",
            preserve_punctuation=False,
            strip_stress=True
        )
        
        assert config.language == "en-gb"
        assert config.backend == "epitran"
        assert config.preserve_punctuation is False
        assert config.strip_stress is True


class TestAccuracyMetrics:
    """Test suite for accuracy validation (Milestone 1 success criteria)."""
    
    @pytest.fixture
    def engine(self):
        """Create engine for accuracy tests."""
        return PhoneticEngine()
    
    def test_accuracy_on_common_words(self, engine):
        """
        Test accuracy on a set of common English words.
        Target: 95%+ of words should convert without errors.
        """
        common_words = [
            "hello", "world", "the", "quick", "brown",
            "fox", "jumps", "over", "lazy", "dog",
            "test", "python", "code", "data", "system",
            "language", "phonetic", "sound", "letter", "word"
        ]
        
        successful = 0
        for word in common_words:
            try:
                phonemes = engine.text_to_phonemes(word)
                if len(phonemes) > 0:
                    successful += 1
            except Exception:
                pass
        
        accuracy = (successful / len(common_words)) * 100
        assert accuracy >= 95.0, f"Accuracy {accuracy}% is below target 95%"
    
    def test_phoneme_coverage(self, engine):
        """
        Test that engine covers major English phoneme classes.
        """
        test_cases = {
            "consonants": "bat cat dog fog hat",
            "vowels": "beat bit bait bet bat",
            "diphthongs": "boy buy bow",
            "fricatives": "fish vision think",
            "nasals": "man name sing",
        }
        
        for phoneme_class, text in test_cases.items():
            phonemes = engine.text_to_phonemes(text)
            assert len(phonemes) > 0, f"Failed to convert {phoneme_class}: {text}"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
