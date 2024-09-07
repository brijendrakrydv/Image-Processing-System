from flask import request, jsonify, current_app as app
from app.models import db, Request, Product
from app.tasks import process_images
import csv
import uuid
from app.utils import validate_csv

@app.route('/upload', methods=['POST'])
def upload_csv():
    file = request.files['file']
    if not file or not file.filename.endswith('.csv'):
        return jsonify({'error': 'Invalid file format'}), 400

    # Validate and parse CSV data
    csv_data = file.read().decode('utf-8')
    csv_rows = list(csv.reader(csv_data.splitlines()))
    if not validate_csv(csv_rows):
        return jsonify({'error': 'Invalid CSV format'}), 400

    # Create unique request ID
    request_id = str(uuid.uuid4())
    new_request = Request(request_id=request_id, status='Pending')
    db.session.add(new_request)
    db.session.commit()

    # Insert product data and trigger async processing
    for row in csv_rows[1:]:
        product_name, input_urls = row[1], row[2]
        new_product = Product(request_id=request_id, product_name=product_name, input_image_urls=input_urls)
        db.session.add(new_product)
    
    db.session.commit()

    # Trigger async task
    process_images.delay(request_id)

    return jsonify({'request_id': request_id}), 200

@app.route('/status/<request_id>', methods=['GET'])
def check_status(request_id):
    req = Request.query.filter_by(request_id=request_id).first()
    if req is None:
        return jsonify({'error': 'Request not found'}), 404

    return jsonify({'request_id': request_id, 'status': req.status})

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    request_id = data.get('request_id')
    status = data.get('status')

    req = Request.query.filter_by(request_id=request_id).first()
    if req:
        req.status = status
        db.session.commit()

    return jsonify({'message': 'Webhook processed'}), 200
