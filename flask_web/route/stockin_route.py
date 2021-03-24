from flask import Blueprint, request
from flask_cors import cross_origin

from bases.lib_common import getFirstAndLastDay
from business.stockin import stockin

stockin_bp = Blueprint('stockin_bp',__name__)


#Time Chart Sub Grid
@stockin_bp.route('/stockin_detail', methods= ['POST'])
@cross_origin()
def stockin_detail():
    if request.method == "POST":
        data = request.form
        sno = data.get('sno')
        com_name = data.get('com')

        si = stockin()
        result = si.getStockInDetailByNo(com_name,sno)
    return result


#Time Chart Grid
@stockin_bp.route('/stockin_info/<sdate>', methods= ['GET'])
@cross_origin()
def stockin_info(sdate):
    if request.method == "GET":
        si = stockin()
        result = si.getAllStockInInfoByDay(sdate)
    return result


#Time Chart
@stockin_bp.route('/stockin_summary', methods= ['POST'])
@cross_origin()
def stockin_timechart():
    if request.method == "POST":
        data = request.form
        param = data.get('yyyymm')
        yyyymm = str(param).split('-')
        firstDay, lastDay = getFirstAndLastDay(int(yyyymm[0]), int(yyyymm[1]))
        si = stockin()
        firstDay = firstDay.strftime("%Y-%m-%d")
        lastDay = lastDay.strftime("%Y-%m-%d")
        result = si.StockInSummaryByMonth(firstDay, lastDay)
    return result