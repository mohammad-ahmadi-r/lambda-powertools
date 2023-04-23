import json
from aws_lambda_powertools import Logger, Tracer
#from aws_lambda_powertools.middleware_factory import lambda_handler_decorator
from aws_lambda_powertools.event_handler import (
    APIGatewayRestResolver,
    APIGatewayHttpResolver,
    Response,
)
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
#from aws_lambda_powertools.utilities.validation import validate

logger = Logger()
tracer = Tracer()
#metrics = Metrics()

app = APIGatewayRestResolver()

@app.post("/greet")
def greet():
    logger.info("Processing background event")
    #username = event.get("username", "world")
    user_data: dict = app.current_event.json_body
    username= user_data['username']
    response = {
        "message": f"hello {username}"
    }
    #return Response(statuis_code=200, body={"message": "Background processing started"})
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(response)
    }


@app.get("/greet")
def handle_post():
    logger.info("Received POST request with body")
    #return Response(body={"message": "Hello brother, im get"})
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps({"message": f"Hello brother, im get"}),
    }




@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)

'''
@app.post("/remove-background")
@validate(
    request_schema={
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 1},
            "age": {"type": "number", "minimum": 18},
        },
        "required": ["name", "age"],
    }
)
@tracer.capture_lambda_handler
def background_remover(event, context):
    logger.info("Received event: {}".format(event))

    response = {
        "statusCode": 200,
        "body": json.dumps({
            "message": "image-> background removed"
        }),
    }

    return response
'''
