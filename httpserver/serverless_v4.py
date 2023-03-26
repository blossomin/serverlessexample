import os
import boto3

s3 = boto3.resource('s3')
bucket_name = 'your-bucket-name'
counter_key = 'counter.txt'
max_requests = 100

def lambda_handler(event, context):
    if event['httpMethod'] == 'GET':
        path = event['path']
        if path == '/':
            path = '/index.html'
        try:
            # Get the current request count from S3
            current_count = get_request_count_from_s3()
            if current_count > max_requests:
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
                # Increment the request count and store it in S3
                increment_request_count_in_s3(current_count + 1)
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

def get_request_count_from_s3():
    # Get the current request count from S3
    bucket = s3.Bucket(bucket_name)
    counter_object = bucket.Object(counter_key)
    try:
        current_count = int(counter_object.get()['Body'].read().decode('utf-8'))
    except:
        current_count = 0
    return current_count

def increment_request_count_in_s3(count):
    # Increment the request count and store it in S3
    counter_object = s3.Object(bucket_name, counter_key)
    counter_object.put(Body=str(count))

