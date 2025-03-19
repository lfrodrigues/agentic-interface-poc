import logging
import boto3
import json
import os
from dotenv import load_dotenv
from pathlib import Path


# amazon.titan-text-premier-v1:0
# us.meta.llama3-3-70b-instruct-v1:0


class BedrockClient:
    def __init__(
        self, region="us-east-1", model_id="us.meta.llama3-3-70b-instruct-v1:0"
    ):
        self.inference_counter = 0
        # Load environment variables
        load_dotenv()

        # Initialize Bedrock runtime client
        self.bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name=region,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        self.model_id = model_id

    def __del__(self):
        print(f"BRC: num of inference counts: {self.inference_counter}")

    def infer(self, prompt, logger=logging.getLogger(), temperature=0.2):
        self.inference_counter += 1
        newline = "\n"
        logger.info(f"BRC: inferring {prompt.replace(newline, ' ')}")
        """
        Send inference request to AWS Bedrock model and return generated output.
        :param prompt: str - Input prompt to the model
        :param temperature: decimal - temperature
        :return: str - Model-generated response
        """
        # Prepare the request payload
        body = json.dumps({"prompt": prompt, "temperature": temperature, "top_p": 0.9})

        try:
            # Send inference request
            response = self.bedrock_runtime.invoke_model(
                body=body,
                modelId=self.model_id,
                accept="application/json",
                contentType="application/json",
            )

            # Read and decode response body
            response_body = response["body"].read().decode("utf-8")
            response_data = json.loads(response_body)
            logger.info(f"BRC: inference results: {response_data}")

            # Return the generated output
            return response_data.get("generation", None)

        except Exception as e:
            print(f"❌ Error during inference: {e}")
            return None


if __name__ == "__main__":
    load_dotenv()
    bedrock_control = boto3.client(
        service_name="bedrock",
        region_name="us-west-2",  # or your relevant region
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        response = bedrock_control.list_foundation_models()
        models = response.get("modelSummaries", [])
        # print(f"Available foundation models: {response}")

        print(json.dumps(models, indent=4))
        # for m in models:
        #     print(f"- Model Name: {m.get('modelName')} | Provider: {m.get('providerName')} | ARN {m.get('modelArn')}")
    except Exception as e:
        print(f"Error listing foundation models: {e}")
