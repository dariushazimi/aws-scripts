#!/usr/bin/env python3

"""
Script Name: s3-unused-bucket-checker.py
Author: Dariush Azimi 
Date: 2024-06-27

Description:
    This script identifies unused S3 buckets based on the last modified date of their contents.
    The user provides the number of days as an argument, and the script lists buckets that 
    haven't been accessed in that time period. It also flags empty buckets.
"""

import boto3
import sys
import argparse
from datetime import datetime, timedelta, timezone
from prettytable import PrettyTable

def list_unused_buckets(days):
    # Calculate the cutoff date
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    # Create a session using Boto3
    s3_client = boto3.client('s3')
    sts_client = boto3.client('sts')
    
    # Get the current AWS account number
    account_id = sts_client.get_caller_identity()["Account"]
    
    # Get the list of all S3 buckets
    response = s3_client.list_buckets()
    buckets = response['Buckets']
    
    # Initialize the table
    table = PrettyTable()
    table.field_names = ["Account Number", "Bucket Name", "Status"]
    
    # Left-align columns
    table.align["Account Number"] = "l"
    table.align["Bucket Name"] = "l"
    table.align["Status"] = "l"
    
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
                status = f"Not used since {recent_date.strftime('%Y-%m-%d')}"
            else:
                status = "Recently used"
        else:
            status = "Empty"
        
        # Add a row to the table
        table.add_row([account_id, bucket_name, status])
    
    # Print the table
    print(table)

if __name__ == "__main__":
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Identify unused S3 buckets based on the last modified date of their contents.")
    
    # Add the 'days' argument
    parser.add_argument(
        'days', 
        type=int, 
        help="Number of days to check for unused S3 buckets."
    )
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Call the function with the provided number of days
    list_unused_buckets(args.days)

