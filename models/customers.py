from datetime import datetime

from flask.globals import request
from app import db

import sqlalchemy_utils as su


customerhistory = db.Table('cust_hist',
    db.Column('customerid', db.Integer,
        db.ForeignKey('customers.customerid'), nullable=False),
    db.Column('orderid', db.Integer,
        db.ForeignKey('orders.orderid'), nullable=False),
    db.Column('prod_id', db.Integer,
        db.ForeignKey('products.prod_id'), nullable=False)
)

class Customers(db.Model):
    __tablename__ = 'customers'

    MALE = 'M'
    FEMALE = 'F'
    GENDERS = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    # TODO: Add unique constraint to columns
    customerid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), info={'anonymize': True})
    lastname = db.Column(db.String(50), info={'anonymize': True})
    address1 = db.Column(db.String(50), info={'anonymize': True})
    address2 = db.Column(db.String(50), info={'anonymize': True})
    city = db.Column(db.String(50), info={'anonymize': True})
    state = db.Column(db.String(50), info={'anonymize': True})
    zip = db.Column(db.Integer, info={'anonymize': True})
    country = db.Column(su.CountryType, info={'anonymize': True})
    region = db.Column(db.Integer)
    email = db.Column(su.EmailType(50))
    phone = db.Column(su.PhoneNumberType(max_length=50),
        info={'anonymize': True})
    creditcardtype = db.Column(db.Integer, info={'anonymize': True})
    creditcard = db.Column(db.String(50), info={'anonymize': True})
    creditcardexpiration = db.Column(db.String(50),
        info={'anonymize': True})
    username = db.Column(db.String(50), info={'anonymize': True})
    password = db.Column(su.PasswordType(schemes=['pbkdf2_sha512']),
        info={'anonymize': True})
    age = db.Column(db.Integer, info={'anonymize': True})
    income = db.Column(db.Integer, info={'anonymize': True})
    gender = db.Column(su.ChoiceType(GENDERS,
        impl=db.String(1)), info={'anonymize': True})
    _deleted_at = db.Column('deleted_at', db.DateTime)
    shopping_history = db.relationship('Orders', secondary='cust_hist')

    @property
    def is_active(self):
        return self._deleted_at is None
  
    @classmethod
    def from_form(cls, form):
        """Retorna um novo Customer a partir de um form"""
        customer = cls()
        form.populate_obj(customer)
        return customer

    def anonymized(self):
        """Anonimiza informacoes que identificam uma pessoa"""
        # TODO: Change anonymization process to
        # TODO: Atualizar forma de aplicar data
        self._deleted = datetime.now()
        for column in self.__table__.columns:
            if column.info.get('anonymize'):
                setattr(self, column.name, None)
        return self


class Orders(db.Model):
    """Tabela de pedidos"""

    __tablename__ = 'orders'

    orderid = db.Column(db.Integer, primary_key=True)
    orderdate = db.Column(db.DateTime, nullable=False)
    customerid = db.Column(db.Integer,
        db.ForeignKey('customers.customerid'), nullable=True)
    netamount = db.Column(db.Numeric(precision=12, scale=2), nullable=False)
    tax = db.Column(db.Numeric(precision=12, scale=2), nullable=False)
    totalamount  = db.Column(db.Numeric(precision=12, scale=2), nullable=False)
    customer = db.relationship('Customers')
    products = db.relationship('Products', secondary='cust_hist')


class OrderLines(db.Model):
    """Tabela com os produtos por pedido"""

    __tablename__ = 'orderlines'

    orderlineid = db.Column(db.Integer, nullable=False)
    orderid = db.Column(db.Integer,
        db.ForeignKey('orders.orderid'), primary_key=True)
    prod_id = db.Column(db.Integer,
        db.ForeignKey('products.prod_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    orderdate = db.Column(db.DateTime, nullable=False)
    product = db.relationship('Products')
    orders = db.relationship('Orders')