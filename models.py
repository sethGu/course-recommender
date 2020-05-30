import pickle
import stanfordnlp
import os
import numpy as np
from random import sample
from sklearn.metrics.pairwise import cosine_similarity

np.set_printoptions(threshold=np.inf)  # print the whole matrix

course_code = "crawling/courseCode.pickle"
course_detail = "crawling/courseDetail.pickle"
raw_keyword = "rawKeyWord.pickle"
student_GPA = "studentGPA.pickle"


class Solutions:
    def __init__(self):
        pass

    def cosineSimilarity(self, list1: list, list2: list, kwd_num: int) -> float:
        a = np.array(list1)
        b = np.array(list2)
        # use library, operates on sets of vectors
        aa = a.reshape(1, kwd_num)
        ba = b.reshape(1, kwd_num)
        cos_lib = cosine_similarity(aa, ba)
        return cos_lib

    def sparseMatrixPenalty(self, max_limit: int, min_limit: int, x: int):
        return (x-min_limit+1)/(max_limit-min_limit+1)

    def contentSimilarityMatrix(self, keyword_matrix: list, kwd_len: int):
        # the keyword_matrix means the Keyword matrix of different courses
        res = []
        for i, li_i in enumerate(keyword_matrix):
            res.append([])
            for j, li_j in enumerate(keyword_matrix):
                # the result of cosine similarity is typed as np.array, so float it
                sim_ij = self.cosineSimilarity(li_i, li_j, kwd_len)
                res[i].append(round(float(sim_ij), 4))
        return np.array(res)

    def collaborativeSimilarityMatrix(self, sbj_mtx: list, ipt_li = []):
        if ipt_li == []:
            res, sbj_len = [], len(sbj_mtx[0])
            for i, li_i in enumerate(sbj_mtx):
                res.append([])
                for j, li_j in enumerate(sbj_mtx):
                    # the result of cosine similarity is typed as np.array, so float it
                    sim_ij = self.cosineSimilarity(li_i, li_j, sbj_len)
                    res[i].append(round(float(sim_ij), 4))
        else:
            res, sbj_len = [], len(sbj_mtx[0])
            for i, li_i in enumerate(sbj_mtx):
                sim_i = self.cosineSimilarity(ipt_li, li_i, sbj_len)
                res.append(round(float(sim_i), 4))
        return np.array(res)

    def collaborativeInputRecommendation(self, ipt_dict: dict, sbj_mtx: list):
        pass

    # I have pe number of students and each one have selected 12 courses
    def randomGPA(self):
        if not os.path.exists(student_GPA):
            self.generateRandomGPA()  # check if first use, do this function
        else:
            pass

    def generateRandomGPA(self, course_list: list, pe: int, course_num: int) -> list:
        res = []
        for i in range(pe):
            sub_co = sample(course_list, course_num)
            random_GPA = np.random.randint(3, 8, course_num)
            # every member of the student GPA list is a tuple ('course code', mark)
            tmp_dic = dict(zip(sub_co, random_GPA))
            # print(len(sub_co),len(random_GPA),len(tmp_dic))
            res.append(tmp_dic)
        # the result is [[student gpa],[('course code', mark)]...]
        return res

    def subjectMatrixGeneration(self, subject_li: list, gpa_li: list, min_score=3, max_score=7):
        res, subject_num = [], len(subject_li)
        val_li = [0 for n in range(subject_num)]
        for i in gpa_li:
            tmp_dic = dict(zip(subject_li, val_li))
            for j in i: tmp_dic[j] += self.sparseMatrixPenalty(max_score, min_score,i[j])
            tmp_val = list(tmp_dic.values())
            res.append(tmp_val)
        return np.array(res)


class Nlp:
    def __init__(self):
        self.subject_course = []
        self.course_detail = []
        self.raw_keyword_list = []

    def loadCourseCode(self):
        with open(course_code, "rb") as f:
            self.subject_course = pickle.load(f)

    def loadCourseDetail(self):
        with open(course_detail, "rb") as f:
            self.course_detail = pickle.load(f)

    def sentenceSegmentation(self, description: str) -> list:
        en_nlp = stanfordnlp.Pipeline(lang='en')
        en_doc = en_nlp(description)
        res = []
        for i, sent in enumerate(en_doc.sentences):
            for word in sent.words:
                if not word.dependency_relation in ['cc', 'case', 'punct', 'det', 'obl', 'fixed', 'mark', 'aux:pass',
                                                    'aux', 'cop']:
                    if not word.dependency_relation in ['advmod'] and not word.pos in ['RB']:
                        if not word.dependency_relation in ['nsubj'] and not word.pos in ['PRP']: res.append(
                            word.lemma.lower())
                    # print(word.text, word.dependency_relation)
        return res

    def keywordDemonstration(self) -> list:
        self.loadCourseDetail()
        res = []
        for i in self.course_detail:
            tmp = self.sentenceSegmentation(i)
            res.append(tmp)
        self.raw_keyword_list = res
        # de = ['student', 'introduce', 'course', 'study', 'range', 'provide', 'include']
        # self.deleteKeyword(de)
        self.saveRawKeyword()
        return res

    def saveRawKeyword(self):
        with open(raw_keyword, "wb") as f:
            pickle.dump(self.raw_keyword_list, f)

    def loadRawKeyword(self):
        with open(raw_keyword, "rb") as f:
            self.raw_keyword_list = pickle.load(f)

    def keywordGeneration(self) -> list:
        if not os.path.exists(raw_keyword): self.keywordDemonstration()  # check if first use, do this function
        self.loadRawKeyword()
        raw_kw = self.raw_keyword_list
        res_dic = {}
        for i in raw_kw:
            for j in i:
                if j not in res_dic: res_dic[j] = 0  # diction search O(1) is far faster than list O(n)
        res_li = list(res_dic)
        # delete some keywords
        # de = ['student', 'introduce', 'course', 'study', 'range', 'provide', 'include']
        # for i in de: res_li.remove(i)
        return res_li

    def keywordMatrixGeneration(self) -> tuple:
        # use diction to speed up
        res, keyword_num = [], len(self.keywordGeneration())
        val_li = [0 for n in range(keyword_num)]
        for i in self.raw_keyword_list:
            tmp_dic = dict(zip(self.keywordGeneration(), val_li))
            for j in i: tmp_dic[j] += 1
            tmp_val = list(tmp_dic.values())
            res.append(tmp_val)
        # here tmp_dic is like: {'introduction': 0, 'software': 0, 'engineering': 0, 'programming': 0...,
        # which is {'keyword0': int, 'keyword1': int...}
        return np.array(res), keyword_num
