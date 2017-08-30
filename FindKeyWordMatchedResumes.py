from Utils import get_keywords, split_text_to_tokens, copy_file_to_folder
import glob
import os
path = '/Users/ashleyzhao/Desktop/talents.ai/SampleResumes'


def get_computer_vision_keywords():
    return get_keywords('./keywords/computer_vision.txt')


def get_experienced_candidates():
    return get_keywords('./keywords/title.txt')


def find_key_word_matched_resumes(get_keywords, new_path):
    keywords = get_keywords
    for filename in glob.glob(os.path.join(path, '*.pdf')):
        new_file = new_path + filename[len(path):]
        if new_file not in glob.glob(os.path.join(new_path, '*.pdf')):
            tokens = split_text_to_tokens(filename)
            for token in tokens:
                if token in keywords:
                    print (token)
                    copy_file_to_folder(filename, new_path)


def find_all_computer_vision_resumes():
    new_path = "./computer_vision/"
    find_key_word_matched_resumes(get_computer_vision_keywords(), new_path)


def find_experienced_candidates_resumes():
    new_path = "./experienced_candidates/"
    find_key_word_matched_resumes(get_experienced_candidates(), new_path)
