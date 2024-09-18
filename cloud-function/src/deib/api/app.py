import time
import pandas as pd
import duckdb
from google.cloud import storage
import os
from flask import Flask, request
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

app = Flask(__name__)


def download_file_from_gcs(bucket_name, file_name, local_file):
    try:
        start_time = time.time()
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.download_to_filename(local_file)
        download_duration = time.time() - start_time
        logger.info(f"File download took: {download_duration:.2f} seconds")
    except Exception as e:
        logger.error(f"Error downloading file from GCS: {str(e)}")
        raise RuntimeError(f"Error downloading file from GCS: {str(e)}")


def process_parquet_file_with_duckdb(local_file):
    try:
        start_time = time.time()  # Start timing DuckDB processing
        con = duckdb.connect()
        con.execute("CREATE TABLE data AS SELECT * FROM parquet_scan(?)", [local_file])
        result = con.execute("SELECT * FROM data LIMIT 100").fetchall()
        con.close()
        processing_duration = time.time() - start_time
        logger.info(f"DuckDB processing took: {processing_duration:.2f} seconds")
        return result
    except Exception as e:
        logger.error(f"Error processing Parquet file with DuckDB: {str(e)}")
        raise RuntimeError(f"Error processing Parquet file with DuckDB: {str(e)}")


def process_parquet_file_with_pandas(local_file):
    try:
        start_time = time.time()  # Start timing Pandas processing
        df = pd.read_parquet(local_file)
        result = df.head(100).to_dict(orient='records')
        processing_duration = time.time() - start_time
        logger.info(f"Pandas processing took: {processing_duration:.2f} seconds")
        return result
    except Exception as e:
        logger.error(f"Error processing Parquet file with Pandas: {str(e)}")
        raise RuntimeError(f"Error processing Parquet file with Pandas: {str(e)}")


@app.route("/", methods=["GET"])
def process_parquet():
    try:
        bucket_name = os.environ.get('BUCKET_NAME')
        file_name = os.environ.get('FILE_NAME')
        processing_tool = request.args.get('tool', 'pandas')  # Default to Pandas if not specified

        if not bucket_name or not file_name:
            logger.error("BUCKET_NAME or FILE_NAME environment variable not set")
            return "BUCKET_NAME or FILE_NAME environment variable not set", 400

        local_file = f'/tmp/{file_name}'
        download_file_from_gcs(bucket_name, file_name, local_file)

        if processing_tool == 'duckdb':
            process_parquet_file_with_duckdb(local_file)
        else:
            process_parquet_file_with_pandas(local_file)

        os.remove(local_file)  # Cleanup the file after processing
        logger.info("Data processed successfully")
        return "Data processed successfully", 200
    except RuntimeError as e:
        logger.error(f"Runtime error: {str(e)}")
        return str(e), 500
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return f"Unexpected error: {str(e)}", 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
