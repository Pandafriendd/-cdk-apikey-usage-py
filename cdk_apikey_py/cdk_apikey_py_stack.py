from aws_cdk import (    
    core as cdk,
    aws_apigateway as aws_apigateway
)

class CdkApikeyPyStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        
        ap_api = aws_apigateway.RestApi(self, id='alpha-price-mule-api', deploy=False)
        
        ap_deployment = aws_apigateway.Deployment(self, id='ap-deployment', api=ap_api)
        aws_apigateway.Stage(self, id='ap-stage', deployment=ap_deployment, stage_name='Prod')
        
        ap_api.root.add_method('ANY')
        
        ap_deployment2 = aws_apigateway.Deployment(self, id='ap-deployment2', api=ap_api)
        stagename = aws_apigateway.Stage(self, id='ap-stage2', deployment=ap_deployment2, stage_name='Stage')
        
        ap_api.deployment_stage = stagename
        
        key_mule = ap_api.add_api_key(id='mule', api_key_name='mule')
        plan = ap_api.add_usage_plan(id='Usage-plan-mule', name='mule', api_key=key_mule, throttle=aws_apigateway.ThrottleSettings(rate_limit=100, burst_limit=200))
        plan.add_api_stage(api=ap_api, stage=ap_api.deployment_stage)