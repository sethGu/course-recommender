# UQcourseRecommendation
This one significant part of Citizen-centric Smart Campus, which is the second section (3 for all) I have done in my project. The scripts are divided into crawling (which you can see in a public repository https://github.com/sethGu/UQcourselistCrawling) and recommendation part. In recommendation part, I did not build an interaction interface because ALL of the algorithms and functions in the models are for recommendation system services. All the route is adjusted to the relative route which you can use directly after download or clone. All this work are using hard coding except the usage of StanfordNlp.

## Matters need attention
Since this is a private repository, you see this page means you are a member/grader of Mr. Junquan Gu and Dr. Peter Worthy's Citizen-centric smart campus research.   
The initialization.py is the main script that you can use for recommendation algorithms checking. The demo.py is currently empty because there are no needs to build a interactive interface for this course recommendation section. If this section was significant or indepently matters as a research direction, the demo will be developed at that moment. Thus, this section is just one attempt for course recommendation basiclly relying on collaborative-based filtering and content-based filtering.   
The section of collaborative filtering is developed by trying generating a random GPA data because I failed to have access to any student GPA data not even in UQ or internet.

## How to use
PyCharm is highly recommended here, other IDE is also fine.   
Download or clone this repository, run initialization.py first. Then check the variable based on the naming hints and the comment line. Use print($variable$) to see the results.

## Recommendation principle
#### content-based filtering
The content of each course is the course description in the UQ ECP page (here use UQ course selection page as an example). After course description crawling, We get a list like [course_description1, course_description2 ...]. Then StanfordNlp is used to cut the description sentences into words. So it should be like: keywords generation ==> stem extraction ==> keyword duplicates removement.
Then each of the course has its own keywords list so the big list is like [[keyword1, keyword5...],[keyword2, keyword3...]...] and the overall keyword list is like [keyword1, keyword2...].   
The next step is sparse matrix generation which turn the big list into sparse matrix which take keyword(n) into 1 if exists or 0 if not exists. So if the number of the keyword list is n = len(keyword_list), then sparse_matrix is like [[1,0,0,0,1...], [0,1,1...], ...] while its length equals to the course number and the length of each of its member sparse_matrix[i] equals to the keyword number.    
Similarity can be used now as we get the sparse matrix. In release v0.0.2 the similarity matrix is calculated by cosine similarity. The similarity calculation will be added other methods like Pearson similarity in later release.   
After we get the similarity, the core idea is almost there, which is we can let the students to choose a course whose content is overlapping with their previous selected course.    
This move makes the students have more possibility to keep up with the course and achieve a higher mark because the course they learn has similiar content with their previous knowledge. It is not only about getting higher mark, but also helping students to focusing on one specific direction (e.g. to become data scientist by recommending statistic and machine learning, to become web developer by recommending cloud computing and web information system...).

#### collaborative-basd filtering
This approach is mainly about using collaborative (here other students' gpa information) to give students best options in the courselist.   
Here the first few steps are similar with the content-based filtering including generating the big list and sparse matrix. I still take i.th student as row and the course grade as column (feature). However, the big list is like [{'course': mark; 'course': mark;...},{...}...] here.    
Besides, I use a proportionality coefficient to measure one student's mastery of the course. This is like [[1, 0, 0.8, 0, 0.4...],[0, 0, 0.6, 1, 0...]...] which 0 represents this student did not choose this course and 0-1 represents his grade in this course (i.e. if the GPA gap is 3-7 <==> {3,4,5,6,7} and one student get a [4, 6] so it should be [0.4, 0.8]). Based on this, the sparse matrix is more meaningful and take student's scores into account.     
Finally, if we get a student whoes GPA is [{'COMU1140': 3, 'BIOL2202': 4, 'COMP3702': 7, 'DECO1400': 7}] which is the initialization.py case, we can calculate the most N-similar-student with him/her, and look at the high-score course that selected by the similar student.
Feel free to have a play with initialization.py.

## Further work
Email junquan.gu@uqconnect.edu.au or find Dr. Peter Worthy for help and coorperation.
