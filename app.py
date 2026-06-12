import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Medicare Advantage Plan Advisor",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Medicare Advantage Plan Advisor")
st.write("Compare Medicare Advantage plan types based on income, eligibility, premiums, benefits, and needs.")

st.warning(
    "This app is educational only. Always verify real plans, premiums, doctors, drugs, and rules on Medicare.gov or with a licensed Medicare advisor."
)

plans = [
    {
        "Plan Type": "HMO",
        "Premium": "$0–$50/month + Part B premium",
        "Best For": "Low or moderate income users who can stay in-network",
        "Advantages": "Low premium, simple network, may include dental, vision, hearing, and drug coverage",
        "Disadvantages": "Less flexibility, usually must use in-network doctors",
        "Income Fit": "Low / Moderate"
    },
    {
        "Plan Type": "PPO",
        "Premium": "$0–$100+/month + Part B premium",
        "Best For": "People who want more doctor and hospital flexibility",
        "Advantages": "Can use out-of-network providers at higher cost, fewer referral rules",
        "Disadvantages": "Can cost more than HMO, network still matters",
        "Income Fit": "Moderate / Higher"
    },
    {
        "Plan Type": "SNP",
        "Premium": "Often $0 if qualified, varies by state and plan",
        "Best For": "People with Medicaid, chronic illness, or institutional care needs",
        "Advantages": "Care coordination, tailored benefits, strong for dual-eligible members",
        "Disadvantages": "Strict eligibility rules",
        "Income Fit": "Low / Special Eligibility"
    },
    {
        "Plan Type": "PFFS",
        "Premium": "Varies widely",
        "Best For": "People who want provider choice where doctors accept plan terms",
        "Advantages": "Potential provider flexibility",
        "Disadvantages": "Doctors may refuse plan terms",
        "Income Fit": "Moderate / Higher"
    },
    {
        "Plan Type": "MSA",
        "Premium": "Usually $0 plan premium, high deductible",
        "Best For": "Higher-income users comfortable with high deductibles",
        "Advantages": "Medical savings account deposit, useful for low healthcare use",
        "Disadvantages": "High deductible, no built-in drug coverage",
        "Income Fit": "Higher"
    }
]

enrollment_periods = pd.DataFrame([
    ["Initial Enrollment Period", "Around first Medicare eligibility", "Join when first eligible"],
    ["Annual Open Enrollment", "Oct 15 – Dec 7", "Join, switch, or drop MA/Part D"],
    ["Medicare Advantage Open Enrollment", "Jan 1 – Mar 31", "Switch MA plans or return to Original Medicare"],
    ["Special Enrollment Period", "Depends on event", "Move, lose coverage, gain Medicaid/Extra Help, etc."]
], columns=["Period", "Timing", "Purpose"])

checklist = [
    "Medicare card",
    "Medicare Number",
    "Part A effective date",
    "Part B effective date",
    "Permanent address and ZIP code",
    "Doctor and hospital list",
    "Pharmacy list",
    "Prescription drug list",
    "Medicaid card or Extra Help proof, if applicable",
    "Current insurance card",
    "Payment method if the plan has a premium"
]

st.sidebar.header("Applicant Information")

age = st.sidebar.number_input("Age", min_value=18, max_value=120, value=65)
has_part_a = st.sidebar.checkbox("Has Medicare Part A", value=True)
has_part_b = st.sidebar.checkbox("Has Medicare Part B", value=True)
zip_code = st.sidebar.text_input("ZIP Code")
income = st.sidebar.selectbox("Income Level", ["Low", "Moderate", "Higher"])
has_medicaid = st.sidebar.checkbox("Has Medicaid / Dual Eligible")
has_chronic = st.sidebar.checkbox("Has chronic condition")
needs_drugs = st.sidebar.checkbox("Needs prescription drug coverage", value=True)

st.sidebar.header("Preferences")
low_premium = st.sidebar.slider("Need low premium", 1, 5, 4)
doctor_flexibility = st.sidebar.slider("Need doctor flexibility", 1, 5, 3)
travel_need = st.sidebar.slider("Travel often", 1, 5, 2)
deductible_comfort = st.sidebar.slider("Comfort with high deductible", 1, 5, 2)

def score_plan(plan_type):
    score = 0

    if plan_type == "HMO":
        score += low_premium * 3
        score += max(0, 6 - doctor_flexibility)
        if income in ["Low", "Moderate"]:
            score += 4

    elif plan_type == "PPO":
        score += doctor_flexibility * 3
        score += travel_need * 2
        if income in ["Moderate", "Higher"]:
            score += 3

    elif plan_type == "SNP":
        if has_medicaid:
            score += 15
        if has_chronic:
            score += 10
        if income == "Low":
            score += 5

    elif plan_type == "PFFS":
        score += doctor_flexibility * 2
        score += travel_need

    elif plan_type == "MSA":
        score += deductible_comfort * 3
        if income == "Higher":
            score += 5
        if needs_drugs:
            score -= 3

    return max(score, 0)

df = pd.DataFrame(plans)
df["Fit Score"] = df["Plan Type"].apply(score_plan)
df = df.sort_values("Fit Score", ascending=False)

st.subheader("Eligibility Check")

if has_part_a and has_part_b:
    st.success("Basic Medicare Advantage eligibility appears possible.")
else:
    st.error("Medicare Advantage usually requires both Medicare Part A and Part B.")

if age < 65:
    st.info("People under 65 may still qualify through disability or other Medicare eligibility rules.")

if not zip_code:
    st.warning("Enter ZIP code before applying because plans are based on service area.")

st.subheader("Recommended Plan Types")
st.dataframe(df, use_container_width=True, hide_index=True)

top_plan = df.iloc[0]

st.success(f"Best match based on your answers: {top_plan['Plan Type']}")

tab1, tab2, tab3, tab4 = st.tabs([
    "Plan Details",
    "Enrollment Periods",
    "Application Checklist",
    "Final Advice"
])

with tab1:
    for _, row in df.iterrows():
        with st.expander(f"{row['Plan Type']} — Fit Score: {row['Fit Score']}"):
            st.write(f"**Premium:** {row['Premium']}")
            st.write(f"**Best For:** {row['Best For']}")
            st.write(f"**Advantages:** {row['Advantages']}")
            st.write(f"**Disadvantages:** {row['Disadvantages']}")
            st.write(f"**Income Fit:** {row['Income Fit']}")

with tab2:
    st.table(enrollment_periods)

with tab3:
    st.write("Before applying, collect these materials:")
    for item in checklist:
        st.checkbox(item)

with tab4:
    st.markdown("""
### What to compare before choosing a plan

- Monthly premium
- Medicare Part B premium
- Maximum out-of-pocket limit
- Doctor network
- Hospital network
- Prescription drug coverage
- Dental, vision, and hearing benefits
- Prior authorization rules
- Specialist copays
- Pharmacy network
- Star rating

### Important

A $0 premium plan does not mean all care is free. You may still pay copays, coinsurance, deductibles, and the Medicare Part B premium.
""")
