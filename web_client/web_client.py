import os
import pyjoint_loader

from joint_adapters import *

from flask import Flask
from flask import redirect, render_template, request
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

core = pyjoint_loader.LoadModule('../core/Core.jm')
client = core.GetRootObject(jmr_IClient, 'MakeClient')

client.CreateTable("/home/user1/doc1");
client.CreateTable("/home/user1/doc2");
client.CreateTable("/home/user2/whatever");
client.CreateTable("/tmp/ergnsgoin34");


navigation_entries = [
    {'id': 'navigation', 'href': '/navigation', 'title': 'Navigation'},
    {'id': 'operations', 'href': '/operations', 'title': 'Operations'},
    {'id': 'version', 'href': '/version', 'title': 'Version'}
]


@app.route('/')
def index():
    return redirect('/navigation')


@app.route('/version')
def version():
    return render_template(
        'version.html',
        nav_entries=navigation_entries,
        nav_active='version',
        version=client.GetVersionString()
    )


@app.route('/navigation', strict_slashes=False)
def navigation():
    path = request.args.get('path', '/')
    assert path.startswith('/')
    parsed_path = path.split('/')

    cur_dir = pyjoint.Cast(client, jmr_fs_IFsClient).GetFsRoot()
    for path_entry in parsed_path:
        if path_entry:
            next_node = next(c for c in cur_dir.GetChildren() if c.GetName() == path_entry)
            cur_dir = pyjoint.Cast(next_node, jmr_fs_IDirectory)

    return render_template(
        'navigation.html',
        nav_entries=navigation_entries,
        nav_active='navigation',
        version=client.GetVersionString(),
        path=path,
        dirs=sorted([c.GetName() for c in cur_dir.GetChildren()]),
        path_join=os.path.join,
        path_dirname=os.path.dirname
    )


@app.route('/operations', strict_slashes=False)
def operations():
    return render_template(
        'operations.html',
        nav_entries=navigation_entries,
        nav_active='operations',
        version=client.GetVersionString()
    )

