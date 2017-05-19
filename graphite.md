# Graphite

Here's how to get the time series data into the Graphite Time Series Database.

The conversion from mbed cloud data format to Graphite data format is done within an AWS Lambda / Gateway API data gateway.

## Preparing Your Environment

Setup an AWS account.



## Setting up the Graphite Server

Creating a Graphite server is not a trivial task and the work has been done and packaged in a Docker image.  This image is hosted on Docker Hub and built from github [here](https://github.com/hopsoft/docker-graphite-statsd).  This image will be run within the Amazon Elastic Container Service (AWS ECS).

1. On the first page of the ECS walk-through, there is a pair of checkboxes.  Select the 'Deploy a sample application onto an Amazon Cluster' and deselect 'Store container images securely with Amazon ECR', then press 'Continue'.  ![Configure](screenshots/graphite/ecs_configure_1.png)

1. Next, create a task definition.
On this form, specify a task name, an image name, the docker image location, and the ports to be used.  Once specified, click 'Next Step' to move to Configure Service.  ![Task](screenshots/graphite/ecs_define_task.png)

1. Now, configure a service.
![Service](screenshots/graphite/ecs_define_service.png)

1. Then, configure the cluster.
![Service](screenshots/graphite/ecs_define_cluster.png)

1. Finally, review and deploy.
![Service](screenshots/graphite/ecs_review.png)

1. (Optional) For a production environment, there are a number of steps to secure and customize the Graphite server.  Recommendations and instructions can be found on the [Github Page](https://github.com/hopsoft/docker-graphite-statsd).

After all of these steps, 

## Data Format Gateway (Conversion Step)

The conversion from mbed cloud data delived by webhook to a format consumable by the Graphite system is done with a combined Gateway API / Lambda system very similar to  this same step in the RDS / Quicksight example.
