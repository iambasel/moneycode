# stydy pal (your class tracker)
## Video Demo:  <https://youtu.be/2M_kp3GuAu4>
## Description:
this is a web application designed to help student to keep track of their academic courses and how their grades can be done
### dashboard
the main dashboard is used to keep track of the all the studen's courses and what are his grades throughout his term and how he change them
#### current_grading:
this is the sum of all total grades including midterm exam , final exam , course work(quizes, assignemts,labs,etc...)
#### max_possible grading:
this the your goal or what can you possibly reach with your current grade as it calculated from a score of 100 points so
##### example:
if your started a course and then you got in midterm 10 out of 25 then you lost aroung 15 point those points will be subtracted from the 100 points
so you can aim for 85 point
#### hours per week :
this is the number of hours you dedicate each week to study that particular course
#### goal:
this is your north star. in the beginning you decide it as you initila max_ grading is 100 so you can choose form  (A+ till c-)
#### diffculty
this meter help you with seeing if that with current parameter you choose (hours per week and goal) will it be a diffcult challenge
and it is either (diffcult or easy)
### new course:
this is where you register your new courses to be displayed in the dashboard and they are
#### course name
#### hours per week
#### your grades:
for your grades you decide what is the max grade you can get in each exam so later you can compare your current grades against it and this was done this way because diffrent universites have diffrent criteria for exams and how are they graded as in one college a final could contibute 50 points and in another one it can be 70 points.

the rule here that the sum of all grades must equal 100 points which is the standard so if your grades are more than that convert it to be from 100 points
#### goal:
the goal you want at the beginning which will change eventually if you you dropped than its equivlant grades where it descriped in the below image:

![Getting Started](./images/grade.jpg)
### editing a course:
here after you register the course you can add grades while you proceed along the term and changing any grade will affect 3 things:
#### 1. you current grades
#### 2. your max possible grade
#### 3. your goal:
as if your goa was A+ and your max possible grade dropped down less than 97 point that was mentioned in the refrence grades it will drop down to the nex possible goal
but if your goal equvilant grade was less than your max possible grade then it will not change