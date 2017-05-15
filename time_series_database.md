# Introduction

This reference deployment shows how to store and graph time series data coming from your mbed device.  By the end, you'll be able to see the number of button presses per hour coming from your mbed device.

It guides you through the following tasks:

**TODO**: fill out these explicit steps.  Maybe they're the same as below?

# mbed Connector

**TODO**: fill out these explicit steps using  the online IDE

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

Here's how to get time series data into AWS.

1. [Configure the API Gateway](#)
1. [Create the API Gateway Lambda function](#)

![](aws_flow.svg)

## Setup IAM Role

1. Go to the IAM service in the AWS console
1. Create a new role called `mbed_time_series_database`
1. Attach the `AWSLambdaBasicExecutionRole` policy
1. Attach the `AWSLambdaMicroserviceExecutionRole` policy

**TODO**: add a screenshot here of the finished role screen

## Create the API Gateway Lambda function

**TODO**: finish me

## Configure the API Gateway

1. Go to the API Gateway service in the AWS console
1. Create an API called `mbed time series database webhook`
1. Create a resource called `/webhook`
1. Create a GET method
    * Integration type should be `Mock`
    * Add a method response that returns 200

**TODO**: finish me

## Setup DynamoDB Table

**TODO**: finish me

## Create the DynamoDB Lambda function

**TODO**: finish me

## Setup the CloudWatch Dashboard

**TODO**: finish me

## Register webhook callback

**TODO**: finish me
