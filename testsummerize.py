from yake import KeywordExtractor

ext = KeywordExtractor(top=10, stopwords=None)
keywords = ext.extract_keywords("""/ /  model, and Niels Bohr's planetary model. These models have contributed to our understanding of the structure and behavior of atoms [2].

isciplines, including chemistry, physics, materials science, and biochemistry.""")

print(keywords)