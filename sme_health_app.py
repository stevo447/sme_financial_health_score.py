import streamlit as st
import os

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="Quant Vision Labs",
    page_icon="📊",
    layout="wide"
)

# -------------------------
# Hide Streamlit Default Menu
# -------------------------
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# -------------------------
# Control App Width
# -------------------------
st.markdown("""
    <style>
    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        margin: auto;
    }
    </style>
""", unsafe_allow_html=True)

from PIL import Image

# -------------------------
# Load Logo Safely
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(BASE_DIR, "logo.png")

try:
    logo = Image.open(logo_path)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(logo, width=300)

except Exception as e:
    st.error("Logo not found. Please check file location.")
    st.write("Debug:", os.listdir(BASE_DIR))

# -------------------------
# Main Page Header
# -------------------------
st.title("📊 SME Financial Health Score")

st.write(
    "Evaluate your business financial strength using "
    "profitability, liquidity, and debt pressure indicators."
)

# -------------------------
# Financial Health Function
# -------------------------
def calculate_sme_financial_health(
    industry,
    years_in_operation,
    monthly_revenue,
    monthly_operating_expenses,
    cash_balance,
    accounts_receivable,
    accounts_payable,
    total_debt,
    monthly_debt_repayment
):
    profit = monthly_revenue - monthly_operating_expenses
    profit_margin = profit / monthly_revenue if monthly_revenue > 0 else 0

    if profit_margin >= 0.25:
        profitability_score = 40
        profitability_label = "Strong"
    elif profit_margin >= 0.10:
        profitability_score = 28
        profitability_label = "Moderate"
    elif profit_margin >= 0:
        profitability_score = 18
        profitability_label = "Weak"
    else:
        profitability_score = 5
        profitability_label = "Poor"

    denominator = accounts_payable + monthly_debt_repayment
    liquidity_ratio = (
        (cash_balance + accounts_receivable) / denominator
        if denominator > 0 else cash_balance + accounts_receivable
    )

    if liquidity_ratio >= 2:
        liquidity_score = 35
        liquidity_label = "Strong"
    elif liquidity_ratio >= 1.2:
        liquidity_score = 24
        liquidity_label = "Moderate"
    elif liquidity_ratio >= 0.8:
        liquidity_score = 14
        liquidity_label = "Weak"
    else:
        liquidity_score = 5
        liquidity_label = "Poor"

    debt_pressure_ratio = (
        monthly_debt_repayment / monthly_revenue
        if monthly_revenue > 0 else 1
    )

    if debt_pressure_ratio <= 0.10:
        debt_score = 25
        debt_label = "Low"
    elif debt_pressure_ratio <= 0.20:
        debt_score = 18
        debt_label = "Moderate"
    elif debt_pressure_ratio <= 0.35:
        debt_score = 10
        debt_label = "Elevated"
    else:
        debt_score = 4
        debt_label = "High"

    total_score = profitability_score + liquidity_score + debt_score

    if total_score >= 80:
        overall = "Strong Financial Health"
    elif total_score >= 60:
        overall = "Moderate Financial Health"
    elif total_score >= 40:
        overall = "Weak Financial Health"
    else:
        overall = "High Financial Stress"

    return {
        "financial_health_score": total_score,
        "overall_assessment": overall,
        "profitability": profitability_label,
        "liquidity": liquidity_label,
        "debt_risk": debt_label,
        "profit_margin": round(profit_margin * 100, 2),
        "liquidity_ratio": round(liquidity_ratio, 2),
        "debt_pressure_ratio": round(debt_pressure_ratio * 100, 2)
    }

# -------------------------
# Input Form
# -------------------------
with st.form("sme_health_form"):
    industry = st.selectbox(
        "Industry",
        ["Retail", "Services", "Manufacturing", "Agriculture", "Technology", "Other"]
    )

    years_in_operation = st.number_input("Years in Operation", min_value=0, step=1)

    monthly_revenue = st.number_input("Monthly Revenue (₦)", min_value=0.0, step=1000.0)
    monthly_operating_expenses = st.number_input("Monthly Operating Expenses (₦)", min_value=0.0, step=1000.0)

    cash_balance = st.number_input("Cash Balance (₦)", min_value=0.0, step=1000.0)
    accounts_receivable = st.number_input("Accounts Receivable (₦)", min_value=0.0, step=1000.0)
    accounts_payable = st.number_input("Accounts Payable (₦)", min_value=0.0, step=1000.0)

    total_debt = st.number_input("Total Debt (₦)", min_value=0.0, step=1000.0)
    monthly_debt_repayment = st.number_input("Monthly Debt Repayment (₦)", min_value=0.0, step=1000.0)

    submitted = st.form_submit_button("Calculate Score")

# -------------------------
# Results
# -------------------------
if submitted:

    if monthly_revenue <= 0:
        st.error("Monthly revenue must be greater than zero.")
    else:
        result = calculate_sme_financial_health(
            industry,
            years_in_operation,
            monthly_revenue,
            monthly_operating_expenses,
            cash_balance,
            accounts_receivable,
            accounts_payable,
            total_debt,
            monthly_debt_repayment
        )

        st.success("Assessment Complete")

        st.metric("Financial Health Score", f"{result['financial_health_score']}/100")

        st.subheader("Overall Assessment")
        st.write(f"**{result['overall_assessment']}**")

        st.subheader("Risk Dimensions")
        st.write(f"**Profitability:** {result['profitability']}")
        st.write(f"**Liquidity:** {result['liquidity']}")
        st.write(f"**Debt Risk:** {result['debt_risk']}")

        st.subheader("Key Indicators")
        st.write(f"**Profit Margin:** {result['profit_margin']}%")
        st.write(f"**Liquidity Ratio:** {result['liquidity_ratio']}")
        st.write(f"**Debt Pressure Ratio:** {result['debt_pressure_ratio']}%")

        st.info(
            "Indicative output only. "
            "For deeper financial advisory or dashboard solutions, "
            "contact Quant Vision Labs."
        )

        st.markdown("### Need a More Detailed Review?")
        st.markdown("[Request Consultation](https://quantvisionlabs.com/request-consultation)")