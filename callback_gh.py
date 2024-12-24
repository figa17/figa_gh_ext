from functions_framework  import http 
from google.cloud import storage
import json


stg_client = storage.Client()


@http
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
