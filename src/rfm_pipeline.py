"""End-to-end RFM customer segmentation pipeline.

The pipeline validates transaction data, calculates RFM metrics,
assigns quintile scores, applies K-Means clustering, and exports
business-friendly customer segments.
"""

from pathlib import Path
import argparse

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


SEGMENT_ACTIONS = {
    "Champions": (
        "VIP loyalty, early access, premium bundles, referral rewards"
    ),
    "Loyal Customers": (
        "Cross-sell, upsell and loyalty-point campaigns"
    ),
    "At-Risk Customers": (
        "Win-back offer, reminder sequence and personalized recommendations"
    ),
    "Potential Loyalists": (
        "Second-purchase incentive and product discovery campaign"
    ),
    "Lost Customers": (
        "Low-cost reactivation test; suppress expensive incentives"
    ),
}

SEGMENT_PRIORITY = {
    "Champions": "Protect",
    "Loyal Customers": "Grow",
    "At-Risk Customers": "Win Back",
    "Potential Loyalists": "Convert",
    "Lost Customers": "Reactivate selectively",
}


def load_transactions(input_path: Path) -> pd.DataFrame:
    """Load, validate and clean transaction-level data."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if input_path.suffix.lower() in {".xlsx", ".xls"}:
        data = pd.read_excel(input_path)
    else:
        data = pd.read_csv(input_path)

    required_columns = [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "CustomerID",
        "Country",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    data["InvoiceNo"] = data["InvoiceNo"].astype(str)
    data["InvoiceDate"] = pd.to_datetime(
        data["InvoiceDate"], errors="coerce"
    )
    data["CustomerID"] = pd.to_numeric(
        data["CustomerID"], errors="coerce"
    )
    data["Quantity"] = pd.to_numeric(
        data["Quantity"], errors="coerce"
    )
    data["UnitPrice"] = pd.to_numeric(
        data["UnitPrice"], errors="coerce"
    )

    data = data.dropna(
        subset=[
            "InvoiceDate",
            "CustomerID",
            "Quantity",
            "UnitPrice",
        ]
    ).copy()

    data["TotalSales"] = data["Quantity"] * data["UnitPrice"]

    valid_transactions = (
        (data["Quantity"] > 0)
        & (data["UnitPrice"] > 0)
        & ~data["InvoiceNo"].str.upper().str.startswith("C")
    )

    return data.loc[valid_transactions].copy()


def calculate_rfm(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate Recency, Frequency and Monetary metrics."""
    snapshot_date = data["InvoiceDate"].max() + pd.Timedelta(days=1)

    rfm = (
        data.groupby("CustomerID")
        .agg(
            Recency=(
                "InvoiceDate",
                lambda dates: (
                    snapshot_date - dates.max()
                ).days,
            ),
            Frequency=("InvoiceNo", "nunique"),
            Monetary=("TotalSales", "sum"),
            Country=(
                "Country",
                lambda values: (
                    values.mode().iat[0]
                    if not values.mode().empty
                    else values.iloc[0]
                ),
            ),
            LastPurchaseDate=("InvoiceDate", "max"),
            FirstPurchaseDate=("InvoiceDate", "min"),
        )
        .reset_index()
    )

    rfm["AverageOrderValue"] = (
        rfm["Monetary"] / rfm["Frequency"]
    )

    return rfm


def assign_rfm_scores(rfm: pd.DataFrame) -> pd.DataFrame:
    """Assign safe quintile scores from 1 to 5."""
    scored = rfm.copy()

    scored["R_Score"] = pd.qcut(
        scored["Recency"].rank(method="first"),
        5,
        labels=[5, 4, 3, 2, 1],
    ).astype(int)

    scored["F_Score"] = pd.qcut(
        scored["Frequency"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5],
    ).astype(int)

    scored["M_Score"] = pd.qcut(
        scored["Monetary"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5],
    ).astype(int)

    scored["RFM_Score"] = scored[
        ["R_Score", "F_Score", "M_Score"]
    ].sum(axis=1)

    scored["RFM_Code"] = (
        scored["R_Score"].astype(str)
        + scored["F_Score"].astype(str)
        + scored["M_Score"].astype(str)
    )

    return scored


def apply_kmeans(
    rfm: pd.DataFrame,
    cluster_count: int = 5,
    random_state: int = 42,
) -> tuple[pd.DataFrame, KMeans, float]:
    """Cluster customers using transformed and standardized RFM features."""
    features = rfm[
        ["Recency", "Frequency", "Monetary"]
    ].astype(float)

    transformed = np.log1p(features)
    scaled = StandardScaler().fit_transform(transformed)

    model = KMeans(
        n_clusters=cluster_count,
        random_state=random_state,
        n_init=20,
    )

    result = rfm.copy()
    result["Cluster"] = model.fit_predict(scaled)

    quality_score = silhouette_score(
        scaled,
        result["Cluster"],
    )

    return result, model, quality_score


def name_segments(rfm: pd.DataFrame) -> pd.DataFrame:
    """Convert numeric clusters into business-friendly segment names."""
    result = rfm.copy()

    cluster_means = (
        result.groupby("Cluster")[
            ["Recency", "Frequency", "Monetary", "RFM_Score"]
        ]
        .mean()
        .sort_values("RFM_Score")
    )

    segment_names = [
        "Lost Customers",
        "Potential Loyalists",
        "At-Risk Customers",
        "Loyal Customers",
        "Champions",
    ]

    cluster_to_segment = dict(
        zip(cluster_means.index, segment_names)
    )

    result["Segment"] = result["Cluster"].map(
        cluster_to_segment
    )
    result["Priority"] = result["Segment"].map(
        SEGMENT_PRIORITY
    )
    result["RecommendedAction"] = result["Segment"].map(
        SEGMENT_ACTIONS
    )

    return result


def run_pipeline(
    input_path: Path,
    output_path: Path,
) -> tuple[pd.DataFrame, float]:
    """Run the complete segmentation pipeline and save customer output."""
    transactions = load_transactions(input_path)
    rfm = calculate_rfm(transactions)
    rfm = assign_rfm_scores(rfm)
    rfm, _, silhouette = apply_kmeans(rfm)
    rfm = name_segments(rfm)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    rfm.to_csv(output_path, index=False)

    print(f"Customers: {len(rfm):,}")
    print(
        f"Revenue: "
        f"{rfm['Monetary'].sum():,.2f}"
    )
    print(
        f"Silhouette score: "
        f"{silhouette:.4f}"
    )
    print(f"Saved: {output_path}")

    return rfm, silhouette


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Run the RFM customer segmentation pipeline."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/cleaned_transactions.xlsx"),
        help="Input transaction workbook or CSV.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/customer_rfm_segments.csv"),
        help="Customer-level RFM output CSV.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the command-line pipeline."""
    arguments = parse_arguments()
    run_pipeline(
        input_path=arguments.input,
        output_path=arguments.output,
    )


if __name__ == "__main__":
    main()
