import pandas as pd
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

def hindi_to_hinglish(text: str) -> str:
    """
    Convert Hindi (Devanagari) text to Hinglish (Latin).
    """
    try:
        return transliterate(text, sanscript.DEVANAGARI, sanscript.ITRANS)
    except Exception:
        return text


if __name__ == "__main__":
    print("⏳ Converting Hindi to Hinglish...")

    data["text"] = data["text"].apply(to_hinglish)

    data.to_csv("fraud_calls_hinglish.csv", index=False, encoding="utf-8")

    print("✅ Hinglish CSV created successfully")
