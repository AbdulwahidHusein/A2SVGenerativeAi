from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from stop_words import get_stop_words
import re

#a class that summerizes a given text
class Summerizer:
    def __init__(self, text_data):
        self.summarizer = LexRankSummarizer()
        self.text_data = text_data
        self.summarized_data = ""

    def _remove_stop_words(self):
        try:
            stop_words = get_stop_words('english')
            tokens = re.findall(r'\w+|[^\w\s]+', self.text_data)
            #tokens = self.summarized_data.split()
            filtered_text = [word for word in tokens if word.casefold() not in stop_words]
            self.text_data = ' '.join(filtered_text)
            return self.text_data
        except Exception as e:
            print(f"Error removing stop words: {e}")
            return ""

    def summarize(self, divider):
        try:
            assert divider >= 1

            length_of_sentences = len([sentence for sentence in self.text_data.split('.')])

            parser = PlaintextParser.from_string(self.text_data, Tokenizer("english"))
            summary = self.summarizer(parser.document, length_of_sentences // divider)

            self.summarized_data = "".join(str(word) for word in summary)

            return self.summarized_data
        except Exception as e:
            print(f"Error summarizing text: {e}")
            return False
