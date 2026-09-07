# Cloud-Native Network Telemetry & Latency API

A serverless microservice hosted on AWS that performs real-time TCP socket handshakes to diagnose network endpoint connectivity and measure packet round-trip time (RTT).

## System Architecture
1. **Inbound Gateway:** AWS HTTP API Gateway exposes a public REST endpoint (`/default/NetworkTelemetryHandler`).
2. **Compute:** Python 3.14 AWS Lambda function parses incoming request payloads, initializes raw sockets (`socket.connect_ex`), and measures execution time in milliseconds.
3. **Database Logging:** Test results (target host, timestamp, latency, reachability status) are persisted directly to an AWS DynamoDB table (`NetworkTelemetryLogs`).
4. **Access Control:** IAM policies restrict Lambda permissions specifically to DynamoDB table writes (`put_item`).

## Tech Stack
- **Cloud Infrastructure:** Amazon Web Services (API Gateway, Lambda, DynamoDB, IAM)
- **Language/Libraries:** Python 3.14 (`socket`, `boto3`, `time`, `json`)
