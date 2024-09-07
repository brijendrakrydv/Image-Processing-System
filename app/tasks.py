from celery import shared_task
from app.models import Product, Request
from app import db
from PIL import Image
import requests
import io
import os

@shared_task
def process_images(request_id):
    products = Product.query.filter_by(request_id=request_id).all()
    for product in products:
        input_urls = product.input_image_urls.split(',')
        output_urls = []

        for url in input_urls:
            response = requests.get(url.strip())
            image = Image.open(io.BytesIO(response.content))

            # Compress image
            image = image.resize((image.width // 2, image.height // 2))
            output_buffer = io.BytesIO()
            image.save(output_buffer, format='JPEG', quality=50)

            # In a real-world case, this would be an S3 upload or similar
            output_image_path = f'compressed_{os.path.basename(url.strip())}'
            image.save(output_image_path)
            output_urls.append(output_image_path)

        # Update product with output URLs
        product.output_image_urls = ','.join(output_urls)
        db.session.commit()

    # Update request status
    req = Request.query.filter_by(request_id=request_id).first()
    req.status = 'Completed'
    db.session.commit()

    # Trigger webhook (simulated)
    import requests
    requests.post('https://webhook-url.com', json={'request_id': request_id, 'status': 'Completed'})
