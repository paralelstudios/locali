# -*- coding: utf-8 -*-
from flask_script import Manager
from locali.api import create_app
from commands.ingest import Ingest

manager = Manager(create_app())

manager.add_command('ingest', Ingest)

if __name__ == '__main__':
    manager.run()
