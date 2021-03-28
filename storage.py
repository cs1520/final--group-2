from google.cloud import storage
from uuid import uuid4

CLOUD_STORAGE_BUCKET = "astute-acolyte-149912.appspot.com"

gcs = storage.Client()
bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

def upload_file(file):
	if not file:
		return

	blob = bucket.blob(uuid4().hex + "." + file.filename.split(".")[-1])
	blob.upload_from_string(
		file.read(),
		content_type=file.content_type
	)

	return blob.public_url
