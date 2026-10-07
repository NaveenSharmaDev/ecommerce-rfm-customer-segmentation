"""Validation tests for the RFM customer segmentation project."""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RFM_OUTPUT = PROJECT_ROOT / "output" / "customer_rfm_segments.csv"


def load_rfm_output() -> pd.DataFrame:
    """Load the generated customer-level RFM output."""
    assert RFM_OUTPUT.exists(), (
        f"Missing RFM output: {RFM_OUTPUT}"
    )
    return pd.read_csv(RFM_OUTPUT)


def test_required_outputs_exist() -> None:
    """Verify the main analytical deliverables exist."""
    required_files = [
        RFM_OUTPUT,
        PROJECT_ROOT / "output/segment_summary.csv",
        PROJECT_ROOT / "output/RFM_Analysis_Report.xlsx",
        PROJECT_ROOT / "powerbi/Customer_RFM.csv",
    ]

    for file_path in required_files:
        assert file_path.exists(), (
            f"Missing required output: {file_path}"
        )


def test_rfm_scores_are_valid() -> None:
    """Verify RFM scores and customer-level uniqueness."""
    data = load_rfm_output()

    for score_column in ["R_Score", "F_Score", "M_Score"]:
        assert data[score_column].between(1, 5).all()

    assert data["RFM_Score"].between(3, 15).all()
    assert data["CustomerID"].is_unique
    assert (data["Monetary"] > 0).all()


def test_required_business_segments_exist() -> None:
    """Verify all five business segments are present."""
    data = load_rfm_output()

    expected_segments = {
        "Champions",
        "Loyal Customers",
        "At-Risk Customers",
        "Potential Loyalists",
        "Lost Customers",
    }

    assert expected_segments.issubset(
        set(data["Segment"].dropna())
    )
