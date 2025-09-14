import streamlit as st
import datetime
import matplotlib.pyplot as plt
from health_assistant import Symptom, HealthAssistant, HealthAssistantCLI


# Import your classes here (Symptom, HealthAssistant, etc.)
# from health_assistant import Symptom, HealthAssistant

# Initialize assistant
if "assistant" not in st.session_state:
    st.session_state.assistant = HealthAssistant((40.7128, -74.0060))  # default NY location
    st.session_state.cli = HealthAssistantCLI()  # to load sample data

assistant = st.session_state.assistant

# ================= Page Config =================
st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🩺",
    layout="wide"
)

# ================= Custom CSS =================
st.markdown("""
<style>
/* Global settings */
body {
    background-color: #f9fafc;
    color: #1f2937;
    font-family: 'Segoe UI', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #1e293b;
}
section[data-testid="stSidebar"] h1, 
section[data-testid="stSidebar"] h2, 
section[data-testid="stSidebar"] h3, 
section[data-testid="stSidebar"] p, 
section[data-testid="stSidebar"] li {
    color: white !important;
}

/* Tabs */
div[data-baseweb="tab"] {
    background-color: #e2e8f0;
    border-radius: 10px 10px 0 0;
    padding: 10px;
    font-weight: bold;
}
div[data-baseweb="tab"][aria-selected="true"] {
    background-color: #2563eb !important;
    color: white !important;
}

/* Buttons */
div.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
}
div.stButton > button:hover {
    background-color: #1d4ed8;
}

/* Metric Cards */
div[data-testid="stMetricValue"] {
    color: #2563eb !important;
    font-weight: bold;
    font-size: 1.4rem;
}

/* Headers */
h1, h2, h3 {
    color: #111827;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ================= Title =================
st.title("🩺 AI-Powered Personal Health Assistant")
st.markdown("""
This system helps you:
- ✅ Understand your symptoms  
- 📊 Track health metrics  
- 💊 Manage medications  
- 👨‍⚕️ Find doctors  
- 🚨 Send emergency alerts
""")

# ================= Tabs =================
tabs = st.tabs(["🤒 Symptoms Checker", "📊 Health Trends", "💊 Medications", "🚨 Emergency"])

# ================= SYMPTOM CHECKER =================
with tabs[0]:
    st.header("Symptom Checker")

    with st.form("symptom_form"):
        name = st.text_input("Enter symptom")
        severity = st.slider("Severity (1-10)", 1, 10, 5)
        duration = st.text_input("Duration (e.g., '2 days')", "1 day")
        submitted = st.form_submit_button("Analyze")

    if submitted and name:
        symptom = Symptom(name, severity, duration)
        result = assistant.analyze_symptoms([symptom])

        if result.get("emergency"):
            st.error(result["message"])
            st.warning(result["recommendation"])
        else:
            st.subheader("Possible Conditions")
            for cond in result["conditions"]:
                st.write(f"- **{cond['condition']}** ({cond['confidence']:.0%} confidence)")

            st.info(f"Recommendation: {result['recommendation']}")

            st.subheader("Recommended Doctors")
            for doc in result["recommended_doctors"]:
                st.write(f"👨‍⚕️ **{doc['name']}** ({doc['specialty']}) — ⭐ {doc['rating']}/5")
                st.write(f"📍 {doc['distance_km']} km away | 📞 {doc['contact']}")
                st.divider()

# ================= HEALTH TRENDS =================
with tabs[1]:
    st.header("Health Trends")

    metric = st.selectbox("Choose a metric", ["weight", "blood pressure"])
    days = st.slider("Number of days", 7, 60, 30)

    trends = assistant.get_health_trends(metric, days)

    if "error" in trends:
        st.warning(trends["error"])
    else:
        st.metric(label=f"Latest {metric}", value=f"{trends['latest']} {trends['metric']}")
        st.write(f"**Average:** {trends['average']} | **Range:** {trends['minimum']}–{trends['maximum']} | **Trend:** {trends['trend']}")

        # Line Chart
        fig, ax = plt.subplots()
        ax.plot(trends["timeline"]["dates"], trends["timeline"]["values"], marker="o", color="#2563eb")
        ax.set_xlabel("Date")
        ax.set_ylabel(metric)
        ax.set_title(f"{metric.capitalize()} over last {days} days")
        st.pyplot(fig)

# ================= MEDICATIONS =================
with tabs[2]:
    st.header("Medication Tracker")

    st.subheader("Reminders")
    reminders = assistant.get_medication_reminders()
    if reminders:
        for r in reminders:
            st.warning(f"💊 {r['message']} (Last taken: {r['last_taken']})")
    else:
        st.success("✅ No medications due right now.")

    st.subheader("Record Medication Taken")
    meds = [m.name for m in assistant.medications]
    if meds:
        chosen = st.selectbox("Select medication", meds)
        if st.button("Mark as Taken"):
            assistant.record_medication_taken(chosen)
            st.success(f"Recorded {chosen} as taken at {datetime.datetime.now().strftime('%H:%M')}")

    st.subheader("Add New Medication")
    with st.form("add_med"):
        med_name = st.text_input("Medication name")
        dosage = st.text_input("Dosage (e.g., '200mg')")
        freq = st.text_input("Frequency (e.g., 'every 6 hours')")
        days_supply = st.number_input("Days supply", 1, 365, 30)
        add_submit = st.form_submit_button("Add Medication")

    if add_submit and med_name:
        med = assistant.add_medication(med_name, dosage, freq, days_supply)
        st.success(f"Added {med.name} ({med.dosage}, {med.frequency})")

# ================= EMERGENCY ALERT =================
with tabs[3]:
    st.header("🚨 Emergency Alert")

    msg = st.text_area("Enter emergency message")
    if st.button("Send Alert"):
        if msg:
            assistant.send_emergency_alert(msg)
            st.error("🚨 Emergency alerts sent to all registered contacts!")
        else:
            st.warning("Please enter a message before sending.")
