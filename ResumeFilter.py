# iterate all pdfs in the folder and assign a score
from ScoreCalculator import *
from FindKeyWordMatchedResumes import *
from FindSimilarResumes import *

path = '/Users/xin/Dropbox/DataScienceJobFairResumes/'

def main():
    cal_scores_of_all_files()

    find_all_computer_vision_resumes()

    find_experienced_candidates_resumes()

    find_similar_resumes()

if __name__ == '__main__':
    main()


