import json
import socket
import time
from datetime import datetime
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('NetworkTelemetryLogs')

def lambda_handler(event, context):
    try:
        # Parse target host and port from request body or query string
        body = json.loads(event.get('body', '{}')) if event.get('body') else {}
        query_params = event.get('queryStringParameters') or {}
        
        target_host = body.get('host') or query_params.get('host', '8.8.8.8')
        port = int(body.get('port') or query_params.get('port', 80))

        # Perform low-level TCP Socket Handshake and track latency
        start_time = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2.0)
        
        result = sock.connect_ex((target_host, port))
        latency_ms = round((time.time() - start_time) * 1000, 2)
        sock.close()

        status = "REACHABLE" if result == 0 else "UNREACHABLE"
        timestamp = datetime.utcnow().isoformat()

        # Build telemetry record
        log_item = {
            'target_ip': target_host,
            'timestamp': timestamp,
            'latency_ms': str(latency_ms),
            'status': status,
            'port': port
        }

        # Save record directly to DynamoDB
        table.put_item(Item=log_item)

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(log_item)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
