# create a hello world lambda function

import json

def lambda_handler(event, context):
    # TODO implement
    # this is comment
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from --DEV-- Lambda!')
    }