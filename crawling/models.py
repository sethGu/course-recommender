import pickle

course_code = "courseCode.pickle"
course_detail = "courseDetail.pickle"


class Solutions:
    def __init__(self):
        self.subject_course = []
        self.course_detail = []

    def getCourseCode(self, li: list):
        if not li: return
        res = []
        for i in li:
            tmp = i[12:20]
            res.append(tmp)
        self.subject_course = res
        return res

    def saveCourseCode(self):
        with open(course_code, "wb") as f:
            pickle.dump(self.subject_course, f)

    def getCourseDetail(self, s: str):
        if not s: return
        self.course_detail.append(s)
        return

    def saveCourseDetail(self):
        with open(course_detail, "wb") as f:
            pickle.dump(self.course_detail, f)

    def loadCourseCode(self):
        with open(course_code, "rb") as f:
            self.subject_course = pickle.load(f)

    def loadCourseDetail(self):
        with open(course_detail, "rb") as f:
            self.course_detail = pickle.load(f)

    def deleteSubsequentText(self, s: str, target: str) -> str:
        idx = self.strStr(s, target)
        s = s[:idx]
        return s

    def deletePreviousText(self, s: str, target: str) -> str:
        idx = self.strStr(s, target)
        s = s[idx:]
        return s

    def strStr(self, haystack: str, needle: str) -> int:
        if needle not in haystack: return -1
        return haystack.index(needle)

    def deleteOccationalBasis(self, li: list):
        for i in li:
            self.subject_course.remove(i)
