import streamlit as st
import subprocess, os, glob, urllib.parse, urllib.request, json, re, time
import pandas as pd

st.set_page_config(
    page_title="Sofxemo Leads | Enterprise Pipeline Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Realistic Enterprise Studio Design (Linear & Stripe Aesthetic)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #0A0D14 !important;
        color: #F1F5F9 !important;
    }

    /* Subtle Real Studio Micro-Dot Background */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-image: radial-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px);
        background-size: 24px 24px;
        z-index: 0;
        pointer-events: none;
    }

    /* Ambient Warm Studio Fill */
    .stApp::after {
        content: "";
        position: fixed;
        top: -10vh;
        left: 20vw;
        width: 60vw;
        height: 50vh;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.04) 0%, rgba(99, 102, 241, 0.03) 40%, transparent 70%);
        z-index: 0;
        pointer-events: none;
    }

    .main .block-container {
        max-width: 1020px !important;
        padding-top: 1.8rem !important;
        padding-bottom: 4rem !important;
        margin: auto !important;
        position: relative;
        z-index: 10;
    }

    /* Executive Studio Card */
    .executive-card {
        background: #111622;
        border-radius: 20px;
        padding: 2.2rem 2.6rem;
        border: 1px solid rgba(255, 255, 255, 0.07);
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.6);
        margin-bottom: 1.4rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 2rem;
    }
    .exec-text-wrap { flex: 1.35; }
    
    .brand-eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #94A3B8;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.73rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    .brand-eyebrow-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: #38BDF8;
    }

    .exec-heading {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 2.3rem;
        font-weight: 800;
        line-height: 1.2;
        color: #F8FAFC !important;
        letter-spacing: -0.03em;
        margin: 0 0 0.6rem 0;
    }
    .exec-heading-accent {
        color: #38BDF8;
    }

    .exec-desc {
        font-size: 0.95rem;
        color: #94A3B8 !important;
        font-weight: 400;
        line-height: 1.6;
        margin: 0;
    }

    .exec-img-wrap {
        flex: 0.65;
        display: flex;
        justify-content: center;
    }
    .exec-img-wrap img {
        width: 100%;
        max-width: 250px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 16px 30px -10px rgba(0, 0, 0, 0.7);
        object-fit: cover;
    }

    /* Enterprise Link Action Buttons */
    div[data-testid="stLinkButton"] > a {
        background: #161D2B !important;
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        color: #E2E8F0 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.83rem !important;
        padding: 0.52rem 1rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2) !important;
    }
    div[data-testid="stLinkButton"] > a:hover {
        background: #1E293B !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        color: #FFFFFF !important;
        transform: translateY(-1px) !important;
    }

    /* Form Container */
    .form-panel {
        background: #111622;
        border-radius: 16px;
        padding: 1.6rem 2rem;
        border: 1px solid rgba(255, 255, 255, 0.07);
        box-shadow: 0 10px 25px -10px rgba(0, 0, 0, 0.5);
        margin-top: 1.2rem;
        margin-bottom: 1.4rem;
    }

    .stTextInput label, .stSlider label, .stRadio label, .stCheckbox label {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
        font-size: 0.87rem !important;
    }
    .stTextInput input {
        background-color: #0A0D14 !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
        padding: 0.65rem 0.95rem !important;
        font-weight: 500 !important;
    }
    .stTextInput input:focus {
        border-color: #38BDF8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.15) !important;
    }
    .stRadio div[role="radiogroup"] label span p,
    .stCheckbox label span p {
        color: #CBD5E1 !important;
        font-weight: 500 !important;
    }

    /* Natural Polished Action Button */
    div.stButton > button:first-child {
        background: #2563EB !important;
        color: #FFFFFF !important;
        border: 1px solid #3B82F6 !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.8rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    }
    div.stButton > button:first-child:hover {
        background: #1D4ED8 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4) !important;
    }

    /* KPI Summary Cards */
    .kpi-card {
        background: #111622;
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 1.1rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }
    .kpi-val { font-size: 1.7rem; font-weight: 800; color: #FFFFFF; }
    .kpi-tag {
        color: #64748B;
        font-size: 0.72rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.05em;
    }

    /* Real-Time Processing Box */
    .processing-box {
        background: #111622;
        border-radius: 16px;
        padding: 2.2rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.09);
        box-shadow: 0 15px 30px rgba(0,0,0,0.4);
        margin: 2rem 0;
    }
    .clean-spinner {
        width: 44px;
        height: 44px;
        border: 3px solid rgba(255, 255, 255, 0.08);
        border-top: 3px solid #38BDF8;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1.2rem auto;
    }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    .proc-title { font-size: 1.1rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.25rem; }
    .proc-sub { font-size: 0.85rem; color: #64748B; }
</style>
""", unsafe_allow_html=True)

# Executive Studio Header Banner
with st.container():
    st.markdown("""
    <div class="executive-card">
        <div class="exec-text-wrap">
            <div class="brand-eyebrow">
                <span class="brand-eyebrow-dot"></span>
                SOFXEMO INFOTECH • SALES INTELLIGENCE
            </div>
            <h1 class="exec-heading">Acquire Qualified Local Clients <br><span class="exec-heading-accent">With Actionable Pipeline Data.</span></h1>
            <p class="exec-desc">Direct Google Maps scraper configured to surface high-converting local businesses without websites, complete with automated sales pain points and verified ratings.</p>
        </div>
        <div class="exec-img-wrap">
            <img src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=600&q=80" alt="Tech Workplace Studio">
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Clean Link Actions
    col_a, col_b, col_c, col_d = st.columns([1.1, 1.2, 1.25, 1.05])
    with col_a:
        st.link_button("🌐 sofxemo.com", "https://sofxemo.com", use_container_width=True)
    with col_b:
        st.link_button("✉️ info@sofxemo.com", "mailto:info@sofxemo.com", use_container_width=True)
    with col_c:
        st.link_button("💬 WhatsApp: 8298326803", "https://wa.me/918298326803", use_container_width=True)
    with col_d:
        st.link_button("📞 +91 8298326803", "tel:+918298326803", use_container_width=True)

# Form Panel
st.markdown('<div class="form-panel">', unsafe_allow_html=True)
c1, c2 = st.columns([3, 1])
with c1:
    query = st.text_input("Target Query & Location", placeholder="e.g. Hotels in Patna, Beauty Parlour in Motihari, Schools in Bettiah")
with c2:
    depth = st.slider("Result Depth (Scrolls)", 1, 10, 3, help="1 depth = ~15 leads. 3 depth = ~60 leads.")

fc1, fc2 = st.columns([1.5, 1])
with fc1:
    website_filter = st.radio(
        "Website Strategy:",
        ["Only Without Website (Prime Web Clients)", "Only With Website", "Show All Leads"],
        index=0,
        horizontal=True
    )
with fc2:
    st.write("")
    require_phone = st.checkbox("Sirf valid Phone Numbers filter karein", value=True)
st.markdown('</div>', unsafe_allow_html=True)

def parse_num(val, is_float=False):
    if pd.isna(val) or val is None:
        return 0.0 if is_float else 0
    clean = re.sub(r'[^0-9\.]', '', str(val))
    if not clean:
        return 0.0 if is_float else 0
    try:
        return round(float(clean), 1) if is_float else int(float(clean))
    except:
        return 0.0 if is_float else 0

def analyze_lead_exact(row, query_str):
    name = str(row.get('title', 'Business')).strip()
    category = str(row.get('category', 'Local Business')).strip()
    if category == 'nan' or not category:
        category = "Local Business"
    
    rating = parse_num(row.get('review_rating', row.get('rating', 0)), is_float=True)
    reviews = parse_num(row.get('review_count', row.get('reviews', 0)), is_float=False)
    
    web = str(row.get('website', '')).strip()
    has_web = bool(web and web != 'nan' and len(web) > 3)
    
    addr = str(row.get('address', row.get('located_in', ''))).strip()
    if addr == 'nan':
        addr = ""

    city = ""
    for c in ['Bettiah', 'Motihari', 'Patna', 'Muzaffarpur', 'Gaya', 'Darbhanga', 'Raxaul', 'Siwan', 'Gopalganj']:
        if c.lower() in query_str.lower() or c.lower() in addr.lower():
            city = c
            break
    if not city:
        city = "Local"

    area_locality = addr if addr else "Local Area"
    cat_lower = (category + " " + name + " " + query_str).lower()

    if not has_web:
        if (rating >= 4.0 and reviews >= 15) or (reviews >= 35) or (any(k in cat_lower for k in ['hotel', 'resort', 'clinic', 'hospital']) and reviews >= 8):
            priority = "A - Hot"
        elif (rating >= 3.5 and reviews >= 5) or (reviews >= 8):
            priority = "B - Warm"
        else:
            priority = "C - Cold"
    else:
        priority = "B - Warm" if (rating >= 4.0 and reviews >= 20) else "C - Cold"

    if any(k in cat_lower for k in ['hotel', 'resort', 'stay', 'lodge', 'inn']):
        solution = "Direct Hotel Room Booking Website + Payment Gateway + Room Availability Management System"
        value = "₹30,000.00" if priority == "A - Hot" else "₹22,000.00"
        pain = f"{reviews}+ Google reviews aur {rating}★ reputation hone ke bawajood direct booking website nahi hai; OTAs par heavy commission lose ho raha hai."
    elif any(k in cat_lower for k in ['salon', 'parlour', 'beauty', 'makeup', 'spa']):
        solution = "High-End Bridal Portfolio Website + Service Rate Card + WhatsApp Slot Booking"
        value = "₹22,000.00" if priority == "A - Hot" else "₹16,000.00"
        pain = f"{reviews} reviews aur {rating}★ rating hone ke bawajood koi official bridal catalogue ya appointment booking portal nahi hai."
    elif any(k in cat_lower for k in ['clinic', 'hospital', 'doctor', 'dental', 'hair', 'derma']):
        solution = "Clinic Web Portal + Before/After Case Studies + Consultation Booking"
        value = "₹35,000.00" if priority == "A - Hot" else "₹25,000.00"
        pain = "Aesthetic/medical treatments ke liye before/after portfolio aur doctor consultation booking portal missing hai."
    elif any(k in cat_lower for k in ['school', 'coaching', 'institute', 'classes', 'college']):
        solution = "Institute Management Portal + Student Inquiry Capture System + Online Prospectus"
        value = "₹28,000.00" if priority == "A - Hot" else "₹20,000.00"
        pain = f"{reviews} reviews ke sath goodwill hai par online fee collection, admission enquiry funnel aur syllabus portal missing hai."
    else:
        solution = "High-Conversion Business Landing Page + Google Business SEO + WhatsApp Funnel"
        value = "₹20,000.00" if priority == "A - Hot" else "₹15,000.00"
        if reviews > 0:
            pain = f"{rating}★ rating ({reviews} reviews) hone ke bawajood official website nahi hai; local competitors search se deals le rahe hain."
        else:
            pain = "Google presence par official website missing hai; customers direct trust establish nahi kar paate."

    search_query = f"{name}, {addr}".strip(", ")
    direct_link = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(search_query)}"

    phone = str(row.get('phone', '')).strip()
    if phone == 'nan':
        phone = ""

    notes = f"{rating} rating ({reviews} reviews). Address: {addr}. Pitch {solution.split('+')[0].strip()}."

    return {
        "Business Name": name,
        "Category": category,
        "City": city,
        "Area/Locality": area_locality,
        "Google Maps Link": direct_link,
        "Google Rating": rating if rating > 0 else "Not Rated",
        "Review Count": reviews,
        "Website Available": "Yes" if has_web else "No",
        "Website Status": "Available" if has_web else "No Website",
        "Website URL": web if has_web else "",
        "Instagram Available": "Unknown",
        "Facebook Available": "Unknown",
        "Phone Number": phone,
        "WhatsApp Available": "Yes" if phone else "No",
        "Decision Maker": "Owner",
        "Decision Maker Name": "Unknown",
        "Lead Source": "Google Maps",
        "Pain Point": pain,
        "Suggested Solution": solution,
        "Estimated Project Value": value,
        "Lead Priority": priority,
        "First Contact Date": "",
        "Contact Method": "Phone Call",
        "Contact Status": "Not Contacted",
        "Response": "Not Required",
        "Last Contact Date": "",
        "Next Follow-up Date": "",
        "Demo Status": "Not Sent",
        "Proposal Status": "Not Sent",
        "Deal Status": "New",
        "Lost Reason": "",
        "Notes": notes
    }

st.write("")
if st.button("Start Search & Extract Leads", type="primary"):
    if not query.strip():
        st.warning("Kripya search query enter karein.")
    else:
        loader_slot = st.empty()
        loader_slot.markdown("""
        <div class="processing-box">
            <div class="clean-spinner"></div>
            <div class="proc-title">Extracting Local Business Data...</div>
            <div class="proc-sub">Scanning listings, validating reviews, and mapping CRM schema</div>
        </div>
        """, unsafe_allow_html=True)

        url = f"https://nominatim.openstreetmap.org/search?format=json&q={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
                lat, lon = (data[0]['lat'], data[0]['lon']) if data else ("26.1542", "85.8918")
        except Exception:
            lat, lon = "26.1542", "85.8918"

        subprocess.run(["bash", "scripts/scrape.sh", query, str(lat), str(lon), str(depth)])

        loader_slot.empty()

        files = sorted(glob.glob("results-*.csv"), key=os.path.getmtime, reverse=True)
        if files:
            raw_df = pd.read_csv(files[0])
            total_scraped = len(raw_df)
            raw_df.columns = [c.lower() for c in raw_df.columns]

            if require_phone and 'phone' in raw_df.columns:
                raw_df = raw_df[raw_df['phone'].notna() & (raw_df['phone'].astype(str).str.strip() != '')]

            if 'website' in raw_df.columns:
                if "Without Website" in website_filter:
                    raw_df = raw_df[raw_df['website'].isna() | (raw_df['website'].astype(str).str.strip() == '')]
                elif "With Website" in website_filter:
                    raw_df = raw_df[raw_df['website'].notna() & (raw_df['website'].astype(str).str.strip() != '')]

            crm_records = [analyze_lead_exact(row, query) for _, row in raw_df.iterrows()]
            crm_df = pd.DataFrame(crm_records)

            st.markdown("---")
            k1, k2, k3, k4 = st.columns(4)
            with k1:
                st.markdown(f"""<div class="kpi-card"><div class="kpi-tag">Total Discovered</div><div class="kpi-val">{total_scraped}</div></div>""", unsafe_allow_html=True)
            with k2:
                st.markdown(f"""<div class="kpi-card"><div class="kpi-tag">Qualified Pipeline</div><div class="kpi-val" style="color:#38BDF8;">{len(crm_df)}</div></div>""", unsafe_allow_html=True)
            with k3:
                hot_leads = len(crm_df[crm_df['Lead Priority'] == 'A - Hot']) if not crm_df.empty else 0
                st.markdown(f"""<div class="kpi-card"><div class="kpi-tag">Prime Hot (A)</div><div class="kpi-val" style="color:#F43F5E;">{hot_leads}</div></div>""", unsafe_allow_html=True)
            with k4:
                total_sum = 0
                for val in crm_df['Estimated Project Value']:
                    try:
                        clean_v = int(re.sub(r'[^0-9]', '', str(val).split('.')[0]))
                        total_sum += clean_v
                    except:
                        pass
                pipeline_val = f"₹{total_sum:,}" if total_sum > 0 else "₹0"
                st.markdown(f"""<div class="kpi-card"><div class="kpi-tag">Est. Deal Value</div><div class="kpi-val" style="color:#10B981;">{pipeline_val}</div></div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.dataframe(crm_df, use_container_width=True)

            csv = crm_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Full CRM Pipeline (.CSV)",
                data=csv,
                file_name=f"{query.replace(' ', '_')}_CRM_Pipeline.csv",
                mime="text/csv"
            )
        else:
            st.error("Data scrape nahi ho saka. Docker verification required.")
