import os
import pyjoint_loader

from joint_adapters import *

from flask import Flask
from flask import render_template, request


app = Flask(__name__)
core = pyjoint_loader.LoadModule('../core/Core.jm')
client_session = core.GetRootObject(jmr_IClientSession, 'MakeClientSession')


@app.route('/')
def index():
    return render_template(
        'index.html',
        version=client_session.GetVersionString()
    )


@app.route('/navigation')
@app.route('/navigation/')
def navigation():
    path = request.args.get('path', '/')
    return render_template(
        'navigation.html',
        version=client_session.GetVersionString(),
        path=path,
        dirs=['dir1', 'dir2', 'dir3'],
        path_join=os.path.join,
        path_dirname=os.path.dirname
    )
