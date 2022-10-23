from cronus.services.accounts import AccountService
import sqlalchemy
import cronus
import pytest

engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=True)
sessionmaker = sqlalchemy.orm.sessionmaker(bind=engine)


@pytest.fixture(autouse=True)
def run_around_each():
    cronus.db.Base.metadata.create_all(engine)
    yield


def test_account_create_account():
    session = sessionmaker()
    service = cronus.services.AccountService(session=session)

    user = service.create_account(
        username="test_user", password="test_password", source="test_source", identity="test_identity")
    assert user.username == "test_user"
    assert user.password is not None
    assert user.password != "test_password"
    assert len(user.identities) == 1
    assert user.identities[0].source == "test_source"
    assert user.identities[0].identity == "test_identity"
    assert user.identities[0].identity_code is not None
    assert user.permissions == []
    assert user.attributes == []


def test_account_add_identity():
    session = sessionmaker()
    service: AccountService = cronus.services.AccountService(session=session)

    user = service.create_account(
        username="test_user", password="test_password", source="test_source", identity="test_identity")
    user = service.add_identity(
        user.id, "test_added_source", "test_added_identity")
    assert len(user.identities) == 2
    assert user.identities[1].source == "test_added_source"
    assert user.identities[1].identity == "test_added_identity"
    assert user.identities[1].identity_code is not None
