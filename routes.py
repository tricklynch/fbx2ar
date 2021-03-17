#!/usr/bin/env python3
from os import path
from random import randint
from subprocess import run

from flask import (Flask, redirect, render_template, send_from_directory,
                   url_for)
from flask_wtf import FlaskForm
from flask_wtf.file import FileField

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
        #upload_name = base_name + '.fbx'
        upload_name = base_name + '.glb'
        file_path = path.join(app.config['UPLOAD_FOLDER'], upload_name)
        form.file.data.save(file_path)
        #fbx_to_gltf(base_name)
        gltf_to_usdz(base_name)

        return redirect(url_for('sendFile', filename=base_name +'.usdz'))

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

def gltf_to_usdz(base_name, input_dir=app.config['UPLOAD_FOLDER'], output_dir=app.config['UPLOAD_FOLDER']):
    #usd_from_gltf /$1_out/box.glb /$1_out/$1.usdz
    cmd_name = 'usd_from_gltf'
    input_path = path.join('.',input_dir, base_name+'.glb')
    output_path = path.join('.',output_dir,base_name + '.usdz')
    run([cmd_name,input_path,output_path])

app.run('0.0.0.0', 3000, debug=True)
