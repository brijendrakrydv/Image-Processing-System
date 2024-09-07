from app import db

class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.String, unique=True, nullable=False)
    status = db.Column(db.String, nullable=False, default='Pending')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.String, db.ForeignKey('requests.request_id'), nullable=False)
    product_name = db.Column(db.String, nullable=False)
    input_image_urls = db.Column(db.String, nullable=False)
    output_image_urls = db.Column(db.String)
