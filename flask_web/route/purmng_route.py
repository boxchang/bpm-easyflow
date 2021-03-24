from flask import Blueprint, request
from flask_cors import cross_origin

from business.purmng import purmng

purmng_bp = Blueprint('purmng_bp',__name__)


#PR not to PO Grid
@purmng_bp.route('/prnopo_list', methods= ['GET'])
@cross_origin()
def prnot2po_list():
    if request.method == "GET":
        pur = purmng()
        results = pur.getPRnot2PO()

    return results

#PR Item not to PO Grid
@purmng_bp.route('/prnopo_list2', methods= ['GET'])
@cross_origin()
def pritemnot2po_list():
    if request.method == "GET":
        pur = purmng()
        results = pur.getPRItemNot2PO()

    return results


#PO undeliver Grid
@purmng_bp.route('/undeliver', methods= ['GET'])
@cross_origin()
def undeliver_list():
    if request.method == "GET":
        pur = purmng()
        results = pur.getPOnot2Deliver()

    return results


#Q Reject Grid
@purmng_bp.route('/qreject', methods= ['POST'])
@cross_origin()
def qreject():
    results = ""
    if request.method == "POST":
        data = request.form
        date_from = str(data.get('date_from'))
        date_to = str(data.get('date_to'))

        pur = purmng()
        results = pur.getRejectData(date_from, date_to)

    return results