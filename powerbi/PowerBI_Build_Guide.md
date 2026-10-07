# Power BI Build & Refresh Guide

## Primary tables
Load these files from this folder:
- `Customer_RFM.csv` — customer-level RFM model
- `Segment_Summary.csv` — segment KPIs
- `Monthly_Sales.csv` — monthly trend
- `Country_Summary.csv` — geographic summary
- `Top_Products.csv` — product performance

## Recommended pages
1. Executive Overview — KPIs, revenue by segment, customer count by segment, country revenue.
2. RFM Segmentation — R/F scatter, RFM score distribution, segment table.
3. Customer Targeting — Champions, At-Risk, Lost, recommended action and customer drill-through.
4. Sales Trend — monthly revenue, orders, customers, AOV and top products.

## DAX
```DAX
Total Customers = DISTINCTCOUNT(Customer_RFM[CustomerID])
Total Revenue = SUM(Customer_RFM[Monetary])
Average Customer Value = AVERAGE(Customer_RFM[Monetary])
Average Frequency = AVERAGE(Customer_RFM[Frequency])
Average Recency = AVERAGE(Customer_RFM[Recency])
Average RFM Score = AVERAGE(Customer_RFM[RFM_Score])
Champions Revenue = CALCULATE([Total Revenue], Customer_RFM[Segment] = "Champions")
At Risk Customers = CALCULATE([Total Customers], Customer_RFM[Segment] = "At-Risk Customers")
Champions Revenue % = DIVIDE([Champions Revenue], [Total Revenue])
```

## Validation values
- Customers: 4,334
- Transactions: 391,150
- Invoices: 18,402
- Products: 3,659
- Revenue: £8,737,227.64
- K-Means k: 5
- Silhouette score: 0.3172

## Important
The uploaded project's original `raw_data.xlsx` was only 2 bytes and was not a readable workbook. The validated cleaned workbook is therefore the analytical source. The legacy PBIX is preserved for reference; refresh/rebuild it using the new `Customer_RFM.csv` and summary tables rather than submitting the legacy segmentation unchanged.
