from flask import Flask, redirect, render_template, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from subprocess import run
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['SECRET_KEY'] = '\x00'

class UploadForm(FlaskForm):
    file = FileField()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save('uploads/' + filename)
        return redirect(url_for('index'))

    return render_template('template.html', form=form)

app.run('0.0.0.0', 8080, debug=True)
