#!/bin/bash

set -e

# Define your Lambda function name
LAMBDA_FUNCTION_NAME="present-reminder"

# Create a temporary directory for the deployment package
mkdir -p lambda_package

pipenv requirements > lambda_package/requirements.txt

cd lambda_package

# Use pipenv to export your dependencies to a requirements.txt file

# Install the Python dependencies from requirements.txt into a directory named 'package'
pip install --target ./package -r requirements.txt

# Add your Python code to the 'package' directory
cp ../main.py ../telegram.py ./package


# Zip the contents of the 'package' directory
cd package
zip -r9 ../${LAMBDA_FUNCTION_NAME}.zip .

# Go back to the root directory of your project
cd ../..

echo "Deployment package ${LAMBDA_FUNCTION_NAME}.zip created."

# Upload the ZIP file to AWS Lambda using AWS CLI
aws lambda update-function-code \
    --function-name ${LAMBDA_FUNCTION_NAME} \
    --zip-file fileb://lambda_package/${LAMBDA_FUNCTION_NAME}.zip

# Clean up the temporary directory
rm -rf lambda_package

echo "Deployment to ${LAMBDA_FUNCTION_NAME} completed"
