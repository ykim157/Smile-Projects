
# coding: utf-8

# In[1]:


import scipy
import numpy as np
import json

import spacy
import tensorflow
import keras
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1   import Features, KeywordsOptions, EntitiesOptions, SemanticRolesOptions

import nltk
from nltk.stem import WordNetLemmatizer

# from __future__ import absolute_import
# from __future__ import division, print_function, unicode_literals

# from sumy.parsers.html import HtmlParser
# from sumy.parsers.plaintext import PlaintextParser
# from sumy.nlp.tokenizers import Tokenizer
# from sumy.summarizers.lsa import LsaSummarizer as Summarizer
# from sumy.nlp.stemmers import Stemmer
# from sumy.utils import get_stop_words

import inflection
import en_core_web_lg
import language_check
nlp = en_core_web_lg.load()

#nltk.download('punkt')
#nltk.download('wordnet')


# In[2]:


#Load credentials from file (Store credentials in json format)
with open('credentials.json') as f:
    data = json.load(f)
url = data["url"]
username = data["username"]
password = data["password"]


# In[3]:


# set grammar checker
grammar_tool = language_check.LanguageTool('en-US')


# In[4]:


natural_language_understanding = NaturalLanguageUnderstandingV1(
  username=username,
  password=password,
  version='2018-03-16')

response = natural_language_understanding.analyze(
    url='https://www.nytimes.com/2018/07/16/opinion/trump-and-putin-vs-america.html?action=click&pgtype=Homepage&clickSource=story-heading&module=opinion-c-col-left-region&region=opinion-c-col-left-region&WT.nav=opinion-c-col-left-region',
    language='en',
    features=Features(
        keywords=KeywordsOptions(
            sentiment=False,
            emotion=False,
            limit=20),
    entities=EntitiesOptions(
        sentiment=False,
            emotion=False,
            limit=50),
    semantic_roles=SemanticRolesOptions()
  ))
entities = response['entities']
keywords = response['keywords']
semantic = response['semantic_roles']


# In[5]:


# Question 1
# Extract keywords and entities
# define type of words
# create questions
def Q1(x):
    return {
        'Person': "Who is ",
        'Location': "Where is "
    }.get(x, "What is ")

with open("Questions1.txt", "w") as file:
    for en in entities:
        text = Q1(en['type']) + en['text'] + "?"
        matches = grammar_tool.check(text)
        correct_text = language_check.correct(text, matches)
        file.write("%s\n" % correct_text)


# In[6]:


#Question 2
# Extract keywords and entities
# define plurality of keywords using nltk
# create question What are? Who are? 
# TODO. How to determine plurality of word?
# TODO. If condition does not suffice, what else?


wnl = WordNetLemmatizer()

def isplural(word):
    lemma = wnl.lemmatize(word, 'n')
    plural = True if word is not lemma else False
    return plural


# In[7]:


# Question 3
# How would you compare A to B?
# For each keyword, look for other words that have same type and relatively high relevance in DB of news articles???


# In[8]:


# Question 4
# Why (factual statement)?
# TODO. How to determine which sentences are important enough to negate? TEXTSUM, sumy NOTWORKING

# Question 5
# What if (negated statements)?
# TODO. How to negate sentences? add not, find antonym
# TODO. How to determine which sentences are important enough to negate? summarize? gensim, pyteaser, pytextrank, TEXTSUM, sumy


# LANGUAGE = "english"
# SENTENCES_COUNT = 6
# if __name__ == "__main__":
#     #url = "https://en.wikipedia.org/wiki/Steven_Spielberg"
#     #parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
#     # or for plain text files
#     parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
#     stemmer = Stemmer(LANGUAGE)

#     summarizer = Summarizer(stemmer)
#     summarizer.stop_words = get_stop_words(LANGUAGE)

#     for sentence in summarizer(parser.document, SENTENCES_COUNT):
#         result = natural_language_understanding.analyze(text=str(sentence), features=Features(semantic_roles=SemanticRolesOptions()))
#         #print(json.dumps(result, indent=2))
#         for sentence in result['semantic_roles']:
#             print(len(sentence))
#             if len(sentence) == 4:
#                 print("Why Does", sentence['subject']['text'], verb, obj)
#                 print("What if", sentence['subject']['text'], "did not",verb, obj)



Q4 = []
Q5 = []

listOfPlurals = ["they", "some", "most", "we"]

for sentence in semantic:
    if len(sentence) == 4:
        verb = sentence['action']['normalized']
        subj = sentence['subject']['text'].lower()
        obj = sentence['object']['text']
        if verb is not "s" and verb != "be":
            plurality = subj is not inflection.singularize(subj) or subj in listOfPlurals
            print(verb)
            if plurality:
                Q4.append("Why do " + subj + " " + verb + " " + obj + "?")
            else:
                Q4.append("Why does " + subj + " " + verb + " " + obj + "?")
            Q5.append("What if " + subj + " did not " + verb + " " + obj + "?")
        elif verb == "be":
            plurality = subj is not inflection.singularize(subj) or subj in listOfPlurals
            if plurality:
                Q4.append("Why are " + subj + " " + obj + "?")
                Q5.append("What if " + subj + " were not " + obj + "?")
            else:
                Q4.append("Why is " + subj + " " + obj + "?")
                Q5.append("What if " + subj + " was not " + obj + "?")
        
with open("Questions4.txt", "w", encoding='UTF-8') as file:
    for q in Q4:
        matches = grammar_tool.check(q)
        corrected_q = language_check.correct(q, matches)
        file.write("%s\n" % corrected_q)
with open("Questions5.txt", "w", encoding='UTF-8') as file:
    for q in Q5:
        matches = grammar_tool.check(q)
        corrected_q = language_check.correct(q, matches)
        file.write("%s\n" % corrected_q)

# TODO: Check relevance to text
# TODO: lets do grammar check first and delete or fix the grammar before comparing relevance to text


# In[9]:


# make sure to use larger model!
tokens = nlp(u'Google Facebook Honda')

for token1 in tokens:
  for token2 in tokens:
      print(token1.text, token2.text, token1.similarity(token2))

