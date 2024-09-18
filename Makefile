# Project-specific variables
PROJECT_ID = "example"
IMAGE_NAME = gcr.io/$(PROJECT_ID)/datastreamgcp
REGION = us-central1

# Directories
CLOUD_FUNCTION_DIR = cloudfunction
INFRA_DIR = infra
COMMON_DIR = $(INFRA_DIR)/common
MODULES_DIR = $(INFRA_DIR)/modules
ENVS_DIR = $(INFRA_DIR)/envs

# Build the Docker image using the Dockerfile in the cloudfunction directory
build:
	docker build -t $(IMAGE_NAME) $(CLOUD_FUNCTION_DIR)

# Push the Docker image to Google Container Registry
push:
	docker push $(IMAGE_NAME)

# Initialize Terraform with Terragrunt in the infra/envs directory
terraform-init:
	cd $(ENVS_DIR) && terragrunt init

# Apply Terraform changes with Terragrunt in the infra/envs directory
terraform-apply:
	cd $(ENVS_DIR) && terragrunt apply

# Clean up local Docker images
clean:
	docker rmi $(IMAGE_NAME)

# Zip the function code (if packaging the Cloud Function code as a zip for deployment)
zip-function:
	cd $(CLOUD_FUNCTION_DIR) && zip -r function.zip .
