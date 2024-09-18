import os
import pytest
from deib.api.app import (download_file_from_gcs, process_parquet_file_with_duckdb, process_parquet_file_with_pandas,
                          app)


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# Test 1: Simulate downloading from Google Cloud Storage
def test_download_file_from_gcs(mocker):
    # Mock the GCS client
    mock_storage_client = mocker.patch('google.cloud.storage.Client')
    mock_bucket = mock_storage_client.return_value.bucket.return_value
    mock_blob = mock_bucket.blob.return_value

    # Mock logger
    mock_logger = mocker.patch('deib.api.app.logger')

    # Call the function to download the file
    download_file_from_gcs('test-bucket', 'test-file.parquet', '/tmp/test-file.parquet')

    # Verify that the file was downloaded with the correct filename
    mock_blob.download_to_filename.assert_called_once_with('/tmp/test-file.parquet')

    # Verify that logging happened
    mock_logger.info.assert_called_with(mocker.ANY)


# Test 2: Process Parquet file using DuckDB with logging
def test_process_parquet_file_with_duckdb(mocker):
    local_file = '/tmp/test-file.parquet'

    # Mock DuckDB connection and query execution
    mock_connect = mocker.patch('duckdb.connect')
    mock_conn = mock_connect.return_value
    mock_conn.execute.return_value.fetchall.return_value = [(1, 'test')]

    # Mock logger
    mock_logger = mocker.patch('deib.api.app.logger')

    # Call the function that processes the Parquet file with DuckDB
    result = process_parquet_file_with_duckdb(local_file)

    # Verify the expected result
    assert result == [(1, 'test')]

    # Ensure both queries were executed in the correct order
    mock_conn.execute.assert_has_calls([
        mocker.call("CREATE TABLE data AS SELECT * FROM parquet_scan(?)", [local_file]),
        mocker.call("SELECT * FROM data LIMIT 100")
    ])

    # Verify that logging happened
    mock_logger.info.assert_called()


# Test 3: Process Parquet file using Pandas with logging
def test_process_parquet_file_with_pandas(mocker):
    local_file = '/tmp/test-file.parquet'

    # Mock Pandas' read_parquet method
    mock_read_parquet = mocker.patch('pandas.read_parquet')
    mock_df = mock_read_parquet.return_value
    mock_df.head.return_value.to_dict.return_value = [{'id': 1, 'name': 'test'}]

    # Mock logger
    mock_logger = mocker.patch('deib.api.app.logger')

    # Call the function that processes the Parquet file with Pandas
    result = process_parquet_file_with_pandas(local_file)

    # Verify the expected result
    assert result == [{'id': 1, 'name': 'test'}]

    # Ensure that Pandas' read_parquet was called
    mock_read_parquet.assert_called_once_with(local_file)
    mock_df.head.assert_called_once_with(100)

    # Verify that logging happened
    mock_logger.info.assert_called_with(mocker.ANY)


# Test 4: Cloud Function with DuckDB processing and logging
def test_process_parquet_with_duckdb(mocker, client):
    # Mock download and processing functions
    mock_download_file_from_gcs = mocker.patch('deib.api.app.download_file_from_gcs')
    mock_process_parquet_file_with_duckdb = mocker.patch('deib.api.app.process_parquet_file_with_duckdb')
    mock_remove = mocker.patch('os.remove')

    # Set mock return value for DuckDB processing
    mock_process_parquet_file_with_duckdb.return_value = [(1, 'test')]

    # Mock logger
    mock_logger = mocker.patch('deib.api.app.logger')

    # Set environment variables
    os.environ['BUCKET_NAME'] = 'test-bucket'
    os.environ['FILE_NAME'] = 'test-file.parquet'

    # Perform a GET request to the Flask app with DuckDB as the tool
    response = client.get("/?tool=duckdb")

    # Verify that the request was successful
    assert response.status_code == 200
    assert response.data.decode() == "Data processed successfully"

    # Ensure the correct functions were called with the right parameters
    mock_download_file_from_gcs.assert_called_once_with('test-bucket', 'test-file.parquet', '/tmp/test-file.parquet')
    mock_process_parquet_file_with_duckdb.assert_called_once_with('/tmp/test-file.parquet')
    mock_remove.assert_called_once_with('/tmp/test-file.parquet')

    # Verify that logging happened
    mock_logger.info.assert_called()


# Test 5: Cloud Function with Pandas processing and logging
def test_process_parquet_with_pandas(mocker, client):
    # Mock download and processing functions
    mock_download_file_from_gcs = mocker.patch('deib.api.app.download_file_from_gcs')
    mock_process_parquet_file_with_pandas = mocker.patch('deib.api.app.process_parquet_file_with_pandas')
    mock_remove = mocker.patch('os.remove')

    # Set mock return value for Pandas processing
    mock_process_parquet_file_with_pandas.return_value = [{'id': 1, 'name': 'test'}]

    # Mock logger
    mock_logger = mocker.patch('deib.api.app.logger')

    # Set environment variables
    os.environ['BUCKET_NAME'] = 'test-bucket'
    os.environ['FILE_NAME'] = 'test-file.parquet'

    # Perform a GET request to the Flask app with Pandas as the tool
    response = client.get("/?tool=pandas")

    # Verify that the request was successful
    assert response.status_code == 200
    assert response.data.decode() == "Data processed successfully"

    # Ensure the correct functions were called with the right parameters
    mock_download_file_from_gcs.assert_called_once_with('test-bucket', 'test-file.parquet', '/tmp/test-file.parquet')
    mock_process_parquet_file_with_pandas.assert_called_once_with('/tmp/test-file.parquet')
    mock_remove.assert_called_once_with('/tmp/test-file.parquet')

    # Verify that logging happened
    mock_logger.info.assert_called()


# Test 6: Error during the download from GCS, check logging
def test_process_parquet_download_error(mocker, client):
    # Mock download function to raise an error
    mock_download_file_from_gcs = mocker.patch('deib.api.app.download_file_from_gcs',
                                               side_effect=RuntimeError("Download error"))

    # Mock logger
    mock_logger = mocker.patch('deib.api.app.logger')

    # Set environment variables
    os.environ['BUCKET_NAME'] = 'test-bucket'
    os.environ['FILE_NAME'] = 'test-file.parquet'

    # Perform a GET request to the Flask app
    response = client.get("/?tool=pandas")

    # Verify that the error was caught and the response is a 500 error
    assert response.status_code == 500
    assert "Download error" in response.data.decode()

    # Verify that error logging happened
    mock_logger.error.assert_called_with('Runtime error: Download error')


# Test 7: Missing environment variables (BUCKET_NAME or FILE_NAME), check logging
def test_process_parquet_env_var_error(mocker, client):
    # Mock logger
    mock_logger = mocker.patch('deib.api.app.logger')

    # Remove the environment variables
    if 'BUCKET_NAME' in os.environ:
        del os.environ['BUCKET_NAME']
    if 'FILE_NAME' in os.environ:
        del os.environ['FILE_NAME']

    # Perform a GET request to the Flask app
    response = client.get("/?tool=pandas")

    # Verify that the environment variable error is caught and a 400 error is returned
    assert response.status_code == 400
    assert "BUCKET_NAME or FILE_NAME environment variable not set" in response.data.decode()

    # Verify that error logging happened
    mock_logger.error.assert_called_with("BUCKET_NAME or FILE_NAME environment variable not set")
