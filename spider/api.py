import flask
from .db import Mongo_save
import json

app = flask.Flask(__name__)

@app.route('/getFastProxy')
def getFastProxy():
    return Mongo_save().get_fastest_proxy()

@app.route('/getRandomProxy')
def getRandomProxy():
    return Mongo_save().get_random_proxy()

@app.route('/getManyProxy')
def getManyProxy():
    args = dict(flask.request.args)
    return json.dumps(Mongo_save().get_proxy(int(args['count'][0])))

@app.route('/delateProxy')
def delateProxy():
    args = dict(flask.request.args)
    try:
        Mongo_save().delete_proxy({'proxy': args['proxy'][0]})
        print('删除成功')
        return ('删除成功')
    except Exception:
        print('删除失败')
        return ('删除成功')

def api_run():
    app.run(port='23333')