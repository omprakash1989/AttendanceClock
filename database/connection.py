import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

logger = logging.getLogger("punching_clock")


class Connection(object):
    """
    """
    def __init__(self, username, password, host, db):
        self._session_factory = None
        self._session = None
        self._engine = create_engine("postgresql://{0}:{1}@{2}/{3}".format(username, password, host, db),
                                     pool_recycle=3600,
                                     pool_size=10,
                                     echo=False,
                                     convert_unicode=True,
                                     encoding='utf-8')

    @classmethod
    def instance(cls):
        """Singleton like accessor to instantiate backend object"""
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def get_session_factory(self):
        self._session_factory = scoped_session(sessionmaker(bind=self._engine))
        return self._session_factory

    def get_session(self):
        self.get_session_factory()
        logger.info('Current Pool Status: {}'.format(self._engine.pool.status()))
        self._session = self._session_factory()
        return self._session
