from main import main as main_function

def lambda_handler(event, context):
    """
    Entry point for AWS Lambda to execute.
    
    :param event: The event that triggered the Lambda function.
    :param context: The runtime information of the Lambda execution.
    """
    main_function()
    return {
        'statusCode': 200,
        'body': 'The main function executed successfully!'
    }
