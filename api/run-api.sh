#/bin/$SHELL

# export MONGO_HOST="172.20.0.1"
# export MONGO_HOST="localhost"
# MONGO_HOST="mongo"
export MONGO_DETAILS="mongodb://root:yurt@${MONGO_HOST}:27017/local.yield?authSource=local"
uvicorn app.server.app:app --host 0.0.0.0 --port=$1
