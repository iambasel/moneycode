import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required,usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    id=session["user_id"]
    courses=db.execute("select * from courses where user_id=?",id)
    return render_template("main.html",courses=courses)


@app.route("/login" , methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

    # if method is get show the form return
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was

        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif request.form.get("password")!=request.form.get("confirmation"):
             return apology("password not match", 400)
             # getting a hash to store it in the user's data base
        elif len(rows) == 1:
            return apology("username already taken", 400)

             #TODO
             # make username check with data base

             # inserting the username and his hash in the users data base
        name=request.form.get("username")
        db.execute("INSERT INTO users (username,hash) values (?,?)",name,generate_password_hash(request.form.get("password")))
        return redirect("/")
    else:
        return render_template("register.html")
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
@app.route("/newcourse", methods=["GET", "POST"])
@login_required
def course_register():
    id=session["user_id"]
    if request.method == "POST":
        # request all variables
        course_name=request.form.get("course_name")
        hours= int(request.form.get("hours"))
        mid_term=int(request.form.get("mid_term"))
        final= int(request.form.get("final"))
        course_work=int(request.form.get("course_work"))
        goal=request.form.get("goal")



        #TODO
        if not course_name:
            return apology("must provide course name", 403)
        elif not hours:
            return apology("hours", 403)
        elif not mid_term:
            return apology("mid_term", 403)
        elif not final:
            return apology("final", 403)
        elif not course_work:
            return apology("course work", 403)
        # check the sum of all grades all equal 100
        if (mid_term+final+course_work)>100:
            return apology("your grades are more than 100", 403)
        # diffculty calculations
        # if  i want A+ i must have it more than 3 hours per day then 21 hour per week
        if (goal=="A+") or (goal=="A") or (goal=="A-"):
            if (hours<21):
                diffculty ="diffcult"
            else:
                diffculty ="easy"
                # B+
        if (goal=="B+") or (goal=="B") or (goal=="B-"):
            if (hours<14):
                diffculty ="diffcult"
            else:
                diffculty ="easy"
        if (goal=="C+") or (goal=="C") or (goal=="C-"):
            if (hours<7):
                diffculty ="diffcult"
            else:
                diffculty ="easy"
        # max grading
        max_grading=100
        current_grading=0

        # insert into data base
        db.execute("insert into courses (user_id,course,hour_per_week,goal,max_grading,current_grading,diffculty,mid,final,course_work) values(?,?,?,?,?,?,?,?,?,?)",id,course_name,hours,goal,max_grading,current_grading,diffculty,mid_term,final,course_work)
        return redirect("/")

    else:
        return render_template("newcourse.html")

# editing courses
@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    id=session["user_id"]
    if request.method == "POST":
        course_name=request.form.get("name")
        mid_term =int(request.form.get("mid"))
        final= int(request.form.get("final"))
        course_work=int(request.form.get("course_work"))
        if not course_name:
            return apology("must provide course name", 403)
        # diffrence
        if final == 0:
            final_loss = 0
        else:
            final_loss=40-final
        if mid_term==0:
            mid_loss=0
        else:
            mid_loss=25-mid_term
        if course_work == 0:
            course_work_loss = 0
        else:
            course_work_loss=35-course_work

        max_grading=100-(final_loss + mid_loss + course_work_loss)
        current_grading=(final+mid_term+course_work)
        # new goal based on
        goal=db.execute("select * from courses where user_id=? and course=? ",id,course_name)
        if (max_grading <100 and max_grading>=97 ):
            if (goal[0]["goal"]  in ["A+"] ):
                new_goal="A+"
            else:
             new_goal=goal[0]["goal"]
        elif(max_grading <97 and max_grading>=93):
            if (goal[0]["goal"] in ["A+"]):
                new_goal="A"
            else:
             new_goal=goal[0]["goal"]
        elif(max_grading <93 and max_grading>=87):
            if (goal[0]["goal"] in ["A+","A"]):
                new_goal="A-"
            else:
             new_goal=goal[0]["goal"]
        elif(max_grading <87 and max_grading>=83):
            if (goal[0]["goal"]in ["A+","A","A-"]):
                new_goal="B+"
            else:
             goal=goal[0]["goal"]
        elif(max_grading <83 and max_grading>=79):
            if (goal[0]["goal"] in ["A+","A","A-","B+"]):
                new_goal="B"
            else:
             new_goal=goal[0]["goal"]
        elif(max_grading <79 and max_grading>=76):
            if (goal[0]["goal"] in ["A+","A","A-","B+","B"]):
                new_goal="B-"
            else:
             new_goal=goal[0]["goal"]
        elif(max_grading <76 and max_grading>=73):
            if (goal[0]["goal"] in ["A+","A","A-","B+","B-","B"]):
                new_goal="C+"
            else:
             new_goal=goal[0]["goal"]
        elif(max_grading <73 and max_grading>=70):
            if (goal[0]["goal"] in ["A+","A","A-","B+","B-","B","C+"]):
                new_goal="C"
            else:
             new_goal=goal[0]["goal"]
        elif(max_grading <70 and max_grading>=67):
            if (goal[0]["goal"] in ["A+","A","A-","B+","B-","B","C+","C"]):
                 new_goal="C-"
            else:
                 new_goal="F"
        else:
            new_goal="F"
        # update into data base
        db.execute("update courses set max_grading=?,goal=?,current_grading=? where user_id=? and course =?",max_grading,new_goal,current_grading,id,course_name)
        return redirect("/")

    else:
        courses=db.execute("select * from courses where user_id=?",id)
        return render_template("edit.html",courses=courses)

