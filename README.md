# Image-Processing-System
This project processes image data from CSV files. It asynchronously downloads and compresses images from URLs, stores the processed images in a database, and provides APIs for uploading files and checking processing status.

Features
CSV upload and validation
Asynchronous image processing (50% compression)
Status tracking via request ID
Webhook trigger upon completion
Output CSV with processed image URLs

Tech Stack
Python, Flask, SQLAlchemy (SQLite or Postgres)
Celery (for async tasks), Redis (as task queue)
Pillow (for image compression)
