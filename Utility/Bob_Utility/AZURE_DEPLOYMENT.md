# Azure Deployment Guide
## Enterprise Payload Utility Toolkit

This guide covers deploying the application to Azure using Azure App Service.

---

## Prerequisites

1. **Azure Account** with active subscription
2. **Azure CLI** installed ([Download](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))
3. **Git** installed
4. **Python 3.12+** installed locally

---

## Deployment Options

### Option 1: Azure App Service (Recommended)
- Best for production workloads
- Auto-scaling capabilities
- Built-in SSL/HTTPS
- Easy CI/CD integration

### Option 2: Azure Container Instances
- For containerized deployments
- More control over environment

### Option 3: Azure Kubernetes Service (AKS)
- For enterprise-scale deployments
- Advanced orchestration

---

## Option 1: Deploy to Azure App Service (Step-by-Step)

### Step 1: Install Azure CLI and Login

```bash
# Install Azure CLI (if not already installed)
# Windows: Download from https://aka.ms/installazurecliwindows

# Login to Azure
az login

# Set your subscription (if you have multiple)
az account list --output table
az account set --subscription "YOUR_SUBSCRIPTION_ID"
```

### Step 2: Create Azure Resources

```bash
# Set variables
RESOURCE_GROUP="payload-toolkit-rg"
LOCATION="eastus"  # or your preferred region
APP_NAME="payload-toolkit-app"  # Must be globally unique
APP_SERVICE_PLAN="payload-toolkit-plan"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create App Service Plan (B1 tier - suitable for production)
az appservice plan create \
    --name $APP_SERVICE_PLAN \
    --resource-group $RESOURCE_GROUP \
    --sku B1 \
    --is-linux

# Create Web App
az webapp create \
    --resource-group $RESOURCE_GROUP \
    --plan $APP_SERVICE_PLAN \
    --name $APP_NAME \
    --runtime "PYTHON:3.12"
```

### Step 3: Configure Application Settings

```bash
# Set environment variables
az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME \
    --settings \
        ENVIRONMENT="production" \
        LOG_LEVEL="INFO" \
        BACKEND_HOST="0.0.0.0" \
        BACKEND_PORT="8000"

# Configure startup command
az webapp config set \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME \
    --startup-file "startup.sh"
```

### Step 4: Deploy Application

#### Method A: Deploy from Local Git

```bash
# Configure local git deployment
az webapp deployment source config-local-git \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP

# Get deployment credentials
az webapp deployment list-publishing-credentials \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --query "{username:publishingUserName, password:publishingPassword}"

# Add Azure remote
git remote add azure https://$APP_NAME.scm.azurewebsites.net/$APP_NAME.git

# Deploy
git add .
git commit -m "Deploy to Azure"
git push azure main
```

#### Method B: Deploy via ZIP

```bash
# Create deployment package
zip -r deploy.zip . -x "*.git*" -x "*__pycache__*" -x "*.pyc"

# Deploy ZIP
az webapp deployment source config-zip \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME \
    --src deploy.zip
```

#### Method C: Deploy from GitHub (CI/CD)

```bash
# Configure GitHub deployment
az webapp deployment source config \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --repo-url https://github.com/YOUR_USERNAME/YOUR_REPO \
    --branch main \
    --manual-integration
```

### Step 5: Verify Deployment

```bash
# Get app URL
az webapp show \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --query defaultHostName --output tsv

# Open in browser
az webapp browse --name $APP_NAME --resource-group $RESOURCE_GROUP

# View logs
az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP
```

---

## Post-Deployment Configuration

### Enable HTTPS Only

```bash
az webapp update \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME \
    --https-only true
```

### Configure Custom Domain (Optional)

```bash
# Add custom domain
az webapp config hostname add \
    --webapp-name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --hostname www.yourdomain.com

# Enable SSL
az webapp config ssl bind \
    --certificate-thumbprint YOUR_CERT_THUMBPRINT \
    --ssl-type SNI \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP
```

### Enable Application Insights (Monitoring)

```bash
# Create Application Insights
az monitor app-insights component create \
    --app $APP_NAME-insights \
    --location $LOCATION \
    --resource-group $RESOURCE_GROUP

# Get instrumentation key
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
    --app $APP_NAME-insights \
    --resource-group $RESOURCE_GROUP \
    --query instrumentationKey --output tsv)

# Configure app to use Application Insights
az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME \
    --settings APPINSIGHTS_INSTRUMENTATIONKEY=$INSTRUMENTATION_KEY
```

### Scale Up/Out

```bash
# Scale up (increase instance size)
az appservice plan update \
    --name $APP_SERVICE_PLAN \
    --resource-group $RESOURCE_GROUP \
    --sku P1V2

# Scale out (increase instance count)
az webapp scale \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --instance-count 3
```

---

## Troubleshooting

### View Application Logs

```bash
# Enable logging
az webapp log config \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --application-logging filesystem \
    --level information

# Stream logs
az webapp log tail \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP
```

### SSH into Container

```bash
az webapp ssh \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP
```

### Restart Application

```bash
az webapp restart \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP
```

---

## Cost Optimization

### Pricing Tiers

- **F1 (Free)**: Good for testing, limited resources
- **B1 (Basic)**: $13/month, suitable for small production
- **S1 (Standard)**: $70/month, auto-scaling, staging slots
- **P1V2 (Premium)**: $146/month, better performance

### Stop App When Not in Use

```bash
az webapp stop --name $APP_NAME --resource-group $RESOURCE_GROUP
az webapp start --name $APP_NAME --resource-group $RESOURCE_GROUP
```

---

## Security Best Practices

1. **Enable HTTPS Only** (already configured above)
2. **Use Managed Identity** for Azure resource access
3. **Store secrets in Azure Key Vault**
4. **Enable Azure AD authentication** (optional)
5. **Configure CORS** properly
6. **Enable DDoS protection**
7. **Regular security updates**

---

## Monitoring and Alerts

### Set Up Alerts

```bash
# CPU alert
az monitor metrics alert create \
    --name high-cpu-alert \
    --resource-group $RESOURCE_GROUP \
    --scopes /subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Web/sites/$APP_NAME \
    --condition "avg Percentage CPU > 80" \
    --window-size 5m \
    --evaluation-frequency 1m

# Memory alert
az monitor metrics alert create \
    --name high-memory-alert \
    --resource-group $RESOURCE_GROUP \
    --scopes /subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Web/sites/$APP_NAME \
    --condition "avg MemoryPercentage > 80" \
    --window-size 5m \
    --evaluation-frequency 1m
```

---

## Cleanup (Delete Resources)

```bash
# Delete entire resource group (WARNING: This deletes everything!)
az group delete --name $RESOURCE_GROUP --yes --no-wait
```

---

## Quick Reference Commands

```bash
# View app status
az webapp show --name $APP_NAME --resource-group $RESOURCE_GROUP --query state

# View app URL
az webapp show --name $APP_NAME --resource-group $RESOURCE_GROUP --query defaultHostName -o tsv

# View deployment status
az webapp deployment list --name $APP_NAME --resource-group $RESOURCE_GROUP

# View app settings
az webapp config appsettings list --name $APP_NAME --resource-group $RESOURCE_GROUP

# Update app settings
az webapp config appsettings set --name $APP_NAME --resource-group $RESOURCE_GROUP --settings KEY=VALUE
```

---

## Support and Documentation

- [Azure App Service Documentation](https://docs.microsoft.com/en-us/azure/app-service/)
- [Azure CLI Reference](https://docs.microsoft.com/en-us/cli/azure/)
- [Python on Azure](https://docs.microsoft.com/en-us/azure/developer/python/)

---

## Next Steps

1. Set up CI/CD pipeline (see `azure-pipelines.yml`)
2. Configure custom domain and SSL
3. Enable Application Insights monitoring
4. Set up automated backups
5. Configure staging slots for zero-downtime deployments