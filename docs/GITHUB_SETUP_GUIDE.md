# SchemaForge Data-OS: Public GitHub Repository Publishing Guide

> **Target:** Publishing the verified, clean SchemaForge Data-OS codebase to a public GitHub repository with zero credential exposure.

---

## 1. Pre-Flight Verification Checklist

Before publishing, verify the repository has zero leaked secrets or personal credentials:

```bash
# 1. Verify working directory is clean of untracked secrets
git status

# 2. Confirm no private keys or tokens exist in tracked files
git grep -i "BEGIN PRIVATE KEY"
git grep -i "client_secret"
```

✅ **Status:** Verified clean. All credentials authenticate via Google Cloud Application Default Credentials (ADC) or environment variables (`.env.example`).

---

## 2. Publish to GitHub in 3 Steps

### Step 1: Create a New Empty Repository on GitHub
1. Go to [GitHub - New Repository](https://github.com/new).
2. Set **Repository name**: `schemaforge-data-os` (or your preferred name).
3. Set **Visibility**: **Public**.
4. **DO NOT** initialize with a README, .gitignore, or license (we already have pristine versions).
5. Click **Create repository**.

### Step 2: Add Remote and Push Local Commits
In your local terminal (Windows PowerShell or Command Prompt), run:

```bash
# Make sure you are on the main branch
git branch -M main

# Add your GitHub repository as remote (replace YOUR_GITHUB_USERNAME)
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/schemaforge-data-os.git

# Push the verified codebase
git push -u origin main
```

### Step 3: Recommended GitHub Repository Settings
- **About / Description**: `SchemaForge Data-OS: Autonomous Ingestion & Neuro-Symbolic Self-Healing Data Engineering Platform powered by Google Cloud Run, BigQuery, Pub/Sub & Gemini.`
- **Website**: `https://schemaforge-app-605335322761.us-central1.run.app`
- **Topics / Tags**:
  - `google-cloud`
  - `bigquery`
  - `cloud-run`
  - `gemini`
  - `neuro-symbolic-ai`
  - `data-observability`
  - `self-healing`
  - `fastapi`
  - `pubsub`

---

## 3. Continuous Cloud Run Deployment from GitHub (Optional CI/CD)

If you wish to enable continuous deployment directly from your GitHub repository to Google Cloud Run:

```bash
gcloud run deploy schemaforge-app \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```
