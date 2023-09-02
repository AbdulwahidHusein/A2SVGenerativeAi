import PyPDF2
#import docx
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer

#handles different types of files.
# Pdf, docx and rtf files are converted to plain text
class FileHandler:
    def __init__(self, file) -> None:
        self.file = file
        self.text = ""
        self.summerizer = LsaSummarizer()
        self.summerised_data = ""
        
    def read_pdf(self, start_page=0, end_page=0):
        pdf_reader = PyPDF2.PdfReader(self.file)
        num_pages = len(pdf_reader.pages)
        
        if end_page == 0:
            end_page = num_pages
            
        if end_page >= num_pages:
            end_page = num_pages-1
            
        for page in range(start_page, end_page+1):
            self.text += pdf_reader.pages[page].extract_text().strip()
        if self.text:
            return self.text
        return False
    
    def read_docx(self):
        pass
    
    def summerized(self, max_sentences, max_tokens):
        parser = PlaintextParser.from_string(self.text, Tokenizer("english"))
        summary = self.summerizer(parser.document, max_sentences)
        for i in summary:
            self.summerised_data += str(i)
        return self.summerised_data
    
    def num_of_tokens(self):
        return len(self.summerised_data.split())
        
    
text = '''
Django is a high-level Python web framework that follows the model-view-controller (MVC) architectural pattern. It provides a robust set of tools and features for developing web applications quickly and efficiently. Django follows the principle of "Don't Repeat Yourself" (DRY) and promotes clean, reusable code.

One of the key features of Django is its powerful Object-Relational Mapping (ORM) layer, which allows developers to interact with databases using Python classes and methods. This abstraction simplifies the process of working with databases and facilitates rapid development.

Django also includes a built-in administrative interface, known as the Django Admin, which provides an out-of-the-box solution for managing data and performing CRUD (Create, Read, Update, Delete) operations on models. The Django Admin can be customized to fit the specific needs of an application.

Another notable aspect of Django is its URL routing system. URLs in Django are mapped to views, which are Python functions or classes responsible for handling HTTP requests and returning HTTP responses. The URL routing mechanism allows for clean and flexible URL patterns, making it easy to build user-friendly and SEO-friendly web applications.

Django follows a templating system that separates the design and logic of a web application. Templates are written in HTML and can include dynamic content through the use of template tags and filters. This separation of concerns enhances code readability and maintainability.

Additionally, Django provides robust support for handling forms, managing user authentication and authorization, handling file uploads, and implementing caching mechanisms. It also offers internationalization and localization features to build applications that can be easily translated into different languages.

Django's extensibility is one of its strengths. It has a vast ecosystem of reusable packages, known as Django Apps, which provide additional functionality and can be easily integrated into projects. Django's community actively contributes to the development and maintenance of these packages.

Overall, Django is a powerful web framework that simplifies the process of building complex web applications. Its emphasis on efficiency, reusability, and maintainability makes it a popular choice among developers for projects of all sizes
'''

    
    
    
    
    
    
    
    
    
    
    
    
    #handles docx files and returns a string
'''def docx(self):
        doc = docx.Document(self.file)
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        return text
    
    #handles rtf files and returns string
    def rtf(self):
        doc = docx.Document(self.file)
        text = ' '.join([paragraph.text for paragraph in doc.paragrapgs])
        return text'''
                
#summerise the text to reduce the number of tokens
#retruns thre summerised text that can be directely sent to the GenerativeAI API
class Summerizer:
    def __init__(self, text) -> None:
        self.text = text
        self.summerizer = LexRankSummarizer()

    def summery(self, divider):
        parser = PlaintextParser.from_string(self.text, Tokenizer("english"))
        summary = self.summerizer(parser.document, len(self.text)/ divider)
        txt = ' '
        for i in summary:
            txt += str(i)
        return (txt)
    
text = '''
Time is an intangible and yet incredibly powerful force that governs our lives and the entire universe. It is a fundamental aspect of our existence, shaping our experiences, perceptions, and the very fabric of reality itself. From the ticking of a clock to the cycles of day and night, time manifests in various forms and influences every aspect of our lives.

At its core, time is a measurement of change and motion. It provides a framework within which events occur and sequences unfold. It allows us to organize our lives, plan for the future, and reflect on the past. Without time, life would be chaotic and unpredictable, lacking any sense of order or continuity.

One of the most fascinating aspects of time is its subjective nature. Time can feel fast or slow depending on our circumstances and state of mind. When we are engaged in an enjoyable activity, time seems to fly by, while moments of boredom or discomfort can make time drag on endlessly. This subjective perception of time highlights its intricate relationship with our consciousness and emotions.

Philosophers, scientists, and thinkers from various disciplines have grappled with the concept of time throughout history. The nature of time has been the subject of intense debate, with questions about its directionality, existence, and even its potential relativity. The theories of time put forth by ancient philosophers like Aristotle, who defined time as the measurement of change, to the groundbreaking work of Albert Einstein, who revolutionized our understanding of time through his theory of relativity, have significantly shaped our perception of this fundamental dimension.

Einstein's theory of relativity, in particular, introduced the notion that time is not an absolute quantity but rather a flexible and dynamic entity. According to this theory, time is intertwined with space, forming a four-dimensional fabric known as spacetime. The curvature of spacetime is influenced by mass and energy, causing time to flow differently in the presence of gravitational fields or when traveling at high speeds. This groundbreaking insight has been confirmed by numerous experiments and observations, solidifying our understanding of the intricate relationship between time and the physical world.

Beyond its scientific and philosophical significance, time holds immense cultural and symbolic value. It serves as a metaphor for life, reminding us of the transient and fleeting nature of our existence. Countless poems, songs, and works of art have been inspired by the concept of time, capturing its beauty, mystery, and profound impact on human consciousness. From the ancient Greek concept of "kairos," representing the opportune moment, to the famous Latin phrase "carpe diem" urging us to seize the day, time has been a recurring theme in human expression and a source of contemplation and inspiration.

In our modern world, time has become an increasingly precious and scarce resource. The rapid pace of technological advancements, the demands of work and personal life, and the constant connectivity of the digital age have created a sense of time scarcity and an ever-present pressure to be productive and efficient. Time management has become a critical skill, with individuals seeking ways to optimize their schedules, prioritize their tasks, and find a balance between work, leisure, and self-care.

However, amidst the hustle and bustle of contemporary life, it is crucial to remember the importance of taking a pause and savoring the present moment. The mindfulness movement, with its emphasis on being fully present and aware, encourages us to cultivate a deeper relationship with time. By slowing down, practicing gratitude, and embracing the richness of each passing moment, we can find a sense of fulfillment and meaning in our lives, unburdened by the constant pressure of the ticking clock.

Ultimately, time remains an enigma, both captivating and elusive. While science has unraveled many of its mysteries, there is still much we do not understand. The nature of time continues to inspire curiosity and fuel our quest for knowledge. As we navigate the ever-changing landscape of our lives, it is essential to appreciate the profound influence of time, cherish the moments we have, and strive to make the most of the precious gift that it is.
'''

        
        



