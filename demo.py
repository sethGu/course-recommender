### run crawling before use
from models import Nlp, Solutions

nlp, solution = Nlp(), Solutions()
nlp.loadCourseCode()


# content-based recommendation
res = nlp.keywordGeneration()
print(res)
print('number of words: ', len(res))
# print(nlp.raw_keyword_list)

mtx = nlp.matrixGeneration()
sim_mtx = solution.similarityMatrix(mtx)
sim_01 = solution.cosineSimilarity(mtx[0], mtx[1])
print(sim_01, type(sim_01), float(sim_01))
print(nlp.subject_course)
print(sim_mtx)

### user-based recommendation
