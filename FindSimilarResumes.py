from gensim import corpora, models, similarities
from Utils import get_keywords, split_text_to_tokens
import glob
import os

path = '/Users/ashleyzhao/Desktop/talents.ai/SampleResumes'
template_file = './keywords/computer_vision.txt'

# find the similarity of files with respect to given template_file.
# not tested yet.

def find_similar_resumes():
    template_words = get_template_words()
    corpus, dictionary, file_loc_dict = convert_all_files_to_corpus(template_words)
    template_file_corpus = dictionary.doc2bow(template_words)

    tfidf = models.TfidfModel(corpus)
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(template_words))
    sims = index[tfidf[template_file_corpus]]

    for i, similarity in enumerate(sims):
        print (file_loc_dict[i], similarity)


def get_template_words():
    return get_keywords(template_file)


def convert_all_files_to_corpus(template_words):
    similarity_words = []
    file_loc_dict, i = {}, 0
    for filename in glob.glob(os.path.join(path, '*.pdf')):
        bag_of_words = convert_file_to_corpus(filename, template_words)
        similarity_words.append(bag_of_words)
        if filename not in file_loc_dict:
            file_loc_dict[i] = filename
            i += 1

    dictionary = corpora.Dictionary(similarity_words)
    print (dictionary.token2id)
    corpus = [dictionary.doc2bow(words) for words in similarity_words]
    print (similarity_words)
    return corpus, dictionary, file_loc_dict


def convert_file_to_corpus(filename, template_words):
    tokens = split_text_to_tokens(filename)
    bag_of_words = []
    for token in tokens:
        if token in template_words and token not in bag_of_words:
            bag_of_words.append(token)
    return bag_of_words







