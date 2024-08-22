
"""
Script Name: s3-unused-bucket-checker.py
Author: Dariush Azimi
Date: June 2024

Description:
    This script identifies unused S3 buckets based on the last modified date of their contents.
    The user provides the number of days as an argument, and the script lists buckets that 
    haven't been accessed in that time period. If the bucket is empty, it flags it accordingly.
"""

import boto3
import sys
from datetime import datetime, timedelta, timezone

def list_unused_buckets(days):
    # Calculate the cutoff date
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    # Create a session using Boto3
    s3_client = boto3.client('s3')
    
    # Get the list of all S3 buckets
    response = s3_client.list_buckets()
    buckets = response['Buckets']
    
    # Loop through each bucket
    for bucket in buckets:
        bucket_name = bucket['Name']
        
        # Get the most recent object in the bucket
        objects = s3_client.list_objects_v2(Bucket=bucket_name)
        
        if 'Contents' in objects:
            recent_object = max(objects['Contents'], key=lambda x: x['LastModified'])
            recent_date = recent_object['LastModified']
            
            # Check if the recent date is older than the cutoff date
            if recent_date < cutoff_date:
                print(f"Bucket '{bucket_name}' has not been used since {recent_date.strftime('%Y-%m-%d')}")
        else:
            print(f"Bucket '{bucket_name}' is empty or has no objects since creation.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_s3_buckets.py <number_of_days>")
        sys.exit(1)
    
    days = int(sys.argv[1])
    list_unused_buckets(days)

