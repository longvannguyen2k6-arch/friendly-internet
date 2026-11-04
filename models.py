from datetime import datetime, timezone

from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey, Index, Integer, Numeric, String, func,
)
from sqlalchemy.orm import declarative_base, relationship

from db import engine

Base = declarative_base()


def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _money(precision, scale=2):
    return Numeric(precision, scale, asdecimal=False)


class Plan(Base):
    __tablename__ = 'plans'
    plan_ID = Column(Integer, primary_key=True, autoincrement=True)
    provider = Column(String(50), nullable=False)
    type_of_plan = Column(String(50), nullable=False)
    data_label = Column(String(20))
    data_gb = Column(_money(6))
    unlimited = Column(Boolean, default=False)
    calls_texts = Column(String(20))
    phone = Column(String(100))
    price_per_month = Column(_money(6), nullable=False)

    __table_args__ = (
        Index('idx_plan_search', 'provider', 'type_of_plan', 'phone', 'price_per_month'),
    )

    def __repr__(self):
        return (
            f"<Plan(id={self.plan_ID}, provider={self.provider}, type_of_plan={self.type_of_plan}, "
            f"data_gb={self.data_gb}, data_label={self.data_label}, unlimited={self.unlimited}, "
            f"calls_texts={self.calls_texts}, phone={self.phone}, price_per_month={self.price_per_month})>"
        )


class membership(Base):
    __tablename__ = 'memberships'
    id = Column(Integer, primary_key=True, autoincrement=True)
    membership_id = Column(String(30), nullable=False, unique=True)
    full_name = Column(String(70), nullable=False)
    email = Column(String(100), nullable=False, index=True)
    age = Column(Integer, nullable=False)
    plan_id = Column(Integer, ForeignKey('plans.plan_ID'), nullable=False, index=True)
    spend_cap = Column(_money(7))
    age_restricted = Column(Boolean, default=False)
    created = Column(DateTime, server_default=func.now())
    phone_number = Column(String(20))

    plan = relationship('Plan', lazy='joined')

    def __repr__(self):
        return (
            f"<membership(id={self.id}, membership_id={self.membership_id}, full_name={self.full_name}, "
            f"email={self.email}, age={self.age}, plan_id={self.plan_id}, spend_cap={self.spend_cap}, "
            f"phone_number={self.phone_number}, created={self.created})>"
        )


class account(Base):
    __tablename__ = 'accounts'
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    phone_number = Column(String(20))
    hash_password = Column(String(255), nullable=False)
    membership_id = Column(String(30))
    status_of_account = Column(String(20), default='active')
    age = Column(Integer)
    is_admin = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return (
            f"<account(account_id={self.account_id}, username={self.username}, "
            f"email={self.email}, phone_number={self.phone_number})>"
        )


class PasswordReset(Base):
    __tablename__ = 'password_resets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.account_id', ondelete='CASCADE'), nullable=False, index=True)
    code_hash = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    attempts = Column(Integer, nullable=False, default=0)
    used = Column(Boolean, nullable=False, default=False)
    created = Column(DateTime, nullable=False, default=utcnow)


def create_table():
    try:
        Base.metadata.create_all(engine)
        print('table created successfully')
    except Exception as e:
        print(f" error:{e}")


if __name__ == '__main__':
    create_table()
