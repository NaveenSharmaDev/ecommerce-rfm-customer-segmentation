"""Professional Streamlit dashboard for E-Commerce RFM customer segmentation."""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "output" / "customer_rfm_segments.csv"

PAGE_TITLE = "Customer Segmentation & RFM Analytics"

SEGMENT_ORDER = [
    "Champions",
    "Loyal Customers",
    "At-Risk Customers",
    "Potential Loyalists",
    "Lost Customers",
]

SEGMENT_COLORS = {
    "Champions": "#18C7A6",
    "Loyal Customers": "#2388F5",
    "At-Risk Customers": "#FF8A32",
    "Potential Loyalists": "#9B63DC",
    "Lost Customers": "#EF4B58",
}

MARKETING_ACTIONS = {
    "Champions": "Exclusive loyalty programs and early access to new launches.",
    "Loyal Customers": "Upsell and cross-sell with personalized bundle offers.",
    "At-Risk Customers": "Targeted win-back offers and email re-engagement.",
    "Potential Loyalists": "Second-purchase incentives and personalized recommendations.",
    "Lost Customers": "Low-cost reactivation tests; control incentive spend.",
}


def configure_page() -> None:
    """Configure Streamlit page and inject the corporate dashboard theme."""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        :root {
            --background: #080F1D;
            --panel: #121D2E;
            --panel-alt: #101929;
            --border: #2B3950;
            --text: #F7F9FC;
            --muted: #AEBBD0;
            --accent: #18C7A6;
        }

        .stApp {
            background:
                radial-gradient(
                    circle at 10% 0%,
                    rgba(36, 116, 220, 0.14),
                    transparent 30%
                ),
                linear-gradient(
                    180deg,
                    #080F1D 0%,
                    #0A1220 100%
                );
            color: var(--text);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stSidebar"] {
            background: #0A1323;
            border-right: 1px solid #27364E;
        }

        [data-testid="stSidebar"] * {
            color: #EDF3FB !important;
        }

        .block-container {
            width: 100%;
            max-width: 100%;
            padding: 1.15rem 1rem 1rem;
        }

        .topbar {
            background: linear-gradient(90deg, #111C2E, #0D1626);
            border: 1px solid #2A3850;
            border-radius: 10px;
            padding: 17px 22px;
            margin-bottom: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.22);
        }

        .dashboard-title {
            color: #FFFFFF;
            font-size: 29px;
            font-weight: 800;
            line-height: 1.15;
            letter-spacing: 0.2px;
        }

        .dashboard-subtitle {
            color: #B5C1D3;
            font-size: 14px;
            margin-top: 5px;
        }

        .refresh-text {
            color: #71829A;
            font-size: 11px;
            margin-top: 4px;
        }

        .kpi {
            background: linear-gradient(145deg, #141F31, #101929);
            border: 1px solid #2B3950;
            border-radius: 9px;
            min-height: 122px;
            padding: 14px 17px;
            box-shadow: 0 7px 22px rgba(0, 0, 0, 0.20);
        }

        .kpi-title {
            color: #EAF0F8;
            font-size: 15px;
            font-weight: 650;
            border-bottom: 1px solid #35435A;
            padding-bottom: 8px;
            white-space: nowrap;
        }

        .kpi-value {
            color: #FFFFFF;
            font-size: 35px;
            font-weight: 800;
            line-height: 1.1;
            margin-top: 11px;
        }

        .kpi-note {
            color: #30CAA4;
            font-size: 12px;
            margin-top: 4px;
        }

        .section-panel {
            background: linear-gradient(145deg, var(--panel), var(--panel-alt));
            border: 1px solid var(--border);
            border-radius: 9px;
            padding: 10px 12px 5px;
            box-shadow: 0 7px 22px rgba(0, 0, 0, 0.18);
            height: 100%;
        }

        .panel-title {
            color: #F7F9FC;
            font-size: 16px;
            font-weight: 800;
            padding: 3px 0 7px;
            letter-spacing: 0.1px;
        }

        .insight-table {
            width: 100%;
            border-collapse: collapse;
            color: #E9EEF7;
            font-size: 12px;
        }

        .insight-table th {
            background: #172235;
            border: 1px solid #35445D;
            padding: 8px;
            text-align: left;
        }

        .insight-table td {
            border: 1px solid #35445D;
            padding: 8px;
            vertical-align: top;
        }

        .footer {
            color: #6F7E95;
            text-align: center;
            font-size: 11px;
            padding: 18px 0 8px;
        }

        div[data-baseweb="select"] > div {
            background: #111C2D !important;
            border-color: #3B4A63 !important;
        }

        [data-testid="stDataFrame"] {
            border: 1px solid #29364D;
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def load_customer_data() -> pd.DataFrame:
    """Load and prepare the customer-level RFM dataset."""
    if not DATA_FILE.exists():
        st.error(f"Required data file was not found: {DATA_FILE}")
        st.stop()

    data = pd.read_csv(DATA_FILE)
    data["FirstPurchaseDate"] = pd.to_datetime(
        data["FirstPurchaseDate"], errors="coerce"
    )
    data["LastPurchaseDate"] = pd.to_datetime(
        data["LastPurchaseDate"], errors="coerce"
    )
    data["Cohort"] = data["FirstPurchaseDate"].dt.to_period("M").astype(str)
    return data


def apply_filters(data: pd.DataFrame) -> pd.DataFrame:
    """Render dashboard filters and return the filtered customer data."""
    filter_columns = st.columns(4)

    with filter_columns[0]:
        date_filter = st.selectbox(
            "Date Range",
            ["All Dates", "Last 12 Months", "Last 6 Months", "Last 3 Months"],
        )

    with filter_columns[1]:
        country_filter = st.selectbox(
            "Country",
            ["All Countries"] + sorted(data["Country"].dropna().unique()),
        )

    with filter_columns[2]:
        cohort_filter = st.selectbox(
            "Cohort",
            ["All Cohorts"]
            + sorted(data["Cohort"].dropna().unique(), reverse=True),
        )

    with filter_columns[3]:
        segment_filter = st.selectbox(
            "Segment",
            ["All Segments"] + SEGMENT_ORDER,
        )

    filtered = data.copy()

    if date_filter != "All Dates":
        month_map = {
            "Last 12 Months": 12,
            "Last 6 Months": 6,
            "Last 3 Months": 3,
        }
        cutoff = (
            filtered["LastPurchaseDate"].max()
            - pd.DateOffset(months=month_map[date_filter])
        )
        filtered = filtered[filtered["LastPurchaseDate"] >= cutoff]

    if country_filter != "All Countries":
        filtered = filtered[filtered["Country"] == country_filter]

    if cohort_filter != "All Cohorts":
        filtered = filtered[filtered["Cohort"] == cohort_filter]

    if segment_filter != "All Segments":
        filtered = filtered[filtered["Segment"] == segment_filter]

    return filtered


def render_header() -> None:
    """Render the dashboard header."""
    st.markdown(
        """
        <div class="topbar">
            <div class="dashboard-title">
                📊 CUSTOMER SEGMENTATION &amp; RFM ANALYTICS
            </div>
            <div class="dashboard-subtitle">
                Corporate Marketing Intelligence |
                E-Commerce Customer Analytics
            </div>
            <div class="refresh-text">
                Refresh: October 2026 |
                RFM Quintile Scoring + K-Means
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpis(data: pd.DataFrame) -> None:
    """Render four equally sized KPI cards."""
    customer_count = len(data)
    average_recency = data["Recency"].mean()
    average_frequency = data["Frequency"].mean()
    total_value = data["Monetary"].sum()

    metrics = [
        (
            "Total Segmented Customers",
            f"{customer_count:,}",
            "RFM customer base",
        ),
        (
            "Average Recency",
            f"{average_recency:.0f} Days",
            "Lower is better",
        ),
        (
            "Avg. Purchase Frequency",
            f"{average_frequency:.2f}",
            "Distinct orders / customer",
        ),
        (
            "Total Customer Value",
            f"£{total_value / 1_000_000:.2f}M",
            "Monetary value",
        ),
    ]

    columns = st.columns(4)

    for column, (title, value, note) in zip(columns, metrics):
        with column:
            st.markdown(
                f"""
                <div class="kpi">
                    <div class="kpi-title">{title}</div>
                    <div class="kpi-value">{value}</div>
                    <div class="kpi-note">{note}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def build_segment_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Create the segment-level summary used by dashboard visuals."""
    summary = (
        data.groupby("Segment", as_index=False)
        .agg(
            Customers=("CustomerID", "count"),
            Revenue=("Monetary", "sum"),
        )
    )

    summary["Segment"] = pd.Categorical(
        summary["Segment"],
        categories=SEGMENT_ORDER,
        ordered=True,
    )

    return summary.sort_values("Segment")


def render_segment_donut(summary: pd.DataFrame) -> None:
    """Render the customer segment share donut chart."""
    st.markdown(
        '<div class="section-panel"><div class="panel-title">'
        "CUSTOMER SEGMENTS %"
        "</div>",
        unsafe_allow_html=True,
    )

    figure = px.pie(
        summary,
        names="Segment",
        values="Customers",
        hole=0.56,
        color="Segment",
        color_discrete_map=SEGMENT_COLORS,
    )
    figure.update_traces(
        textposition="outside",
        textinfo="percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Customers: %{value:,}<br>"
            "Share: %{percent}<extra></extra>"
        ),
    )
    figure.update_layout(
        height=365,
        margin=dict(l=5, r=5, t=5, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E8EEF7"),
        legend=dict(
            orientation="h",
            y=-0.18,
            x=0.5,
            xanchor="center",
            font=dict(size=9),
        ),
    )

    st.plotly_chart(
        figure,
        width="stretch",
        config={"displayModeBar": False},
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_3d_rfm(data: pd.DataFrame) -> None:
    """Render the interactive three-dimensional RFM customer map."""
    st.markdown(
        '<div class="section-panel"><div class="panel-title">'
        "K-MEANS CLUSTER VISUALIZATION (RFM)"
        "</div>",
        unsafe_allow_html=True,
    )

    sample = data.sample(min(1800, len(data)), random_state=42)

    figure = px.scatter_3d(
        sample,
        x="Recency",
        y="Frequency",
        z="Monetary",
        color="Segment",
        color_discrete_map=SEGMENT_COLORS,
        hover_data=[
            "CustomerID",
            "RFM_Code",
            "RFM_Score",
            "Country",
        ],
        opacity=0.78,
    )

    figure.update_traces(marker=dict(size=3.8))
    figure.update_layout(
        height=365,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        scene=dict(
            bgcolor="#121D2E",
            xaxis=dict(
                title="Recency (Days)",
                gridcolor="#34435C",
            ),
            yaxis=dict(
                title="Frequency (Orders)",
                gridcolor="#34435C",
            ),
            zaxis=dict(
                title="Monetary (£)",
                gridcolor="#34435C",
            ),
        ),
        font=dict(color="#DCE5F2"),
        legend=dict(font=dict(size=9)),
    )

    st.plotly_chart(
        figure,
        width="stretch",
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_marketing_actions(summary: pd.DataFrame) -> None:
    """Render business-friendly segment recommendations."""
    st.markdown(
        '<div class="section-panel"><div class="panel-title">'
        "SEGMENT INSIGHTS &amp; MARKETING RECOMMENDATIONS"
        "</div>",
        unsafe_allow_html=True,
    )

    available_segments = set(summary["Segment"].astype(str))
    rows = []

    for segment in SEGMENT_ORDER:
        if segment in available_segments:
            rows.append(
                "<tr>"
                f'<td><b style="color:{SEGMENT_COLORS[segment]}">'
                f"{segment}</b></td>"
                f"<td>{MARKETING_ACTIONS[segment]}</td>"
                "</tr>"
            )

    table_html = (
        '<table class="insight-table">'
        "<tr><th>Segment</th><th>Action plan</th></tr>"
        + "".join(rows)
        + "</table>"
    )

    st.markdown(table_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_distribution(summary: pd.DataFrame) -> None:
    """Render the horizontal segment distribution chart."""
    st.markdown(
        '<div class="section-panel"><div class="panel-title">'
        "SEGMENT DISTRIBUTION"
        "</div>",
        unsafe_allow_html=True,
    )

    chart_data = summary.sort_values("Customers", ascending=True)

    figure = px.bar(
        chart_data,
        x="Customers",
        y="Segment",
        orientation="h",
        text="Customers",
        color="Segment",
        color_discrete_map=SEGMENT_COLORS,
    )
    figure.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        cliponaxis=False,
    )
    figure.update_layout(
        height=365,
        margin=dict(l=5, r=45, t=5, b=5),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E8EEF7"),
        xaxis=dict(
            title=None,
            gridcolor="#2F3D55",
        ),
        yaxis=dict(title=None),
        showlegend=False,
    )

    st.plotly_chart(
        figure,
        width="stretch",
        config={"displayModeBar": False},
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_customer_preview(data: pd.DataFrame) -> None:
    """Render the top-customer RFM preview table."""
    st.markdown(
        '<div class="section-panel"><div class="panel-title">'
        "RFM DATA PREVIEW (TOP CUSTOMERS)"
        "</div>",
        unsafe_allow_html=True,
    )

    preview = (
        data[
            [
                "CustomerID",
                "Recency",
                "Frequency",
                "Monetary",
                "R_Score",
                "F_Score",
                "M_Score",
                "RFM_Score",
                "Segment",
            ]
        ]
        .sort_values(
            ["Monetary", "RFM_Score"],
            ascending=[False, False],
        )
        .head(15)
        .copy()
    )

    preview["CustomerID"] = preview["CustomerID"].astype(int)
    preview["Monetary"] = preview["Monetary"].map(
        lambda value: f"£{value:,.2f}"
    )

    st.dataframe(
        preview,
        width="stretch",
        hide_index=True,
        height=365,
        column_config={
            "CustomerID": "Customer ID",
            "Recency": "Recency (R)",
            "Frequency": "Frequency (F)",
            "Monetary": "Monetary (M)",
            "R_Score": "R-Score",
            "F_Score": "F-Score",
            "M_Score": "M-Score",
            "RFM_Score": "RFM Score",
            "Segment": "Segment",
        },
    )

    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    """Run the complete dashboard application."""
    configure_page()

    data = load_customer_data()

    render_header()
    filtered_data = apply_filters(data)

    if filtered_data.empty:
        st.warning(
            "No customers match the selected filters. "
            "Please broaden the filters."
        )
        return

    render_kpis(filtered_data)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    summary = build_segment_summary(filtered_data)

    # Equal three-column analytics section.
    analytics_columns = st.columns(3)

    with analytics_columns[0]:
        render_segment_donut(summary)

    with analytics_columns[1]:
        render_3d_rfm(filtered_data)

    with analytics_columns[2]:
        render_marketing_actions(summary)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # Equal two-column detail section.
    detail_columns = st.columns(2)

    with detail_columns[0]:
        render_distribution(summary)

    with detail_columns[1]:
        render_customer_preview(filtered_data)

    st.markdown(
        '<div class="footer">'
        "E-Commerce Customer Segmentation & RFM Analytics | "
        "VEDA Technology Project | Power BI Ready"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
