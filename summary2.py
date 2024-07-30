from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import nltk
from readallfiles import read_file
#nltk.download('punkt')
summarizer_lex = LexRankSummarizer()

# Summarize using sumy LexRank
#summary= summarizer_lex("parse.txt", 2)

document1 ="""Machine learning (ML) is the scientific study of algorithms and statistical models that computer systems use to progressively improve their performance on a specific task. Machine learning algorithms build a mathematical model of sample data, known as "training data", in order to make predictions or decisions without being explicitly programmed to perform the task. Machine learning algorithms are used in the applications of email filtering, detection of network intruders, and computer vision, where it is infeasible to develop an algorithm of specific instructions for performing the task. Machine learning is closely related to computational statistics, which focuses on making predictions using computers. The study of mathematical optimization delivers methods, theory and application domains to the field of machine learning. Data mining is a field of study within machine learning, and focuses on exploratory data analysis through unsupervised learning.In its application across business problems, machine learning is also referred to as predictive analytics."""

def summarize(filename):
    try:
        # file = open(filename, 'r')
        # data = file.read()
        data = read_file(filename)
        parser = PlaintextParser.from_string(data, Tokenizer("english"))
        summary = summarizer_lex(parser.document, 1)

        lex_summary = ""
        for sentence in summary:
            lex_summary+=str(sentence)
        return lex_summary
    except:
        return "N/A"

def summarize_text(data):
    try:
        parser = PlaintextParser.from_string(data, Tokenizer("english"))
        summary = summarizer_lex(parser.document, 1)

        lex_summary = ""
        for sentence in summary:
            lex_summary+=str(sentence)
        return lex_summary
    except:
        return "N/A"
# file = open('parse.txt', 'r')
# data = file.read()
# parser = PlaintextParser.from_string(data,Tokenizer("english"))

# summary = summarizer_lex(parser.document, 1)

# lex_summary=""
# for sentence in summary:
#     lex_summary+=str(sentence)
# print(lex_summary)
