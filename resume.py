import csv
import pandas
import numpy as np
import warnings

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import gensim

pathname = "C:\\Users\\admin\\Desktop\\sampleresume.txt"
pathname_jd = "C:\\Users\\admin\\Desktop\\sampleJD.txt"
columns=["NAME","CONTACT","EMAIL","SKILLS","WORK HISTORY"]

def concatenate_list_data(list):
    result= ''
    for element in list:
        result += str(element)
    return result

def add_resume(pathname):
    x = [[] for i in range(5)]
    words = ["NAME","CONTACT","EMAIL","SKILLS","WORK HISTORY"]
    for i in range(len(words)):
         do_print = False
        if i==4:
            word =words[i]
            for line in open(pathname, 'r'):
                if do_print:
                    x[i].append(line)
                if word in line:
                    do_print= True

        else:
            word= words[i]
            word2= words[i+1]
            for line in open(pathname, 'r'):
                if word2 in line:
                    do_print = False
                if do_print:
                    x[i].append(line)
                if word in line:
                    do_print = True
    x_new = []
    for y in x:
        y=concatenate_list_data(y)
        y=y.replace("\n"," ")
        y=y.replace(","," ")
        x_new.append(y)
    return x_new

def add_JD(pathname_jd):
    x = [[] for i in range(2)]
    words = ["SKILLS","EXPERIENCE"]
    for i in range(len(words)):
        do_print = False
        if i==1:
            word =words[i]
            for line in open(pathname_jd, 'r'):
                if do_print:
                    x[i].append(line)
                if word in line:
                    do_print= True

        else:
            word= words[i]
            word2= words[i+1]
            for line in open(pathname_jd, 'r'):
                if word2 in line:
                    do_print = False
                if do_print:
                    x[i].append(line)
                if word in line:
                    do_print = True
                    
    x_new = []
    print(x_new)

    for y in x:
        y=concatenate_list_data(y)
        y=y.replace("\n"," ")
        y=y.replace(","," ")
        x_new.append(y)

    jd= pandas.DataFrame([x_new],columns=words)
    return jd

new_entry = add_resume(pathname)

fd = open('C:\\Users\\admin\\Desktop\\db.csv','a')

for val in range(len(new_entry)):
	if val==len(new_entry)-1:
		fd.write(new_entry[val]+'\n')

	else :
		fd.write(new_entry[val]+',')

fd.close()

resume_db = pandas.read_csv('C:\\Users\\admin\\Desktop\\db.csv',names=columns)

JD = add_JD(pathname_jd)

from gensim import corpora

resume_skills = resume_db["SKILLS"]
skill_list = []

for i in range(len(resume_db["SKILLS"])):
	skill_list.append(resume_db.iloc[i]["SKILLS"])

stoplist = set('for a of the and to in on all an * % I have can'.split())

texts = [[word for word in skill.lower().split() if word not in stoplist]

		  for skill in skill_list]
# from pprint import pprint
# # pprint(texts)

skill_dic = corpora.Dictionary(texts)

#dictionary.save('')
# print(skill_dic.token2id)

skill_corpus = [skill_dic.doc2bow(text) for text in texts]

#corpora.MmCorpus.serialize('', corpus)
# for vector in skill_corpus:
# 	print(vector)
# class MyCorpus(object):
#      def __iter__(self):
#          for line in open('mycorpus.txt'):
#              # assume there's one document per line, tokens separated by whitespace
#              yield dictionary.doc2bow(line.lower().split())
#  corpus_memory_friendly = MyCorpus()  # doesn't load the corpus into memory!
#  print(corpus_memory_friendly)

#Similarly, to construct the dictionary without loading all texts into memory:
# from six import iteritems
# collect statistics about all tokens
# dictionary = corpora.Dictionary(line.lower().split() for line in open('mycorpus.txt'))
# remove stop words and words that appear only once
# stop_ids = [dictionary.token2id[stopword] for stopword in stoplist
#              if stopword in dictionary.token2id]
# once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
# dictionary.filter_tokens(stop_ids + once_ids)  # remove stop words and words that appear only once
# dictionary.compactify()  # remove gaps in id sequence after words that were removed
# print(dictionary)
# Dictionary(12 unique tokens)

from gensim import models,similarities

tfidf = models.TfidfModel(skill_corpus,normalize=True)

skill_corpus_tfidf = tfidf[skill_corpus]

# for doc in skill_corpus_tfidf:
# 	print(doc)

skills_jd = add_JD(pathname_jd).iloc[0]["SKILLS"]

# print(skills_jd)

lsi = models.LsiModel(skill_corpus, id2word=skill_dic, num_topics=2)
vec_corpus=[skill_dic.doc2bow(skills_jd.lower().split())]
vec_lsi = lsi[vec_corpus]

index = similarities.MatrixSimilarity(lsi[skill_corpus])
sims = index[vec_lsi]

flat_list = [item for sublist in list(sims) for item in sublist]

ranked_sims = sorted(enumerate(flat_list), key=lambda item: -item[1])

top_ten_resumes = ranked_sims[:10]

d= pandas.DataFrame(top_ten_resumes,columns=["key","val"])

ranked_indices = d["key"]

print(list(ranked_indices))

results = resume_db.iloc[list(ranked_indices)]

results.to_csv("C:\\Users\\admin\\Desktop\\sherlock.txt")

# #print(top_ten_resumes)
# print(resume_db.iloc[list(ranked_indices)])                    