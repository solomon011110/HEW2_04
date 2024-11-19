from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Flask-SQLAlchemyを初期化
db = SQLAlchemy()

# ユーザーテーブル（Flask-Login用）
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

# プロジェクトテーブル
class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    jid = db.Column(db.Integer)  # 外部キーにする場合は設定
    name = db.Column(db.String(50), nullable=False)
    funding_target = db.Column(db.Integer, nullable=False)
    current_funding = db.Column(db.Integer, default=0)
    overview = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100))

# 生産者テーブル
class Producer(db.Model):
    __tablename__ = 'producers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    products = db.relationship("Product", back_populates="producer")

# 商品テーブル
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    producer_id = db.Column(db.Integer, db.ForeignKey('producers.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 例: 農産物、魚介類
    defect_reason = db.Column(db.String(100))  # 例: 規格外理由
    purchase_price = db.Column(db.Float, nullable=False)
    sale_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum("available", "not_available", name="product_status"), default="available")

    producer = db.relationship("Producer", back_populates="products")
    inventories = db.relationship("Inventory", back_populates="product")
    sales = db.relationship("Sale", back_populates="product")
    donations = db.relationship("Donation", back_populates="product")

# 在庫テーブル
class Inventory(db.Model):
    __tablename__ = 'inventories'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    updated_at = db.Column(db.Date, default=datetime.utcnow)

    product = db.relationship("Product", back_populates="inventories")

# 販売テーブル
class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    sale_date = db.Column(db.Date, default=datetime.utcnow)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    product = db.relationship("Product", back_populates="sales")

# 寄付テーブル
class Donation(db.Model):
    __tablename__ = 'donations'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('donation_recipients.id'), nullable=False)
    donation_date = db.Column(db.Date, default=datetime.utcnow)
    quantity = db.Column(db.Integer, nullable=False)

    product = db.relationship("Product", back_populates="donations")
    recipient = db.relationship("DonationRecipient", back_populates="donations")

# 寄付先テーブル
class DonationRecipient(db.Model):
    __tablename__ = 'donation_recipients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    donations = db.relationship("Donation", back_populates="recipient")

# 問い合わせテーブル
class Contact(db.Model):
	__tablename__ = 'contact'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	address = db.Column(db.String(100))
	text = db.Column(db.Text)
