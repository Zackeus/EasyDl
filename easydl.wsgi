import sys

sys.path.insert(0,"D:/PyCharm/workspaces/EasyDl")

from app import create_app

application = create_app('production')
