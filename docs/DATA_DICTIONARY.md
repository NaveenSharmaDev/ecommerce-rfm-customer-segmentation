# Data Dictionary

| Field | Meaning |
|---|---|
| CustomerID | Unique customer identifier |
| Country | Customer's most frequent country |
| FirstPurchaseDate | First purchase date |
| LastPurchaseDate | Most recent purchase date |
| Recency | Days since most recent purchase |
| Frequency | Number of distinct invoices |
| Monetary | Total revenue = Quantity × UnitPrice |
| AverageOrderValue | Monetary / Frequency |
| R_Score | Recency quintile; 5 is best |
| F_Score | Frequency quintile; 5 is best |
| M_Score | Monetary quintile; 5 is best |
| RFM_Score | R + F + M |
| RFM_Code | Concatenated R/F/M score |
| Cluster | K-Means cluster ID |
| Segment | Business-friendly segment |
| Priority | Marketing priority |
| RecommendedAction | Suggested campaign |
