import boto3
from urllib.parse import unquote_plus
import json
import datetime

rekognition=boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = unquote_plus(event['Records'][0]['s3']['object']['key'])
    response = rekognition.detect_moderation_labels(Image={'S3Object': {'Bucket': bucket, 'Name': key}})
    try:
        table = dynamodb.Table('contenido_imagenes')
        time = int(datetime.datetime.now().timestamp())
        response_dynamo = table.put_item(
           Item={
                'id': time,
                'res':json.dumps(response['ModerationLabels'])
            }
        )
    except Exception, e:
        raise e
