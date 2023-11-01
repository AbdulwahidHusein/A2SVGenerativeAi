from yake import KeywordExtractor


def extract_keywords(text, top):
    extractor = KeywordExtractor(top=top, stopwords=None)
    extracted = extractor.extract_keywords(text)
    keywords = []
    
    for word, rank in extracted:
        keywords.append(word)
        
    return keywords