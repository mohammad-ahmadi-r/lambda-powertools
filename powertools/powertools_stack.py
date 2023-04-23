from aws_cdk import (
    Stack,
    aws_apigateway as apigw,
    aws_lambda as _lambda,
)

import aws_cdk as cdk
from constructs import Construct

class PowertoolsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        api = apigw.RestApi(
            self, "MainApi",
            rest_api_name="API",
            description="An API that triggers lamdba",
            deploy_options={
                "stage_name": "prod",
            }
        )
        

        lambdaLayer = _lambda.LayerVersion(self, 'lambda-layer',
              code = _lambda.AssetCode('lambdas/layer/'),
              compatible_runtimes = [_lambda.Runtime.PYTHON_3_8],
        )

        lambda_fn = _lambda.Function(
            self, "TestFn",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset("lambdas/code/"),
            handler="background_remover.lambda_handler",
            timeout=cdk.Duration.seconds(30),
            memory_size=256,
            layers = [lambdaLayer],
        )
        '''
        api = apigw.HttpApi(
            self, "HelloWorldAPI",
            cors_preflight=apigw.CorsPreflightOptions(
                allow_origins=["https://example.com"],
                allow_headers=["Content-Type", "Authorization", "X-Amz-Date"],
                max_age=core.Duration.seconds(300)
            ),
            api_name="Hello World API",
            description="Hello world event handler API Gateway",
            create_default_stage=False,
            binary_media_types=["*/*"]
        )

        api.add_routes(path="/{proxy+}", methods=[apigw.HttpMethod.ANY], integration=apigw.LambdaProxyIntegration(handler=lambda_fn))

        '''
        '''
        #api_fn = api.root.add_resource("all")
        api.root.add_method(
            "ANY",
            apigw.LambdaIntegration(
                lambda_fn,
                request_templates={
                    "application/json": '{ "statusCode": "200" }'
                }
            )
        
        )
        '''
        resource = api.root.add_resource("{proxy+}")
        resource.add_method(
            'ANY',
            apigw.LambdaIntegration(
                lambda_fn,
                request_templates={
                    "multipart/form-data": '{ "statusCode": "200" }'
                },
                passthrough_behavior=apigw.PassthroughBehavior.WHEN_NO_MATCH,
                content_handling=apigw.ContentHandling.CONVERT_TO_BINARY
            ),
            request_parameters={
                "method.request.header.Content-Type": True
            }

                #proxy=False,
                #integration_responses=[{
                #    'statusCode': '200'
                #    }]
        )
        
        #api.root.add_resource(path="/{proxy+}", methods=[apigw.HttpMethod.ANY], integration=apigw.LambdaProxyIntegration(handler=lambda_fn))

        '''
        api_fn.add_resource("test").add_method(
            "POST",
            apigw.LambdaIntegration(handler=lambda_fn)
        )
        '''
        '''
        apigw.LambdaRestApi(self, "myapi",
            handler=backend
        )
        '''
