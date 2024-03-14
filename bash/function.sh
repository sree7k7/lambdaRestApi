# function handler () {
#     EVENT_DATA=$1
#     COMMAND=`aws s3 mb sran-619831221558 --region 'eu-central-1'`
#         aws s3 mb sran-619831221558 --region 'eu-central-1'
#     RESPONSE="{\"statusCode\": 200, \"body\": \"Date: $COMMAND\"}"

#     echo $RESPONSE
# }


# function handler () {
#     EVENT_DATA=$1
#     COMMAND=`date`
#     RESPONSE="{\"statusCode\": 200, \"body\": \"Date: $COMMAND\"}"
#     echo $RESPONSE
# }

function handler () {
    EVENT_DATA=$1
    # echo 'hello world'
    COMMAND=`touch test.txt`
    # RESPONSE="{\"statusCode\": 200, \"body\": \"output: $COMMAND\"}"
    # echo $RESPONSE
    
    COMMAND_2=`ls`
    RESPONSE_2="{\"statusCode\": 200, \"body\": \"output: $COMMAND_2\"}"
    echo $RESPONSE_2
}

# !/bin/bash
# handler() {
#     echo "Hello, World!"
# }

# handler "$@"
