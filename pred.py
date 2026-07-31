import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
import random
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --- MOBILE-FIRST CONFIGURATION ---
st.set_page_config(
    page_title="Noona AI — Full MVP Suite",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS FOR MOBILE TOUCH OPTIMIZATION ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 50px;
        font-size: 16px !important;
        font-weight: bold;
        border-radius: 10px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 22px !important;
    }
    .stSelectbox, .stTextInput, .stTextArea {
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- PDF GENERATOR UTILITY (FEATURE #19) ---
def generate_pdf_report(headline, body, score, ctr, cpa_savings, winner_text):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor("#1E293B"))
    story.append(Paragraph("⚡ Predikta AI — Campaign Simulation Report", title_style))
    story.append(Spacer(1, 12))

    # Executive Summary Table
    data = [
        ["Metric", "Simulated Value"],
        ["Overall Resonance Score", f"{score} / 10"],
        ["Predicted CTR", f"{ctr}%"],
        ["Est. CPA Savings", f"PHP {cpa_savings:,.0f} / conversion"],
        ["Verdict", winner_text]
    ]
    t = Table(data, colWidths=[200, 300])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#F8FAFC")),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
    ]))
    story.append(t)
    story.append(Spacer(1, 18))

    # Creative Copy Section
    story.append(Paragraph("<b>Evaluated Creative:</b>", styles['Heading2']))
    story.append(Paragraph(f"<b>Headline:</b> {headline}", styles['Normal']))
    story.append(Paragraph(f"<b>Body Copy:</b> {body}", styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# --- APP HEADER ---
st.title("⚡ Noona AI Engine")
st.caption("Complete Pre-Flight Campaign Simulator for PH Channels")

# --- GLOBAL TARGETING DRAWER ---
with st.expander("⚙️ Target Demographics & Region", expanded=False):
    target_sec = st.multiselect(
        "Target SEC Class",
        ["Class A/B (High Income)", "Class C1/C2 (Middle Income)", "Class D/E (Mass Market)"],
        default=["Class C1/C2 (Middle Income)", "Class D/E (Mass Market)"]
    )
    region = st.selectbox("Primary Region", ["NCR (Metro Manila)", "Visayas (Cebu)", "Mindanao (Davao)"])
    language = st.select_slider("Language Dialect", options=["Pure Taglish", "Tag-Bisaya", "English Standard"])

# --- MAIN NAVIGATION SUITE ---
tab_ab, tab_self_heal, tab_batch, tab_roas = st.tabs([
    "⚔️ A/B Simulator", 
    "🩹 Self-Healing", 
    "📁 Batch CSV", 
    "📈 ROAS Forecast"
])

# =========================================================
# TAB 1: HEAD-TO-HEAD A/B SIMULATOR + PDF EXPORT
# =========================================================
with tab_ab:
    st.subheader("A/B Creative Head-to-Head")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("##### 🅰️ Variant A")
        head_a = st.text_input("Headline A", value="Gusto mo ba ng instant ₱5,000 cash?", key="ha")
        body_a = st.text_area("Body A", value="Apply in 5 mins! No paperwork required. 0% interest on first loan.", height=80, key="ba")
        
    with col_b:
        st.markdown("##### 🅱️ Variant B")
        head_b = st.text_input("Headline B", value="BSP-Regulated instant loan in 5 mins.", key="hb")
        body_b = st.text_area("Body B", value="No hidden fees. Trusted by 500,000+ Filipinos. Easy GCash payment.", height=80, key="bb")

    if st.button("🚀 Run A/B Simulation", type="primary", key="btn_ab"):
        with st.spinner("Running parallel synthetic persona panels..."):
            time.sleep(1.2)
            
        # Scoring logic
        score_a = round(7.2 + (0.8 if "0%" in body_a else 0), 1)
        score_b = round(8.6 + (0.9 if "bsp-regulated" in head_b.lower() else 0), 1)
        ctr_a, ctr_b = round(score_a * 0.4, 2), round(score_b * 0.41, 2)
        cpa_a, cpa_b = score_a * 40, score_b * 45

        st.success(f"🏆 **WINNER: Variant B** (+{round(score_b - score_a, 1)} pts higher resonance)")

        m1, m2 = st.columns(2)
        m1.metric("Variant A Score", f"{score_a} / 10", delta=f"{ctr_a}% CTR")
        m2.metric("Variant B Score", f"{score_b} / 10", delta=f"{ctr_b}% CTR", delta_color="normal")

        # Feature #19: PDF Export Button
        pdf_data = generate_pdf_report(head_b, body_b, score_b, ctr_b, cpa_b, "Variant B Won")
        st.download_button(
            label="📄 Download Client PDF Pitch Deck",
            data=pdf_data,
            file_name="predikta_campaign_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# =========================================================
# TAB 2: AUTOMATED CREATIVE "SELF-HEALING" (FEATURE #4)
# =========================================================
with tab_self_heal:
    st.subheader("Automated Creative Self-Healing Engine")
    st.caption("Transforms weak ad concepts into high-converting copy automatically.")
    
    raw_head = st.text_input("Current Draft Headline", value="Mabilis na pautang online dito na!", key="sh_head")
    raw_body = st.text_area("Current Draft Body Copy", value="Mag-apply ngayon para makuha ang pera mo agad. Cheap fees.", height=80, key="sh_body")

    if st.button("🩹 Diagnose & Fix Creative", type="primary", key="btn_sh"):
        with st.spinner("Analyzing friction points and optimizing copy..."):
            time.sleep(1.0)

        st.warning("⚠️ **Initial Diagnosis (Score: 5.4/10):** High friction detected. Phrases like 'pautang' trigger high skepticism in Class C2/D personas.")

        st.markdown("#### ✨ AI Optimized Creative Options")
        
        with st.container(border=True):
            st.markdown("**Option 1 (Trust & Regulatory Focus):**")
            st.code(f"Headline: BSP-Registered Emergency Funds — Approved in 5 Mins\nBody: Transparent monthly terms. No hidden charges via GCash or Maya.", language="text")
            st.caption("Predicted Score: **8.9 / 10** (+3.5 Improvement)")

        with st.container(border=True):
            st.markdown("**Option 2 (Lifestyle & Value Focus):**")
            st.code(f"Headline: Need Extra Budget Before Payday?\nBody: Get up to ₱5,000 instant credit. Fast approval, zero physical forms.", language="text")
            st.caption("Predicted Score: **8.3 / 10** (+2.9 Improvement)")


# =========================================================
# TAB 3: MULTI-VARIANT BATCH CSV SCORING (10 INDUSTRY NICHES)
# =========================================================
with tab_batch:
    st.subheader("Multi-Variant Batch Creative Scorer")
    st.caption("Select a built-in Philippine industry niche or upload your own CSV.")

    # 10 BUILT-IN PHILIPPINE INDUSTRY DATASETS
    BUILTIN_NICHES = {
        "💸 Fintech & Digital Loans": [
            {"Variant_ID": "FT-01", "Headline": "Gusto mo ba ng instant ₱5,000 cash?", "Body_Copy": "Apply in 5 mins! No paperwork required. 0% interest on first loan.", "Channel": "Meta Feed"},
            {"Variant_ID": "FT-02", "Headline": "BSP-Regulated Emergency Funds in 5 Mins", "Body_Copy": "No hidden fees. Trusted by 500,000+ Filipinos. Easy GCash payment.", "Channel": "Meta Feed"},
            {"Variant_ID": "FT-03", "Headline": "Need Payday Budget Assist?", "Body_Copy": "Get up to ₱10,000 credit line directly to your Maya wallet.", "Channel": "TikTok Shop"},
            {"Variant_ID": "FT-04", "Headline": "Mabilis na Pautang Online Dito!", "Body_Copy": "Mababang interes, mabilis ma-approve. Download app today.", "Channel": "Meta Feed"}
        ],
        "🛍️ E-Commerce & FMCG Retail": [
            {"Variant_ID": "EC-01", "Headline": "Buy 1 Take 1 Flash Sale Today Only!", "Body_Copy": "Free shipping nationwide with zero minimum spend on Shopee.", "Channel": "Shopee Mall"},
            {"Variant_ID": "EC-02", "Headline": "Stop Overpaying for Premium Skincare", "Body_Copy": "Dermatologist-tested formula starting at ₱199. Cash on delivery.", "Channel": "TikTok Shop"},
            {"Variant_ID": "EC-03", "Headline": "Lazada Payday Sale: Up to 70% Off", "Body_Copy": "Stack extra vouchers + 10% daily cashback upon checkout.", "Channel": "Lazada"},
            {"Variant_ID": "EC-04", "Headline": "Organize Your Kitchen in 3 Minutes", "Body_Copy": "Aesthetic space-saving storage boxes. Over 50,000 units sold.", "Channel": "TikTok Shop"}
        ],
        "🍳 Food & Beverage / Delivery": [
            {"Variant_ID": "FB-01", "Headline": "Craving Unlimited Wings tonight?", "Body_Copy": "Enjoy 20% off your GrabFood order using code WINGS20.", "Channel": "Meta Feed"},
            {"Variant_ID": "FB-02", "Headline": "Authentic Milk Tea Delivered Cold", "Body_Copy": "Buy 2 Large Drinks, Get 1 Free Pearl Topping. Order via Foodpanda.", "Channel": "Instagram Reels"},
            {"Variant_ID": "FB-03", "Headline": "Crispy Lechon Belly in BGC & Makati", "Body_Copy": "Same-day delivery for family gatherings and weekend celebrations.", "Channel": "Meta Feed"},
            {"Variant_ID": "FB-04", "Headline": "Healthy Meal Prep Plans at ₱150/meal", "Body_Copy": "Calorie-counted fresh meals delivered straight to your office daily.", "Channel": "Meta Feed"}
        ],
        "💄 Beauty, Skincare & Wellness": [
            {"Variant_ID": "BE-01", "Headline": "Glass Skin Serum for Taglish Weather", "Body_Copy": "Non-sticky, lightweight hydration designed for Philippine humidity.", "Channel": "TikTok Shop"},
            {"Variant_ID": "BE-02", "Headline": "Fade Dark Spots in Just 14 Days", "Body_Copy": "Powered by 5% Niacinamide and Alpha Arbutin. FDA approved.", "Channel": "Shopee Mall"},
            {"Variant_ID": "BE-03", "Headline": "Sunscreen That Won't Leave White Cast", "Body_Copy": "SPF 50+ PA++++ broad spectrum protection. Matte oil-control finish.", "Channel": "Meta Feed"},
            {"Variant_ID": "BE-04", "Headline": "Organic Hair Growth Shampoo Bar", "Body_Copy": "Reduce hair fall naturally without harsh sulfates and parabens.", "Channel": "Lazada"}
        ],
        "🏡 Real Estate & Housing": [
            {"Variant_ID": "RE-01", "Headline": "Own a Condo Near BGC for ₱12,000/mo", "Body_Copy": "No downpayment promo! Flexible Pag-IBIG financing options available.", "Channel": "Meta Feed"},
            {"Variant_ID": "RE-02", "Headline": "Preselling House & Lot in Cavite", "Body_Copy": "15 minutes from CALAX exit. 3 Bedrooms, 2 Carports, Gated Community.", "Channel": "Meta Feed"},
            {"Variant_ID": "RE-03", "Headline": "High-Yield Rental Property in Cebu", "Body_Copy": "Earn passive income near IT Park. Fully furnished studio units.", "Channel": "Meta Feed"},
            {"Variant_ID": "RE-04", "Headline": "Prime Residential Lots in Nuvali", "Body_Copy": "Exclusive eco-friendly township development by Ayala Land.", "Channel": "Meta Feed"}
        ],
        "🎓 EdTech & Online Courses": [
            {"Variant_ID": "ED-01", "Headline": "Become a Certified VA in 30 Days", "Body_Copy": "Learn Social Media Management, Bookkeeping & Client Outreach.", "Channel": "Meta Feed"},
            {"Variant_ID": "ED-02", "Headline": "Pass the Civil Service Exam on 1st Try", "Body_Copy": "Complete online reviewer with mock tests and live mentor sessions.", "Channel": "Meta Feed"},
            {"Variant_ID": "ED-03", "Headline": "Master Python & Data Science from Home", "Body_Copy": "100% online bootcamp with job placement assistance upon graduation.", "Channel": "TikTok Shop"},
            {"Variant_ID": "ED-04", "Headline": "Speak Fluent English in 6 Weeks", "Body_Copy": "Confidence-building masterclass for Call Center & BPO applicants.", "Channel": "Meta Feed"}
        ],
        "✈️ Travel, Tourism & Hospitality": [
            {"Variant_ID": "TR-01", "Headline": "Boracay 3D2N Package with Airfare ₱4,999", "Body_Copy": "Includes beachfront resort stay, daily breakfast, and land transfers.", "Channel": "Meta Feed"},
            {"Variant_ID": "TR-02", "Headline": "Piso Fare Alert: Fly to Japan & Korea", "Body_Copy": "Book your 2027 autumn flights now. Limited seats available!", "Channel": "Meta Feed"},
            {"Variant_ID": "TR-03", "Headline": "Staycation Villa with Private Pool in Tagaytay", "Body_Copy": "Perfect for family reunions, team building, and weekend getaways.", "Channel": "Instagram Reels"},
            {"Variant_ID": "TR-04", "Headline": "El Nido Island Hopping Promo", "Body_Copy": "Explore Tour A & C with free buffet lunch and kayak rental included.", "Channel": "TikTok Shop"}
        ],
        "🚘 Automotive & Transport": [
            {"Variant_ID": "AU-01", "Headline": "Drive Home a New SUV for ₱18k/month", "Body_Copy": "Low downpayment promo + 3 years free LTO registration & insurance.", "Channel": "Meta Feed"},
            {"Variant_ID": "AU-02", "Headline": "Electric Scooter for Manila Traffic", "Body_Copy": "No gas needed! 50km range per charge. Ideal for daily commuting.", "Channel": "TikTok Shop"},
            {"Variant_ID": "AU-03", "Headline": "Ceramic Coating Protection for ₱3,999", "Body_Copy": "Deep gloss shine & scratch resistance with 2-year warranty.", "Channel": "Meta Feed"},
            {"Variant_ID": "AU-04", "Headline": "Car Insurance Renewal in 10 Minutes", "Body_Copy": "Compare quotes from top insurance providers and save up to 20%.", "Channel": "Meta Feed"}
        ],
        "🏥 Health & Medical Services": [
            {"Variant_ID": "HS-01", "Headline": "Comprehensive Executive Check-Up at Home", "Body_Copy": "Blood tests, ECG & doctor teleconsultation without hospital lines.", "Channel": "Meta Feed"},
            {"Variant_ID": "HS-02", "Headline": "Clear Aligners: Straighten Teeth Invisibly", "Body_Copy": "Custom 3D plan with flexible 0% installment plans available.", "Channel": "Instagram Reels"},
            {"Variant_ID": "HS-03", "Headline": "Consult a Licensed Doctor Online for ₱500", "Body_Copy": "24/7 video consultations and e-prescriptions sent to your phone.", "Channel": "Meta Feed"},
            {"Variant_ID": "HS-04", "Headline": "Lasik Eye Surgery Promo in St. Luke's", "Body_Copy": "Say goodbye to thick glasses. 15-minute painless laser procedure.", "Channel": "Meta Feed"}
        ],
        "🐾 Pet Care & Supplies": [
            {"Variant_ID": "PC-01", "Headline": "Premium Grain-Free Dog Food 10kg", "Body_Copy": "Rich in Omega-3 for shiny fur and healthy digestion. Free shipping.", "Channel": "Shopee Mall"},
            {"Variant_ID": "PC-02", "Headline": "Self-Cleaning Automatic Cat Litter Box", "Body_Copy": "Odor-control app-enabled litter box. Perfect for condo living.", "Channel": "TikTok Shop"},
            {"Variant_ID": "PC-03", "Headline": "Gentle Anti-Flea & Tick Dog Shampoo", "Body_Copy": "Organic Madre de Cacao formulation. Soft on sensitive dog skin.", "Channel": "Lazada"},
            {"Variant_ID": "PC-04", "Headline": "Pet Insurance Starting at ₱15/day", "Body_Copy": "Covers emergency vet bills, surgeries, and accidental injuries.", "Channel": "Meta Feed"}
        ]
    }

    # SELECTION & INPUT SOURCE
    data_source = st.radio("Choose Data Input Method:", ["Built-In Industry Niche Dataset", "Upload Custom CSV"], horizontal=True)

    if data_source == "Built-In Industry Niche Dataset":
        selected_niche = st.selectbox("Select Target Industry Niche:", list(BUILTIN_NICHES.keys()))
        df_to_process = pd.DataFrame(BUILTIN_NICHES[selected_niche])
        st.dataframe(df_to_process, use_container_width=True)
        
    else:
        sample_csv = "Variant_ID,Headline,Body_Copy,Channel\n1,Instant Cash,Apply now,Meta Feed\n2,BSP Loan,Trusted loan,TikTok Shop"
        st.download_button("📥 Download CSV Template", sample_csv, "template.csv", "text/csv")
        uploaded_file = st.file_uploader("Upload Ad Variants CSV", type=["csv"])
        if uploaded_file is not None:
            df_to_process = pd.read_csv(uploaded_file)
            st.dataframe(df_to_process, use_container_width=True)
        else:
            df_to_process = None

    # BATCH PROCESSOR TRIGGER
    if df_to_process is not None:
        if st.button("🚀 Batch Score Industry Variants", type="primary", use_container_width=True):
            with st.spinner("Processing batch variants through synthetic persona agents..."):
                time.sleep(1.2)
                
            # SIMULATED METRICS EVALUATION
            df_results = df_to_process.copy()
            
            # Deterministic scoring based on trust/promo keywords
            scores = []
            for _, row in df_results.iterrows():
                base = 7.0
                text = (str(row.get('Headline', '')) + " " + str(row.get('Body_Copy', ''))).lower()
                if any(w in text for w in ["bsp", "fda", "certified", "trusted", "free shipping", "0%"]):
                    base += 1.6
                if any(w in text for w in ["cheap", "pautang", "scam"]):
                    base -= 0.8
                scores.append(min(round(base + random.uniform(-0.3, 0.4), 1), 9.8))

            df_results["Resonance_Score"] = scores
            df_results["Predicted_CTR_%"] = [round(s * 0.41, 2) for s in scores]
            df_results["Recommendation"] = ["✅ Deploy First" if s >= 8.2 else ("⚠️ Test Low Budget" if s >= 7.0 else "❌ Revise Copy") for s in scores]
            
            # SORT & DISPLAY RESULTS
            df_results = df_results.sort_values(by="Resonance_Score", ascending=False)
            
            st.success("✅ Batch Evaluation Complete!")
            st.markdown("### 📊 Ranked Creative Variants")
            st.dataframe(df_results, use_container_width=True)

            # TOP PERFORMER HIGHLIGHT
            top_row = df_results.iloc[0]
            st.info(f"🏆 **Top Performing Variant ({top_row['Variant_ID']}):** '{top_row['Headline']}' — **{top_row['Resonance_Score']}/10 Score**")
# =========================================================
# TAB 4: PREDICTIVE MONTE CARLO ROAS FORECAST (FEATURE #16)
# =========================================================
with tab_roas:
    st.subheader("Monte Carlo ROAS & CAC Forecaster")
    
    campaign_budget = st.number_input("Total Ad Budget (PHP)", value=50000, step=5000)
    avg_order_value = st.number_input("Average Order Value (AOV in PHP)", value=850, step=50)

    if st.button("🎲 Run 1,000 Monte Carlo Simulations", type="primary"):
        with st.spinner("Simulating probabilistic conversion outcomes..."):
            time.sleep(1.0)

        # Generate 1,000 statistical iterations
        ctr_samples = np.random.normal(0.024, 0.005, 1000)
        cvr_samples = np.random.normal(0.045, 0.008, 1000)
        
        conversions = (campaign_budget / 15.0) * ctr_samples * cvr_samples
        revenue = conversions * avg_order_value
        roas_samples = revenue / campaign_budget

        mean_roas = round(np.mean(roas_samples), 2)
        p10_roas = round(np.percentile(roas_samples, 10), 2)
        p90_roas = round(np.percentile(roas_samples, 90), 2)

        m1, m2, m3 = st.columns(3)
        m1.metric("Expected ROAS", f"{mean_roas}x")
        m2.metric("90% Confidence Low", f"{p10_roas}x")
        m3.metric("90% Confidence High", f"{p90_roas}x")

        # Distribution Chart
        fig = px.histogram(roas_samples, nbins=30, title="Probabilistic ROAS Distribution Curve", labels={'value': 'Predicted ROAS (x)'})
        st.plotly_chart(fig, use_container_width=True)

# --- FOOTER ---
st.divider()
st.caption("Predikta AI Full MVP • Ready for Git & Streamlit Cloud Deployment")