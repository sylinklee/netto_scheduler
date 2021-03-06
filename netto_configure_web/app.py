import tornado.web
import configparser
from netto_scheduler_agent.scripts.schedule_db import SchedulerDb
from netto_scheduler_agent.scripts.task import TaskEnvironment


class AppHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        conf = configparser.ConfigParser()
        conf.read("web.ini")
        ip = conf.get("redis", "ip")
        port = conf.getint("redis", "port")
        timeout = conf.getint("redis", "timeout")
        self.db = SchedulerDb(ip, port, timeout)

    def get(self, *args, **kwargs):
        title = "netto configure web"
        environments = self.db.query_all_environments()
        if len(environments) > 0:
            cur_env = environments[0]
        else:
            cur_env = TaskEnvironment("netto", [])
        self.render("app.html", title=title, environments=environments, cur_env=cur_env)
