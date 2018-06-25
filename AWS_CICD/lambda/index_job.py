from libs.job import send_command

import boto3, os
import time

def lambda_handler(event, context):
    input_parameters = {
        "bucket_name" : event['bucketName'],
        "object_key" : event['objectKey'],
        "input_prefix" : event['inputPrefix']
    }
    
    input_parameters['output_path'] = os.getenv('OutputDataPrefix') + input_parameters['input_prefix'].split('/')[-1]
    input_parameters['conso_path'] = '/'.join(os.getenv('OutputDataPrefix').split('/')[:-2])+'/consolidated'     
    
    return prepare_jobs(input_parameters, input_parameters['input_prefix'], event)
    
def prepare_jobs(input_parameters, output_prefix, event):
    
    jobIds = []
    
    timestr = str(int(time.time()))
    print("## Starting pricing data transformation operations ##\n{}".format(event))
 
    main_job_environment_variables = [{'name':'BUCKET_NAME', 'value':input_parameters['bucket_name']}, 
                        {'name':'JOB_TO_EXECUTE', 'value':os.getenv('JobToExecute')}]

    main_job_jobid = send_command(input_parameters['bucket_name'], input_parameters['input_prefix'], output_prefix, timestr,
        'run_' + os.getenv('JobToExecute'),
        environment_variables= main_job_environment_variables)
    jobIds.append(main_job_jobid)
    
    return jobIds