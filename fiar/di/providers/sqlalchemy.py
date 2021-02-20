from typing import Optional

from flask import Flask

from fiar.di.providers import ServiceProvider
from fiar.persistence.sqlalchemy.db import SqlAlchemyDb
from fiar.persistence.sqlalchemy.orm import metadata


class SqlAlchemyDbProvider(ServiceProvider):

    def init(self, app: Flask) -> SqlAlchemyDb:
        url = self._create_url(
            app.config['SQL_ALCHEMY'].get('DIALECT', None),
            app.config['SQL_ALCHEMY'].get('DRIVER', None),
            app.config['SQL_ALCHEMY'].get('USERNAME', None),
            app.config['SQL_ALCHEMY'].get('PASSWORD', None),
            app.config['SQL_ALCHEMY'].get('HOST', None),
            app.config['SQL_ALCHEMY'].get('PORT', None),
            app.config['SQL_ALCHEMY'].get('DATABASE', None)
        )

        db = SqlAlchemyDb(url, metadata)
        app.teardown_appcontext(lambda e: db.exit_session())

        return db

    def shutdown(self, resource: SqlAlchemyDb) -> None:
        pass

    def _create_url(self,
                    dialect: str,
                    driver: Optional[str],
                    username: Optional[str],
                    password: Optional[str],
                    host: Optional[str],
                    port: Optional[int],
                    database: str):
        url = f'{dialect}'

        if driver is not None:
            url += f'+{driver}'

        url += '://'

        if username is not None:
            url += f'{username}'

        if password is not None:
            url += f':{password}'

        if host is not None or port is not None:
            url += f'@'

        if host is not None:
            url += f'{host}'

        if port is not None:
            url += f':{port}'

        url += f'/{database}'

        return url
