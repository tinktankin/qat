#!/usr/bin/env python
# coding: utf-8

# Importing Modules

# In[2]:


import nltk
from nltk import word_tokenize
import string
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
import numpy as np
import math    


# In[3]:


def keyword_gen(Text):
    def clean(text):
        text = text.lower() #make text to lowercase
        printable = set(string.printable)
        text = filter(lambda x: x in printable, text)
        text = "".join(list(text))
        return text
    Cleaned_text = clean(Text)
    # print(Cleaned_text)
    text = word_tokenize(Cleaned_text)
    #print ("Tokenized Text: \n")
    #print (text)
    POS_tag = nltk.pos_tag(text)
    #print ("Tokenized Text with POS tags: \n")
    #print (POS_tag)
    wordnet_lemmatizer = WordNetLemmatizer()
    adjective_tags = ['JJ','JJR','JJS']
    lemmatized_text = []
    for word in POS_tag:
        if word[1] in adjective_tags:
            lemmatized_text.append(str(wordnet_lemmatizer.lemmatize(word[0],pos="a")))
        else:
            lemmatized_text.append(str(wordnet_lemmatizer.lemmatize(word[0]))) #default POS = noun
    #print ("Text tokens after lemmatization of adjectives and nouns: \n")
    #print (lemmatized_text)
    POS_tag = nltk.pos_tag(lemmatized_text)
    #print ("Lemmatized text with POS tags: \n")
    #print (POS_tag)
    stopwords = []
    wanted_POS = ['NN','NNS','NNP','NNPS','JJ','JJR','JJS','VBG','FW']
    for word in POS_tag:
        if word[1] not in wanted_POS:
            stopwords.append(word[0])
    punctuations = list(str(string.punctuation))
    stopwords = stopwords + punctuations
    stopword_file = open("long_stopwords.txt", "r")
    #Source = https://www.ranks.nl/stopwords
    lots_of_stopwords = []
    for line in stopword_file.readlines():
        lots_of_stopwords.append(str(line.strip()))
    stopwords_plus = []
    stopwords_plus = stopwords + lots_of_stopwords
    stopwords_plus = set(stopwords_plus)
    #Stopwords_plus contain total set of all stopwords
    processed_text = []
    for word in lemmatized_text:
        if word not in stopwords_plus:
            processed_text.append(word)
    #print (processed_text)
    vocabulary = list(set(processed_text))
    #print (vocabulary)
    vocab_len = len(vocabulary)

    weighted_edge = np.zeros((vocab_len,vocab_len),dtype=np.float32)

    score = np.zeros((vocab_len),dtype=np.float32)
    window_size = 3
    covered_coocurrences = []

    for i in range(0,vocab_len):
        score[i]=1
        for j in range(0,vocab_len):
            if j==i:
                weighted_edge[i][j]=0
            else:
                for window_start in range(0,(len(processed_text)-window_size)):

                    window_end = window_start+window_size

                    window = processed_text[window_start:window_end]

                    if (vocabulary[i] in window) and (vocabulary[j] in window):

                        index_of_i = window_start + window.index(vocabulary[i])
                        index_of_j = window_start + window.index(vocabulary[j])

                        # index_of_x is the absolute position of the xth term in the window 
                        # (counting from 0) 
                        # in the processed_text

                        if [index_of_i,index_of_j] not in covered_coocurrences:
                            weighted_edge[i][j]+=1/math.fabs(index_of_i-index_of_j)
                            covered_coocurrences.append([index_of_i,index_of_j])
    inout = np.zeros((vocab_len),dtype=np.float32)

    for i in range(0,vocab_len):
        for j in range(0,vocab_len):
            inout[i]+=weighted_edge[i][j]
    MAX_ITERATIONS = 50
    d=0.85
    threshold = 0.0001 #convergence threshold

    for iter in range(0,MAX_ITERATIONS):
        prev_score = np.copy(score)

        for i in range(0,vocab_len):

            summation = 0
            for j in range(0,vocab_len):
                if weighted_edge[i][j] != 0:
                    summation += (weighted_edge[i][j]/inout[j])*score[j]

            score[i] = (1-d) + d*(summation)

        if np.sum(np.fabs(prev_score-score)) <= threshold: #convergence condition
            #print("Converging at iteration "+str(iter)+"....")
            break
    phrases = []

    phrase = " "
    for word in lemmatized_text:

        if word in stopwords_plus:
            if phrase!= " ":
                phrases.append(str(phrase).strip().split())
            phrase = " "
        elif word not in stopwords_plus:
            phrase+=str(word)
            phrase+=" "

    #print("Partitioned Phrases (Candidate Keyphrases): \n")
    #print(phrases)
    unique_phrases = []

    for phrase in phrases:
        if phrase not in unique_phrases:
            unique_phrases.append(phrase)

    #print("Unique Phrases (Candidate Keyphrases): \n")
    #print(unique_phrases)
    for word in vocabulary:
        #print word
        for phrase in unique_phrases:
            if (word in phrase) and ([word] in unique_phrases) and (len(phrase)>1):
                #if len(phrase)>1 then the current phrase is multi-worded.
                #if the word in vocabulary is present in unique_phrases as a single-word-phrase
                # and at the same time present as a word within a multi-worded phrase,
                # then I will remove the single-word-phrase from the list.
                unique_phrases.remove([word])
        #print("Thinned Unique Phrases (Candidate Keyphrases): \n")
        #print(unique_phrases)
    phrase_scores = []
    keywords = []
    for phrase in unique_phrases:
        phrase_score=0
        keyword = ''
        for word in phrase:
            keyword += str(word)
            keyword += " "
            phrase_score+=score[vocabulary.index(word)]
        phrase_scores.append(phrase_score)
        keywords.append(keyword.strip())
    return keywords


# In[4]:


import nltk
import re,math
from nltk import sent_tokenize,word_tokenize
from nltk.corpus import wordnet as wn
from pattern.en import conjugate, lemma, lexeme,PRESENT,SG


# In[5]:


def get_marks(c_answer,answer2,max_marks=5):

    keywords_matched=0
    maximum_marks =max_marks
    
    # keywords=['data','mine','database','characterization','knowledge','background','task','classify','associate','visualize','predict','cluster']
    keywords=keyword_gen(c_answer)
    expected_keywords = len(keywords)
    #print(expected_keywords)
    
    #expected_no_of_words = 200
    expected_no_of_words =len(word_tokenize(c_answer))
    
    #expected_no_of_sentences = 15
    expected_no_of_sentences =len(sent_tokenize(c_answer))
    forms = [] #We'll store the derivational forms in a set to eliminate duplicates
    for word in keywords:
        for happy_lemma in wn.lemmas(word): #for each "happy" lemma in WordNet
            forms.append(happy_lemma.name()) #add the lemma itself
            for related_lemma in happy_lemma.derivationally_related_forms(): #for each related lemma
                forms.append(related_lemma.name()) #add the related lemma
    #print(forms)
    # keywords.extend(extended_keywords)
    keywords.extend(forms)
    keywords =  [x.lower() for x in keywords]
    keywords = list(set(keywords))
    #print(keywords)
    string = answer2.replace('\n',' ').lower() #for converting to lower case
    ans_key=keyword_gen(string)
    word_list = word_tokenize(string) #for word spliting
    no_of_words = len(word_list)
    if no_of_words>expected_no_of_words:
        no_of_words=expected_no_of_words
    
    no_of_sentences = len(sent_tokenize(string))
    if no_of_sentences>expected_no_of_sentences:
        no_of_sentences=expected_no_of_sentences
    #print('no_of_words',no_of_words)
    #print('no_of_sentences',no_of_sentences)
    
    for keyword in keywords:
        if(keyword in ans_key):
            keywords_matched=keywords_matched+1        
    if keywords_matched>expected_keywords:
        keywords_matched = expected_keywords
    #print('keywords matched',keywords_matched)
    
    keywords_percentage = 0.55*(keywords_matched/expected_keywords)    
    word_percentage = 0.35*(no_of_words/expected_no_of_words)
    sentence_percentage = 0.10*(no_of_sentences/expected_no_of_sentences)
    
    #print('keywords_percentage',keywords_percentage)
    #print('word_percentage',word_percentage)
    #print('sentence_percentage',sentence_percentage)
    
    total_marks = maximum_marks*(keywords_percentage+word_percentage+sentence_percentage)
    total_marks=round(total_marks,1)
    digit=total_marks*10
    if(digit%10<5):
        total_marks=math.floor(total_marks)
    if(digit%10>5):
        total_marks=math.ceil(total_marks)  
    print('total_marks',total_marks)
    return total_marks


# In[7]:


ans="the full form is central processing unit."
c_ans="central processing unit."
a=get_marks(c_ans,ans)


# In[ ]:




