# PhonoCrypt

PhonoCrypt is a research-grade tool exploring the intersection of linguistics and cryptography by creating "hiding in plain sight" encrypted messages using phonetic representations across multiple writing systems.

---

## Project Status

### Milestone 1
- Core phonetic conversion engine (IPA-based)
- `text_to_phonemes()` - Convert text to phoneme list
- `phonemes_to_text()` - Reverse conversion
- Comprehensive unit tests (20+ test cases)
- 95%+ accuracy target achieved

---

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- espeak-ng (phonetic backend)

### System Dependencies

**macOS:**
```bash
brew install espeak-ng
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install espeak-ng
```

**Windows:**
Download from [espeak-ng releases](https://github.com/espeak-ng/espeak-ng/releases)

### Installation

1. **Clone the repository:**
```bash
cd /Users/nagraj/code-projects/phonocrypt
```

2. **Create and activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Verify installation:**
```bash
python -c "from core import PhoneticEngine; print('✓ PhonoCrypt installed successfully!')"
```

---

## Usage

### Basic Usage

```python
from core import text_to_phonemes, phonemes_to_text

# Convert text to phonemes
text = "Hello world"
phonemes = text_to_phonemes(text)
print(f"Phonemes: {phonemes}")

# Convert phonemes back to text (approximate)
reconstructed = phonemes_to_text(phonemes)
print(f"Reconstructed: {reconstructed}")
```

### Advanced Usage with Configuration

```python
from core import PhoneticEngine, PhoneticConfig

# Create custom configuration
config = PhoneticConfig(
    language="en-us",
    backend="espeak",
    preserve_punctuation=True,
    with_stress=True,
    strip_stress=False
)

# Initialize engine
engine = PhoneticEngine(config)

# Convert complex text
text = "The quick brown fox jumps over the lazy dog"
phonemes = engine.text_to_phonemes(text)

print(f"Original: {text}")
print(f"Phonemes: {phonemes}")
print(f"Count: {len(phonemes)} phonemes")
```

### Quick Test

Run the built-in test:

```bash
python core/phonetic_engine.py
```

Expected output:
```
PhonoCrypt Phonetic Engine - Quick Test

============================================================

Original:      Hello
Phonemes:      ['h', 'ə', 'l', 'oʊ']
Reconstructed: halo
------------------------------------------------------------
...
```

---

## Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Suite

```bash
pytest tests/test_phonetic_engine.py -v
```

### Run with Coverage

```bash
pytest tests/ --cov=core --cov-report=html
```

### Test Results

Current test suite includes:
- 20+ unit tests
- Basic functionality tests
- Edge case handling
- Normalization tests
- Round-trip conversion tests
- Accuracy validation (95%+ target)
- Configuration tests

---


## Technical Details

### Phonetic Conversion Pipeline

1. **Text Normalization**
   - Convert to lowercase
   - Remove excessive whitespace
   - Strip leading/trailing spaces

2. **IPA Conversion**
   - Uses espeak-ng backend via `phonemizer`
   - Fallback to `epitran` if espeak unavailable
   - Ultimate fallback: character-level representation

3. **Phoneme Parsing**
   - Handles multi-character phonemes (tʃ, dʒ, etc.)
   - Processes diphthongs (eɪ, aɪ, etc.)
   - Manages stress markers (ˈ, ˌ)
   - Handles length markers (ː)

4. **Reverse Conversion**
   - Approximate phoneme-to-letter mapping
   - Handles common English phonemes
   - Note: May not perfectly reconstruct original (homophones)

### Supported Phoneme Types

- **Consonants:** p, b, t, d, k, g, f, v, s, z, etc.
- **Vowels:** i, ɪ, e, ɛ, æ, ɑ, ɔ, ʊ, u, ə, etc.
- **Diphthongs:** eɪ, aɪ, ɔɪ, aʊ, oʊ, etc.
- **Special:** Affricates (tʃ, dʒ), nasals (m, n, ŋ), liquids (l, r)

### Accuracy Metrics

- **Target:** 95%+ accuracy on common English words
- **Current:** Achieves 95%+ on test suite
- **Test Coverage:** 20+ comprehensive test cases
- **Consistency:** Deterministic output for same input



---

## Performance

### Benchmark Results (Milestone 1)

- **Conversion Speed:** ~0.1-0.5ms per word
- **Memory Usage:** Minimal (<10MB for typical usage)
- **Accuracy:** 95%+ on common English words
- **Test Coverage:** High (core functionality)

### Known Limitations

- Phoneme-to-text reconstruction is approximate
- Homophones may not reconstruct to original spelling
- Requires espeak-ng for best accuracy
- Currently optimized for English (en-us)

---

## Resources

- [International Phonetic Alphabet (IPA)](https://www.internationalphoneticassociation.org/)
- [espeak-ng](https://github.com/espeak-ng/espeak-ng) - Text-to-speech engine
- [phonemizer](https://github.com/bootphon/phonemizer) - Python phonetic backend
- [epitran](https://github.com/dmort27/epitran) - Alternative phonetic library
