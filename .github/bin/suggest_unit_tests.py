import boto3
import sys
from botocore.exceptions import ClientError

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client("bedrock-runtime", region_name="us-west-2")

#model_id = "anthropic.claude-opus-4-20250514-v1:0" model_id = "us.anthropic.claude-opus-4-20250514-v1:0"
model_id = "us.amazon.nova-pro-v1:0"

with open(sys.argv[1], "rb") as file:
    document_bytes = file.read()

# Start a conversation with a user message and the document
conversation = [
    {
        "role": "user",
        "content": [
            {"text": "I'm including below a pull request (as a diff) I submitted to the Trino repository.  Looking at just the proposed changes, do you think I included enough unit testing? If you think I did, just say so.  Otherwise, please suggest additional tests. Please refrain from suggesting trivial or useless unit tests; only new and valuable coverage."},
            {
                "document": {
                    # Available formats: html, md, pdf, doc/docx, xls/xlsx, csv, and txt
                    "format": "txt",
                    "name": "GitHub pull-request as a diff",
                    "source": {"bytes": document_bytes},
                }
            },
        ],
    }
]

try:
    response = client.converse(
        modelId=model_id,
        messages=conversation,
        inferenceConfig={"maxTokens": 5000, "temperature": 0.3},
    )

    response_text = response["output"]["message"]["content"][0]["text"]
    print(response_text)

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)
