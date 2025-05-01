from lib.util_sqlalchemy import ResourceMixin
from sqlalchemy.dialects.postgresql import JSON
from scrapegod.extensions import db
import boto3
from botocore.exceptions import BotoCoreError, ClientError

class Scraper(ResourceMixin, db.Model):
    __tablename__ = 'scraper'

    id = db.Column(db.Integer, primary_key=True)  # Unique ID for the scraper
    name = db.Column(db.String(128), nullable=False, unique=True)  # Name of the scraper
    description = db.Column(db.Text, nullable=True)  # Description of the scraper
    lambda_link = db.Column(db.String(256), nullable=False, unique=True)  # ARN of the Lambda function
    status = db.Column(db.String(32), default='active')  # Status of the scraper (e.g., active, inactive)

    def invoke(self, payload=None):
        """
        Execute the scraper by invoking the associated Lambda function using boto3.

        :param payload: Optional payload to send to the Lambda function.
        :return: Response from the Lambda function.
        """
        if self.status != 'active':
            return {"error": "Scraper is not active"}

        try:
            # Initialize the boto3 Lambda client
            lambda_client = boto3.client('lambda')

            # Invoke the Lambda function
            response = lambda_client.invoke(
                FunctionName=self.lambda_link,  # The ARN or name of the Lambda function
                InvocationType='RequestResponse',  # Synchronous invocation
                Payload=json.dumps(payload or {})  # Convert the payload to JSON
            )

            # Parse the response
            response_payload = json.loads(response['Payload'].read())
            return response_payload
        except (BotoCoreError, ClientError) as e:
            return {"error": str(e)}

    def __repr__(self):
        return f"<Scraper {self.name}>"

    