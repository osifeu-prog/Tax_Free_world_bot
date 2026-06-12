from lingua import Language, LanguageDetectorBuilder

detector = LanguageDetectorBuilder.from_languages(
    Language.HEBREW,
    Language.ENGLISH,
    Language.RUSSIAN,
    Language.ARABIC
).build()

def get_user_language(text: str, user_preferred: str = None) -> str:
    if user_preferred and user_preferred not in ['auto', None, '']:
        return user_preferred
    
    if not text or len(text.strip()) < 2:
        return 'he'
    
    try:
        confidences = detector.compute_language_confidence_values(text)
        if confidences:
            best = max(confidences, key=lambda x: x.value)
            if best.value > 0.5:
                return best.language.iso_code_639_1.value
    except:
        pass
    
    return 'he'
