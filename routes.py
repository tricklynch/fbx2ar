#!/usr/bin/env python3
from os import path
from random import randint
from subprocess import run
from flask import (Flask, redirect, render_template, send_from_directory,
                   url_for, request, current_app)
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import MultipleFileField

app = Flask(__name__, static_url_path='/static/client/public/build')
app.config['UPLOAD_FOLDER'] = 'static'
app.config['OUTPUT_FOLDER'] = 'output'
# SECRET_KEY is used to prevent CSRF
# As this is an unauthenticated application, CSRF is not a concern
app.config['SECRET_KEY'] = '\x00'


class MultiFileForm(FlaskForm):
    files = MultipleFileField()


@app.route("/file", methods=['POST'])
def files_recieved():
    form = MultiFileForm()
    if form.validate_on_submit:
        base_name = 'download' + str(randint(0, 10000))

        create_uploads_directory(base_name)

        file_to_convert = ''

        print(form.files.data)

        for upload in form.files.data:
            file_path = path.join(
                app.config['UPLOAD_FOLDER'], base_name, upload.filename)

            if '.fbx' in upload.filename:
                file_to_convert = upload.filename
                upload.save(file_path)

        if file_to_convert != '':
            fbx_to_usdz(file_to_convert.split('.')[0], base_name, path.join(app.config['UPLOAD_FOLDER'], base_name))
            return redirect(url_for('sendFile', filename=base_name + '.usdz'))
            
    return send_from_directory('client/public', 'index.html')

@ app.route('/output/<path:filename>')
def sendFile(filename):
    return send_from_directory(app.config["OUTPUT_FOLDER"], filename)

@ app.route("/")
def index():
    return send_from_directory('client/public', 'index.html')

@ app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

def create_uploads_directory(base_name, input_dir=app.config['UPLOAD_FOLDER'], output_dir=app.config['OUTPUT_FOLDER']):
    cmd_name = 'mkdir'
    run([cmd_name, input_dir+"/"+base_name, app.config['OUTPUT_FOLDER']])


def fbx_to_usdz(file_name, base_name, input_dir,  output_dir=app.config['OUTPUT_FOLDER']):
    fbx_to_gltf(file_name, base_name, input_dir, output_dir)
    gltf_to_usdz(base_name, input_dir, output_dir)


def fbx_to_gltf(file_name, base_name, input_dir, output_dir=app.config['OUTPUT_FOLDER']):
    # fbx2gltf --input uploads/cube.fbx --output output/cube.glb
    cmd_name = 'fbx2gltf'
    input_path = path.join('.', input_dir, file_name+'.fbx')
    output_path = path.join('.', input_dir, base_name+'.glb')
    run([cmd_name, '--input', input_path, '--output', output_path])


def gltf_to_usdz(base_name, input_dir, output_dir=app.config['OUTPUT_FOLDER']):
    # usd_from_gltf /$1_out/box.glb /$1_out/$1.usdz
    cmd_name = 'usd_from_gltf'
    input_path = path.join('.', input_dir, base_name+'.glb')
    output_path = path.join('.', output_dir, base_name + '.usdz')
    run([cmd_name, input_path, output_path])


app.run('0.0.0.0', 3000, debug=True)
