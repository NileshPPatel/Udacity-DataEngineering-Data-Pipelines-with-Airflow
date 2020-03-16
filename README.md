# Project: Data Pipelines
 
A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines 
and come to the conclusion that the best tool to achieve this is Apache Airflow.  
 
## Introduction

To assist the analytics team, an ETL pipline will need to be built that extracts their data from S3, loads data into staging tables which are 
used to load data into fact and dimensional tables for the analytics team to easily query.  
High grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills need to be created. 

They have also noted that the data quality plays a big part when analyses are executed on top the data warehouse and want to run tests 
against their datasets after the ETL steps have been executed to catch any discrepancies in the datasets.

The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. 
The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

## Project Files

The project workspace includes the below components:

1. udac_example_dag.py  - This file has the tasks and dependencies of the DAG. 
   It should be placed in the /dags directory of Airflow.
2. create_tables.sql  - This file has the SQL queries that creates all the tables in Redshift. 
   It should be placed in the /dags directory of Airflow.
3. sql_queries.py - This file has the SQL queries used to load data into the fact and dimensions tables in Redshift. 
   It should be placed in the /plugins/helpers directory of Airflow.

The following operators should be placed in the /plugins/operators  directory of Airflow: 
4. stage_redshift.py - StageToRedshiftOperator which loads JSON data from S3 into staging tables on Redshift.
5. load_fact.py - LoadFactOperator which loads data from staging tables on Redshift into a fact table.
6. load_dimension.py - LoadDimensionOperator which loads data from staging tables on Redshift into dimension tables.
7. data_quality.py - DataQualityOperator which runs a data quality check by running a SQL query and checking against an expected result.

## Data Sets

There are 2 datasets that need to be loaded and processed to be used for analysis:

1. Song Dataset
   The first dataset is a subset of real data from the Million Song Dataset. 
   Each file is in JSON format and contains metadata about a song and the artist of that song. 
2. Log Dataset
   The second dataset consists of log files in JSON format generated by the event simulator based on the 
   songs in the dataset above. These simulate activity logs from a music streaming app based on specified 
   configurations.
   
## Configuration

Add the below 2 connections on Airflow, via Airflow's UI:

1. AWS credentials
   Conn Id: Enter aws_credentials.
   Conn Type: Enter Amazon Web Services.
   Login: Enter your Access key ID from the IAM User credentials.
   Password: Enter your Secret access key from the IAM User credentials.

2. Connection to Redshift
    Conn Id: Enter redshift.
    Conn Type: Enter Postgres.
    Host: Enter the endpoint of your Redshift cluster, excluding the port at the end of the string.
    Schema: Enter dev. This is the Redshift database you want to connect to.
    Login: Enter your Redshift username created when launching your Redshift cluster.
    Password: Enter the password you created when launching your Redshift cluster.
    Port: Enter 5439.

## Usage

These are the instructions to load the data from S3 into staging tables on Redshift and then into fact and dimension tables:
 
1. Launch an AWS Redshift cluster.

2. Configure AWS S3 and redshift Airflow Connections.

3. Run create_tables.py script on Redshift to create tables on Redshift.

4. Access the Airflow UI and switch on the udac_example_dag DAG.