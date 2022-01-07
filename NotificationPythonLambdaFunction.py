import urllib3
import json
import os
import boto3
http = urllib3.PoolManager()
def index_handler(event, context):
    url = os.environ['TEAMS_URL']
    event_message = event['Records'][0]['Sns']['Message']
    message_dict = json.loads(event_message)
    pipeline_name = message_dict["detail"]["pipeline"]
    pipeline_status = message_dict["detail"]["state"]
    execution_id = message_dict["detail"]["execution-id"]
    text = f"Code Pipeline: {pipeline_name} with execution-id {execution_id} has: {pipeline_status}."
    title = "[Red Alert] - Code Deployment Failed"
    msg = {
        "@context": "https://schema.org/extensions",
        "@type": "MessageCard",
        "themeColor": "d63333",
        "text": text,
        "title": title,
        "sections": [{
            "facts": [{
                "name": "Pipeline",
                "value": f"{pipeline_name}"
            }, {
                "name": "Execution Id",
                "value": f"{execution_id}"
            }, {
                "name": "Status",
                "value": f"{pipeline_status}"
            }],
            "markdown": True
        }]
    }
    encoded_msg = json.dumps(msg).encode('utf-8')
    resp = http.request('POST', url, body=encoded_msg)
    print({
        "message": pipeline_name,
        "status_code": resp.status,
        "response": resp.data
    })
    message = {
        "mailContentType": "text",
        "mailBody": text,
        "mailSubject": title,
        "toAddresses": os.environ["EMAIL_LIST"]
    }
    boto3.client("sns").publish(
        TargetArn=os.environ["SNS_TOPIC"],
        Message=json.dumps(message),
    )
