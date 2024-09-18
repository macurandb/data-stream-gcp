# DataStreamGCP

**DataStreamGCP** is a cloud-based data processing pipeline that integrates **BigQuery**, **Google Cloud Storage (GCS)**, **Cloud Run**, and **DuckDB** for efficient data extraction, transformation, and analysis. This project provides a scalable solution for querying large datasets from BigQuery, exporting them to GCS, and processing them in real-time using Cloud Run and DuckDB.

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [Features](#features)
- [Setup and Deployment](#setup-and-deployment)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Makefile Commands](#makefile-commands)
  - [Terraform Deployment](#terraform-deployment)
- [Cloud Run Application](#cloud-run-application)
- [BigQuery Scheduled Queries](#bigquery-scheduled-queries)
- [Google Cloud Scheduler](#google-cloud-scheduler)
- [Contribution Guidelines](#contribution-guidelines)
- [License](#license)

---

## Overview

**DataStreamGCP** provides a data processing pipeline designed to:
1. Query data from **BigQuery** at scheduled intervals.
2. Export the queried data to **Google Cloud Storage (GCS)** in **Parquet** format.
3. Process the exported data using **Cloud Run** and **DuckDB** for fast, in-memory analytics.
4. Automate this process using **Google Cloud Scheduler** to manage the workflow without manual intervention.

This architecture allows for fast, flexible, and scalable data processing in a serverless environment, ensuring high performance and reduced infrastructure management.

---

## Project Structure

The project is structured into several modules to ensure clarity, modularity, and scalability:

project-root/
├── cloud-function/
│   ├── src/
│   │   └── main.py               # Python script for processing data with DuckDB
│   ├── Dockerfile                # Dockerfile to build the Cloud Run service
├── infra/
│   ├── modules/
│   │   ├── bigquery-scheduled-query/
│   │   │   ├── main.tf           # Terraform for scheduling BigQuery queries
│   │   ├── cloud-run/
│   │   │   ├── main.tf           # Terraform for deploying Cloud Run
│   │   │   ├── Dockerfile        # Dockerfile for the Cloud Run service
│   │   ├── gcs-bucket/
│   │   │   ├── main.tf           # Terraform for creating GCS bucket
│   │   ├── permissions/
│   │   │   ├── main.tf           # IAM permissions setup
│   ├── envs/
│   │   ├── dev/
│   │   │   └── terragrunt.hcl     # Terragrunt configuration for dev environment
│   │   ├── prod/
│   │   │   └── terragrunt.hcl     # Terragrunt configuration for prod environment
├── Makefile # Makefile for simplifying commands
└── README.md      
# Project documentation

---

## Technologies

- **Google BigQuery**: For querying large datasets.
- **Google Cloud Storage (GCS)**: For storing the exported data.
- **Google Cloud Run**: To run the serverless container that processes data.
- **DuckDB**: A lightweight, fast database engine for in-memory data processing.
- **Terraform**: Infrastructure as code for automating the setup.
- **Terragrunt**: For managing multiple environments (dev, prod).
- **Google Cloud Scheduler**: For automating periodic execution of the pipeline.
- **Makefile**: For automating common tasks such as building, deploying, and testing the application.

---

## Features

- **Scheduled Data Export**: Export data from BigQuery to GCS using BigQuery scheduled queries.
- **Efficient Processing with DuckDB**: Use DuckDB to perform in-memory analytics on the exported data.
- **Serverless Execution**: Cloud Run provides an auto-scaling, cost-effective serverless environment.
- **Automated Workflows**: Use Cloud Scheduler to trigger the data processing pipeline at scheduled intervals.
- **Multi-environment Support**: Manage infrastructure for multiple environments (e.g., dev, prod) using Terraform and Terragrunt.
- **Automation with Makefile**: Simplifies tasks like building Docker images, deploying Cloud Run services, and running Terraform commands.

---

## Setup and Deployment

### Prerequisites

- Google Cloud Platform (GCP) project.
- **gcloud** CLI installed.
- **Terraform** and **Terragrunt** installed.
- Docker installed for building the Cloud Run service.
- Make installed to automate tasks using the Makefile.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/DataStreamGCP.git
   cd DataStreamGCP

### Set up Google Cloud SDK

1. **Install and initialize gcloud**:
   Install the **Google Cloud SDK** if you haven't already. You can follow the installation instructions [here](https://cloud.google.com/sdk/docs/install).

   Once installed, initialize the `gcloud` CLI:
   ```bash
   gcloud init
   ```

2. **Authenticate your GCP account: Ensure you're authenticated to interact with your Google Cloud project**:
    ```bash 
       gcloud auth login
    ```
   
3. **Set the active project: Select the GCP project where you want to deploy the infrastructure**:
```bash
    gcloud config set project [YOUR_PROJECT_ID]
```

### Enable Required GCP Services
```bash 
    gcloud services enable bigquery.googleapis.com \
                         storage.googleapis.com \
                         run.googleapis.com \
                         cloudbuild.googleapis.com \
                         cloudscheduler.googleapis.com

```

## Using Makefile