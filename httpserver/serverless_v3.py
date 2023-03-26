import os
import boto3
import json
import logging

s3 = boto3.resource('s3')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

MAX_REQUESTS = 100

def lambda_handler(event, context):
    bucket_name = 'your-bucket-name'
    if event['httpMethod'] == 'GET':
        path = event['path']
        if path == '/':
            path = '/index.html'
        try:
            # Get the current request count from CloudWatch Logs
            current_count = get_request_count_from_logs()
            if current_count > MAX_REQUESTS:
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
                # Log the new request count to CloudWatch Logs
                log_request_count(current_count + 1)
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

def get_request_count_from_logs():
    # Query CloudWatch Logs for the current request count
    log_group_name = 'your-log-group-name'
    log_stream_name = 'your-log-stream-name'
    client = boto3.client('logs')
    query = 'fields @timestamp, message | sort @timestamp desc | limit 1'
    response = client.start_query(
        logGroupName=log_group_name,
        startTime=int((time.time() - 60) * 1000),
        endTime=int(time.time() * 1000),
        queryString=query,
        logStreamNames=[log_stream_name]
    )
    query_id = response['queryId']
    status = None
    while status == None or status == 'Running':
        status_response = client.get_query_results(
            queryId=query_id
        )
        if 'results' in status_response:
            status = 'Complete'
            result = status_response['results'][0][1]['value']
            return int(result)
        elif 'status' in status_response:
            status = status_response['status']
        else:
            time.sleep(1)

def log_request_count(count):
    # Log the new request count to CloudWatch Logs
    log_group_name = 'your-log-group-name'
    log_stream_name = 'your-log-stream-name'
    message = f'Request count: {count}'
    client = boto3.client('logs')
    response = client.describe_log_streams(
        logGroupName=log_group_name,
        logStreamNamePrefix=log_stream_name
    )
    log_stream_name = response['logStreams'][0]['logStreamName']
    client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[
            {
                'timestamp': int(time.time() * 1000),
                'message': message
            }
        ]
    )

