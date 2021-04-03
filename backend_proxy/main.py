import sys
import os

# run from root dir
sys.path.append(".")

if __name__ == '__main__':
    from backend_proxy.api.endpoints import *
    app.run(host='0.0.0.0', port=5000)
