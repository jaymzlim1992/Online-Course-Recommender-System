from flask import render_template, flash, redirect, url_for, request,jsonify
from flask_login import login_user, login_required, current_user, logout_user

from app import app,bcrypt,db
from app.forms import SignupForm, LoginForm, SurveyForm
from app.models import User, Preference, Course, Favourites, Recommendations

default10 = [1,200,300,400,500,600,700,1800,2900,5000]

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    title = 'MOOC Recommender'
    defaultCourseList = []
    for item in default10:
        # Append the course details by courseId
        defaultCourseList.append(Course.query.filter_by(courseId=item).first())
    difficulty = {0: "Beginner", 1: "Intermediate", 2: "Advanced"}
    duration = {0: "Short", 1: "Medium", 2: "Long"}
    freeOption = {0: "Paid", 1: "Free"}
    platform = {0: "Edx", 1: "Udemy", 2: "Coursera"}
    for course in defaultCourseList:
        course.difficulty = difficulty.get(course.difficulty, "Unknown")
        course.duration = duration.get(course.duration, "Unknown")
        course.freeOption = freeOption.get(course.freeOption, "Unknown")
        course.platform = platform.get(course.platform, "Unknown")
    return render_template('index.html', title=title,  defaultCourseList=defaultCourseList, index=True)

@app.route('/home')
@login_required
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('/'))
    title = 'MOOC Recommender'
    id = current_user.id
    defaultCourseList = []
    for item in default10:
        #Append the course details by courseId
        defaultCourseList.append(Course.query.filter_by(courseId=item).first())
    difficulty = {0:"Beginner", 1:"Intermediate",2:"Advanced"}
    duration = {0:"Short", 1:"Medium", 2:"Long"}
    freeOption = {0:"Paid", 1:"Free"}
    platform = {0:"Edx", 1:"Udemy", 2:"Coursera"}
    favourites = Favourites().query.filter_by(id=id)
    favList = []
    for item in favourites:
        favList.append(item.courseId)
    for course in defaultCourseList:
        course.difficulty = difficulty.get(course.difficulty, "Unknown")
        course.duration = duration.get(course.duration, "Unknown")
        course.freeOption = freeOption.get(course.freeOption, "Unknown")
        course.platform = platform.get(course.platform, "Unknown")
    return render_template('index.html', title=title, defaultCourseList=defaultCourseList, favList=favList, home=True)

@app.route('/signup', methods=['GET','POST'])
def signup():
    title = 'User sign up'
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=name, username=username,password=password)
        db.session.add(user)
        db.session.commit()
        flash('Successfully registered!', category='success')
        return redirect(url_for('home'))
    return render_template('signup.html',form=form,title=title,signup=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'User login'
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember = remember)
            flash('Login successful. Welcome back!', category='info')
            if request.args.get('next'):
                next_page =request.args.get('next')
                return redirect(next_page)
            return redirect(url_for('home'))
        flash('User not exists or password not match', category='danger')

    return render_template('login.html', title=title, form=form, login=True)

@app.route('/preferences', methods=['GET','POST'])
def preferences():
    title = 'Personalized course recommendations'
    form = SurveyForm()
    if form.validate_on_submit():
        id = current_user.id
        count = Preference.query.filter_by(id=id).order_by(Preference.searchCount.desc()).first()
        if count == None:
            searchCount = 0
        else:
            searchCount = int(count.searchCount)
        topic = form.topic.data
        duration = form.duration.data
        difficulty = form.difficulty.data
        freePaid = form.freePaid.data
        preference = Preference(id=id, searchCount=searchCount+1, topic=topic,duration=duration,difficulty=difficulty,freePaid=freePaid)
        db.session.add(preference)
        db.session.commit()
        flash('Got your preferences!', category='success')
        return redirect(url_for('results'))
    return render_template('preferences.html',form=form,title=title,preferences=True)

@app.route('/results', methods=['GET','POST'])
def results():
    id = current_user.id
    recommendations = Recommendations().query.filter_by(id=id).order_by(Recommendations.searchCount.desc()).order_by(
        Recommendations.ranking.asc())
    recCourseList = []
    for item in recommendations:
        # Append the course details by courseId
        recCourseList.append(Course.query.filter_by(courseId=item.courseId).first())
    difficulty = {1: "Beginner", 2: "Intermediate", 3: "Advanced"}
    duration = {1: "Short", 2: "Medium", 3: "Long"}
    freeOption = {0: "Paid", 1: "Free"}
    platform = {0: "Edx", 1: "Udemy", 2: "Coursera"}
    favourites = Favourites().query.filter_by(id=id)
    favList = []
    for item in favourites:
        favList.append(item.courseId)
    for course in recCourseList:
        course.difficulty = difficulty.get(course.difficulty, "Unknown")
        course.duration = duration.get(course.duration, "Unknown")
        course.freeOption = freeOption.get(course.freeOption, "Unknown")
        course.platform = platform.get(course.platform, "Unknown")
    return render_template('results.html', recCourseList=recCourseList, favList=favList)

@app.route('/favourites', methods=['GET','POST'])
def favourites():
    title = 'My favourited courses'
    id = current_user.id
    favourites = Favourites().query.filter_by(id=id)
    favCourseList = []
    for item in favourites:
        favCourseList.append(Course.query.filter_by(courseId=item.courseId).first())
    difficulty = {0:"Beginner", 1:"Intermediate",2:"Advanced"}
    duration = {0:"Short", 1:"Medium", 2:"Long"}
    freeOption = {0:"Paid", 1:"Free"}
    platform = {0:"Edx", 1:"Udemy", 2:"Coursera"}
    for course in favCourseList:
        course.difficulty = difficulty.get(course.difficulty, "Unknown")
        course.duration = duration.get(course.duration, "Unknown")
        course.freeOption = freeOption.get(course.freeOption, "Unknown")
        course.platform = platform.get(course.platform, "Unknown")
    return render_template('favourites.html',title = title, favCourseList = favCourseList)

@app.route('/history', methods=['GET'])
def history():
    title = 'My past searches'
    id = current_user.id
    historySearches = Preference().query.filter_by(id=id).order_by(Preference.searchCount.desc())
    #if len(historySearches) > 5:
    #    historySearches = historySearches[0:5]
    freePaid = {0: "Free and paid courses", 1: "Only free courses"}
    difficulty = {0:"Any", 1: "Beginner", 2: "Intermediate", 3: "Advanced"}
    duration = {0:"Any", 1: "Short", 2: "Medium", 3: "Long"}
    for search in historySearches:
        search.difficulty = difficulty.get(search.difficulty, "Unknown")
        search.duration = duration.get(search.duration, "Unknown")
        search.freePaid = freePaid.get(search.freePaid, "Unknown")
    return render_template('history.html', title=title, historySearches=historySearches)

@app.route('/history/<int:searchCount>', methods=['GET'])
def displayPastResult(searchCount):
    title = 'My past searches'
    id = current_user.id
    searchResult = Recommendations().query.filter_by(id=id).filter_by(searchCount=searchCount)
    searchResultDetails = []
    for item in searchResult:
        # Append the course details by courseId
        searchResultDetails.append(Course.query.filter_by(courseId=item.courseId).first())
    freeOption = {0: "Paid", 1: "Free"}
    platform = {0: "Edx", 1: "Udemy", 2: "Coursera"}
    difficulty = {0:"Any", 1: "Beginner", 2: "Intermediate", 3: "Advanced"}
    duration = {0:"Any", 1: "Short", 2: "Medium", 3: "Long"}
    for course in searchResultDetails:
        course.difficulty = difficulty.get(course.difficulty, "Unknown")
        course.duration = duration.get(course.duration, "Unknown")
        course.freeOption = freeOption.get(course.freeOption, "Unknown")
        course.platform = platform.get(course.platform, "Unknown")
    favourites = Favourites().query.filter_by(id=id)
    favList = []
    for item in favourites:
        favList.append(item.courseId)
    return render_template('results.html', title=title, searchCount=searchCount, recCourseList=searchResultDetails,favList=favList)

@app.route('/likeunlike',methods=['POST','GET'])
def likeunlike():
    id = current_user.id
    if request.method=='POST':
        course_id=request.form['course_id']
        type=request.form['type']
        print(id)
        print(type)
        print(course_id)
        entry = Favourites(id=id,courseId=course_id)
        if type=='1':
            db.session.add(entry)
            db.session.commit()
        if type=='0':
            entry= Favourites.query.filter_by(id=id,courseId=course_id).first()
            db.session.delete(entry)
            db.session.commit()
    return jsonify('Success')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
