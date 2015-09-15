# coding=utf-8

import bleach

from flask import Flask, render_template, request

from flask.ext.restplus import Api, apidoc
from flask.ext.restplus import Resource
from flask.ext.restplus import fields

app = Flask(__name__)

API_PATH = '/api'


@app.route('/api/', endpoint='api')
def swagger_ui():
    return apidoc.ui_for(api)


@app.route('/')
@app.route('/app')
def hello_world():
    return render_template('criteria.html')


api = Api(app, version='1', title='USSC test task', ui=False)
criteria_ns = api.namespace(name='Criteria', description="Запросы, связанные с критериями", path=API_PATH)
input_box_ip = api.model('BoxIPInput', {'data': fields.String})


@criteria_ns.route('/criteria/<criterion_id>', endpoint='criterion')
class CriterionAPI(Resource):
    def __init__(self):
        super(CriterionAPI, self).__init__()

    def get(self, criterion_id):
        u"""
        Получить критерий
        """
        return {
                "data": {
                        "id": "0b1c7f57-0a89-41bc-966d-474301c25bc9",
                        "oval_id": "oval:ru.ussc:tst:3044",
                        "name": "KAV: мониторинг уязвимостей включен",
                        "current_state_value":
                            {
                            "regkey": "HKEY_LOCAL_MACHINE\\SOFTWARE\\KasperskyLab\\KES10SP1\\profiles\\VulnsScan2rt",
                            "reg_parameter": "enabled",
                            "value_type": "int",  # допустимые значения: "int" и "string"
                            "value": "1",
                            "operator": "equals"
                            # допустимые значения для
                            # value_type int: "equal", "not_equal", "more_or_equal", "more",
                            # "less_or_equal", "less"
                            # для value_type string: "equals", "pattern_match"

                            }
                        }
                }

    @api.doc(body=input_box_ip)
    def patch(self, criterion_id):
        u"""
        Изменить критерий
        """
        if request.headers['Content-Type'] == 'application/json':
            return {"data": bleach.clean(request.json['data'])}
        else:
            api.abort(500, 'json required')


@app.after_request
def add_cors_header(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,PUT,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response


if __name__ == '__main__':
    app.run()
