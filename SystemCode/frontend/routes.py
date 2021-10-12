from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, login_required, current_user, logout_user

from SystemCode.frontend import app, bcrypt, db
from SystemCode.frontend.forms import SignupForm, LoginForm, SurveyForm
from SystemCode.frontend.models import User, Query, Course, Favourite, Recommendation


default10 = [1,200,300,400,500,600,700,1800,2900,5000]


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    title = 'MOOC Recommender'
    defaultcourselist = []
    for item in default10:
        # Append the course details by courseID
        defaultcourselist.append(Course.query.filter_by(courseID=item).first())
    difficulty = {0: "Beginner", 1: "Intermediate", 2: "Advanced"}
    duration = {0: "Short", 1: "Medium", 2: "Long"}
    free_option = {0: "Paid", 1: "Free"}
    platform = {0: "Edx", 1: "Udemy", 2: "Coursera"}
    for course in defaultcourselist:
        course.difficulty = difficulty.get(course.difficulty, "Unknown")
        course.duration = duration.get(course.duration, "Unknown")
        course.free_option = free_option.get(course.free_option, "Unknown")
        course.platform = platform.get(course.platform, "Unknown")
    return render_template('index.html', title=title,  defaultcourselist=defaultcourselist, index=True)


@app.route('/home')
@login_required
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('/'))
    title = 'MOOC Recommender'
    current_id = current_user.userID
    defaultcourselist = []
    for item in default10:
        # Append the course details by courseID
        defaultcourselist.append(Course.query.filter_by(courseID=item).first())
    difficulty = {0: "Beginner", 1: "Intermediate", 2: "Advanced"}
    duration = {0: "Short", 1: "Medium", 2: "Long"}
    free_option = {0: "Paid", 1: "Free"}
    platform = {0: "Edx", 1: "Udemy", 2: "Coursera"}
    fav_query = Favourite().query.filter_by(userID=current_id)
    favlist = []
    for item in fav_query:
        favlist.append(item.courseID)
    for course in defaultcourselist:
        course.difficulty = difficulty.get(course.difficulty, "Unknown")
        course.duration = duration.get(course.duration, "Unknown")
        course.free_option = free_option.get(course.free_option, "Unknown")
        course.platform = platform.get(course.platform, "Unknown")
    return render_template('index.html', title=title, defaultcourselist=defaultcourselist, favlist=favlist, home=True)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    title = 'User sign up'
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=name, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Successfully registered!', category='success')
        return redirect(url_for('home'))
    return render_template('signup.html', form=form, title=title, signup=True)


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
            login_user(user, remember=remember)
            flash('Login successful. Welcome back!', category='info')
            if request.args.get('next'):
                next_page = request.args.get('next')
                return redirect(next_page)
            return redirect(url_for('home'))
        flash('User not exists or password not match', category='danger')
    return render_template('login.html', title=title, form=form, login=True)


@app.route('/query', methods=['GET', 'POST'])
def preferences():
    title = 'Personalized course recommendations'
    form = SurveyForm()
    if form.validate_on_submit():
        current_id = current_user.userID
        count = Query.query.filter_by(userID=current_id).order_by(Query.query_count.desc()).first()
        if count is None:
            query_count = 0
        else:
            query_count = int(count.query_count)
        query_text = form.topic.data
        query_duration = form.duration.data
        query_difficulty = form.difficulty.data
        query_free_option = form.freePaid.data
        query = Query(userID=current_id, query_count=query_count+1, query_text=query_text,
                      query_duration=query_duration, query_difficulty=query_difficulty,
                      query_free_option=query_free_option)
        db.session.add(query)
        db.session.commit()
        flash('Got your preferences!', category='success')
        return redirect(url_for('results'))
    return render_template('query.html', form=form, title=title, preferences=True)


@app.route('/results', methods=['GET', 'POST'])
def results():
    current_id = current_user.userID
    recommendations = Recommendation().query.filter_by(userID=current_id).order_by(Recommendation.query_count.desc()).\
        order_by(Recommendation.ranking.asc())
    rec_list = []
    for item in recommendations:
        # Append the course details by courseID
        rec_list.append(Course.query.filter_by(courseID=item.courseID).first())
    difficulty = {1: "Beginner", 2: "Intermediate", 3: "Advanced"}
    duration = {1: "Short", 2: "Medium", 3: "Long"}
    free_option = {0: "Paid", 1: "Free"}
    platform = {0: "Edx", 1: "Udemy", 2: "Coursera"}
    fav_query = Favourite().query.filter_by(userID=current_id)
    favlist = []
    for item in fav_query:
        favlist.append(item.courseID)
    for course in rec_list:
        course.difficulty = difficulty.get(course.difficulty, "Unknown")
        course.duration = duration.get(course.duration, "Unknown")
        course.free_option = free_option.get(course.free_option, "Unknown")
        course.platform = platform.get(course.platform, "Unknown")
    return render_template('results.html', rec_list=rec_list, favlist=favlist)


@app.route('/favourites', methods=['GET', 'POST'])
def favourites():
    title = 'My favourited courses'
    current_id = current_user.userID
    fav_query = Favourite().query.filter_by(userID=current_id)
    fav_list = []
    for item in fav_query:
        fav_list.append(Course.query.filter_by(courseID=item.courseID).first())
    difficulty = {0: "Beginner", 1: "Intermediate", 2: "Advanced"}
    duration = {0: "Short", 1: "Medium", 2: "Long"}
    free_option = {0: "Paid", 1: "Free"}
    platform = {0: "Edx", 1: "Udemy", 2: "Coursera"}
    for course in fav_list:
        course.difficulty = difficulty.get(course.difficulty, "Unknown")
        course.duration = duration.get(course.duration, "Unknown")
        course.free_option = free_option.get(course.free_option, "Unknown")
        course.platform = platform.get(course.platform, "Unknown")
    return render_template('favourites.html', title=title, fav_list=fav_list)


@app.route('/history', methods=['GET'])
def history():
    title = 'My past searches'
    current_id = current_user.userID
    history_queries = Query().query.filter_by(userID=current_id).order_by(Query.query_count.desc())
    # if len(historySearches) > 5:
    #    historySearches = historySearches[0:5]
    query_free_option = {0: "Free and paid courses", 1: "Only free courses"}
    query_difficulty = {0: "Any", 1: "Beginner", 2: "Intermediate", 3: "Advanced"}
    query_duration = {0: "Any", 1: "Short", 2: "Medium", 3: "Long"}
    for query in history_queries:
        query.query_difficulty = query_difficulty.get(query.query_difficulty, "Unknown")
        query.query_duration = query_duration.get(query.query_duration, "Unknown")
        query.query_free_option = query_free_option.get(query.query_free_option, "Unknown")
    return render_template('history.html', title=title, history_queries=history_queries)


@app.route('/history/<int:query_count>', methods=['GET'])
def displaypastresult(query_count):
    title = 'My past searches'
    current_id = current_user.userID
    query_result = Recommendation().query.filter_by(userID=current_id).filter_by(query_count=query_count)
    query_result_list = []
    for item in query_result:
        # Append the course details by courseID
        query_result_list.append(Course.query.filter_by(courseID=item.courseID).first())
    free_option = {0: "Paid", 1: "Free"}
    platform = {0: "Edx", 1: "Udemy", 2: "Coursera"}
    difficulty = {0: "Any", 1: "Beginner", 2: "Intermediate", 3: "Advanced"}
    duration = {0: "Any", 1: "Short", 2: "Medium", 3: "Long"}
    for course in query_result_list:
        course.difficulty = difficulty.get(course.difficulty, "Unknown")
        course.duration = duration.get(course.duration, "Unknown")
        course.free_option = free_option.get(course.free_option, "Unknown")
        course.platform = platform.get(course.platform, "Unknown")
    fav_query = Favourite().query.filter_by(userID=current_id)
    favlist = []
    for item in fav_query:
        favlist.append(item.courseID)
    return render_template('results.html', title=title, query_count=query_count, rec_list=query_result_list,
                           favlist=favlist)


@app.route('/likeunlike', methods=['POST', 'GET'])
def likeunlike():
    current_id = current_user.userID
    if request.method == 'POST':
        course_id = request.form['course_id']
        req_type = request.form['type']
        print(current_id)
        print(req_type)
        print(course_id)
        entry = Favourite(userID=current_id, courseID=course_id)
        if req_type == '1':
            db.session.add(entry)
            db.session.commit()
        if req_type == '0':
            entry = Favourite.query.filter_by(userID=current_id, courseID=course_id).first()
            db.session.delete(entry)
            db.session.commit()
    return jsonify('Success')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
