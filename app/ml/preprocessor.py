import re
import spacy

_nlp = None


def get_nlp():
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
        except OSError:
            _nlp = False
    return _nlp


def clean_text(text: str) -> str:
    text = str(text or "").lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    nlp = get_nlp()
    if nlp is False:
        return " ".join(w for w in text.split() if len(w) > 1)
    doc = nlp(text)
    tokens = []
    for token in doc:
        if token.is_stop or token.is_punct or token.is_space or len(token.text) <= 1:
            continue
        tokens.append(token.lemma_)
    return " ".join(tokens)
