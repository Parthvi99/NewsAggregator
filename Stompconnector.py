import time
from venv import logger
import stomp
import newspaperlib
import db


def connect_and_subscribe(_config: dict):
    #all the configuration for activemq connection
    host = _config['host']
    port = _config['port']
    user = _config['user']
    passwd = _config['passwd']
    source_queue = _config['source_queue']
    id = _config['id']
    pool_size = _config['pool_size']

    messages = 1000
    #login info of our laptop to activemq which contains host,port,user,passwd and sourcequeue from config
    logger.info(f'ActiveMQ Connection point: host:={host}:{port} / auth:={user}:{passwd} / queue: {source_queue} ')
    threshold = _config['threshold']
    #sets stomp connection with activemq with our laptop's host and port
    conn = stomp.Connection(host_and_ports = [(host, port)], heartbeats=(0,0))
    logger.info("Connected to the Queue Server")
    #listener for activemq
    conn.set_listener('', ConnectionProcessor(conn, _config))
    #connection with activemq
    conn.connect(user, passwd, wait=True, enable_reconnect=True, reconnect_sleep_increase=0.1, reconnect_attempts_max=6000)
    conn.subscribe(destination=source_queue, id=id, ack='client', headers={'activemq.prefetchSize': pool_size})
    logger.info(f"Connected to Queue Server on {host} and subscribed to {source_queue}")
    #returns conn
    return conn


class ConnectionProcessor(stomp.ConnectionListener):
    #initialising attributes for the class
    def __init__(self, conn, _config):
        self.conn = conn   #for connection
        self._config = _config   #for configuration
        self.listener = None     #for listener
        # if _config['listener'] is not None:
        #     self.listener = _config['listener']

    def on_error(self, headers, message):     #notifies when an error occurs while receiving msg
        logger.error('received an error "%s"' % message)

    def on_message(self, headers, message):   #when listener receives msg
        messageId = headers['message-id']     #our received messageId equals the msgid element of headers
        subscription = headers['subscription']  #our received subscription equals the subscription element of headers
        # if self.listener is not None:
        print('Processing Message message "%s"' % message)
        #newspaperlib.upload_news(oururl=message)
        dbconn = db.getConnection()
        db.insertContent(dbconn, newspaperlib.upload_news(oururl=message))
        #t = threading.Thread(target=self.listener, args=(self.conn, headers, message))
        #start with the execution of the thread to process the message
        #t.start()

        # Wait until the thread's execution is completed. Then shut it down
        #t.join()
        self.conn.ack(messageId, subscription)

    def on_disconnected(self):       #if disconnected
        logger.info("Got disconnected - now trying to reconnect")
        self.conn = connect_and_subscribe(self._config)


if __name__ == "__main__":
    _config = {
        'host': 'localhost',
        'port': 61613,
        'user': 'admin',
        'passwd': 'admin',
        'pool_size': 1,
        'id': 'ID:LAPTOP-P0H41LV1-49936-1584366150606-0:1',
        'source_queue': '/queue/newsagg',
        'threshold': 900
    }
    connect_and_subscribe(_config)
    while True:
        time.sleep(5)
