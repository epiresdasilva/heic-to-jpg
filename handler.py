import json
import boto3
from PIL import Image
import pillow_heif
import os
import io

def convert_heic_to_jpg(event, context):
    s3_client = boto3.client('s3')
    
    # Get bucket and key from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    if not key.lower().endswith('.heic'):
        print(f"File {key} is not a HEIC file. Skipping conversion.")
        return
    
    try:
        # Download the HEIC file from S3
        response = s3_client.get_object(Bucket=bucket, Key=key)
        heic_data = response['Body'].read()

        # Convert HEIC to JPG
        heif_file = pillow_heif.read_heif(heic_data)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
        )
        
        # Save the JPG to memory
        jpg_buffer = io.BytesIO()
        image.save(jpg_buffer, format='JPEG')
        jpg_buffer.seek(0)
        
        # Upload JPG to S3
        output_key = key.rsplit('.', 1)[0] + '.jpg'
        output_bucket = f"jpg-output-{os.environ['AWS_ACCOUNT_ID']}-{os.environ['AWS_REGION']}"
        s3_client.upload_fileobj(
            jpg_buffer,
            output_bucket,
            output_key,
            ExtraArgs={'ContentType': 'image/jpeg'}
        )
        
        print(f"Successfully converted {key} to {output_key}")
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Successfully converted {key} to {output_key}',
                'input': event
            })
        }
        
    except Exception as e:
        print(f"Error converting {key}: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Error converting file: {str(e)}',
                'input': event
            })
        }