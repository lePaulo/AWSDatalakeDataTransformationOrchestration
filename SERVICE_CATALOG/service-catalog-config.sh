#!/bin/bash

PIPELINE_PRODUCT_ID=$(aws servicecatalog create-product \
                 --name datalake-batch-pipeline\
                 --owner aws-user\
                 --product-type CLOUD_FORMATION_TEMPLATE\
                 --provisioning-artifact-parameters Name=V1,Info={LoadTemplateFromURL=https://raw.githubusercontent.com/lePaulo/AWSDatalakeDataTransformationOrchestration/master/SERVICE_CATALOG/datalake-batch-pipeline.yml},Type=CLOUD_FORMATION_TEMPLATE\
                 --query ProductViewDetail.ProductViewSummary.ProductId\
                 --output text)

CLOUDTRAIL_PRODUCT_ID=$(aws servicecatalog create-product \
                 --name cloudtrail-for-datalakes\
                 --owner aws-user\
                 --product-type CLOUD_FORMATION_TEMPLATE\
                 --provisioning-artifact-parameters Name=V1,Info={LoadTemplateFromURL=https://raw.githubusercontent.com/lePaulo/AWSDatalakeDataTransformationOrchestration/master/SERVICE_CATALOG/cloudtrail.yml},Type=CLOUD_FORMATION_TEMPLATE\
                 --query ProductViewDetail.ProductViewSummary.ProductId\
                 --output text)

PORTFOLIO_ID=$(aws servicecatalog create-portfolio \
                 --display-name datalake-portfolio\
                 --provider-name aws-user\
                 --query PortfolioDetail.Id\
                 --output text)

MY_ARN=${1:-$(aws sts get-caller-identity --query Arn --output text)}

aws servicecatalog associate-product-with-portfolio --product-id $PIPELINE_PRODUCT_ID --portfolio-id $PORTFOLIO_ID
aws servicecatalog associate-product-with-portfolio --product-id $CLOUDTRAIL_PRODUCT_ID --portfolio-id $PORTFOLIO_ID

aws servicecatalog associate-principal-with-portfolio --portfolio-id $PORTFOLIO_ID --principal-arn $MY_ARN --principal-type IAM
