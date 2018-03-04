def _do_create_table(client, path, rows):
    writer = client.CreateTable(path)
    for py_row in rows:
        row = client.CreateRow()
        for column in py_row:
            row.SetStringField(column, py_row[column])
        writer.WriteRow(row)


def make_fake_db_activity(client):
    _do_create_table(client, "/home/user1/doc1", [
        {"id": "1", "content": "Lorem ipsum dolor sit amet"},
        {"id": "2", "content": "consectetur adipiscing elit"},
        {"id": "3", "content": "sed do eiusmod tempor incididunt"},
    ]);

    _do_create_table(client, "/home/user1/doc2", [
        {"name": "Radeberger", "size": "560", "price": "270"},
        {"name": "Harp", "size": "560", "price": "350"},
        {"name": "Newcastle Brown Ale", "size": "560", "price": "350"},
        {"name": "Leffe Brune ", "size": "400", "price": "280"},
        {"name": "Kasteel Rouge", "size": "400", "price": "310"},
    ]);

    _do_create_table(client, "/home/user2/whatever", []);
    _do_create_table(client, "/tmp/ergnsgoin34", []);
