from aws_cdk import (
    Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from aws_cdk import aws_lambda as lambda_
# from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_apigateway as apigw

from aws_cdk import (
    Stack,
)
class ApiLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ## create a lambda function hello world 
        lambda_function = lambda_.Function(
            self, "HelloHandler",
            function_name='helloworld',
            runtime=lambda_.Runtime.PYTHON_3_10,
            code=lambda_.Code.from_asset('lambda'),
            handler='helloworld.lambda_handler', # file name is helloworld.py, function name is lambda_handler
        )

        # # create a lambda function create s3 bucket
        lambda_function_2 = lambda_.Function(
            self, "HelloPostHandler",
            function_name='post_helloworld',
            runtime=lambda_.Runtime.PYTHON_3_10,
            code=lambda_.Code.from_asset('lambda'),
            handler='post_helloworld.lambda_handler', # file name is create_s3.py, function name is lambda_handler
            environment={
                'body': 'env-test',
            }
        )

        # # create an api gateway with a lambda integration
        api = apigw.RestApi(
            self, 'Endpoints',
            rest_api_name='ApiEndpointService',
            # handler=lambda_function,
            deploy=True,    
            deploy_options=apigw.StageOptions(
                stage_name='dev',
            ),
        )

        # # # add a GET, post method to the root resource of the API
        api.root.add_method('GET', apigw.LambdaIntegration(lambda_function))
        api.root.add_method('POST', apigw.LambdaIntegration(lambda_function_2))


## create an api gateway with a lambda integration from another account. create lambda function in another account. add role to api gateway. execute the cli command in dst account.
        # api.root.add_method('GET', apigw.LambdaIntegration(
        #     credentials_role='arn:aws:lambda:eu-central-1:991958799346:function:helloworld',
        #     ))


############### extra code #####################


        # # define a deployment
        # dev_deployment = apigw.Deployment(
        #     self, 'Deployment',
        #     api=api,
        #     description='deployment for dev and prod',
        # )

        # add dev stage to api gateway
        # dev_stage = apigw.Stage(
        #     self, 'dev',
        #     deployment=dev_deployment,
        #     stage_name='dev',
        # )

        # api = apigw.RestApi(self, "hello-api")

        # # Define the integration
        # integration = apigw.LambdaIntegration(lambda_function)

        # v1 = api.root.add_resource("v1")
        # echo = v1.add_resource("echo")
        # echo_method = echo.add_method("GET", integration, api_key_required=True)

        # plan = api.add_usage_plan("UsagePlan",
        #     name="Easy",
        #     throttle=apigw.ThrottleSettings(
        #         rate_limit=10,
        #         burst_limit=2
        #     )
        # )

        # key = api.add_api_key("ApiKey")
        # plan.add_api_key(key)