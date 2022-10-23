import bcrypt
from sqlalchemy import select
from ..db.models import accounts

class AccountService():
    def __init__(self, session) -> None:
        self.session = session

    def create_account(self, username, password, source, identity) -> accounts.Account:
        account = accounts.Account(
            username=username, password=bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()),
            identities=[])
        self.session.add(account)
        return self.add_identity(account_id=account.id, source=source, identity=identity)

    def add_identity(self, account_id, source, identity) -> accounts.Account:
        identity = accounts.AccountIdentity(
            account_id=account_id, source=source, identity=identity)
        self.session.add(identity)
        self.session.commit()
        return self.session.execute(select(accounts.Account).where(
            accounts.Account.id == account_id
        )).fetchone()

    def authenticate(self, source, identity, password):
        identity = self.session.execute(select(accounts.AccountIdentity).where(
            accounts.AccountIdentity.source == source,
            accounts.AccountIdentity.identity == identity,
            accounts.AccountIdentity.deleted is False
        )).fetchone()
        if not identity:
            return -1
        account = self.session.execute(select(accounts.Account).where(
            accounts.Account.id == identity.account_id,
            accounts.Account.password == password
        ))
        if not account:
            return -2
        return account
