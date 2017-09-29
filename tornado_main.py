#!/usr/bin/env python

# Run this with
# PYTHONPATH=. DJANGO_SETTINGS_MODULE=testsite.settings testsite/tornado_main.py

from tornado.options import options, define, parse_command_line
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import os
from django.utils import simplejson
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soc.settings")
from website.models import TextbookCompanionExampleDependency, TextbookCompanionDependencyFiles

from concurrent.futures import ThreadPoolExecutor
from tornado import gen
from website.dataentry import entry
from instances import ScilabInstance
import threading

define('port', type=int, default=8080)

# Custom settings
from soc.settings import PROJECT_DIR
from django.core.wsgi import get_wsgi_application


# request_count keeps track of the number of requests at hand, it is incremented
# when post method is invoked and decremented before exiting post method in
# class ExecutionHandler.
DEFAULT_WORKERS = 5
request_count = 0

# ThreadPoolExecutor is an Executor subclass that uses a pool of threads to execute
# function calls asynchronously.
# It runs numbers of threads equal to DEFAULT_WORKERS in the background.
executor = ThreadPoolExecutor(max_workers = DEFAULT_WORKERS)

# scilab_executor is an object of class ScilabInstance used to manage(spawn, kill)
# the Scilab instances and execute the code using those instances.
scilab_executor = ScilabInstance()
scilab_executor.spawn_instance()

# instance_manager function is run at a fixed interval to kill the Scilab instances
# not in use. If the number of user requests is more than the count of active Scilab
# instances, maximum instances defined will be in process. Instances will be killed
# only when their number is more than the user requests.
def instance_manager():
  if(scilab_executor.count > request_count):
    scilab_executor.kill_instances(scilab_executor.count-request_count-1)
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

        token = buffer(self.request.arguments['token'][0])
        token = str(token)
        code =  buffer(self.request.arguments['code'][0])
        code = str(code)
        book_id = int(self.request.arguments['book_id'][0])
        chapter_id = int(self.request.arguments['chapter_id'][0])
        example_id = int(self.request.arguments['example_id'][0])

        dependency_exists = TextbookCompanionExampleDependency.objects.using('scilab')\
            .filter(example_id=example_id).exists()
        print example_id
        print dependency_exists
        dependency_exists = entry(code, example_id, dependency_exists, book_id)
        data  = yield executor.submit(scilab_executor.execute_code, code, token,
            book_id, dependency_exists, chapter_id, example_id)
        print data
        print "********************************"
        self.write(data)
        request_count -= 1


def main():
  parse_command_line()
  wsgi_app = tornado.wsgi.WSGIContainer(
    get_wsgi_application())
  tornado_app = tornado.web.Application(
    [
      ('/execute-code', ExecutionHandler),
      ('/static/(.*)', tornado.web.StaticFileHandler, {'path': PROJECT_DIR + '/static/'}),
      ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
      ], debug=False)
  server = tornado.httpserver.HTTPServer(tornado_app)
  server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
  main()
