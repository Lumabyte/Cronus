from sqlalchemy import select
from cronus.db.models.accounts import Account, AccountIdentity
from cronus.db import Session, engine


def get_account_by_identity(source: str, identity: str) -> Account:
    session = Session(engine)
    q = select(AccountIdentity).where(AccountIdentity.source == source and AccountIdentity.identity == identity)
    return session.execute(q).account
    
def has_scope(account: Account, scopes: str) -> bool:
    for permission in account.permissions:
        if permission.scope in scopes:
            return True
    return False

def has_scopes(account: Account, scopes: list[str]) -> bool:
    for scope in scopes:
        if not has_scope(account, scope):
            return False
    return True
