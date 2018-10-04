import logging
import os

import psycopg2 as psycopg2
from psycopg2.extras import DictCursor

log = logging.getLogger(__name__)


class DbWrapper(object):
    host = os.environ.get('OMNISYAN_DB_HOST')
    port = os.environ.get('OMNISYAN_DB_PORT', 5432)
    dbname = os.environ.get('OMNISYAN_DB_NAME')
    user = os.environ.get('OMNISYAN_DB_USER')
    password = os.environ.get('OMNISYAN_DB_PASS')

    def __init__(self):
        if not self.host:
            log.error("%s.host is not set" % self.__class__.__name__)
        if not self.dbname:
            log.error("%s.dbname is not set" % self.__class__.__name__)
        if not self.user:
            log.error("%s.user is not set" % self.__class__.__name__)
        log.info(
            "Connecting to %s:%s %s@%s" % (
                self.host,
                self.port,
                self.user,
                self.dbname
            )
        )
        self.conn = self.get_conn()
        self.cursor = self.get_cursor()

    def __str__(self):
        return "%s(%s@%s:%s/%s)" % (
            self.__class__.__name__,
            self.user,
            self.host,
            self.port,
            self.dbname
        )

    def get_conn(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            sslmode='prefer',
            connect_timeout=5,
        )

    def get_cursor(self, cursor_factory=DictCursor):
        return self.conn.cursor(cursor_factory=cursor_factory)
