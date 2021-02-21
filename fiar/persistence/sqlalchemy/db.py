from typing import Optional

from flask import g
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker, Session


class SqlAlchemyDb:
    G_PREFIX = 'db_'
    G_SESSION = G_PREFIX + 'session'

    def __init__(self, url: str, metadata: MetaData) -> None:
        self._metadata = metadata
        self._engine = create_engine(url)
        self._session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    @property
    def session(self) -> Session:
        session = self._get_session()

        if session is None:
            session = self._session_factory()
            self._set_session(session)

        return session

    def create_tables(self):
        """
        Create all tables associated with this database.
        """
        self._metadata.create_all(self._engine)

    def drop_tables(self):
        """
        Drop all tables associated with this database.
        """
        # self._metadata.drop_all(self._engine)
        for table in reversed(self._metadata.sorted_tables):
            table.drop(self._engine)

    def exit_session(self):
        """
        Exit session and release connection resources.
        """
        session = self._get_session()
        if session:
            session.commit()
            self._session_factory.remove()
            self._set_session(None)

    def _set_session(self, session: Optional[Session]):
        setattr(g, self.G_SESSION, session)

    def _get_session(self) -> Optional[Session]:
        return getattr(g, self.G_SESSION, None)
