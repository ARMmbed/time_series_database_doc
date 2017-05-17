# Introduction

This reference deployment shows how to store and graph time series data coming from your mbed device.  By the end, you'll be able to see the number of button presses per hour coming from your mbed device.

It guides you through the following tasks:

**TODO**: fill out these explicit steps.  Maybe they're the same as below?

# mbed Device Setup

The steps here will use the mbed web-compiler. This will load an operating system onto your mbed device so that it can upload data every time a button is pressed. This uses version pre-1.0 of mbed connector.

1. Visit [mbed-os-example-client](https://developer.mbed.org/teams/mbed-os-examples/code/mbed-os-example-client/).
1. Click the button "Import into Compiler" in the upper right.
1. A new browser window opens to the mbed web compiler. Click the "import" button to begin the import process.
1. Visit [connector.mbed.com](https://connector.mbed.com/#home)
1. Login and click the "Security credentials" link.
1. Click the "Get my device security credentials" button.
1. Select the text that displays, and copy it.
1. Go back to the mbed web compiler and click on the file `security.h`.
1. Delete the existing text and paste the text you copied.
1. Click the "Save" button near the top and the "Compile" button near the top.
1. After compilation succeeds a file is downloaded automatically: `mbed-os-example-client_K64F.bin`.
1. Drag-and-drop this file to the disk for your mbed device.

Follow the [mbed-os-example-client](https://github.com/ARMmbed/mbed-os-example-client) to get data from a device into mbed Connector.

# Pick a Time Series Platform

**TODO**: flush out once we have more platforms than just Amazon.

# Microsoft Azure

**TODO**: finish me

# InfluxDB

**TODO**: finish me

# Google Cloud

**TODO**: finish me

# Graphite

**TODO**: finish me

# Amazon Web Services

Here's how to get time series data into Amazon Web Services (AWS).

## Configure the API Gateway

1. Click "Services" in the upper-left to display a large menu of services.
1. Click "API Gateway" listed under "Application Services".
1. Click "Get Started", this will open a page to create a new API.
1. Select "New API" and for API name enter `mbed time series database webhook`.
1. Click "Create API" button.
1. Click the "Actions" button and click "Create Resource".
1. For "Resource Name" enter the text `webhook`.
1. Click the "Create Resource" button.
1. Click the "Actions" button and click "Create Method".
1. Select the "GET" method in the drop-down and click the check mark.
1. Under "Integration Type" select "Mock" and click "Save".
1. Create a PUT method
    * Integration type should be `Lambda`
    * Lambda function: `mbed_time_series_webhook`
1. Click on `Stages` -> `webhook` -> `PUT` to see the URL to use as the webhook callback below.

1. [Configure the API Gateway](#)
1. [Create the API Gateway Lambda function](#)

![](time_series_database-aws_flow.svg)

## Setup DynamoDB Table

1. Go to the DynamoDB service in the AWS console.
1. Click `Create Table`
    * Name: `mbed_connector_button_presses`
    * Primary Partition Key: Endpoint(String)
    * Add Sort Key: yes
    * Sort Key: EventHour(String)

Use the ARN of the DynamoDB table to create the IAM Role below.

**TODO**: add a screenshot here of the finished DynamoDB screen

## Setup IAM Role

1. Go to the IAM service in the AWS console
1. Click `Policies`
1. Click `Create a policy`
1. Click `Create Your Own Policy`
   * Policy Name: `AWSLambdaMicroserviceExecutionRole`
   * Policy Document:

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "dynamodb:DeleteItem",
                    "dynamodb:GetItem",
                    "dynamodb:PutItem",
                    "dynamodb:Scan",
                    "dynamodb:UpdateItem"
                ],
                "Resource": "[your_dynamodb_arn]"
            }
        ]
    }
    ```
1. Create a new role called `mbed_time_series_database`
1. Attach the `AWSLambdaBasicExecutionRole` policy
1. Attach the `AWSLambdaMicroserviceExecutionRole` policy

**TODO**: add a screenshot here of the finished role screen

## Create the API Gateway Lambda function

1. Go to the lambda service in the AWS console
1. Check out [this repo](https://github.com/ARMmbed/exd_mysql_lambda)
1. cd exd_mysql_lambda
1. make
1. In Lambda console, create a new lambda function
    * Runtime: Python 2.7
    * Template: Blank Function
    * Trigger: none (just click "Next")
    * Name: `mbed_time_series_webhook`
    * Code: upload a the .zip file from before

**TODO**: add a screenshot here of the finished Lambda function screen

 
**TODO**: Create a metric of securing the webhook(API keys?)

**TODO**: add a screenshot here of the finished API Gateway screen

## Register webhook callback

1. Register the webhook callback URL by running: `curl -s -H "Authorization: Bearer yourauthtoken" -H "Content-Type: application/json" -X PUT --data '{"url": "https://myapidomain.amazonaws.com/test/webhook"}' "https://api.connector.mbed.com/v2/notification/callback"` 
1. Subscribe to button presses by running: `curl -s -H "Authorization: Bearer yourauthtoken" -X PUT "https://api.connector.mbed.com/v2/subscriptions/yourendpointid/3200/0/5501/"`

## Create RDS database

1. Make Aurora/MySQL on [RDS](https://aws.amazon.com/rds/)
2. download [MySQL Workbench](https://www.mysql.com/products/workbench/)
1. Authorize mysql workbench **TODO**
1. Create table “events” **TODO**

**TODO**: Document adding data to RDS

## View data using QuickSight

1. Sign up for [QuickSight](https://quicksight.aws/)
1. [Authorize](http://docs.aws.amazon.com/quicksight/latest/user/enabling-access-rds.html) connection from QuickSight to RDS
1. In QuickSight, choose “New Analysis”
1. “New data set”
1. “RDS”
1. Choose Instance ID, database name, username, password, give it a data source name, 
1. “Create new data source”
1. “Edit data set”
1. “New field”
1. parseDate({timestamp}, “yyyy-MM-dd HH:mm:ss”)
1. name the new field ‘date"
1. “Save and Visualize”
1. highlight “date” and “value”
1. click the arrows next to “Field wells”
1. X axis dropdown, aggregate by hour
