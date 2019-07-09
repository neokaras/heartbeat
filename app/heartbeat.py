import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import datetime
import redis

from tornado.options import define, options
define("port", default=8000, help="run on a given port", type=int)

heartbeat_path = '/data/heartbeat/'
TTL = 60

r = redis.Redis(host='redis', port=6379, db=0)

class HeartbeatHandler(tornado.web.RequestHandler):

    def post(self):
        device = self.get_argument('device', None)
        if device is not None:
            with open(heartbeat_path + device, 'w') as f:
                f.write("")
            self.write("OK:device:" + device)
            r.setex(device, TTL, 'ok')


class HeartbeatReportHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("<html><head><title>Heartbeat Report</title></head><body>\n")
        self.write("<table border=\"1\"><tr><td>Device Name</td><td>Last Seen</td><td>Status</td></tr>\n")
        with os.scandir(heartbeat_path) as dir:
            for device in dir:
                if device.is_file():
                    mtime = os.path.getmtime(os.path.join(heartbeat_path, device.name))
                    device_last_seen = datetime.datetime.fromtimestamp(mtime).isoformat()
                    status = 'UP' if r.get(device.name) else 'DOWN'
                    self.write("<tr><td>" + device.name + "</td><td>" + device_last_seen + "</td><td>" + status + "</td></tr>\n")
        self.write("</table></body></html>")
                    





if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
            handlers=[
                (r"/heartbeat", HeartbeatHandler),
                (r"/report", HeartbeatReportHandler),
                ]
            )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
