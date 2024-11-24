# Image Hashing API

This project provides a RESTful API for managing images and generating unique hash values based on the image content. It allows users to create, update, list, and delete image entries with metadata such as perceptual hash (`p_hash`), MD5 hash, and image URL.

## Features

- **Create an Image**: Upload an image URL and generate two types of hashes: `p_hash` (perceptual hash) and `md5_hash`.
- **Update an Image**: Update the image URL and regenerate the associated hashes'''.
- **List Images**: Retrieve a list of all stored images with their hashes and links.
- **Delete an Image**: Delete an image from the database based on its unique ID.

## Requirements

- Python 3.x
- Django
- Django REST Framework
- Pillow (for image processing)
- imagehash (for perceptual hashing)
- Requests (for fetching images from URLs)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/image-hashing-api.git
cd image-hashing-api
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Setup the database
```bash
python manage.py migrate
```
### 4. Start the development server
```bash
python manage.py runserver
```

Now you can access the API at http://127.0.0.1:8000/.




