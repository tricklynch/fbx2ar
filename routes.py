#!/usr/bin/env python3
from flask import Flask, redirect, render_template, url_for, send_from_directory
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from subprocess import run
from os import path
from random import randint

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'
# SECRET_KEY is used to prevent CSRF
# As this is an unauthenticated application, CSRF is not a concern
app.config['SECRET_KEY'] = '\x00'

class UploadForm(FlaskForm):
    file = FileField()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()

    if form.validate_on_submit():
        base_name = 'download' + str(randint(0,10000)) 
        upload_name = base_name + '.fbx'
        file_path = path.join(app.config['UPLOAD_FOLDER'], upload_name)
        form.file.data.save(file_path)
        fbx_to_gltf(base_name)

        return redirect(url_for('sendFile', filename=base_name+'.glb'))

    return render_template('template.html', form=form)

@app.route('/output/<filename>')
def sendFile(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def fbx_to_gltf(base_name, input_dir=app.config['UPLOAD_FOLDER'], output_dir=app.config['UPLOAD_FOLDER']):
    # fbx2gltf --input uploads/cube.fbx --output output/cube.glb
    cmd_name = 'fbx2gltf'
    input_path = path.join('.', input_dir, base_name+'.fbx')
    output_path = path.join('.', output_dir, base_name+'.glb')
    run([cmd_name, '--input', input_path, '--output', output_path])

app.run('0.0.0.0', 3000, debug=True)
