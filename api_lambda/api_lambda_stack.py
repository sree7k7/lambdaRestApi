from aws_cdk import (
    Duration,
    Stack,
    # aws_cloudformation as cfn,
    # aws_sqs as sqs,
)

import subprocess
from constructs import Construct
from aws_cdk import aws_lambda as lambda_
# from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_iam as iam
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as route53_targets
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_cloudfront_origins as origins


from aws_cdk import (
    Stack,
)
class ApiLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ## create a lambda function hello world
        # # Get method
        lambda_function = lambda_.Function(
            self, "HelloHandler",
            function_name='helloworldxy',
            runtime=lambda_.Runtime.PYTHON_3_10,
            code=lambda_.Code.from_asset('lambda'),
            handler='helloworld.lambda_handler', # file name is helloworld.py, function name is lambda_handler
        )

        # # create a lambda function create s3 bucket
        # # Post method
        lambda_function_2 = lambda_.Function(
            self, "HelloPostHandler",
            function_name='post_helloworld',
            runtime=lambda_.Runtime.PYTHON_3_10,
            code=lambda_.Code.from_asset('lambda'),
            handler='post_helloworld.lambda_handler', 
            environment={
                'body': 'env-test',
            }
        )

        # # create a lambda function to execute the bash script
        # lambda_function_3 = lambda_.Function( 
        #     self, "HelloBashHandler",
        #     function_name='bash',
        #     runtime=lambda_.Runtime.PROVIDED_AL2,
        #     code=lambda_.Code.from_asset('bash'),
        #     handler='function.handler', # file name is bash.py, function name is lambda_handler
        # )

        # lambda_function_3.add_to_role_policy(
        #     statement=iam.PolicyStatement(
        #         actions=['s3:*'],
        #         resources=['*'],
        #     ),
        #     # service_principal='lambda.amazonaws.com'
        # )

        not_my_money_net = route53.HostedZone.from_lookup(
            self, 'HostedZone',
            domain_name='not-my-money.net',

        )

        # acm
        certificate = acm.DnsValidatedCertificate(
            self, 'Certificate',
            certificate_name='not-my-money.net',
            domain_name=not_my_money_net.zone_name,
            hosted_zone=not_my_money_net,
            region='us-east-1',
            validation=acm.CertificateValidation.from_dns(
                not_my_money_net,               
                ), # records are added to the zone automatically
            cleanup_route53_records=True, # default is True
        )

        #To automate the creation of a record in Route53 for ACM using AWS CDK

        # route53.CnameRecord(
        #     self, 'CnameRecord',
        #     zone=not_my_money_net,
        #     domain_name=not_my_money_net.zone_name,
        #     record_name='not-my-money.net',
        #     ttl=Duration.seconds(300),
        # )

        # api domain name options, api mapping
        domain_name_options = apigw.DomainNameOptions(
            certificate=certificate,
            domain_name=not_my_money_net.zone_name,
            # base_path=base_path,
            endpoint_type=apigw.EndpointType.EDGE,
            security_policy=apigw.SecurityPolicy.TLS_1_2,
        )

        # # create an api gateway with a lambda integration
        api = apigw.RestApi(
            self, 'Endpoints',
            rest_api_name='ApiEndpointService',
            deploy=True,    
            deploy_options=apigw.StageOptions(
                stage_name='dev',
            ),
            domain_name=domain_name_options,
            retain_deployments=False,
        )
        

        # # create record set for api gateway
        route53.ARecord(
            self, 'AliasRecord',
            zone=not_my_money_net,
            target=route53.RecordTarget.from_alias(
                route53_targets.ApiGateway(api)
            ),
            ttl=Duration.seconds(300),
        )

        # # # add a GET, post method to the root resource of the API
        api.root.add_method('GET', apigw.LambdaIntegration(lambda_function))
        api.root.add_method('POST', apigw.LambdaIntegration(lambda_function_2))


## create an api gateway with a lambda integration from another account. create lambda function in another account. add role to api gateway. execute the cli command in dst account.
        # api.root.add_method('GET', apigw.LambdaIntegration(
        #     credentials_role='arn:aws:lambda:eu-central-1:991958799346:function:helloworld',
        #     ))

# # dns lookup

        # create Amazon certifcate manager for domain name in us-east-1 region
        # certificate = acm.Certificate(
        #     self, 'Certificate',
        #     domain_name='not-my-money.net',
        #     validation=acm.DnsValidatedCertificate(
        #         self, 'Certificate',
        #         hosted_zone=not_my_money_net,
        #         domain_name='not-my-money.net',
        #         region='us-east-1',
        #     ),
        #     )

        
        # cert = acm.DnsValidatedCertificate(self, "CrossRegionCertificate",
        #     domain_name="'not-my-money.net",
        #     hosted_zone='not-my-money.net',
        #     region="us-east-1"
        # )

        # # add a custom domain name to the api gateway
        # domain_name = api.add_domain_name(
        #     'CustomDomain',
        #     certificate=certificate,
        #     endpoint_type=apigw.EndpointType.REGIONAL,
        #     security_policy=apigw.SecurityPolicy.TLS_1_2,
        # )


# api gateway with custom domain name
        # domain_name = api.add_domain_name(
        #     'ApiCustomDomain-not_my_money_net',
        #     certificate=certificate,
        #     endpoint_type=apigw.EndpointType.REGIONAL,
        #     security_policy=apigw.SecurityPolicy.TLS_1_2,
        #     domain_name=not_my_money_net.zone_name,
        # )
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




        # Define the AWS CLI command to run
        # aws_cli_command = "aws s3 mb s3://not-mi-money-net"

        # # Run the AWS CLI command using subprocess
        # process = subprocess.Popen(aws_cli_command, shell=True, stdout=subprocess.PIPE)

        # # Get the output of the AWS CLI command
        # output, error = process.communicate()

        # # Print the output of the AWS CLI command
        # print(output.decode())

# Outputs the bucket name
# print(output.decode().split()[3])

# Define bucket name as a output variable
        # self.aws_cli_command = output.decode()

        # self.aws_cli_command = cdk.CfnOutput(
        #     self,
        #     "bucketname",
        #     description="bucket name",
        #     value=self.aws_cli_command,
        #     export_name="bucketname"
        # )

    # Write the output values to a file
# self.template_options.metadata = {
#         "cdk.out": {
#             "MyOutput": {
#                 "value": output.value
#             }
#         }
#     }
        

        # aws mediaconvert disassociate-certificate --arn arn:aws:acm:us-east-1:619831221558:certificate/1f3b002b-1ec5-491b-854d-51757cc3cfce