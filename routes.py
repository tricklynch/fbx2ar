from flask import Flask, render_template, request
from subprocess import run

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

@app.route('/', methods=['GET'])
def index():
    return render_template('template.html')

@app.route('/convert', methods=['POST'])
def convert():
    print(request.form[None])
    return 'success'

app.run('0.0.0.0', 8080, debug=True)
