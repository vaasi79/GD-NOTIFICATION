![Architecture Diagram](https://github.com/vaasi79/GD-NOTIFICATION/blob/main/architecture.jpg?raw=true)
✅ Step 1:Set Up IAM Roles and Permissions:

Create an IAM role for Lambda with permissions for:

AWSLambdaBasicExecutionRole (for logging to CloudWatch)

AmazonSNSFullAccess

Create a custom policy (if needed) to follow least privilege principles.

✅ Step 2: Configure Amazon SNS (Simple Notification Service)
Create an SNS Topic:

Go to SNS → Create topic (e.g., GameDayNotificationTopic)

Subscribe Email IDs:

Add subscriber emails.

Confirm subscriptions via the email link.

✅ Step 3: Develop the Lambda Function
Use Python or Node.js (Python recommended).

Install Dependencies:

If using external APIs like balldontlie.io, you may need requests (for Python).

Code Logic:

Call the external NBA game API.

Parse JSON response.

Classify games: Final, Live, Scheduled.

Extract:

Teams

Scores

Start time

Channel

Quarter-wise scores

Format as human-readable text.

Publish to SNS topic.

✅ Step 4: Set Up EventBridge for Scheduling
Go to EventBridge → Rules → Create Rule

Name it (e.g., GameDayTrigger)

Choose Schedule → Fixed Rate or Cron expression (e.g., 0 16 * * ? * for 4 PM daily UTC).

Add Target:

Select Lambda Function

Choose your function

✅ Step 5: Monitoring with CloudWatch
CloudWatch Logs:

Enable logging in your Lambda to track:

API responses

Error messages

Notifications sent

Create Log Group (optional): For organized logging.

Set Alarms (future enhancement): For Lambda failures or API issues.

✅ Step 6: Test End-to-End
Run Lambda manually first using test events.

Check SNS Email delivery.

Review CloudWatch logs for validation or errors.

✅ Step 7: Document and Maintain
Document Environment Setup (IAM, SNS, EventBridge).

Keep API keys/configs in AWS Secrets Manager or Lambda environment variables.

Track Enhancements:

Personalized updates (by team)

SMS/Push notifications

Web dashboard

