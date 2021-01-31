from fiar.persistence.db import Database
from fiar.persistence.models import User
from fiar.persistence.repositories import UserRepository
from fiar.services.security import HashService, UidService


def fill_db():
    from fiar import container
    database: Database = container.database()
    user_repo: UserRepository = container.user_repository()
    uid: UidService = container.uid_service()
    hash: HashService = container.hash_service()

    database.start_session()
    user_repo.delete_all()

    user_repo.save(User(
        username="hello",
        email="hello@example.com",
        password=hash.hash_secret("password"),
        is_admin=False,
        uid=uid.make_uid()
    ))

    user_repo.save(User(
        username="jello",
        email="jello@example.com",
        password=hash.hash_secret("password"),
        is_admin=False,
        uid=uid.make_uid()
    ))

    database.end_session()
