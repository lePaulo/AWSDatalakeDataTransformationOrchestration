import boto3, os, fnmatch, json

FILENAME_TRIGGERING_PATTERN_LIST = json.loads(os.environ['FileNameTriggeringPatternList'])
S3_RESOURCE = boto3.resource('s3')


def lambda_handler(event, context):
    
    input_parameters = {"bucket_name" : event['detail']['requestParameters']['bucketName'],
                        "object_key" : event['detail']['requestParameters']['key']}
    input_parameters['input_prefix'] = '/'.join(input_parameters['object_key'].split('/')[:-1])
    
    #Route 
    if route_pattern(input_parameters, FILENAME_TRIGGERING_PATTERN_LIST, 
                     os.getenv('InputDataPrefix')):
        return {
            "bucketName" : event['detail']['requestParameters']['bucketName'],
            "objectKey" : event['detail']['requestParameters']['key'],
            "inputPrefix" : input_parameters['input_prefix']
        }
    return 'not applicable'


def route_pattern(input_parameters, pattern_list, input_data_prefix):
    """
    """
    # if prefix is not the one expect... we can leave the function
    if input_data_prefix not in input_parameters['input_prefix']:
        print("{} not in {}".format(input_data_prefix, input_parameters['input_prefix']))
        return False
    print("{} in {}".format(input_data_prefix, input_parameters['input_prefix']))

    #List all S3 files within input_parameters['input_prefix'] and put them in a list
    files_already_uploaded = []
    for obj in S3_RESOURCE.Bucket(input_parameters['bucket_name']).objects.filter(Prefix=input_parameters['input_prefix']):
        files_already_uploaded.append(obj.key.split('/')[-1:][0])
    
    #For all patterns, we need to get at least one matching file
    patterns_validated = {}
    for pattern in pattern_list:
        patterns_validated[pattern] = False
        for filename in files_already_uploaded:
            if fnmatch.fnmatch(filename, pattern):
                print("{} in {}".format(filename, pattern))
                patterns_validated[pattern] = True
    print(patterns_validated)
    return all(value == True for value in patterns_validated.values())