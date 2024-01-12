from aws_cdk import (
    Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_iam as iam

from aws_cdk import (
    Stack,
)
class ApiLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create a lambda function hello world 
        lambda_function = lambda_.Function(
            self, "HelloHandler",
            runtime=lambda_.Runtime.PYTHON_3_10,
            code=lambda_.Code.from_asset('lambda'),
            handler='helloworld.lambda_handler', # file name is helloworld.py, function name is lambda_handler
        )

        # create a lambda function create s3 bucket
        lambda_function_2 = lambda_.Function(
            self, "HelloPostHandler",
            runtime=lambda_.Runtime.PYTHON_3_10,
            code=lambda_.Code.from_asset('lambda'),
            handler='post_helloworld.lambda_handler', # file name is create_s3.py, function name is lambda_handler
        )

        # create an api gateway with a lambda integration
        api = apigw.LambdaRestApi(
            self, 'Endpointsz',
            rest_api_name='ApiEndpointService',
            handler=lambda_function,
            deploy=True,    
            deploy_options=apigw.StageOptions(
                stage_name='dev',
            ),
        )

        # add a GET, post method to the root resource of the API
        api.root.add_method('GET', apigw.LambdaIntegration(lambda_function))
        api.root.add_method('POST', apigw.LambdaIntegration(lambda_function_2))

        # define a deployment
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

