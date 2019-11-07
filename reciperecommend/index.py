"""
@author: xueying peng
"""
import json
from flask_login import LoginManager
from flask_login import login_user, login_required,current_user
from . import connsql,connmongodb
from constraint import *
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY']='234324234'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://recipeadm:1234@localhost:3306/recipe_recommendation"
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config["MONGO_URI"]="mongodb://localhost:27017/recipe"
connmongodb.mongo.init_app(app)
connsql.db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'
login_manager.init_app(app)

global_var = [""]  # 定义一个全局变量，存在相应的值
def set_var(var):
    global_var[0] = var
    return ""
def get_var():
    return global_var[0]


app.add_template_global(set_var, 'set_var')
app.add_template_global(get_var, 'get_var')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('newindex.html')
@app.route('/chooseflavour',methods=['GET', 'POST'])
def choose_flavor():
    email = current_user.email
    character = connsql.user_character.query.filter(connsql.user_character.email == email).first()
    if character:
        standard = nutrition(character.age,character.weight, character.height, character.gender, character.activity)
        print (standard)
        #choice=request.form["choosedrecipe"]
        #print (choice)
        flavour = character.flavour
        height = character.height
        weight = character.weight
        recipe=connmongodb.getSatisifiedRecipe()
        print (request.form)
        #a=request.form
        choice = int(request.form['choosedrecipe'])
        print (global_var[0])
        recipe=list(global_var[0]['recipe'][choice])
        for i in range(len(recipe)):
            recipe[i]=list(recipe[i])
            lst=recipe[i][2][2:-2]
            ind=0
            arr=[]
            while i<len(lst):
                if lst[i]=="'":
                    arr.append(lst[ind:i])
                    i+=4
                    ind=i
                i+=1
            #arr = recipe[i][2].split("\\")
            #arr=list(lst)
            recipe[choice].append(arr)
            recipe[choice][2]=arr
        print ((recipe[0][4],recipe[0][0],recipe[0][1]))

            #x[2]=json.load(x[2])
        return render_template('recipeRecommend.html', entries=recipe,error=None)
    return render_template('newindex.html')

@app.route('/fill_info',methods=['GET','POST'])
def fill_info():
    if request.method == 'POST':
        email= current_user.email
        print (email)
        flavour = request.form['flavour']
        print (flavour)
        height = request.form['height']
        weight = request.form['weight']
        age = request.form['age']
        gender = request.form['gender']
        activity = request.form['activity']
        region = request.form['region']
        print(activity,gender)
        character = connsql.user_character.query.filter(connsql.user_character.email == email).first()
        # 判断用户名是否存在
        if character:
            character.email=email
            character.flavour=flavour
            character.height=height
            character.weight=weight
            character.age=age
            character.gender=gender
            character.activity=activity
            character.region=region
            connsql.db.session.commit()
        else:
            character = connsql.user_character(email=email,flavour=flavour, height=height, weight=weight, age=age, gender=gender,activity=activity,region=region)
            connsql.db.session.add(character)
            connsql.db.session.commit()
        return redirect(url_for('move_forward'))
        return render_template('newindex.html')
        return redirect(url_for('show_recipes', weight=weight, age=age, gender=gender))
    else:
        return render_template('newindex.html')
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # flavor = request.form['flavor']
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['password']
        pwd2 = request.form['password2']
        print(name, email, pwd)
        user=connsql.User.query.filter(connsql.User.email==email).first()
        #判断用户名是否存在
        if user:
            return u' email existed'
        else:
            user = connsql.User(username=name, password=pwd, email=email)
            connsql.db.session.add(user)
            connsql.db.session.commit()
            login_user(user)
            return redirect(url_for('move_forward', reg=1))
            return redirect(url_for('index', email=email))
    else:
        return render_template('newindex.html')
@login_manager.user_loader
def load_user(userid):
    user= connsql.User.query.filter(connsql.User.id == userid).first()
    return user
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # flavor = request.form['flavor']
        email = request.form['email']
        pwd = request.form['password']
        print(email, pwd)
        #user = connsql.User(username=name, _password=pwd, email=email)
        #connsql.db.session.add(user)
        #connsql.db.session.commit()
        user = connsql.User.query.filter(connsql.User.email == email).first()
        if user:
             if user.check_password(pwd):
                 login_user(user)
                 return redirect(url_for('move_forward', reg=0))
             else:
                return u' password error'
        else:
            return u' username  not existed'
    else:
        return render_template('newindex.html')

@app.route('/moveforward',methods=['GET','POST'])
@login_required
def move_forward():
    email= (current_user.email)

    character = connsql.user_character.query.filter(connsql.user_character.email == email).first()
    if character:
        recipe = connmongodb.getSatisifiedRecipe()
        print(recipe)
        context = {
            'region': character.region,
            'activity': character.activity,
            'height':character.height,
            'weight':character.weight,
            'age':character.age,
            'flavour':character.flavour,
            'gender':character.gender,
            'recipe': recipe
        }
        global_var[0]=context
        return render_template('moveforward.html',context=context)
    return render_template('moveforward.html')



@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

if __name__ == '__main__':
    app.run()
