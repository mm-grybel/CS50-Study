import os
from flask import Flask, flash, redirect, render_template, request, current_app, url_for, abort
from flask_bootstrap import Bootstrap
from flask_login import login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from models import db, login_manager, setup_db, User, Question, Category
from forms import LoginForm, RegistrationForm, QuestionForm, CategoryForm
from config import config


def create_app(test_db=None):
    # Configure application
    app = Flask(__name__)

    app.config.from_object(config['default'])
    config['default'].init_app(app)

    setup_db(app, test_db)

    bootstrap = Bootstrap()
    bootstrap.init_app(app)

    migrate = Migrate(app, db)

    login_manager.init_app(app)
    login_manager.init_app(app)

    return app


APP = create_app()


@APP.route("/")
def index():
    #return render_template('index.html')
    page = request.args.get('page', 1, type=int)
    pagination = Question.query.order_by(Question.id).paginate(
        page, 
        per_page=current_app.config['QUESTIONS_PER_PAGE'],
        error_out=False)
    questions = pagination.items
    return render_template('questions.html', questions=questions, pagination=pagination)


# ------------------- AUTH -----------------------


@APP.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('index')
            return redirect(next)
        flash('Invalid email or password.')
    return render_template('login.html', form=form)


@APP.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@APP.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now sign in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# ------------------- QUESTIONS ------------------------


@APP.route("/questions")
@login_required
def get_questions():
    page = request.args.get('page', 1, type=int)
    pagination = Question.query.order_by(Question.id).paginate(
        page, 
        per_page=current_app.config['QUESTIONS_PER_PAGE'],
        error_out=False)
    questions = pagination.items
    return render_template('questions.html', questions=questions, pagination=pagination)


@APP.route("/questions/<int:question_id>")
@login_required
def get_question(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('question_details.html', questions=[question])


@APP.route("/questions/add", methods=["GET"])
@login_required
def add_question_form():
    form = QuestionForm()
    return render_template('new_question.html', form=form)


@APP.route("/questions/add", methods=["POST"])
@login_required
def add_question_submission():
    try:
        form = QuestionForm()
        if form.validate_on_submit():
            question = Question(
                question_text = request.form['question_text'],
                answer = request.form['answer'],
                difficulty = request.form['difficulty'],
                category = request.form['category'],
                author = current_user._get_current_object()
            )
            db.session.add(question)
            db.session.commit()
            flash('Your question has been added.')
            return redirect(url_for('get_questions'))
    except:
        flash('An error occurred. Your question could not be added.')
        return redirect(url_for('get_questions'))


@APP.route("/questions/<int:question_id>/edit", methods=["GET"])
@login_required
def edit_question_form(question_id):
    form = QuestionForm()
    question = Question.query.get_or_404(question_id)
    form.question_text.data = question.question_text
    form.answer.data = question.answer
    form.category.data = question.category
    form.difficulty.data = question.difficulty
    return render_template('edit_question.html', form=form, questions=[question])


@APP.route("/questions/<int:question_id>/edit", methods=["POST"])
@login_required
def edit_question_submission(question_id):
    question = Question.query.get_or_404(question_id)

    question.question_text = request.form['question_text']
    question.answer = request.form['answer']
    question.category = request.form['difficulty']
    question.difficulty = request.form['category']

    db.session.add(question)
    db.session.commit()
    flash('The question has been updated.')
    return redirect(url_for('get_question', question_id=question.id))


@APP.route("/questions/search", methods=["POST"])
@login_required
def search_questions():
    data = []
    count = 0

    search_term = request.form.get('search_term', '').lower() # case-insensitive search
    questions = Question.query.all()

    for question in questions:
        current_question = question.question_text.lower()
        if current_question.find(search_term) != -1:
            data.append(question)
            count += 1

    response = {
        "count": count,
        "data": data
    }

    return render_template('search_questions.html', results=response, search_term=request.form.get('search_term', ''))


# ------------------- CATEGORIES -----------------------


@APP.route("/categories")
@login_required
def get_categories():
    categories = Category.query.order_by(Category.id)
    return render_template('categories.html', categories=categories)


@APP.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Question=Question, Category=Category)
