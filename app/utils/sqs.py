import boto3

class SQSManager (object):
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.sqs = boto3.client('sqs')

    def send_message(self, message):
        try:
            response = self.sqs.send_message(
                QueueUrl=self.queue_name,
                MessageBody=message
            )
            return response
        except Exception as e:
            raise ValueError(f"Failed to send message to SQS: {e}")

    def receive_message(self):
        try:
            response = self.sqs.receive_message(
                QueueUrl=self.queue_name,
                MaxNumberOfMessages=1,
                VisibilityTimeout=0,
                WaitTimeSeconds=0
            )
            if 'Messages' in response:
                message = response['Messages'][0]
                return message
            else:
                return None
        except Exception as e:
            raise ValueError(f"Failed to receive message from SQS: {e}")

    def delete_message(self, receipt_handle):
        try:
            response = self.sqs.delete_message(
                QueueUrl=self.queue_name,
                ReceiptHandle=receipt_handle
            )
            return response
        except Exception as e:
            raise ValueError(f"Failed to delete message from SQS: {e}")

    def get_queue_url(self):
        try:
            response = self.sqs.get_queue_url(QueueName=self.queue_name)
            return response['QueueUrl']
        except Exception as e:
            raise ValueError(f"Failed to get queue URL: {e}")