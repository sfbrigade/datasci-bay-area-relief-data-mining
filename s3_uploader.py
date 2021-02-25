import boto3
import os


if __name__ == '__main__':
    client = boto3.client('s3')
    pathlib.Path().absolute()
    # os.chdir('data')
    for file in os.listdir():
        if '.csv' in file:
            print(file)
            upload_file_bucket = 'twitter-data-01'
            upload_file_key = 'csv_twitter/' + str(file)
            client.upload_file(file, upload_file_bucket, upload_file_key)
