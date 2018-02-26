SCRIPT_DIR="$(dirname $(readlink -f $0))"
ROOT_DIR="$SCRIPT_DIR"

export PYTHONPATH="$ROOT_DIR/build/bin"

${ROOT_DIR}/build/bin/test_app
