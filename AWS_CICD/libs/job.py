import boto3
import os

BATCH_CLIENT = boto3.client('batch')

def send_command(bucket_name, input_prefix, output_prefix, timestr, job_name, job_dependencies=[], environment_variables=[], command=[], memory = None, vcpus = None):
    container = {
            'environment': environment_variables
        }
    if memory :
        container.update({'memory' : memory})
    if vcpus :
        container.update({'vcpus' : vcpus})
    
    response = BATCH_CLIENT.submit_job(
        jobName= ('pricing-data-transformation'
            + '-' + job_name
            + '-' + timestr),
        jobQueue=os.getenv('JobQueue'),
        dependsOn=job_dependencies,
        jobDefinition=os.getenv('JobDefinition'),
        containerOverrides=container
    )
    return response['jobId']