import os

from flask import Flask, request, redirect
from flask_cors import CORS, cross_origin
from route.cyclelife_route import cyclelife_bp
from route.josof_route import josof_bp
from route.prpolist_route import prpolist_bp
from route.prprogress_route import prprogress_bp
from route.purmng_route import purmng_bp
from route.qtimebar_route import qtimebar_bp
from route.stockin_route import stockin_bp
from route.storedata_route import d6store_bp
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'D:/ExcelTemp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app.register_blueprint(stockin_bp, url_prefix='/stockin')
app.register_blueprint(prpolist_bp, url_prefix='/prpo')
app.register_blueprint(cyclelife_bp)
app.register_blueprint(josof_bp, url_prefix='/josof')
app.register_blueprint(qtimebar_bp)
app.register_blueprint(d6store_bp, url_prefix='/d6store')
app.register_blueprint(prprogress_bp, url_prefix='/prprogress')
app.register_blueprint(purmng_bp, url_prefix='/purmng')

@app.route('/')
@cross_origin()
def hello_world():
    return 'hello world'

@app.route('/upload_file', methods= ['POST'])
@cross_origin()
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        print(file.filename)
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect('http://10.77.9.3:8086/NaNaWeb/CustomModule/ModuleReport/StoreSellData.jsp', code=301)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
