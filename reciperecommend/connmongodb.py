from flask import Flask,render_template
from flask_pymongo import PyMongo
import constraint
#app = Flask(__name__)
#实例化数据库配置，可以直接一行解决
#app.config["MONGO_URI"]="mongodb://localhost:27017/recipe"
mongo = PyMongo()

#也可以两行来实例化配置,这里会把所有以MONGO开头的配置加入。
class MongoDB():
    MONGO_HOST = "127.0.0.1"
    MONGO_PORT = 27017
    MONGO_DBNAME = "recipe"
#app.config.from_object(MongoDB)
#mongo.init_app(app,config_prefix="MONGO%")
def getSatisifiedRecipe():
    recipe=mongo.db.recommendingrecipe
    res=recipe.find()
    arr=[]
    tmp=[]
    resarr=[]
    for x in res:
        arr.append((x["recipeid"],x["name"],x["ingredient"],x["provider"],x["imgurl"]))
    i=0
    while i<len(arr):
        tmp.append(arr[i])
        if i%3==2:
            resarr.append(tmp)
            tmp=[]
        i=i+1
    return resarr

def writeSatisifiedRecipe():
    recitable=mongo.db.recipeinfo
    reci = mongo.db.recipeinfo.find_one({"cuisine":"Chinese"})
    reci = mongo.db.recipeinfo.find_one()
    print((reci,reci["cuisine"]))
    res=recitable.find({"cuisine":"Chinese", "dbscan_label":2})
    arr=[]
    recipearr=[]
    for x in res:
        #print (x)
        arr.append((x["_id"],x["nutrition"]))
        recipearr.append((x["id"],x["name"],x["big_image"],x["ingredient_amount"],x["provider"]))
    for i in range(1,9):
        x=recipearr[i]
        recipe = {
            'recipeid': x[0],
            'name': x[1],
            'imgurl': x[2],
            'ingredient': x[3],
            'provider': x[4]
        }
        mongo.db.recommendingrecipe.insert(recipe)
def writeSatisifiedRecipe():
    recitable=mongo.db.recipeinfo
    reci = mongo.db.recipeinfo.find_one({"cuisine":"Chinese"})
    reci = mongo.db.recipeinfo.find_one()
    print((reci,reci["cuisine"]))
    res=recitable.find({"cuisine":"Chinese", "dbscan_label":2})
    arr=[]
    recipearr=[]
    for x in res:
        #print (x)
        arr.append((x["_id"],x["nutrition"]))
        recipearr.append((x["id"],x["name"],x["big_image"],x["ingredient_amount"],x["provider"]))
    for i in range(1,9):
        x=recipearr[i]
        recipe = {
            'recipeid': x[0],
            'name': x[1],
            'imgurl': x[2],
            'ingredient': x[3],
            'provider': x[4]
        }
        mongo.db.recommendingrecipe.insert(recipe)