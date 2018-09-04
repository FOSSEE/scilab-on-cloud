#!/usr/bin/env python

# Run this with
# PYTHONPATH=. DJANGO_SETTINGS_MODULE=testsite.settings
# testsite/tornado_main.py

from tornado.options import options, define, parse_command_line
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import os
import json as simplejson
import django

#Gist https://gist.githubusercontent.com/wonderbeyond/d38cd85243befe863cdde54b84505784/raw/ab78419248055333a6bf4a50022311cae9d6596c/graceful_shutdown_tornado_web_server.py

import time
import signal
import logging
from functools import partial

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 3

pid = str(os.getpid())
f = open(os.environ['SOC_PID'], 'w')
f.write(pid)
f.close()

django.setup()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soc.settings")

from concurrent.futures import ThreadPoolExecutor
from tornado import gen
from website.models import (TextbookCompanionExampleDependency,
                            TextbookCompanionDependencyFiles)
from website.dataentry import entry
from instances import ScilabInstance
import threading
import pwd

define('port', type=int, default=8000)

# Custom settings
from soc.settings import PROJECT_DIR
from django.core.wsgi import get_wsgi_application

#Gist

def sig_handler(server, sig, frame):
    io_loop = tornado.ioloop.IOLoop.instance()

    def stop_loop(deadline):
        now = time.time()
        #if now < deadline:
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            logging.info('Waiting for next tick')
            io_loop.add_timeout(now + 1, stop_loop, deadline)
        else:
            io_loop.stop()
            logging.info('Shutdown finally')

    def shutdown():
        logging.info('Stopping Django DB connections...')
        from django.db import connections
        for conn in connections.all():
            conn.close()
        logging.info('Stopping http server')
        server.stop()
        logging.info('Will shutdown in %s seconds ...',
                     MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
        stop_loop(time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)

    logging.warning('Caught signal: %s', sig)
    io_loop.add_callback_from_signal(shutdown)

#End Gist


def run_as_nobody():
    """Runs the current process as nobody."""
    # Set the effective uid and to that of nobody.
    nobody = pwd.getpwnam('nobody')
    os.setegid(nobody.pw_gid)
    os.seteuid(nobody.pw_uid)


# request_count keeps track of the number of requests at hand, it is incremented
# when post method is invoked and decremented before exiting post method in
# class ExecutionHandler.
DEFAULT_WORKERS = 5
request_count = 0

# ThreadPoolExecutor is an Executor subclass that uses a pool of threads to
# execute
# function calls asynchronously.
# It runs numbers of threads equal to DEFAULT_WORKERS in the background.
executor = ThreadPoolExecutor(max_workers=DEFAULT_WORKERS)

# scilab_executor is an object of class ScilabInstance used to
# manage(spawn, kill)
# the Scilab instances and execute the code using those instances.
scilab_executor = ScilabInstance()
scilab_executor.spawn_instance()

# instance_manager function is run at a fixed interval to kill the
# Scilab instances not in use. If the number of user requests is more than the
# count of active Scilab instances, maximum instances defined will be in
# process. Instances will be killed only when their number is more than the user
# requests.


def instance_manager():
    if(scilab_executor.count > request_count):
        scilab_executor.kill_instances(
            scilab_executor.count - request_count - 1)
    threading.Timer(300, instance_manager).start()


instance_manager()

# Whenever django server sends an ajax request,
# the request is handled by the  ExecutionHandler
# post method passes all the parameters received from the ajax call and
# passes it to the submit method of ThreadPoolExecutor class through its object.
# yield is used to gather the output asynchronously in the variable data


class ExecutionHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        global request_count
        request_count += 1

        token = self.request.arguments['token'][0]
        token = token.decode('UTF-8')
        code = self.request.arguments['code'][0]
        code = code.decode('UTF-8')
        book_id = int(self.request.arguments['book_id'][0])
        chapter_id = int(self.request.arguments['chapter_id'][0])
        example_id = int(self.request.arguments['example_id'][0])

        dependency_exists = TextbookCompanionExampleDependency.objects\
            .using('scilab').filter(example_id=example_id).exists()
        print (example_id)
        print (dependency_exists)
        dependency_exists = entry(code, example_id, dependency_exists, book_id)
        data = yield executor.submit(scilab_executor.execute_code, code, token,
                                     book_id, dependency_exists, chapter_id,
                                     example_id)
        self.write(data)
        request_count -= 1


def main():
    parse_command_line()
    wsgi_app = tornado.wsgi.WSGIContainer(
        get_wsgi_application())
    tornado_app = tornado.web.Application(
        [
            ('/execute-code', ExecutionHandler),
            ('/static/(.*)', tornado.web.StaticFileHandler,
             {'path': PROJECT_DIR + '/static/'}),
            ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        ], debug=False)
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port)
#Gist

    signal.signal(signal.SIGTERM, partial(sig_handler, server))
    signal.signal(signal.SIGINT, partial(sig_handler, server))


#End Gist
    tornado.ioloop.IOLoop.instance().start()

#Gist

    logging.info("Exit...")

#End Gist

if __name__ == '__main__':
    main()
