from lingua import Language, LanguageDetectorBuilder
from typing import Optional

# בונה דיטקטור מהיר ומדויק
detector = LanguageDetectorBuilder.from_languages(
    Language.HEBREW,
    Language.ENGLISH,
    Language.RUSSIAN,
    Language.ARABIC,
).build()

class LanguageDetector:
    @staticmethod
    def detect(text: str) -> str:
        if not text or len(text.strip()) < 2:
            return "he"
        try:
            confidence_values = detector.compute_language_confidence_values(text)
            if confidence_values:
                best_lang = max(confidence_values, key=lambda x: x.value)
                if best_lang.value > 0.6:
                    return best_lang.language.iso_code_639_1.value
            return "he"
        except Exception:
            return "he"

def get_user_language(text: str, user_preferred: Optional[str] = None) -> str:
    """משלב זיהוי אוטומטי + העדפה מהפרופיל"""
    if user_preferred and user_preferred != "auto":
        return user_preferred
    return LanguageDetector.detect(text)
