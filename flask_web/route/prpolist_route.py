from flask import Blueprint, request
from flask_cors import cross_origin

from data_tt.pr_data import pr_data
from data_tt.stockin_data import stockin_data

prpolist_bp = Blueprint('prpolist_bp',__name__)


#PO Grid
@prpolist_bp.route('/polist_detail/<prno>', methods= ['GET'])
@cross_origin()
def polist_detail(prno):
    if request.method == "GET":
        tt = stockin_data()
        result = tt.getPOListDetail("eaglesky", prno)

    return result


#Sub Grid
@prpolist_bp.route('/prlist_detail/<com>/<prno>', methods= ['GET'])
@cross_origin()
def prlist_detail(com, prno):
    if request.method == "GET":
        tt = pr_data()
        com = str(com).lower()
        result = tt.getPRListDetail(com, prno)

    return result

#Sub Grid
@prpolist_bp.route('/prnopolist_detail/<com>/<prno>', methods= ['GET'])
@cross_origin()
def prnopolist_detail(com, prno):
    if request.method == "GET":
        tt = pr_data()
        com = str(com).lower()
        result = tt.getPRnoPOListDetail(com, prno)

    return result


#Grid Title
@prpolist_bp.route('/prlist', methods= ['POST'])
@cross_origin()
def prlist():
    if request.method == "POST":
        tt = pr_data()
        result = tt.getPRList("eaglesky")

    return result