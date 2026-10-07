# Professional RFM Dashboard

## Purpose

Interactive corporate-style dashboard for the VEDA Technology
E-Commerce Customer Segmentation and RFM Analysis project.

## Features

- Four equal KPI cards
- Four equal top filters
- Three equal analytics panels
- Two equal detail panels
- Customer segment distribution
- Interactive 3D RFM customer map
- Segment marketing recommendations
- Top-customer RFM data preview
- Dark corporate analytics theme
- Power BI-ready customer data

## Run

From the project root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run dashboard/app.py
```

The dashboard reads:

```text
output/customer_rfm_segments.csv
```
