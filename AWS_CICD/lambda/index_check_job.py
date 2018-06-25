import json
import boto3

print('Loading function')

batch = boto3.client('batch')

def lambda_handler(event, context):
    # Log the received event
    print("Received event: " + json.dumps(event, indent=2))
    # Get jobId from the event
    jobIds = event
    
    jobs = {}
    
    for jobId in jobIds :
        try:
            # Call DescribeJobs
            response = batch.describe_jobs(jobs=[jobId])
            # Log response from AWS Batch
            print("Response of " + jobId + ': ' + json.dumps(response, indent=2))
            jobStatus = response['jobs'][0]['status']
            # Return the jobtatus
            if jobStatus == 'FAILED' :
                return 'FAILED'
            jobs[jobId] = jobStatus
        except Exception as e:
            print(e)
            message = 'Error getting Batch Job status'
            print(message)
            raise Exception(message)
    
    if all(value == 'SUCCEEDED' for value in jobs.values()) :
        return 'SUCCEEDED'
    else:
        return jobs