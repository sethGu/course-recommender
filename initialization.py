import stanfordnlp
# stanfordnlp.download('en')

### run crawling before use
from models import Nlp, Solutions

nlp, solution = Nlp(), Solutions()
nlp.loadCourseCode()


### content-based recommendation
kwd = nlp.keywordGeneration()

# The variable kwd_mtx is the number of times keywords appear in different courses, len(kwd_mtx)=course number,
# len(mtx[0])=keyword number.    The kwd_num is just the length of keyword.
kwd_mtx, kwd_num = nlp.keywordMatrixGeneration()
kwd_sim_mtx = solution.contentSimilarityMatrix(kwd_mtx, kwd_num)
# print(kwd_mtx)


### user-based recommendation
course_li = list(set(nlp.subject_course))
# the variables of the gpa are (course list, number of student, number of courses each student select)
gpa = solution.generateRandomGPA(course_li, 30, 16)
sbj_mtx = solution.subjectMatrixGeneration(course_li, gpa)
sbj_sim_mtx = solution.collaborativeSimilarityMatrix(sbj_mtx)
print(gpa)

# find a set of the most similar student, give a recommendation which is highest score
student_input = [{'COMU1140': 3, 'BIOL2202': 4, 'COMP3702': 7, 'DECO1400': 7}]
input_mtx = solution.subjectMatrixGeneration(course_li, student_input)
input_sbj_sim = solution.collaborativeSimilarityMatrix(sbj_mtx, input_mtx)
print(input_sbj_sim)