import os
import pyjoint_loader

from joint_adapters import *

from flask import Flask
from flask import render_template, request


app = Flask(__name__)
core = pyjoint_loader.LoadModule('../core/Core.jm')
client_session = core.GetRootObject(jmr_IClientSession, 'MakeClientSession')

client_session.CreateTable("/home/user1/doc1");
client_session.CreateTable("/home/user1/doc2");
client_session.CreateTable("/home/user2/whatever");
client_session.CreateTable("/tmp/ergnsgoin34");


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
    assert path.startswith('/')
    parsed_path = path.split('/')

    cur_dir = pyjoint.Cast(client_session, jmr_fs_IFsClient).GetFsRoot()
    for path_entry in parsed_path:
        if path_entry:
            next_node = next(c for c in cur_dir.GetChildren() if c.GetName() == path_entry)
            cur_dir = pyjoint.Cast(next_node, jmr_fs_IDirectory)

    return render_template(
        'navigation.html',
        version=client_session.GetVersionString(),
        path=path,
        dirs=[c.GetName() for c in cur_dir.GetChildren()],
        path_join=os.path.join,
        path_dirname=os.path.dirname
    )
