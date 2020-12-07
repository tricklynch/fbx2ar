from flask import Flask, redirect, render_template, url_for, send_from_directory
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from subprocess import run
from werkzeug.utils import secure_filename
from os import path
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['SECRET_KEY'] = '\x00'

class UploadForm(FlaskForm):
    file = FileField()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()

    if form.validate_on_submit():
        baseName = "download" + str( random.randint(0,10000))  # secure_filename(form.file.data.filename)
        form.file.data.save('uploads/' + baseName+".fbx")

#command to run is here
#./FBX2gltf -b -i uploads/cube.fbx -o output/cube
        run(["./FBX2gltf","-b","-i",path.join("uploads",baseName + ".fbx"),"-o",path.join("output", baseName)])

        return redirect(url_for('sendFile',filename=baseName+".glb"))

    return render_template('template.html', form=form)


@app.route('/output/<filename>')
def sendFile(filename):
    print(filename)
    return send_from_directory("output",filename)

app.run('0.0.0.0', 8080, debug=True)
