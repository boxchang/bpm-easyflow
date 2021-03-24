from flask import Blueprint, request
from flask_cors import cross_origin

from business.bpmprocess import bpmprocess
from business.cyclelife import cyclelife

cyclelife_bp = Blueprint('cyclelife_bp',__name__)

@cyclelife_bp.route('/cyclelife', methods= ['POST'])
@cross_origin()
def cyclelifebar():
    print('request.method:'+request.method)
    if request.method == "POST":
        data = request.form
        com_name = data.get('com')
        cl = cyclelife(com_name)
    else:
        print('db_name:Null')
        cl = cyclelife()
    ajax_data = cl.execute()
    return ajax_data


@cyclelife_bp.route('/bpmprocess', methods= ['POST'])
@cross_origin()
def process_queue():
    if request.method == "POST":
        com_name = request.form.get('com')
        print('com_name:'+com_name)
        bp = bpmprocess()
        result = bp.pr_process()

    return result