import json
import os
import pyjoint_loader

from fake_db_activity import make_fake_db_activity
from joint_adapters import *

from flask import Flask
from flask import redirect, render_template, request
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

core = pyjoint_loader.LoadModule('../core/Core.jm')
client = core.GetRootObject(jmr_IClient, 'MakeClient')
make_fake_db_activity(client)

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

    def get_next_node(dir, name):
        return next(c for c in dir.GetChildren() if c.GetName() == name)

    node = pyjoint.Cast(client, jmr_fs_IFsClient).GetFsRoot()
    for path_entry in parsed_path:
        if path_entry:
            node = get_next_node(pyjoint.Cast(node, jmr_fs_IDirectory), path_entry)

    directory = pyjoint.Cast(node, jmr_fs_IDirectory)
    table = pyjoint.Cast(node, jmr_fs_ITable)

    if directory:
        return render_template(
            'navigation-dir.html',
            nav_entries=navigation_entries,
            nav_active='navigation',
            version=client.GetVersionString(),
            path=path,
            dirs=sorted([c.GetName() for c in directory.GetChildren()]),
            path_join=os.path.join,
            path_dirname=os.path.dirname
        )
    elif table:
        columns_set = set()
        py_dict_rows = []
        reader = client.ReadTable(path)
        row = reader.ReadRow()
        while row:
            py_row = json.loads(row.SerializeToJson())
            columns_set = columns_set.union({col for col in py_row})
            py_dict_rows.append(py_row)
            row = reader.ReadRow()

        columns_list = sorted(columns_set)
        py_list_rows = [[r.get(c, None) for c in columns_list] for r in py_dict_rows]

        return render_template(
            'navigation-table.html',
            nav_entries=navigation_entries,
            nav_active='navigation',
            version=client.GetVersionString(),
            path=path,
            columns=columns_list,
            rows=py_list_rows,
            path_join=os.path.join,
            path_dirname=os.path.dirname
        )
    else:
        raise RuntimeError('Unknown node type')


@app.route('/operations', strict_slashes=False)
def operations():
    return render_template(
        'operations.html',
        nav_entries=navigation_entries,
        nav_active='operations',
        version=client.GetVersionString()
    )

