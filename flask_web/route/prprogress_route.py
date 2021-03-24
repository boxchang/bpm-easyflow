from flask import Blueprint, request
from flask_cors import cross_origin

from business.prprogress import prprogress
from data_tt.stockin_data import stockin_data

prprogress_bp = Blueprint('prprogress_bp',__name__)


#PR Grid
@prprogress_bp.route('/list/<month>', methods= ['GET'])
@cross_origin()
def prprogress_list(month):
    if request.method == "GET":
        tt = prprogress()
        result = tt.getPRProgress("eaglesky", month)

    return result