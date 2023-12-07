#general installs
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
app = Flask(__name__, template_folder="templates", static_folder='static')
app.secret_key = '123'

#questions for the quiz in a tuple
questions = ("What is the Scientific Distinction between frogs and toads?","Which group is most closely related to birds?","What is the largest shark?",
    "What group do salamanders belong to?", "What does Neotenic mean?", "How many species of penguin are there?","What are traits of mammals?",
    "Which deer species do both genders grow antlers?", "Which of these isn't a marsupial?","Which bird is not apart of the waterfowl family?")
#the choices for the quiz in a multi layered tuple
options = (("Hind legs", "Skin texture","Colour", "There isn't one"),
    ("Crocodillians", "Humans", "Snakes", "Frogs"),
    ("Tiger Shark", "Great White Shark", "Whale Shark", "Thresher Shark"),
    ("Lizards", "Amphibians", "Snakes", "Fish"),
    ("Retain Juevinile characteristics as adults", "Are able to regrow limbs", "Can shed their tail", "Do not have eyelids"),
    ("55", "10", "17", "32"),
    ("High metabolic rate", "hair", "Heterodont teeth", "all of the above"),
    ("White tail", "Caribou", "Moose", "Elk"),
    ("Cats", "Koala", "Possum", "Kangaroo"),
    ("Geese","Duck","Hummingbird","Swan"))
#Tuple for the answers
answers = ("D","A","C","B","A","C","D","B","A","C")
#Tuple for the secret quiz questions
secretquestions =("Who Made the first computer?", "Who is Luffys right hand man in the anime one piece?", "What NFL teams colors are Green and Gold/Yellow?", 
"Whos the main character in breaking bad?", "What year was the declaration of independence signed?", "What Game series is Master Cheif originally from?",
"How many Canadian providences are there?", "What is the Capital of Illinois?", "Which planet in the solar system is closest to Earth in size?",
"Who is the coolest Teacher?")
#Tuple for the secret quiz options
secretoptions = (("Charles Babbage", "Aaron Jones", "Thomas Ediison", "John Smith"),
("Sanji", "Jinbei", "Zoro", "Ace"),
("New England Patriots","Seattle Seahawks","Green Bay Packers", "Dallas Cowboys"),
("Skylar White", "Skinny Pete", "Gus Fring", "Walter White"),
("1492","1776","1755","1816"),
("Halo","Doom","Rainbow Six Seige","Fotnite"),
("12","13","9","10"),
("Hartford", "Springfeild", "Chicago", "Granby"),
("Mercury","pluto","Venus","Mars"),
("Mrs.Romanenko","Mr.Smith","Mrs.Holly","Mr.West"))
#tuple for secret quiz answers
secretanswers=("A","C","C","D","B","A","D","B","C","A")


#My general app routing functions
@app.route("/")
def home():
    return render_template("home.html", valid='')

@app.route("/results")
def results():
    if session['course'] =='animal world' or session['course'] == 'Animal World' or session['course'] == 'Animal world' or session['course'] == 'animal World':
        session['questions'] = questions
        session['answers'] = answers
        return render_template("results.html", question = questions)
    elif session['course'] =='Secret' or session['course'] == 'secret':
        session['questions'] = secretquestions
        session['answers'] = secretanswers
        return render_template("results.html", question = secretquestions)
    

@app.route("/quiz")
def quiz():
    if  session['course'] =='animal world' or session['course'] == 'Animal World' or session['course'] == 'Animal world' or session['course'] == 'animal World':
        return render_template("quiz.html", questions = questions, options = options)
    elif session['course'] =='Secret' or session['course'] == 'secret':
        return render_template("quiz.html", questions = secretquestions, options = secretoptions)
    

# The more complicated routing functions I kept them seperate for easier development, this function gets the name and course enetered and determines if its valid and will then load up the quiz
@app.route("/",  methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        session['name'] = name
        course = request.form['course']
        session['course'] = request.form['course']
        if course =='animal world' or course == 'Animal World' or course == 'Animal world' or course == 'animal World'and session['name'] != "":
            return redirect(url_for("quiz"))
        elif course == "Secret" or course =="secret" and session['name'] != "":
            return redirect(url_for("quiz"))
        elif name == "":
            return render_template("home.html", valid = "Enter a Name")
        else: 
            return render_template("home.html", valid = "Course entered dosen't have a quiz")

#Function that gets the guesses from the quiz and puts them in a list it also calls the two classes calcscore() and calcguesses()
@app.route("/quiz", methods=['GET', 'POST']) 
def submittest():
    guesses=[]
    test = ''
    if request.method =='POST':
        if session['course'] =='animal world' or session['course'] == 'Animal World' or session['course'] == 'Animal world' or session['course'] == 'animal World':
            for i in range(len(answers)):
                try:
                    guesses.append(request.form[str(i+1)])
                except:
                    guesses.append("Blank")
        

            my_quiz = calcscore(guesses, answers)
            my_quiz.calccorrect()
            my_quiz.performance()

            my_results = calcguesses(guesses, answers, options)
            my_results.getcorrectness()
            my_results.getguess()
            my_results.getcorrect()
        elif session['course'] == "Secret" or session['course'] =="secret":
             for i in range(len(secretanswers)):
                try:
                    guesses.append(request.form[str(i+1)])
                except:
                    guesses.append("Blank")
             my_quiz = calcscore(guesses, secretanswers)
             my_quiz.calccorrect()
             my_quiz.performance()

             my_results = calcguesses(guesses, secretanswers, secretoptions)
             my_results.getcorrectness()
             my_results.getguess()
             my_results.getcorrect()
        session['guesses'] = guesses
        return redirect(url_for('results'))

#Calculates the score on gotten on the quiz and it evaluates your performance
class calcscore():
    def __init__(self, guesses, answers):
        self.guesses = guesses
        self.answers = answers
        self.count=0
    def calccorrect(self):
        for i in range(len(self.answers)):
            if self.guesses[i] == self.answers[i]:
                self.count = self.count + 1
        session['correct'] = self.count
    def performance(self):
        if self.count == 10:
            session['performance'] = 'Perfect score'
        elif self.count >= 7:
            session['performance'] = 'Congratulations'
        elif self.count >= 5:
            session['performance'] = 'Good job'
        elif self.count >= 1:
            session['performance'] = 'Better luck next time'
        else:
            session['performance'] = 'You beat the odds and got a zero'

#Calculates your guesses deciding if they are individually correct or incorrect and it also returns what you guessed
class calcguesses():
    def __init__(self, guesses, answer, option):
        self.guesses= guesses
        self.answers = answer
        self.options = option
        self.check = []
        self.guess = []
        self.correctanswer= []
    def getcorrect(self):
        for i in range(len(self.answers)):
            if self.answers[i] == 'A':
                    self.correctanswer.append(self.options[i][0])
            elif self.answers[i] == 'B':
                    self.correctanswer.append(self.options[i][1])
            elif self.answers[i] == 'C':
                    self.correctanswer.append(self.options[i][2])
            elif self.answers[i] == 'D':
                    self.correctanswer.append(self.options[i][3])
        session['correctanswers'] = self.correctanswer
    def getguess(self):
        for i in range(len(self.guesses)):
            if self.guesses[i] == 'A':
                self.guess.append(self.options[i][0])
            elif self.guesses[i] == 'B':
                self.guess.append(self.options[i][1])
            elif self.guesses[i] == 'C':
                self.guess.append(self.options[i][2])
            elif self.guesses[i] == 'D':
                self.guess.append(self.options[i][3])
            else:
                self.guess.append("didn't guess")
            session['guessmade'] = self.guess
    def getcorrectness(self):
        for i in range(len(self.guesses)):
            if self.answers[i] == self.guesses[i]:
                self.check.append('correct')
            else:
                self.check.append('incorrect:')
            session['check'] = self.check

        

#main function implements txt file explaining project
if __name__=='__main__':
    with open("projectsummary.txt", "r") as f:
        lines=f.readlines()
        print(lines)  
    app.run(debug = True)

  
    














