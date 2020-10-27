AWS = False
XRAY = False

import requests
import json
import re
import validators
import urllib3
from urllib.parse import urlparse, parse_qsl

if AWS:
    import boto3

if XRAY:
    import boto3
    from aws_xray_sdk.core import xray_recorder

#@xray_recorder.capture('## create_response')
def response(msg, status_code):

    #print(msg)

    headers = {}
    headers["Content-Type"] = "application/json"
    headers["Access-Control-Allow-Origin"] = "*"

    if (status_code == 200):
        url = urlparse(msg["message"])
        body = {}
        body["url"] = url.scheme + "://" + url.netloc + "/" + url.path
        body["qs"] = dict(parse_qsl(url.query))
    else:
        body = msg

    return {
        "statusCode": status_code,
        "isBase64Encoded": False,
        "headers": headers,
        "body": body
    }
    
from flask import Flask, request
app = Flask(__name__)

def formaturl(url):
    if not re.match('(?:http|ftp|https)://', url):
        return 'http://{}'.format(url)
    return url

# Define the client to interact with AWS Lambda

if AWS:
    client = boto3.client('lambda')

@app.route("/")
def url_handler():

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)       

    #print('starting now')

    try:
        # for k, v in request.args.items():
        # print(f"{k}: {v}")

        if "url" in request.args:
            url = request.args["url"]
        else:
            output = response({'message': 'No URL specified'}, 400)
            return (output)

        if len(url) > 0:
            url = formaturl(url)
        else:
            return response({'message': 'No URL specified'}, 400)

        if not validators.url(url):
            return response({'message': 'Bad Url'}, 400)

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

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)