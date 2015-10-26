# -*- coding: utf-8 -*-
from config import FLASK_DEBUG, FLASK_PORT
from app import app

if __name__ == '__main__':
    app.debug = FLASK_DEBUG
    app.run(port=FLASK_PORT)
