# Quick Start: Deploy to Azure in 5 Minutes

This is a simplified guide to get your application running on Azure quickly.

---

## Prerequisites

- Azure account ([Get free trial](https://azure.microsoft.com/free/))
- Azure CLI installed ([Download](https://aka.ms/installazurecliwindows))

---

## Step 1: Login to Azure (1 minute)

```bash
# Open PowerShell or Command Prompt
az login

# This will open a browser - login with your Azure credentials
```

---

## Step 2: Create and Deploy (3 minutes)

Copy and paste this entire script into PowerShell:

```powershell
# Set your app name (must be globally unique - try adding your initials)
$APP_NAME = "payload-toolkit-sp"  # Change 'sp' to your initials

# Create everything and deploy
az group create --name payload-toolkit-rg --location eastus

az appservice plan create `
    --name payload-toolkit-plan `
    --resource-group payload-toolkit-rg `
    --sku B1 `
    --is-linux

az webapp create `
    --resource-group payload-toolkit-rg `
    --plan payload-toolkit-plan `
    --name $APP_NAME `
    --runtime "PYTHON:3.12"

az webapp config set `
    --resource-group payload-toolkit-rg `
    --name $APP_NAME `
    --startup-file "startup.sh"

# Deploy from local directory
az webapp up `
    --name $APP_NAME `
    --resource-group payload-toolkit-rg `
    --runtime "PYTHON:3.12"
```

---

## Step 3: Open Your App (1 minute)

```powershell
# Get your app URL
az webapp show --name $APP_NAME --resource-group payload-toolkit-rg --query defaultHostName -o tsv

# Or open directly in browser
az webapp browse --name $APP_NAME --resource-group payload-toolkit-rg
```

Your app will be available at: `https://YOUR-APP-NAME.azurewebsites.net`

---

## Troubleshooting

### If deployment fails:

```powershell
# View logs
az webapp log tail --name $APP_NAME --resource-group payload-toolkit-rg

# Restart app
az webapp restart --name $APP_NAME --resource-group payload-toolkit-rg
```

### If app name is taken:

Change `$APP_NAME` to something unique like `payload-toolkit-yourname123`

---

## Update Your App

After making changes locally:

```powershell
az webapp up --name $APP_NAME --resource-group payload-toolkit-rg
```

---

## Stop/Start App (to save costs)

```powershell
# Stop (no charges while stopped)
az webapp stop --name $APP_NAME --resource-group payload-toolkit-rg

# Start
az webapp start --name $APP_NAME --resource-group payload-toolkit-rg
```

---

## Delete Everything (cleanup)

```powershell
# WARNING: This deletes all resources
az group delete --name payload-toolkit-rg --yes --no-wait
```

---

## Cost Estimate

- **B1 Basic Plan**: ~$13/month
- **Free tier available** but with limitations

---

## Next Steps

- See [`AZURE_DEPLOYMENT.md`](AZURE_DEPLOYMENT.md) for advanced configuration
- Set up custom domain
- Enable HTTPS
- Configure monitoring
- Set up CI/CD pipeline

---

## Need Help?

- Check logs: `az webapp log tail --name $APP_NAME --resource-group payload-toolkit-rg`
- View app status: `az webapp show --name $APP_NAME --resource-group payload-toolkit-rg --query state`
- Azure Support: https://azure.microsoft.com/support/