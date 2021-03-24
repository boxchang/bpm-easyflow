import json

from flask import Blueprint, request
from flask_cors import cross_origin

from business.josof import josof
from business.josofsum import josofsummary
from data_bpm.josof_data import josof_data
from data_bpm.josofsum_data import josofsum_data

josof_bp = Blueprint('josof_bp',__name__)


#Grid Title
@josof_bp.route('/sofsum', methods= ['POST'])
@cross_origin()
def sofsum():
    if request.method == "POST":
        jsof = josof_data()
        result = jsof.SOFProcessSumbyMonth()

    return result


#Grid Detail
@josof_bp.route('/sofprocess/<month>', methods= ['GET'])
@cross_origin()
def sofprocess(month):
    if request.method == "GET":
        jsof = josof_data()
        result = jsof.SOFProcess(month)

    return result


#Bar Chart
@josof_bp.route('/counteverymonth', methods= ['POST'])
@cross_origin()
def counteverymonth():
    ajax_data = ""
    print('request.method:'+request.method)
    if request.method == "POST":
        data = request.form
        jsof = josof()
        ajax_data = jsof.SOFIncomeAddEveryMonth()
    return ajax_data


#Bar Chart
@josof_bp.route('/sofincome', methods= ['POST'])
@cross_origin()
def sofincome():
    ajax_data = ""
    print('request.method:'+request.method)
    if request.method == "POST":
        data = request.form
        jsof = josof()
        ajax_data = jsof.SOFIncomeByMonth()
    return ajax_data

#BarlineChart   JOSOFSummary.jsp
@josof_bp.route('/summary', methods= ['POST'])
@cross_origin()
def summary():
    ajax_data = ""
    if request.method == "POST":
        year = str(request.form.get('yyyy'))
        js = josofsummary()
        ajax_data = js.JOSOFSummaryByYear(year)

    return ajax_data

#Grid   JOSOFSummary.jsp
@josof_bp.route('/summary_grid', methods= ['POST'])
@cross_origin()
def summary_grid():
    ajax_data = ""
    if request.method == "POST":
        year = str(request.form.get('year'))
        js = josofsum_data()
        print("year:"+year)
        results = js.getJOSOFSummary(year)
        results = [result.__dict__ for result in results.values()]
        for result in results:  #移除無法被JSON化的物件
            result.pop('detail_list')
            result.pop('bpmdb')
        ajax_data = json.dumps(results)

    return ajax_data


#SubGrid   JOSOFSummary.jsp
@josof_bp.route('/summary_grid_detail', methods= ['POST'])
@cross_origin()
def summary_grid_detail():
    ajax_data = ""
    if request.method == "POST":
        month = str(request.form.get('month'))
        js = josofsum_data()
        print("month:"+month)
        #ajax_data = js.getJODetailByMonth(month)
        ajax_data = [result.__dict__ for result in js.getJOSOFSummary(month[0:4])[month].detail_list]
        ajax_data = sorted(ajax_data, key=lambda i: int(i['status_key']))
        print(ajax_data)

    return json.dumps(ajax_data)

