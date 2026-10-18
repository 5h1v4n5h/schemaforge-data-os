# SchemaForge Data-OS: Public GitHub Repository

> **Live Public GitHub Repository:** [https://github.com/5h1v4n5h/schemaforge-data-os](https://github.com/5h1v4n5h/schemaforge-data-os)  
> **Status:** 🟢 Successfully Deployed & Publicly Accessible  
> **Default Branch:** `main`  
> **Zero Credential Guarantee:** Verified (100% ADC / environment variable configuration)  

---

## 1. Repository Quick Links

- **Repository URL:** [https://github.com/5h1v4n5h/schemaforge-data-os](https://github.com/5h1v4n5h/schemaforge-data-os)
- **Live Cloud Run Instance:** [https://schemaforge-app-605335322761.us-central1.run.app](https://schemaforge-app-605335322761.us-central1.run.app)
- **PowerPoint Pitch Deck:** [`docs/SchemaForge_DataOS_PitchDeck.pptx`](SchemaForge_DataOS_PitchDeck.pptx)
- **Technical Architecture Manual:** [`docs/ARCHITECTURE_AND_SYSTEM_MANUAL.md`](ARCHITECTURE_AND_SYSTEM_MANUAL.md)

---

## 2. Pushing Future Updates to GitHub

To push future local commits to GitHub:

```bash
git add .
git commit -m "your commit message"
git push origin main
```

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
