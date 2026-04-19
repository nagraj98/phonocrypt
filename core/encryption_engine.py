import random
from enum import Enum
from typing import List, Tuple, Optional
from core.phonetic_engine import text_to_words

class ScriptType(Enum):
    ENGLISH    = "english"
    IPA        = "ipa"
    DEVANAGARI = "devanagari"

class EncryptionEngine:
    """
    Hides text in plain sight by randomly distributing words
    across different scripts — English, IPA, and Devanagari.
    
    Each word is the same sound, just written in a different script.
    The sentence is fully recoverable if you know the mapping.
    """

    def __init__(
        self,
        phonetic_engine=PhoneticEngine(),
        script: Script = Script.HINDI,
        seed: Optional[int] = None
    ):
        self.phonetic_engine = phonetic_engine
        self.script = script
        if seed is not None:
            random.seed(seed)  # reproducible encryption if needed

    def _word_to_script(self, word: str, target: ScriptType) -> str:
        """Convert a single English word to the target script."""
        if target == ScriptType.ENGLISH:
            return word
        
        if target == ScriptType.IPA:
            return self.phonetic_engine.text_to_ipa(word)
        
        if target == ScriptType.DEVANAGARI:
            return self.phonetic_engine.english_word_to_devanagari(word, script=self.script)


    def encrypt(
        self,
        text: str,
        weights: Tuple[float, float, float] = (0.34, 0.33, 0.33)
    ) -> dict:
        """
        Encrypt text by randomly assigning each word to a script.

        weights: probability distribution for (English, IPA, Devanagari)
                 defaults to roughly equal distribution

        Returns a dict with:
          - 'encrypted'  : the mixed-script sentence
          - 'map'        : word-by-word breakdown for decryption
        """
        words = text_to_words(text)
        scripts = [ScriptType.ENGLISH, ScriptType.IPA, ScriptType.DEVANAGARI]

        word_map = []
        output   = []

        for word in words:
            chosen_script = random.choices(scripts, weights=weights, k=1)[0]
            converted     = self._word_to_script(word, chosen_script)
            output.append(converted)
            word_map.append({
                'original'  : word,
                'script'    : chosen_script.value,
                'converted' : converted,
            })

        return {
            'encrypted' : ' '.join(output),
            'map'       : word_map,
        }

    def decrypt(self, encryption_result: dict) -> str:
        """Recover original English text from the encryption map."""
        return ' '.join(entry['original'] for entry in encryption_result['map'])
    

engine = EncryptionEngine(seed=42)  # seed for reproducible output

result = engine.encrypt("The quick brown fox jumps over the lazy dog")

print(result['encrypted'])
# e.g: the  kwˈɪk्  ब्राउन्  fɑːks  जम्प्स्  ˌoʊvɚ  द  lazy  dˈɑːɡ

print(engine.decrypt(result))
# The quick brown fox jumps over the lazy dog

# See the full map
for entry in result['map']:
    # print the map
    print(f"{entry['original']:10} → [{entry['script']:10}] {entry['converted']}")


# convert to dataframe for better visualization
import pandas as pd

df = pd.DataFrame(result['map'])
print(df)