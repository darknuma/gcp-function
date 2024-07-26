from cs_utils import load_to_bq

def file_processor(event, context):

    bucket_name = event["bucket"]
    file_name = event["name"]
    gcs_uri =  f"gs://{bucket_name}/{file_name}"
    load_to_bq(file_uri=gcs_uri, dataset_id='order_buck_dataset', table_id='customer_orders')

