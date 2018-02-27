import os

from flask import Flask
app = Flask(__name__)

from flask import render_template, request

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/navigation')
@app.route('/navigation/')
def navigation():
    path = request.args.get('path', '/')
    return render_template(
        'navigation.html',
        path=path,
        dirs=['dir1', 'dir2', 'dir3'],
        path_join=os.path.join,
        path_dirname=os.path.dirname
    )
