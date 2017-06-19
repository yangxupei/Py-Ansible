#!flask/bin/python
import logging
from app import app
from app.application import application
from app.hosts import hosts
from app.monitor import monitor

app.register_blueprint(application, url_prefix='/application')
app.register_blueprint(hosts, url_prefix='/hosts')
app.register_blueprint(monitor, url_prefix='/monitor')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='D:/logs/auto666_backup.log',
                        filemode='a')
    app.run(host="0.0.0.0", debug=False)
