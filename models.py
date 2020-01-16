import pickle
import stanfordnlp
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

np.set_printoptions(threshold=np.inf)   # print the whole matrix

course_code = "crawling/courseCode.pickle"
course_detail = "crawling/courseDetail.pickle"
raw_keyword = "rawKeyWord.pickle"


class Solutions:
    def __init__(self):
        pass

    def cosineSimilarity(self, list1: list, list2: list) -> float:
        a = np.array(list1)
        b = np.array(list2)
        # use library, operates on sets of vectors
        aa = a.reshape(1, 981)
        ba = b.reshape(1, 981)
        cos_lib = cosine_similarity(aa, ba)
        return cos_lib

    def similarityMatrix(self, keyword_matrix: list):
        res = []
        for i, li_i in enumerate(keyword_matrix):
            res.append([])
            for j, li_j in enumerate(keyword_matrix):
                sim_ij = self.cosineSimilarity(li_i, li_j)
                res[i].append(round(float(sim_ij), 4))
        m = np.matrix(res)
        return m

    # I have 10,000 stundents and each one have selected 12 courses
    def randomGPA(self):
        pass


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

    def matrixGeneration(self) -> list:
        # use diction to speed up
        res, keyword_num = [], len(self.keywordGeneration())
        val_li = [0 for n in range(keyword_num)]
        # res.append(self.subject_course)
        for i in self.raw_keyword_list:
            tmp_dic = dict(zip(self.keywordGeneration(), val_li))
            for j in i: tmp_dic[j]+=1
            tmp_val = list(tmp_dic.values())
            res.append(tmp_val)
        m = np.matrix(res)
        print(tmp_dic)
        # print(tmp_val)
        # print(res)
        # print(m.T)
        return m
