import boto3
import botocore
from PIL import Image
from io import BytesIO
from datetime import datetime
from io import BytesIO

class Storage:
    def __init__(self, cf_id, key_id, secret_key):
        s3 = boto3.resource('s3', 
            endpoint_url = 'https://' + cf_id +'.r2.cloudflarestorage.com',
            aws_access_key_id = key_id,
            aws_secret_access_key = secret_key
        )
        self.bucket = s3.Bucket('flower')

    def upload_image(self, image):
        try:
            now = datetime.now()
            filename = now.strftime("%Y%m/%d/%H_%M") + '.jpg'
            
            image_buf = BytesIO()
            image.save(image_buf, format='JPEG')
            image_buf.seek(0)

            self.bucket.put_object(Key=filename, Body=image_buf)
            print(filename + ' saved in R2 successfully.')
            return filename
        except botocore.exceptions.ClientError as error:
            print(filename + ' failed to save in R2.')
            print(error)
            return 'NA'
