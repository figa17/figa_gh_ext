
import functions_framework
from google.cloud import storage
from flask import Response
import json

stg_client = storage.Client()


@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    print(request_json)

    def event_stream():
        # contador = 0
        # while True:
        # contador += 1

        data = {"choices":
                [
                    {
                        "index": 0,
                        "delta": {
                            "role": "assistant",
                            "content": f"{request_json}"}
                    }
                ]
                }
        yield f"data: {json.dumps(data)}\n\n"  # Formato SSE

    return Response(event_stream(), mimetype="text/event-stream")


@functions_framework.http
def callback_gh(request):
    """
    Callback for GitHub. 

    Args:
        request (request): The request object.
    """
    bucket = stg_client.get_bucket('figa-dev')
    request_json = request.get_json(silent=True)
    blob = bucket.blob('data.json')
    blob.upload_from_string(json.dumps(request_json))

    return f"Callback received! {request_json}"
