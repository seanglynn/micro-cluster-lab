#/bin/$SHELL
uvicorn app.server.app:app --host 0.0.0.0 --port=$1
