from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Vocabulary, Result
import random
from . import db
import json #Javascript Object Notation
import datetime

views = Blueprint('views', __name__)

@views.route('/')  # dinfine root page as home
@login_required
def home():
    user_id = current_user.id
    user_voca_no = Vocabulary.query.filter_by(user_id = user_id).count()
    user_vocas = Vocabulary.query.filter_by(user_id = user_id)

    word = []
    for user_voca in user_vocas:
        word.append(user_voca.word)
    word_no = len(set(word))

    return render_template("home.html", user = current_user, user_voca_no = user_voca_no, word_no = word_no) #rendering home page based on current_user inforation

@views.route('/test',methods=['GET','POST'])  # dinfine test page location
@login_required
def test():  #spelling test
    user_id = current_user.id
    user_voca_no = Vocabulary.query.filter_by(user_id = user_id).count() #query db Vocabulary table filter by user id return total count
    user_vocas = Vocabulary.query.filter_by(user_id = user_id) #query db Vocabulary table filter by user id return all entries
    word = []
    for user_voca in user_vocas:
        word.append(user_voca.word) #append word column value in filtered table to a list
    word_no = len(set(word))  # remove duplicate items in the list of word by converting to a set
    testnumber = 0
    test_type = ""
    test_vocas_bank = []
    word_length = ""
    if request.method == 'POST':
        test_type = request.form.get('test_type')
        if test_type not in ['r', 's']:
            flash("Please enter the correct test type!!!", category='error')
            try:
                testnumber = int(request.form.get('test_no_input')) #for checking two error messages at the same time
                testnumber = 0 # the page will not render for test field when test number is zero
            except ValueError:
                flash("Please enter an Integer!!", category='error')
        else:
            if test_type == 'r':
                test_type = "Random Selection"

            else:
                test_type = "Sequential Selection"
            try:
                testnumber = int(request.form.get('test_no_input'))  #checking if an integer is entered
                if test_type == "Random Selection":          #picking voca using random method
                    for i in range(testnumber):
                        random_number = random.randint(1, user_voca_no)
                        random_voca = user_vocas[random_number - 1]
                        test_vocas_bank.append([random_voca.word, random_voca.meaning, random_voca.id])
                    for i in test_vocas_bank:
                        print(i)
                    word_length = len(test_vocas_bank[0][0])
                else:
                    #selecting vocabulary number from last circular selection test
                    user_results = Result.query.filter_by( user_id=user_id, result_test_type="Sequential Selection" )
                    user_results_count = Result.query.filter_by( user_id=user_id, result_test_type="Sequential Selection" ).count()
                    last_voca_id = user_results[user_results_count-1].result_last_voca
                    test_start_position = 0
                    #determine last_cova_id postion in user_vocas
                    for i in range(user_voca_no):
                        if user_vocas[i].id == last_voca_id:
                            test_start_position = i+1
                            break
                    #looping from test_start_postion in list of user_covas for a total of testnumber
                    for i in range(testnumber):
                        test_vocas_bank.append( [user_vocas[test_start_position+i].word, user_vocas[test_start_position+i].meaning, user_vocas[test_start_position+i].id] )
                    for i in test_vocas_bank:
                        print(i)
                    word_length = len(test_vocas_bank[0][0])

            except ValueError:
                flash("Please enter an Integer!!", category='error')

    return render_template("test.html", user = current_user, user_voca_no = user_voca_no, word_no = word_no, testnumber = testnumber, test_vocas_bank=test_vocas_bank, word_length=word_length,test_type=test_type) #rendering home page based on current_user inforation

@views.route('/addition',methods=['GET','POST'])  # dinfine page location
@login_required
def addition(): #adding new word and meaning into database
    user_id = current_user.id
    user_voca_no = Vocabulary.query.filter_by(user_id = user_id).count() #query db Vocabulary table filter by user id return total count
    user_vocas = Vocabulary.query.filter_by(user_id = user_id) #query db Vocabulary table filter by usuer id return all entries
    word = []
    for user_voca in user_vocas:
        word.append(user_voca.word) #append word column value in filtered table to a list
    word_no = len(set(word))  # remove duplicate items in the list of word by converting to a set

    if request.method == 'POST':
        new_word = str(request.form.get('word_input'))
        new_meaning = str(request.form.get('meaning_input'))
        new_entry = Vocabulary(word = new_word, meaning = new_meaning, user_id = user_id) #creating new Vocabulary class entry in the format defined in models
        exist_boolean = bool(
            Vocabulary.query.filter_by( word=new_word, meaning=new_meaning, user_id = user_id ).first() )
        may_exist_boolean = bool(
            Vocabulary.query.filter_by( word=new_word,user_id=user_id ).first() )

        if exist_boolean:
            flash( "This pair of word and meaning already exists. Please check vocabularies" )

        elif may_exist_boolean:
            db.session.add( new_entry )  # adding new entry into data base file imported above
            db.session.commit()  # execute in db
            flash( "New pair of word and meaning has been added to your vocabularies!!  However, this word already exists. Please check any possible duplicate meaning in your vocabularies" )

        else:
            db.session.add( new_entry )  # adding new entry into data base file imported above
            db.session.commit()  # execute in db
            flash( "New pair of word and meaning has been added to your vocabulary!!" )

    return render_template("addition.html", user = current_user, user_voca_no = user_voca_no, word_no = word_no) #rendering home page based on current_user inforation

@views.route('/log-result',methods=['POST'])  # dinfine function to process data from JS into Sqlalchmy
def log_result():
    user_id = current_user.id
    result_detail = json.loads(request.data) #loading javscript data
    result_last_voca = result_detail['lastVocabularyID']
    result_score = result_detail['testScore']
    result_number = result_detail['testNo']
    result_date = result_detail['testDate']
    result_test_type = result_detail['testType']
    result_date = datetime.datetime.strptime( result_date, '%Y-%m-%dT%H:%M:%S.%fZ' ) #converting Json date string back to python date format
    new_result = Result( result_time=result_date, result_score=result_score, result_number = result_number,result_last_voca = result_last_voca, result_test_type = result_test_type, user_id = user_id)
    db.session.add( new_result )  # adding new entry into data base file imported above
    db.session.commit()  # execute in db
    return jsonify({}) #not returning anything

@views.route('/delete-vocabulary',methods=['POST'])  # dinfine function to process data from JS into Sqlalchemy
def delete_vocabulary():
    user_id = current_user.id
    vocabulary_to_delete = json.loads( request.data )  # loading javscript data
    vocabulary_id = vocabulary_to_delete['vocabularyId']
    DBvoca_to_delete = Vocabulary.query.get(vocabulary_id)
    if DBvoca_to_delete: # check database has this voca id
        if DBvoca_to_delete.user_id == user_id:  #check if the current user owns this vocabulary
            db.session.delete(DBvoca_to_delete)  # deleting above query get result in Vacabulary
            db.session.commit()  # execute in db
            return jsonify( {} )  # not returning anything
