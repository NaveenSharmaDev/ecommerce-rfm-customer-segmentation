# E-Commerce Customer Segmentation — RFM Analysis

VEDA Technology-ready upgraded project using **RFM analysis + K-Means clustering**, Excel, Power BI-ready datasets, business recommendations and an optional Streamlit dashboard.

## Objective
- Calculate Recency, Frequency and Monetary metrics.
- Assign 1–5 RFM scores.
- Apply K-Means to customer behavior.
- Convert clusters into business-friendly segments.
- Produce campaign recommendations and Power BI-ready outputs.

## Segments
**Champions, Loyal Customers, At-Risk Customers, Potential Loyalists, Lost Customers**

## Dataset validation
The uploaded project contained a broken `raw_data.xlsx` file (2 bytes). It was not usable. The supplied cleaned workbook was validated and retained as `data/cleaned_transactions.xlsx`.

Current analytical population:
- Transactions: **391,150**
- Customers: **4,334**
- Invoices: **18,402**
- Products: **3,659**
- Countries: **37**
- Revenue: **£8,737,227.64**
- Date range: **2010-12-01 to 2011-12-09**

## Upgrades/fixes
- Removed dependency on the unusable raw workbook.
- Added robust validation and transaction filtering.
- Added actual **K-Means** clustering required by the project brief.
- Added rank-safe quintile RFM scoring.
- Added business-friendly segment naming.
- Added silhouette score for model-quality reporting.
- Added Power BI-ready CSVs.
- Added professional Excel report.
- Added business recommendation and data dictionary.
- Added optional Streamlit dashboard.
- Added reproducible pipeline and validation tests.
- Removed temporary/duplicate analysis artifacts.

## Methodology
`Transactions → Validation → RFM Metrics → RFM Scores → log1p → StandardScaler → K-Means (k=5) → Business Segments → Power BI`

**R:** days since latest purchase  
**F:** distinct invoice count  
**M:** total transaction value

Current K-Means silhouette score: **0.3172**

## Run
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/rfm_pipeline.py --input data/cleaned_transactions.xlsx
streamlit run dashboard/app.py
```

## Deliverables
- `output/customer_rfm_segments.csv` — all customers with RFM scores and segments
- `output/RFM_Analysis_Report.xlsx` — professional Excel analysis
- `output/charts/` — visualizations
- `docs/Business_Recommendation.md`
- `powerbi/` — Power BI-ready tables + DAX/build guide
- `dashboard/app.py` — optional interactive dashboard
- `presentation/RFM_Customer_Segmentation_Presentation.pptx`
- `tests/test_outputs.py`

## Power BI
Use `powerbi/Customer_RFM.csv` as the primary table and follow `powerbi/PowerBI_Build_Guide.md`. The uploaded PBIX is preserved as `Customer_Segmentation_Dashboard_legacy.pbix` for reference only; rebuild/refresh it with the new datasets so it does not retain the old segmentation logic.

## Business highlight
Approximately **26.1% of customers account for 80% of customer revenue**. Champions alone contribute **51.5%** of revenue from **7.2%** of customers, making retention a high-priority action.

## Author
**Naveen Kumar Sharma**


## Professional Dashboard

The final Streamlit dashboard uses an equal-column corporate layout with
RFM KPIs, filters, customer segment analysis, interactive 3D RFM clustering,
marketing recommendations and customer-level RFM preview.

Run:

```powershell
streamlit run dashboard/app.py
```

The project uses the current Streamlit `width="stretch"` API and does not
use the deprecated `use_container_width` parameter.
