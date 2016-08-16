import csv
import sys
from urlparse import urlparse
from pyspark import SparkContext
import boto3

#input_file = 's3://team-TA-3-data-pipeline-magic-night/emr-input/791696577_T_ONTIME_2015-01.csv'
#output_file = 's3://team-TA-3-data-pipeline-magic-night/emr-output/san_diego_flights.csv'
local_results = '/tmp/san_diego_flights.csv'

# Get arguments
print('Number of arguments: {} arguments.'.format(len(sys.argv)))
print('Argument List:' + str(sys.argv))
input_file = sys.argv[1]
output_file = sys.argv[2]

# Parse output
parts = urlparse(output_file)
output_bucket = parts.netloc
output_key = parts.path.lstrip('/')

# Create a simple SparkContext
sc = SparkContext(appName="SimpleApp")

# load data from S3
print('Loading data from "{}"'.format(input_file))
data = sc.textFile(input_file)

# Select the date, origin, destination and delay for all flights from San Diego, CA
print('Removing header')
header = data.first()
rows = data.filter(lambda line: line != header)
print('Filtering and collecting data')
from_to_destinations = (rows.map(lambda line: line.split(','))
                        # Select only the date, origin, destination and delay information
                        .map(lambda line: ('{}'.format(line[5]), '{},{}'.format(line[15], line[16]).replace('"', ''), '{},{}'.format(line[25], line[26]).replace('"', ''), '{}'.format(line[33])))
                        # Include only San Diego as an origin
                        .filter(lambda line: True if line[1] == 'San Diego, CA' else False)
                        # Do not include data that has no delay information
                        .filter(lambda line: False if line[3] == '' else True)
                        .collect())

# Generate a CSV file with the results of from_to_destinations
print('Saving data as CSV to local file')
with open(local_results, 'wb') as csv_file:
    wr = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
    for line in from_to_destinations:
        wr.writerow(line)

# NEED TO FIND A DIFFERENT WAY TO UPLOAD FILE TO S3
print('Uploading file to bucket: {} key: {}'.format(output_bucket, output_key))
s3 = boto3.client('s3')
with open(local_results, 'rb') as data:
    s3.upload_fileobj(data, output_bucket, output_key)

print('DONE')
