from flask import Flask,render_template
from flask_pymongo import PyMongo
import constraint
app = Flask(__name__)
#实例化数据库配置，可以直接一行解决
app.config["MONGO_URI"]="mongodb://localhost:27017/recipe"
mongo = PyMongo(app)

#也可以两行来实例化配置,这里会把所有以MONGO开头的配置加入。
class MongoDB():
    MONGO_HOST = "127.0.0.1"
    MONGO_PORT = 27017
    MONGO_DBNAME = "recipe"
#app.config.from_object(MongoDB)
#mongo.init_app(app,config_prefix="MONGO%")
recitable=mongo.db.recipeinfo
reci = mongo.db.recipeinfo.find_one({"cuisine":"Chinese"})
reci = mongo.db.recipeinfo.find_one()

print((reci,reci["cuisine"]))
print (reci["cuisine"])
print ('asdfadsf')
res=recitable.find({"cuisine":"Chinese"})
arr=[]
for x in res:
    #print (x)
    arr.append((x["_id"],x["nutrition"]))
satisfied_recipes = constraint.nutritional_constraints(arr, 24, 66, 177, "male", 'Active')
print (satisfied_recipes)