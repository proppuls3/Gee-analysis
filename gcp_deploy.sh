#!/bin/bash
# ==============================================================================
# Google Cloud (GCP) Deployment Script for GEE Data Agency
# Run these commands in your Google Cloud Shell or local authenticated terminal.
# ==============================================================================

PROJECT_ID="your-gcp-project-id"
REGION="us-central1"

echo "1. Enabling required GCP APIs..."
gcloud services enable run.googleapis.com sqladmin.googleapis.com compute.googleapis.com artifactregistry.googleapis.com

echo "2. Setting up Cloud SQL (PostgreSQL)..."
# This creates a micro PostgreSQL instance (cheap/free tier applicable)
gcloud sql instances create gee-db-instance --database-version=POSTGRES_14 --tier=db-f1-micro --region=$REGION
gcloud sql databases create gee_leads_db --instance=gee-db-instance
gcloud sql users create gee_user --instance=gee-db-instance --password=SuperSecretPassword123!

# Get the connection string format: postgresql+asyncpg://gee_user:SuperSecretPassword123!@/gee_leads_db?host=/cloudsql/PROJECT_ID:REGION:gee-db-instance

echo "3. Deploying the Next.js Frontend to Cloud Run..."
cd web-dashboard
gcloud run deploy gee-frontend \
  --source . \
  --region $REGION \
  --allow-unauthenticated \
  --max-instances 2 \
  --memory 512Mi

echo "4. Deploying the FastMCP Server to Cloud Run..."
cd ../backend
gcloud run deploy gee-mcp-server \
  --source . \
  --region $REGION \
  --allow-unauthenticated \
  --command "python" \
  --args "-m,mcp_server" \
  --set-env-vars DATABASE_URL="postgresql+asyncpg://gee_user:SuperSecretPassword123!@/gee_leads_db?host=/cloudsql/$PROJECT_ID:$REGION:gee-db-instance" \
  --max-instances 1 \
  --memory 512Mi

echo "5. Creating the e2-micro VM for the Python Orchestrator (100% Free Tier)..."
gcloud compute instances create gee-orchestrator-vm \
  --machine-type=e2-micro \
  --zone=${REGION}-a \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --metadata-from-file startup-script=../gcp_vm_startup.sh

echo "Deployment complete. Remember to restrict your Cloud SQL VPC networking!"
