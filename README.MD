# Datalake data transformation orchestration on AWS  

This sample project shows how to build a data transformation workload on AWS, orchestrated by AWS Step Functions and running over AWS Batch with Spot instances.  
It is supposed to be deployed with a devops pipeline involving CodePipeline, CodeCommit, CodeBuild and CloudFormation (see Service Catalog templates on the "SERVICE_CATALOG" directory)

## How to build the project?

### Step 1 - Create Service Catalog products

On your AWS account, go to AWS Service Catalog and create a portfolio with the 2 products available in the SERVICE_CATALOG directory (see https://docs.aws.amazon.com/servicecatalog/latest/adminguide/getstarted.html for the tutorial on how to use Service Catalog).  
There are currently 2 products in this directory:  
* CloudTrail for S3 Datalakes: Create a CloudTrail on S3 arns that are to be followed for event triggering.
* Datalake Batch pipeline: Create a CodePipeline CI/CD pipeline for automatic deployment of project modifications on commit.

or simply execute the following commands and replace {my_role_or_user_arn} with your own arn:

```bash
chmod +x SERVICE_CATALOG/service-catalog-config.sh
SERVICE_CATALOG/service-catalog-config.sh {my_role_or_user_arn}
```

### Step 2 - Provision a Git repository

Provision a Git repository on CodeCommit with the content of the current project.

### Step 3 - Create your datalake

Basically, create a simple S3 Bucket

### Step 4 - Provision a Cloudtrail for S3 Datalakes

From the Service Catalog console, provision one single Cloudtrail for S3 Datalake product, with the arn of your S3 bucket as an init parameter

### Step 5 - Customize the parameter file

You should go and modify the AWS_CICD/config.json, in particular your 'VpcId' and 'subnets' parameters.
Once it's done, commit and push in your CodeCommit repository.

### Step 6 - Provision a CI/CD pipeline

From the Service Catalog console, provision a Datalake Batch pipeline product, targeting your S3 bucket, your CodeCommit Git repository and your master branch.

## Test the data transformation orchestration product

Once you have build the project. You can upload files in your datalake corresponding to the FileNameTriggeringPatternList value of your config.json. It should trigger a Step Functions state machine that will start executing jobs.  

The job executed is a simple 'Hello World' (see 'JOB_SRC'). You can customize it with whatever Data transformation operation you want to do.
