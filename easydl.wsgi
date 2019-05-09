import sys

sys.path.insert(0, "D:/Apache24/webapps/EasyDl")

from app import create_app

application = create_app('production')
