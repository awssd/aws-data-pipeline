# aws-data-pipeline

## About Challenge
- Bureau of Transportation On-Time Performance Statistics
  - All flights in the US for Q1 2015
  - CSV data is stored in an S3 bucket (about 500MB)
- Process the data using EMR (Spark) to get all flights from San Diego, CA including the following information:
  - Date, Origin, Destination, Delay
- Save output data to RDS

## Part 1
- In the S3InputDataLocation:
  - Add a dataFormat property with a reference to the DataFormat1
- In the EmrActivityObj add the correct input, output and runsOn properties
  - The output data looks like this:

```
2015-01-22,"San Diego, CA","Detroit, MI",-6.00
2015-01-22,"San Diego, CA","Atlanta, GA",4.00
...
```

## Part 2
- Create a sqlActivity to create a table for your team with the following fields:
  - date(varchar 20), origin(varchar 20), destination(varchar 20), dealy(varchar 5)
- Create a copyActivity
- Create an EC2 Resource 
- Create an RDS Database object (DataPipeline)
  - Instance ID: <INSTANCE-ID-OF-YOUR-RDS>
  - Database Name: <DATABASE-NAME>
  - Username: <USERNAME>
  - Password: <PASSWORD>
- Create a SQL Data Node

