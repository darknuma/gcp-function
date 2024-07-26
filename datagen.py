import io
import os
import csv
import random
from google.cloud import storage, bigquery
import uuid
from dotenv import load_dotenv


load_dotenv()

BUCKET = 'order_buck'

GCS_AUTH = os.environ.get("GOOGLE_AUTH_FILE")

# Set the environment variable for authentication
if GCS_AUTH:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GCS_AUTH

# generate custom orders
def generate_customer_orders(num_orders=1000):
    orders = []

    for order_id in range(1, num_orders + 1):
        customer_id = random.randint(1000,9999)
        product_id =  random.randint(1, 100)
        quantity = random.randint(1, 10)
        total_amount = round(random.uniform(10, 100), 2)

        order = [order_id, customer_id, product_id, quantity, total_amount]
        orders.append(order)

    return orders

def upload_to_gcs(bucket_name, file_name, data):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    unique_id = str(uuid.uuid4())[:8] # generate a random 8-character uuid

    full_file_name = f"{file_name}_{unique_id}.csv"

    # convert list of list to csv string
    csv_string = io.StringIO()
    csv_writer = csv.writer(csv_string)
    csv_writer.writerow(["OrderID", "CustomerID", "ProductID", "Quantity", "TotalAmount"])
    csv_writer.writerows(data)
    
    # Upload the CSV string to GCS
    blob = bucket.blob(full_file_name)
    blob.upload_from_string(csv_string.getvalue(), content_type='text/csv')

    print(f"Uploaded {full_file_name} successfully")

    return f"gs://{bucket_name}/{full_file_name}"

# def load_to_bq(file_uri, dataset_id, table_id):
#     bigquery_client = bigquery.Client()
#     dataset_ref = bigquery_client.dataset(dataset_id)
#     table_ref = dataset_ref.table(table_id)

#     job_config = bigquery.LoadJobConfig(
#         autodetect=True,
#         skip_leading_rows=1,
#         source_format=bigquery.SourceFormat.CSV,
#     )
    
#     load_job = bigquery_client.load_table_from_uri(file_uri, table_ref, job_config=job_config)
#     load_job.result()

#     print(f"Loaded {file_uri} to {table_id}")

if __name__ == "__main__":
    orders_data = generate_customer_orders()
    file_uri = upload_to_gcs(bucket_name=BUCKET,file_name='customer_orders', data=orders_data)
    # load_to_bq(file_uri, dataset_id='order_buck_dataset', table_id='customer_orders')