import os
import boto3

s3 = boto3.resource('s3')

COUNTER = 0
MAX_REQUESTS = 100

def lambda_handler(event, context):
    global COUNTER
    bucket_name = 'your-bucket-name'
    if event['httpMethod'] == 'GET':
        path = event['path']
        if path == '/':
            path = '/index.html'
        try:
            COUNTER += 1
            if COUNTER > MAX_REQUESTS:
                raise Exception('Too many requests')
            if 'html' in path:
                mimetype = 'text/html'
                object_key = path[1:]
                object = s3.Object(bucket_name, object_key)
                content = object.get()['Body'].read().decode('utf-8')
                response = {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': mimetype
                    },
                    'body': content
                }
                return response
            else:
                raise Exception('File not found')
        except Exception as e:
            response = {
                'statusCode': 404,
                'body': str(e)
            }
            return response
    else:
        response = {
            'statusCode': 405,
            'body': 'Method not allowed'
        }
        return response
