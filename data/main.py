from google.cloud import bigquery, storage

#TO DO:
# Copy the table ID from big query on GCP and paste it below
STAGE_TABLE_ID = "proven-grin-377705.customer_details.customer_detail_stage"

storageClient = storage.Client()
bigQueryClient = bigquery.Client() #to access gcp

def truncateData(uri):
    try:
        job_config = bigquery.LoadJobConfig( #data append
        schema=[
            bigquery.SchemaField("first_name", "STRING", "REQUIRED"),
            bigquery.SchemaField("last_name", "STRING", "REQUIRED"),
            bigquery.SchemaField("company_name", "STRING", "REQUIRED"),
            bigquery.SchemaField("age", "NUMERIC", "REQUIRED"),
            bigquery.SchemaField("mail_id", "STRING", "REQUIRED"),
            bigquery.SchemaField("dob", "DATE", "REQUIRED"),
            bigquery.SchemaField("address", "STRING", "REQUIRED"),
            bigquery.SchemaField("country", "STRING", "REQUIRED")
        ],
            skip_leading_rows=1,
            source_format=bigquery.SourceFormat.CSV,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE  # #APPEND  
        )
        print("Appending Data into table")
        job = bigQueryClient.load_table_from_uri(uri, STAGE_TABLE_ID, job_config=job_config)
        job.result()
        print("Data successfully appended into the table")


        # If file was present, locally, we can use below code to append data
        # with open("customer.csv", "rb") as file:
        #     bigQueryClient.load_table_from_file(file, TABLE_ID ,job_config=job_config)
    except Exception as e:
        print(str(e))
        print("Error while appending data into the table")



def runProcedure():
    try:
        ## TODO:
        ## Copy and paste the PROC_id below from Routines inside your Dataset.
        proc = "proven-grin-377705.customer_details.routine_id"
        if proc:
            print("PROCEDURE STARTED")
            q = """CALL `""" + proc + """`();"""
            print("Running query")
            query_job = bigQueryClient.query(q)
            query_job.result()
            print("Query Executed")
    except Exception as e:
        print("Error while running procedure")
        print(str(e))

def main(event :dict, context):
    fileName = event["name"]
    uri = "gs://" + event['bucket'] + "/" + fileName
    truncateData(uri=uri)
    runProcedure()

    # fileInCurrentBucket = storageClient.bucket(event['bucket'])
    # fileInCurrentBucket.delete_blob(fileName)