# coding=utf-8
import logging
import os
import sys

# fix import paths for internal imports
cmd_folder = os.path.dirname(__file__)
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from flask_script import Server, Manager, Command, Option

import app
manager = Manager(app.app)

class CreateDb(Command):
    def run(self):
        import app
        from app import components
        components.create_tables(app.app, app.models) 

class Runserver(Server):
    def run(self):
        # import app
        logging.info('fasz')
        self.__call__(app.app,
            self.port,
            self.host, 
            self.use_debugger,
            self.use_reloader,
            self.threaded,
            self.process,
            self.passthrough_errors,
            (self.ssl_crt, self.ssl_key)
        )

class RunTests(Command):
    def run(self):
        import unittest
        unittest.main()

# override the default 127.0.0.1 binding ddress
manager.add_command("runserver", Server(host="0.0.0.0", port=8000))
manager.add_command("test", RunTests)
manager.add_command("createdb", CreateDb)

if __name__ == "__main__":
    manager.run()
