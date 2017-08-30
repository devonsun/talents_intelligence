from __future__ import division
import random
import csv
import os
import glob
import ntpath
import pprint
import operator
from docx import Document
from Utils import get_keywords, split_text_to_tokens

path = '/Users/ashleyzhao/Desktop/talents.ai/SampleResumes'
scores = {}
pp = pprint.PrettyPrinter(indent=4)


def write_sorted_scores_to_csv(sorted_scores):
    with open('scores.csv', 'w') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow(['filename', 'total score', 'phd score', 'computer score', 'math score', 'experience score'])
        for line in sorted_scores:
            csv_writer.writerow([line[0], line[1][0], line[1][1], line[1][2], line[1][3], line[1][4]])


def get_computer_keywords():
    return get_keywords('./keywords/computer.txt')


def get_math_keywords():
    return get_keywords('./keywords/math.txt')


def get_experience_keywords():
    return get_keywords('./keywords/experience.txt')



def cal_score_from_words(tokens, c_keywords, m_keywords, e_keywords, phd_keywords):
    #print (tokens)
    C = 0 #Computer Science
    M = 0 #Math
    E = 0 #Experience
    alpha = 1 #0.5
    beta = 1 # 0.3
    gamma = 1 #0.2
    e = random.choice([0.2,0])  #residual
    phd_keywords_set, c_keywords_set, m_keywords_set, e_keywords_set = set(), set(), set(), set()

    for token in tokens:
        if token in phd_keywords: #if degree is Ph.D
            phd_keywords_set.add(token)
            D = 5
        else:
            D = 0
            if token in c_keywords:
                c_keywords_set.add(token)
                C += 1
            if token in m_keywords:
                m_keywords_set.add(token)
                M += 1
            if token in e_keywords:
                e_keywords_set.add(token)
                E += 1

    #print ("phd: ", str(phd_keywords_set))
    #print ("computer: ", str(c_keywords_set))
    #print ("math: ", str(m_keywords_set))
    #print ("experience: ", str(e_keywords_set))
    # Y = 1 + alpha*C + beta*M + gamma*E + D + e # Score of the resume
    D = 3
    Y = 1 + alpha * len(c_keywords_set) + beta * len(m_keywords_set) + gamma * len(e_keywords_set) + D * len(phd_keywords_set)
    return (round(Y,2), 100 * len(phd_keywords_set) / len(phd_keywords), 100 * len(c_keywords_set)/ len(c_keywords),
            100 * len(m_keywords_set) / len(m_keywords), 100 * len(e_keywords_set) / len(e_keywords))

#convert docx to txt
def document_to_text(filename):
    document = Document(filename)
    paratextlist = []
    for paragraph in document.paragraphs:
        paratextlist.append(paragraph.text)
    return '\n'.join(paratextlist)
    
#wrapper for parsing both pdf and docx to tokens
def get_tokens(filename):
    tokens = []
    if filename.endswith("pdf"):
        tokens = split_text_to_tokens(filename)
        #print("pdf tokens: ", tokens)
    else:
        tokens = (document_to_text(filename)).lower().split()  
        #print("docx tokens: ", tokens)
    return tokens

def get_score(filename, c_keywords, m_keywords, e_keywords, phd_keywords):
    tokens = get_tokens(filename)
    return cal_score_from_words(tokens, c_keywords, m_keywords, e_keywords, phd_keywords)


def cal_scores_of_all_files():
    #computer science keywords
    c_keywords = get_computer_keywords()

    #math keywords
    m_keywords = get_math_keywords()
    #degree
    phd_keywords = ['phd','ph.d','doctor']

    #experience keywords
    e_keywords = get_experience_keywords()
    
    all_resumes = glob.glob(os.path.join(path, '*.pdf')) + glob.glob(os.path.join(path, '*.docx'))
    for filename in all_resumes:
        scores[ntpath.basename(filename)] = get_score(filename, c_keywords, m_keywords, e_keywords, phd_keywords)
        
        
    #scores is a dictionary of {'filename': (score, p_score, c_score, m_score, e_score)}
    #sorted_scores is a list sorted by highest score first
    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
    
    write_sorted_scores_to_csv(sorted_scores)
    print("resumes: ",len(sorted_scores))
    pp.pprint(sorted_scores)