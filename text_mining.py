import re
from konlpy.tag import Komoran
from collections import Counter

def text_preprocessing(text):
    # HTML 태그 제거
    text = re.sub('<.+?>', '', text)
    # 특수문자 제거
    text = re.sub('[^가-힣a-zA-Z0-9]', ' ', text)
    # 공백 제거
    text = ' '.join(text.split())
    return text

def extract_keywords(text, n=10):
    komoran = Komoran()
    nouns = komoran.nouns(text)
    count = Counter(nouns)
    keywords = count.most_common(n)
    return keywords
