from flask import Flask, render_template, request,send_file
from tempfile import *
import os 



#app = Flask(__name__)
app = Flask(__name__, template_folder='templates')
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/getreport', methods=['GET','POST'])
def hello():
        if request.method == 'POST':
            date1 = request.form['fi']
            date2 = request.form['ff']
            #return tempfile
            # f = open(tempfile, 'r')
            # pdf = f.read()
            # f.close()
            dir_path = os.path.dirname(os.path.realpath(__file__))
            tempfile=dir_path+ "\\pdfs\\xxx.pdf"
            return send_file(tempfile, attachment_filename='python.pdf')
        else:
            return render_template('index.html')
if __name__ == '__main__':
    app.run(host = 'localhost', port = 5001, debug=True)