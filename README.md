# 🎓 Student Fees Payment Portal

A cloud-native, secure **Django-based web application** hosted on **Microsoft Azure**, built to manage and automate student fee payments.  
The portal integrates with **Microsoft Entra ID (Azure AD)** for authentication, uses **Azure SQL Database** for persistence, and is deployed via a **Dockerized CI/CD pipeline** through **GitHub Actions**, **Azure Container Registry (ACR)**, and **Azure App Service**.

---

## 🌐 Architecture Overview



+------------------+
| End Users |
| (Students/Admin) |
+------------------+
│ HTTPS
▼
+----------------------------+
| Azure App Service (Linux) | <-- Runs Dockerized Django app
| Web App: rec-student-fee-portal
+----------------------------+
│
▼
+---------------------------+
| Azure SQL Database |
| Server: rec-server |
| DB: db |
+---------------------------+
│
▼
+----------------------------+
| Azure Container Registry |
| studentfeeportalacr |
| Stores Docker images |
+----------------------------+
│
▼
+----------------------------+
| GitHub Actions CI/CD |
| (Build → Push → Deploy) |
+----------------------------+


---

## 🧱 Prerequisites

### 1. Azure Resources
Ensure the following resources exist in your subscription:

| Resource | Name | Notes |
|-----------|------|-------|
| Resource Group | `student-fee-portal` | Centralized container |
| App Service Plan | `ASP-studentfeeportal-a966 (B1:1)` | Linux plan |
| App Service (Web App) | `rec-student-fee-portal` | Container-based |
| Azure Container Registry | `studentfeeportalacr` | For image hosting |
| Azure SQL Server | `rec-server` | Contains `db` database |
| Tenant ID | `090e9fac-6b24-42f9-9e35-7120cf0a737a` | Microsoft Entra ID |
| App (Client) ID | `179db131-c3d9-40e5-9ddc-d363147a0e2d` | Django Auth App Registration |

---

## 🧩 Local Setup (Development Environment)

### 1. Clone the Repository

```bash
git clone https://github.com/Kiruthhik/Fees-Payment-Portal.git
cd Fees-Payment-Portal

2. Create a .env file

Create a .env file inside the payment_portal folder with the following keys:

# Django settings
SECRET_KEY=<your-secret-key>
DEBUG=True

# Azure SQL Database credentials
DB_NAME=db
DB_USER=<your-db-username>
DB_PASSWORD=<your-db-password>
DB_HOST=rec-server.database.windows.net

# Azure AD Authentication (django_auth_adfs)
CLIENT_ID=179db131-c3d9-40e5-9ddc-d363147a0e2d
CLIENT_SECRET=<your-client-secret>
TENANT_ID=090e9fac-6b24-42f9-9e35-7120cf0a737a

# Redirect URIs
REDIRECT_URI=http://localhost:8000/oauth2/callback


💡 For local development, ensure the Azure AD App Registration includes
http://localhost:8000/oauth2/callback as a redirect URI.

3. Run with Docker Compose
docker compose up --build


Django will automatically apply migrations and start Gunicorn at http://localhost:8000.

Log in via the /login/ endpoint using your Azure AD account.

☁️ Azure Deployment Setup (from Scratch)

Follow these steps to deploy from scratch to Azure:

1. Create the Resource Group
az group create --name student-fee-portal --location "Central India"

2. Deploy Infrastructure (Optional – using ARM Template)

If using your template.json and parameters.json:

az deployment group create \
  --name student-fee-portal-deploy \
  --resource-group student-fee-portal \
  --template-file template.json \
  --parameters @parameters.json


This provisions:

Azure App Service Plan

Web App

Azure SQL Database

Azure Container Registry (ACR)

3. Build & Push Docker Image to ACR
# Login to ACR
az acr login --name studentfeeportalacr

# Build and tag image
docker build -t studentfeeportalacr.azurecr.io/feepayment-portal:latest .

# Push image
docker push studentfeeportalacr.azurecr.io/feepayment-portal:latest

4. Configure Web App Container
az webapp config container set \
  --name rec-student-fee-portal \
  --resource-group student-fee-portal \
  --docker-custom-image-name studentfeeportalacr.azurecr.io/feepayment-portal:latest \
  --docker-registry-server-url https://studentfeeportalacr.azurecr.io

5. Set Environment Variables
az webapp config appsettings set \
  --name rec-student-fee-portal \
  --resource-group student-fee-portal \
  --settings \
  SECRET_KEY=<secret> \
  DEBUG=False \
  DB_NAME=db \
  DB_USER=<db-user> \
  DB_PASSWORD=<db-password> \
  DB_HOST=rec-server.database.windows.net \
  CLIENT_ID=179db131-c3d9-40e5-9ddc-d363147a0e2d \
  CLIENT_SECRET=<client-secret> \
  TENANT_ID=090e9fac-6b24-42f9-9e35-7120cf0a737a

🔁 CI/CD Pipeline (GitHub Actions)

The project includes a GitHub Actions workflow that automates:

Docker Build →
Builds the image from the Dockerfile in the repo.

Push to ACR →
Uploads the built image to studentfeeportalacr.azurecr.io.

Deploy to Azure Web App →
Updates the App Service with the new image tag.

Example Trigger

Any push to the main branch automatically triggers deployment.

Redeployment

Modify your code and git push to main.

GitHub Actions runs the workflow automatically.

Once successful, Azure Web App pulls the updated image and restarts.

🚀 Manual Redeployment (if pipeline fails)

If you need to redeploy manually:

az acr login --name studentfeeportalacr
docker build -t studentfeeportalacr.azurecr.io/feepayment-portal:<newtag> .
docker push studentfeeportalacr.azurecr.io/feepayment-portal:<newtag>

az webapp config container set \
  --name rec-student-fee-portal \
  --resource-group student-fee-portal \
  --docker-custom-image-name studentfeeportalacr.azurecr.io/feepayment-portal:<newtag> \
  --docker-registry-server-url https://studentfeeportalacr.azurecr.io

az webapp restart --name rec-student-fee-portal --resource-group student-fee-portal

🧠 Authentication Flow (Microsoft Entra ID)

User clicks Login → redirected to Azure AD login page

Azure AD returns an OAuth token with claims (email, name, roles)

django_auth_adfs validates token → logs user in

User is redirected to /home/ dashboard

Important ADFS Settings

Located in payment_portal/settings.py:

AUTH_ADFS = {
    'AUDIENCE': os.getenv('CLIENT_ID'),
    'CLIENT_ID': os.getenv('CLIENT_ID'),
    'CLIENT_SECRET': os.getenv('CLIENT_SECRET'),
    'TENANT_ID': os.getenv('TENANT_ID'),
    'RELYING_PARTY_ID': os.getenv('CLIENT_ID'),
    'USERNAME_CLAIM': 'email',
    'GROUPS_CLAIM': 'roles',
    'MIRROR_GROUPS': True,
    'LOGIN_EXEMPT_URLS': ["^$", "api/", "public/"],
}

🧰 Troubleshooting Guide
Issue	Cause	Fix
500 error on /login/	Missing claim (email)	Change USERNAME_CLAIM to unique_name
DB connection failed	Firewall or wrong credentials	Add App Service outbound IPs to Azure SQL firewall
Container crash	EntryPoint script line endings (CRLF)	Use LF line endings in entrypoint.sh
Static files not loading	collectstatic not run	Add python manage.py collectstatic --noinput before deployment
📊 Monitoring and Logs

Enable logging and monitor performance:

az webapp log config \
  --name rec-student-fee-portal \
  --resource-group student-fee-portal \
  --docker-container-logging filesystem

az webapp log tail \
  --name rec-student-fee-portal \
  --resource-group student-fee-portal


Optional: Enable Application Insights for runtime metrics.

🧩 Future Enhancements

Add Azure Key Vault integration for secret management

Integrate Azure OpenAI API for fee query assistance

Use Azure AD roles for admin/student authorization

Migrate to Azure Kubernetes Service (AKS) for scalability

👥 Contributors

Team Lead: Kiruthhik

Contributors: Abilash M, Team Members

Mentor: [Faculty Name]

📄 License

This project is licensed under the MIT License.

🔗 Useful Links

Azure Portal: https://portal.azure.com

GitHub Repo: https://github.com/Kiruthhik/Fees-Payment-Portal

Deployed App: https://rec-student-fee-portal.azurewebsites.net


---
