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

### Setup IAM Role

1. Go to the IAM service in the AWS console
1. Create a new role called `mbed_time_series_database`
1. Attach the `AWSLambdaBasicExecutionRole` policy
1. Attach the `AWSLambdaVPCAccessExecutionRole` policy

**TODO**: add a screenshot here of the finished role screen

### Create RDS database

1. Make Aurora/MySQL on [RDS](https://aws.amazon.com/rds/)
   * no-publicly-accessible
   * default VPC
   * database name: tsdb
   * username: tsdbuser
   * remember the ip address, and password
1. Authorize access to RDS from your computer using security groups [more info](http://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithSecurityGroups.html).
   1. Find your own IP address.
      * `https://www.google.com/search?client=safari&rls=en&q=my+ip+address&ie=UTF-8&oe=UTF-8`
   1. In AWS EC2 Management console, click Security Groups under `NETWORK & SECURITY`
   1. Click `Create Security Group`
      * Security group name: desktop-RDS-access
      * Description: A security group to access RDS from my desktop PC.
      * VPC: default
   1. Click `Inbound` -> `Add Rule`
      * Type: Custom TCP Rule
      * Port Range: 3306
      * Source: Custom
      * CIDR: Your IP address/32, e.g. 203.0.113.1/32
        * Note that this only adds your one IP address to the access list.  If your IP address changes, you need to update this CIDR to match your new IP address.  Alternatively, if you know your IP address block, you can enter that here.
   1. Click `Create`

### Create the events table

1. Download the [MySQL Shell](https://dev.mysql.com/downloads/shell/)
1. Create a configuration file named `rds.cnf`
   ```
   [client]
   host=<ip address of RDS instance>
   port=3306
   user=tsdbuser
   password=<tsdb password>
   ```
1. In a terminal, run `mysql --defaults-file=rds.cnf`
1. type `use tsdb`
   * output: `Database changed`
1. type ```create table `test` (`id` int(11) NOT NULL AUTO_INCREMENT, `ts` datetime NOT NULL, `value` double NOT NULL, `board` varchar(36) NOT NULL, `sensor` varchar(45) NOT NULL, PRIMARY KEY (`id`), KEY `ts` (`ts`), KEY `board` (`board`));```
   * output: `Query OK, 0 rows affected (0.09 sec)`
1. type `quit`

### Create the API Gateway Lambda function

1. Go to the lambda service in the AWS console
1. Check out [this repo](https://github.com/ARMmbed/exd_mysql_lambda)
1. `cd exd_mysql_lambda`
1. Create a file named `mysqldb.cfg`
   ```
   [mysql]
   hostname: <ip address of RDS>
   username: tsdbuser
   password: <RDS password>
   database: tsdb
   table: events
   ```
1. ```make```
1. In Lambda console, create a new lambda function
    * Runtime: Python 2.7
    * Template: Blank Function
    * Trigger: none (just click "Next")
    * Name: `mbed_time_series_webhook`
    * Code: upload a the .zip file from before
1. In `Advanced Settings`, choose the VPC that RDS was created in, and add all the subnets.
1. `default` security group

**TODO**: add a screenshot here of the finished Lambda function screen

### Configure the API Gateway

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
 
**TODO**: Create a metric of securing the webhook(API keys?)

**TODO**: add a screenshot here of the finished API Gateway screen

### Register webhook callback

1. Register the webhook callback URL by running: `curl -s -H "Authorization: Bearer yourauthtoken" -H "Content-Type: application/json" -X PUT --data '{"url": "https://myapidomain.amazonaws.com/test/webhook"}' "https://api.connector.mbed.com/v2/notification/callback"` 
1. Subscribe to button presses by running: `curl -s -H "Authorization: Bearer yourauthtoken" -X PUT "https://api.connector.mbed.com/v2/subscriptions/yourendpointid/3200/0/5501/"`


### View data using QuickSight

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
