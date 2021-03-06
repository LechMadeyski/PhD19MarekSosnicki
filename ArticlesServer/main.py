from flask import (
    Blueprint, flash, redirect, render_template, url_for, request, session,
    send_from_directory, send_file)
import os
import json
import logging
import io

from wtforms.validators import InputRequired

from .database.ArticleStatus import ArticleStatus
from AutomatedSearchHelperUtilities.extract_doi_from_csv import extract_doi_from_csv
from ArticlesServer.database.DatabaseManager import DatabaseManager
from .prepare_sections import prepare_sections
from TextSearchEngine.parse_finder import parse_finder
from .database.Status import Status
from .database.UsersDatabase import get_user_database
from .directories import DOIS_FILE, FINDER_FILE, DOIS_TEMP, FINDER_TEMP, PUBLISHER_INPUT_DIRECTORIES_AND_FILE_TYPES, \
    OUTPUT_DIRECTORY
from .database.reload_article import reload_article

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, validators, SelectField, RadioField
from shutil import copyfile
from flask import make_response

main = Blueprint('main', __name__)


@main.route('/')
def index():
    db = DatabaseManager.get_instance()

    user = None
    if session.get('user', None):
        user = session['user']['login']

    if db:
        return render_template('main_with_articles.html', articles=db.get_all_articles_short_info(user))
    else:
        return render_template('main_without_articles.html')


def get_or_create_upload_path():
    uploadFolder = './serverUploads'
    if not os.path.exists(uploadFolder):
        os.makedirs(uploadFolder)
    return uploadFolder


def get_doi_list(doi_list_form):
    doi_list_form.data.save(DOIS_TEMP)
    return extract_doi_from_csv(DOIS_TEMP)


def get_finder_string_from_file(finder_form):
    if finder_form and finder_form.data and finder_form.data.filename:
        finder_form.data.save(FINDER_TEMP)
        try:
            with open(FINDER_TEMP, 'r') as finder_file:
                return finder_file.read()
        except:
            flash('Could not open file '+ str(FINDER_TEMP))
            return None
    else:
        return None


class UploadForm(FlaskForm):
    finder = FileField('finder')
    finder_text = StringField('finder_text')


@main.route('/upload_fider', methods=["GET", "POST"])
def upload_finder():
    form = UploadForm()

    if form.validate_on_submit():
        logger = logging.getLogger('upload_post')
        finder_text = get_finder_string_from_file(form.finder)
        finder = None
        if finder_text is None:
            finder_text = str(form.finder_text.data)
        try:
            logger.info("Parsing finder from : " + finder_text)
            finder = parse_finder(finder_text)
        except ValueError as e:
            flash("Invalid finder text " + str(e))
        if finder is None:
            logger.error('Wrong finder provided')
            return render_template('upload_finder_view.html', form=form)
        logger.info('Properly read doiList and finder')
        with open(FINDER_FILE, 'w') as finder_file:
            finder_file.write(str(finder))
        DatabaseManager.reload_database()
        return redirect(url_for('main.index'))

    current_finder = str()
    if os.path.isfile(FINDER_FILE):
        with open(FINDER_FILE, 'r') as finder_file:
            current_finder = finder_file.read()

    return render_template('upload_finder_view.html', form=form, current_finder=current_finder)


def can_remove_comment(login):
    user = session.get('user', None)
    if user:
        return user['login'] == login
    else:
        return False


def prepare_comments(db, doi_id):
    return [
        dict(text=c['text'],
             comment_id=c['comment_id'],
             user_name=get_user_database().get_full_name(c['user']),
             can_delete=can_remove_comment(c['user'])) for c in db.get_comments(doi_id)]


def prepare_statuses(db, doi_id):
    if session.get('user', None):
        return db.get_statuses(doi_id, session['user']['login'])
    return db.get_statuses(doi_id)


def generate_data_doi_data(db, doi_id):
    article_data = db.get_full_article(doi_id)
    return {
        'doi_id': doi_id,
        'comments': prepare_comments(db, doi_id),
        'statuses': prepare_statuses(db, doi_id),
        'title': article_data.title,
        'doi': article_data.doi,
        'issn': article_data.issn,
        'published_in' : article_data.journal_name,
        'journal_info': article_data.journal_info,
        'publisher_link': article_data.publisher_link,
        'publisher': article_data.publisher,
        'authors': article_data.authors,
        'scopus_link': article_data.scopus_link,
        'doi_link': article_data.doi_link,
        'read_error': article_data.read_error,
        'status' : article_data.status,
        'is_ignored': (article_data.status == ArticleStatus.ARTICLE_IGNORED),
        'has_pdf': article_data.get_pdf_filename() is not None,
        'sections': prepare_sections(article_data)}


class CommentForm(FlaskForm):
    comment = StringField('comment')


@main.route('/doiView/<string:doi_id>', methods=['GET', 'POST'])
def view_doi(doi_id):
    db = DatabaseManager.get_instance()
    if not db:
        return redirect(url_for('main.index'))

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        if not session['user']:
            flash("Please login to comment articles")
        else:
            db.add_comment(doi_id, str(comment_form.comment.data), session['user']['login'])

    comment_form.comment.data = str()

    return render_template(
        "doi_view.html",
        display_data=generate_data_doi_data(db, doi_id),
        comment_form=comment_form)


@main.route('/removeComment/<string:doi_id>')
def remove_comment(doi_id):
    db = DatabaseManager.get_instance()
    db.remove_comment(doi_id, int(request.args.get('comment_id')))
    return redirect(url_for('main.view_doi', doi_id=doi_id))


@main.route('/api/doiView/<string:doi_id>')
def api_doi(doi_id):
    db = DatabaseManager.get_instance()
    if not db:
        return redirect(url_for('main.index'))
    return json.dumps(generate_data_doi_data(db, doi_id))


@main.route('/next/<string:doi_id>')
def next_doi(doi_id):
    db = DatabaseManager.get_instance()
    next = db.get_next_article(doi_id)
    if next:
        return redirect(url_for('main.view_doi', doi_id=next))
    else:
        return redirect(url_for('main.index'))


@main.route('/prev/<string:doi_id>')
def prev_doi(doi_id):
    db = DatabaseManager.get_instance()
    prev = db.get_prev_article(doi_id)
    if prev:
        return redirect(url_for('main.view_doi', doi_id=prev))
    else:
        return redirect(url_for('main.index'))


@main.route('/status/<string:doi_id>')
def change_status(doi_id):
    status = request.args.get('status')
    db = DatabaseManager.get_instance()
    if not db:
        return redirect(url_for('main.index'))

    user = session['user']

    if not user:
        flash('Cannot change status without being logged in')
        return redirect(url_for('main.login'))

    if status == '1':
        db.change_status(doi_id, user['login'], Status.TO_BE_CHECKED)
    elif status == '2':
        db.change_status(doi_id, user['login'],  Status.ACCEPTED)
    elif status == '3':
        db.change_status(doi_id, user['login'],  Status.DECLINED)

    return redirect(url_for('main.view_doi', doi_id=doi_id))

@main.route('/toggle_ignored/<string:doi_id>')
def toggle_ignored(doi_id):
    db = DatabaseManager.get_instance()
    if not db:
        return redirect(url_for('main.index'))
    db.toggle_ignored(doi_id)
    return redirect(url_for('main.view_doi', doi_id=doi_id))


class LoginForm(FlaskForm):
    login = StringField('login')
    password = PasswordField('password')


@main.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = get_user_database().login(login_form.login.data, login_form.password.data)
        if user:
            session['user'] = user
            return redirect(url_for('main.index'))
        else:
            flash('Incorrect credentials')

    return render_template('login.html', form=login_form)


@main.route('/logout')
def logout():
    session['user'] = None
    return redirect(url_for('main.index'))


class RegisterForm(FlaskForm):
    login = StringField('Login')
    full_name = StringField('Name')
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


@main.route('/register', methods = ["GET", "POST"])
def register():
    if session.get('user', None):
        flash('Please logout if you want to register')
        return redirect(url_for('main.index'))

    register_form = RegisterForm()

    if register_form.validate_on_submit():
        register_success = get_user_database().register(register_form.login.data,
                                                        register_form.full_name.data,
                                                        register_form.password.data)
        if register_success:
            flash("Successfully registered new user, please log in")
            return redirect(url_for('main.login'))
        else:
            flash("This login is occupied")

    return render_template('register.html', form=register_form)


@main.route('/results')
def results():

    db = DatabaseManager.get_instance()
    if not db:
        return redirect(url_for('main.index'))

    response = 'DOI;TITLE;AUTHORS;'

    users = get_user_database().users()

    response += ';'.join(users) + '\n'

    articles = db.get_all_articles_id()

    for article_id in articles:
        article_data = db.get_full_article(article_id)
        response += article_data.doi + ';' + article_data.title + ';' + ','.join(article_data.authors) + ';'
        response += ';'.join([str(db.get_status(article_id, user)) for user in users])
        response += '\n'

    output = make_response(response)
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@main.route('/reload/<string:doi_id>')
def reload(doi_id):
    reload_article(doi_id)
    return redirect(url_for('main.view_doi', doi_id=doi_id))


class UploadFileForm(FlaskForm):
    articles_list_file = FileField('File with articles', validators=[
        FileRequired()
    ])


@main.route('/articles_lists', methods=["GET"])
def view_articles_list():

    files_with_categories = dict()
    for name, directory, file_type in PUBLISHER_INPUT_DIRECTORIES_AND_FILE_TYPES:
        files_with_categories[(name, file_type)] = os.listdir(directory)

    return render_template('upload_articles_view.html', form=UploadFileForm(), files_with_categories=files_with_categories)


@main.route('/upload_articles_list/<int:file_type>', methods=['POST'])
def upload_articles_list(file_type):
    form = UploadFileForm()
    if form.validate_on_submit():
        directories = [dir for _, dir, t in PUBLISHER_INPUT_DIRECTORIES_AND_FILE_TYPES if t == file_type]

        if directories:
            filepath = directories[0] + '/' + form.articles_list_file.data.filename
            form.articles_list_file.data.save(filepath)
            DatabaseManager.reload_database()

    return redirect(url_for('main.view_articles_list'))


@main.route('/get_pdf/<string:doi_id>')
def get_pdf(doi_id):
    db = DatabaseManager.get_instance()
    if not db:
        return redirect(url_for('main.index'))

    article_data = db.get_full_article(doi_id)
    pdf_filename = article_data.get_pdf_filename()
    logging.info('Getting pdf for article: ' + doi_id)
    try:
        return send_file(pdf_filename)
    except Exception as error:
        logging.info('Could not find pdf for ' + doi_id)
        logging.error('error is ' + str(error))
        return redirect(url_for('main.view_doi', doi_id=doi_id))



