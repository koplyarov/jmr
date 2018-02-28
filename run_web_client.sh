SCRIPT_DIR="$(dirname $(readlink -f $0))"
ROOT_DIR="$SCRIPT_DIR"

export PYTHONPATH="$ROOT_DIR/build/bin"

cd "$ROOT_DIR/build/bin/jmr_web_client"
FLASK_APP=web_client.py flask run
