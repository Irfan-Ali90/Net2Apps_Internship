# Net2Apps Internship — Automation Projects

Automation scripts developed during my internship at Net2Apps, focused on streamlining HR operations across **SAP** and **Dayforce**. This repo contains three task modules, each solving a real workflow automation problem using Python.

## 📁 Repository Structure

```
Net2Apps_Internship/
├── Tasks/
│   ├── sap-rating-scale-automation/       # Task 1
│   ├── dayforce-job-posting-automation/   # Task 2
│   └── sap-email-notification-automation/ # Task 3
├── .gitignore
└── README.md
```


---

## 🧩 Tasks Overview

### 1. SAP Rating Scale Automation (Selenium)
Automates the configuration and update of rating scales within SAP using browser automation, removing the need for manual navigation and data entry in the SAP UI.

- **Tech:** Python, Selenium
- **What it does:** Logs into SAP, navigates to the rating scale module, and creates/updates rating scale entries automatically.
- **Why:** Reduces manual, repetitive UI work and minimizes human error in configuration.

### 2. Dayforce Job Posting Automation (Requests)
Automates the creation and updating of job posting templates in Dayforce via API calls instead of manual form entry.

- **Tech:** Python, Requests
- **What it does:** Sends structured job posting data to Dayforce's API to create/update postings programmatically.
- **Why:** Speeds up job posting turnaround and ensures consistent formatting across postings.

### 3. SAP Email Notification Automation (Requests + BeautifulSoup)
Generates and sends email notification templates by pulling data from SAP via API and parsing/formatting the response.

- **Tech:** Python, Requests, BeautifulSoup
- **What it does:** Fetches relevant SAP data through API requests, parses the response (HTML/XML) with BeautifulSoup, and formats it into a ready-to-send email notification.
- **Why:** Automates recurring notification generation, ensuring accurate and timely communication.

---

## ⚙️ Tech Stack

- **Language:** Python
- **Libraries:** Selenium, Requests, BeautifulSoup4
- **Systems Automated:** SAP, Dayforce

## 🚀 Getting Started

Each task folder contains its own script(s). To run a task:

```bash
cd Tasks/<task-folder-name>
pip install -r requirements.txt   # if applicable
python <script-name>.py
```

> ⚠️ Note: These scripts were built for internal SAP/Dayforce environments and rely on company-specific credentials, endpoints, and configurations. Sensitive values (API keys, URLs, login credentials) have been excluded/sanitized and must be supplied via environment variables or a local config file before running.

## 📌 About

These projects were completed as part of my internship at **Net2Apps**, focused on automating repetitive HR system tasks in SAP and Dayforce to improve efficiency and reduce manual workload.
