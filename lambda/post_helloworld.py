# create a hello world lambda function

import json

def lambda_handler(event, context):
    # TODO implement
    # this is comment
    print(event)
    # return 'Hello from TEST ' + event['body']
    return {
        'body': json.dumps('Hello from' + event['body'])
    }

### --- above code the key is body ----  ###


# create a hello world lambda function

# import json

# def lambda_handler(event, context):
#     # TODO implement
#     # this is comment
#     print(event)
#     # return 'Hello from TEST ' + event['body']
#     return 'Hello from ' + event["Country"]


### --- above code the key is Country----  ###