import os
from google.cloud import storage
bucket_name = 'cve-search-input-1'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gapi-strg-key.json"
project_id = 'striped-impulse-239003'
storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)


def uploadToBucket(destination, source):
    blob = bucket.blob(destination)
    blob.upload_from_filename(source)
    os.remove(source)


def get_result(file_name):
    """Lists all the blobs in the bucket."""
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=file_name)
    for blob in blobs:
        print(blob.name)
        return blob.download_as_string()

    return None


# def main():
#     #Create Bucket
#     #bucket = storage_client.create_bucket(bucket_name)
#     #print('Bucket {} created.'.format(bucket.name))
#     uploadToBucket('vendors', 'vendors')
#
#     #Delete object
#     #blob = bucket.blob('requirements.txt')
#     #blob.delete()
#
# main()

# get_result('avinash')