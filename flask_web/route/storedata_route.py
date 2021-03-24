import json
from flask import Blueprint, request
from flask_cors import cross_origin

from data_tt.sotre_data import AdminStore

d6store_bp = Blueprint('d6store_bp',__name__)

#D6 Store sell Data from Excel
@d6store_bp.route('/selldata', methods= ['POST'])
@cross_origin()
def selldata():
    if request.method == "POST":
        data = request.form
        data_date = data.get('y_date')
        data_date = str(data_date).replace('-', '')
        adminStore = AdminStore()
        result = adminStore.google_excel(data_date)

        index = 1
        result.sort(key=lambda k: (k.get('result_msg', 0)), reverse=True)
        for data in result:
            data['item_no'] = index
            index += 1

    return json.dumps(result)