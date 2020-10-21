#comment test 3
AWS = True
XRAY = False

import requests
import json
import re
import validators
import boto3
import urllib3
from urllib.parse import urlparse, parse_qsl

if XRAY:
    from aws_xray_sdk.core import xray_recorder

#@xray_recorder.capture('## create_response')
def response(msg, status_code):

    #print(msg)
    url = urlparse(msg["message"])

    headers = {}
    headers["Content-Type"] = "application/json"
    headers["Access-Control-Allow-Origin"] = "*"

    body = {}
    body["url"] = url.scheme + "://" + url.netloc + "/" + url.path
    body["qs"] = dict(parse_qsl(url.query))

    return {
        "statusCode": status_code,
        "isBase64Encoded": False,
        "headers": headers,
        "body": json.dumps(body)
    }

def formaturl(url):
    if not re.match('(?:http|ftp|https)://', url):
        return 'http://{}'.format(url)
    return url

# Define the client to interact with AWS Lambda
client = boto3.client('lambda')

def url_handler(event, context):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    #print('starting now')

    try:
        #print("Log stream name:", context.log_stream_name)
        #print("Log group name:",  context.log_group_name)
        #print("Request ID:",context.aws_request_id)
        #print("Mem. limits(MB):", context.memory_limit_in_mb)
        #url1 = event["queryStringParameters"]["url1"]

        qs = event.get('queryStringParameters', None)
        if qs is not None and (qs.get('url', None) is not None):
            url = event["queryStringParameters"]["url"]
        else:
            output = response({'message':  'No URL specified'}, 400)
            return (output)

        if len(url) > 0:
            url = formaturl(url)
        else:
            return response({'message':  'No URL specified'}, 400)

        if not validators.url(url):
            return response({'message':  'Bad Url'}, 400)

        r = requests.get(url, allow_redirects=False, verify=False)

        if (r.headers.get('Location', None) is None):
            output = url
        else:
            output = (r.headers['Location'])  # not guaranteed to have Location

        output = response({'message':  output}, 200)

        if XRAY:
            subsegment = xray_recorder.begin_subsegment('SNS')

        # Define the input parameters that will be passed
        # on to the child function
        if AWS:
            inputParams = {
                "topic": "arn:aws:sns:us-east-2:294402561156:snsFromLambda",
                "subject": "This is the subject of the message.",
                "message": str(output)
            }

        if XRAY:
            xray_recorder.end_subsegment()

        if AWS:
            child = client.invoke(
                FunctionName='arn:aws:lambda:us-east-2:294402561156:function:dsbPublishtoSNS',
                InvocationType='RequestResponse',
                Payload=json.dumps(inputParams)
            )
            #print(json.load(child['Payload']))
            #print('\n')

        return (output)

    except Exception as e:
        return response({'message': e}, 400)
