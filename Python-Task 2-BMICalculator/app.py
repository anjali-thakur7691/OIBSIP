"""Professional BMI Calculator dashboard. Run: python -m streamlit run app.py"""
import pandas as pd
import streamlit as st

from bmi import CATEGORY_DETAILS, calculate_bmi, get_category, healthy_weight_range, imperial_to_metric, validate_input
from csv_handler import CSVHandler, HEADERS
from database import BMIDatabase
from graph import BMIGraph
from gauge import create_bmi_gauge
from pdf_report import PDFReport

st.set_page_config(page_title="BMI Calculator", page_icon="assets/bmi-reference.png", layout="wide")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
html, body, [class*="css"] {font-family:'Nunito',sans-serif;}
.block-container {padding-top:1.6rem; padding-bottom:2.5rem; max-width:1200px;}
.hero {padding:2rem 2.2rem; border-radius:22px; color:white; margin-bottom:1.5rem;
background:linear-gradient(120deg,#6d28d9 0%,#2563eb 47%,#06b6d4 100%); box-shadow:0 12px 30px #4f46e544;}
.hero h1 {color:white!important; font-size:2.35rem!important; margin:0!important;}
.hero p {font-size:1.05rem; margin:.4rem 0 0; opacity:.92;}
.section-title {color:#312e81; font-weight:800; margin-top:1rem;}
.badge {display:inline-block; background:#e0e7ff; color:#4338ca; border-radius:20px; padding:5px 12px; margin:4px 5px 0 0; font-weight:700; font-size:.84rem;}
div[data-testid='stMetric'] {background:linear-gradient(145deg,#ffffff,#f3f8ff); border:1px solid #dbeafe; border-radius:16px; padding:15px; box-shadow:0 6px 16px #1d4ed80d;}
div[data-testid='stMetricLabel'] {color:#4f46e5; font-weight:800;}
div.stButton > button {border:0; border-radius:10px; font-weight:800; padding:.55rem 1rem; color:white; background:linear-gradient(100deg,#7c3aed,#2563eb); box-shadow:0 5px 12px #4f46e533;}
div.stButton > button:hover {transform:translateY(-1px); color:white; border:0; background:linear-gradient(100deg,#6d28d9,#0891b2);}
[data-testid='stSidebar'] {background:linear-gradient(180deg,#ede9fe 0%,#e0f2fe 100%);}
[data-testid='stSidebar'] h1 {color:#312e81; font-weight:800;}
[data-testid='stSidebar'] [data-testid='stRadio'] label {font-weight:700; color:#3730a3;}
div[data-testid='stDataFrame'] {border:1px solid #dbeafe; border-radius:12px; overflow:hidden;}
</style>""", unsafe_allow_html=True)

db, csv_handler, graph, pdf_report = BMIDatabase(), CSVHandler(), BMIGraph(), PDFReport()
st.session_state.setdefault("result", None)
st.session_state.setdefault("draft", None)


def records_frame(records=None):
    return pd.DataFrame(records if records is not None else db.get_all_records(), columns=HEADERS)


def sync_csv():
    csv_handler.sync_records(db.get_all_records())


def page_hero(title, subtitle):
    left, right = st.columns([1, 10])
    with left:
        st.image("assets/bmi-reference.png", width=112)
    with right:
        st.markdown(f"<div class='hero'><h1>{title}</h1><p>{subtitle}</p></div>", unsafe_allow_html=True)


def dashboard_page():
    page_hero("BMI Calculator Dashboard", "Your colourful health companion for smarter BMI tracking.")
    image_left, image_center, image_right = st.columns([1, 2, 1])
    with image_center:
        st.image("assets/bmi-calculator-illustration.jpg", caption="Understand your BMI category at a glance.", use_container_width=True)
    records = db.get_all_records()
    if not records:
        st.info("Welcome! Add your first measurement from the Calculator page.")
        return
    df = records_frame(records)
    a, b, c, d = st.columns(4)
    a.metric("Total users", df["Name"].nunique())
    b.metric("Total records", len(df))
    c.metric("Average BMI", f"{df['BMI'].mean():.2f}")
    d.metric("Normal category", int((df["Category"] == "Normal").sum()))
    st.markdown("<h3 class='section-title'>Recent BMI measurements</h3>", unsafe_allow_html=True)
    st.dataframe(df.head(5), use_container_width=True, hide_index=True)
    st.markdown("<h3 class='section-title'>BMI category guide</h3>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({"Category": ["Underweight", "Normal", "Overweight", "Obese"],
                               "BMI range": ["Below 18.5", "18.5 - 24.9", "25.0 - 29.9", "30.0 and above"],
                               "Colour feedback": ["Blue", "Green", "Amber", "Red"]}),
                 use_container_width=True, hide_index=True)


def calculate_page():
    page_hero("BMI Calculator", "Calculate, understand and privately track your Body Mass Index.")
    st.markdown("<span class='badge'>Accurate calculation</span><span class='badge'>Private history</span><span class='badge'>Wellness insights</span>", unsafe_allow_html=True)
    image_left, image_center, image_right = st.columns([1, 2, 1])
    with image_center:
        st.image("assets/bmi-calculator-illustration.jpg", caption="BMI Calculator", use_container_width=True)
    with st.form("bmi_form"):
        left, right = st.columns(2)
        with left:
            name = st.text_input("Full name", placeholder="Enter your name")
            age = st.number_input("Age", 1, 120, 18)
            gender = st.selectbox("Gender", ["Female", "Male", "Other", "Prefer not to say"])
        with right:
            unit = st.radio("Measurement system", ["Metric", "Imperial"], horizontal=True)
            if unit == "Metric":
                weight = st.number_input("Weight (kg)", 10.0, 500.0, 60.0, 0.1)
                height = st.number_input("Height (m)", 0.5, 3.0, 1.65, 0.01)
            else:
                pounds = st.number_input("Weight (lb)", 22.0, 1102.0, 132.0, 0.1)
                feet = st.number_input("Height (ft)", 1, 8, 5)
                inches = st.number_input("Additional height (in)", 0.0, 11.9, 5.0, 0.1)
                weight, height = imperial_to_metric(pounds, feet, inches)
                st.caption(f"Converted: {weight:.1f} kg | {height:.2f} m")
        submitted = st.form_submit_button("Calculate BMI", use_container_width=True)
    if submitted:
        valid, message = validate_input(weight, height, age)
        if not name.strip(): st.error("Please enter a name before calculating.")
        elif not valid: st.error(message)
        else:
            bmi, category = calculate_bmi(weight, height), get_category(calculate_bmi(weight, height))
            st.session_state.result = (bmi, category, weight, height)
            st.session_state.draft = (name.strip(), age, gender, weight, height, bmi, category)
    if st.session_state.result:
        bmi, category, weight, height = st.session_state.result
        colour, guidance = CATEGORY_DETAILS[category]
        low, high = healthy_weight_range(height)
        a, b, c = st.columns(3)
        a.metric("Your BMI", f"{bmi:.2f}"); b.metric("Category", category); c.metric("Healthy weight range", f"{low}-{high} kg")
        st.markdown(f"<div style='padding:1.2rem;border-radius:16px;background:{colour}18;border:1px solid {colour}55;border-left:7px solid {colour};box-shadow:0 6px 16px {colour}18'><span style='font-size:1.15rem;font-weight:800;color:{colour}'>{category}</span><br>{guidance}</div>", unsafe_allow_html=True)
        st.markdown("<h3 class='section-title'>Your live BMI meter</h3>", unsafe_allow_html=True)
        st.pyplot(create_bmi_gauge(bmi, category), use_container_width=True, clear_figure=True)
        st.caption("BMI is a screening measure, not a medical diagnosis. It is generally intended for adults.")
        if st.button("Save this result to history", type="primary", use_container_width=True):
            if db.save_record(*st.session_state.draft):
                st.balloons() 
                sync_csv(); st.success("Result saved to SQLite history and CSV backup.")
            else: st.error("The record could not be saved. Please try again.")
def history_page():
    page_hero("BMI Calculator History", "Search, filter, edit and export every saved wellness record.")
    records = db.get_all_records()
    if not records:
        st.info("No saved records yet. Calculate and save a BMI result to begin."); return
    search = st.text_input("Search by name")
    
    # DataFrame load karke ID sequence ko 1 se set karne ka logic
    raw_df = records_frame(db.search_user(search) if search.strip() else records)
    df = raw_df.reset_index(drop=True)
    if 'ID' in df.columns:
        df['ID'] = range(1, len(df) + 1)
    else:
        df.insert(0, 'ID', range(1, len(df) + 1))
    
    a, b = st.columns(2)
    categories = a.multiselect("Filter by category", ["Underweight", "Normal", "Overweight", "Obese"])
    genders = b.multiselect("Filter by gender", sorted(df["Gender"].unique()))
    if categories: df = df[df["Category"].isin(categories)]
    if genders: df = df[df["Gender"].isin(genders)]
    if df.empty:
        st.warning("No records match the selected filters."); return
    st.dataframe(df, use_container_width=True, hide_index=True)
    a, b, c = st.columns(3)
    a.metric("Saved measurements", len(df)); b.metric("Average BMI", f"{df['BMI'].mean():.2f}"); c.metric("Latest BMI", f"{df.iloc[0]['BMI']:.2f}")
    st.download_button("Download CSV", df.to_csv(index=False).encode(), "BMI_History.csv", "text/csv")
    if st.button("Prepare PDF report", use_container_width=True):
        path = pdf_report.generate([tuple(row) for row in df.itertuples(index=False, name=None)])
        with open(path, "rb") as report: st.download_button("Download PDF report", report.read(), "BMI_Report.pdf", "application/pdf")
    st.divider()
    with st.expander("Edit or delete a record"):
        choices = {f"#{r[0]} | {r[1]} | {r[8]}": r for r in records}
        selected = choices[st.selectbox("Select record", choices)]
        with st.form("edit_record"):
            name = st.text_input("Name", selected[1]); age = st.number_input("Age", 1, 120, int(selected[2]))
            options = ["Female", "Male", "Other", "Prefer not to say"]
            gender = st.selectbox("Gender", options, index=options.index(selected[3]) if selected[3] in options else 2)
            weight = st.number_input("Weight (kg)", 10.0, 500.0, float(selected[4]), 0.1); height = st.number_input("Height (m)", 0.5, 3.0, float(selected[5]), 0.01)
            update = st.form_submit_button("Update record")
        if update:
            valid, message = validate_input(weight, height, age)
            if not name.strip() or not valid: st.error(message if not valid else "Name is required.")
            else:
                bmi = calculate_bmi(weight, height)
                if db.update_record(selected[0], name, age, gender, weight, height, bmi, get_category(bmi)):
                    sync_csv(); st.success("Record updated."); st.rerun()
        if st.button("Delete selected record") and db.delete_record(selected[0]):
            sync_csv(); st.success("Record deleted."); st.rerun()
    with st.expander("Danger zone"):
        confirm = st.checkbox("I understand this permanently removes every saved record.")
        if st.button("Delete all history", disabled=not confirm) and db.delete_all():
            sync_csv(); st.success("All BMI history was deleted."); st.rerun()


def about_page():
    st.title("About Professional BMI Calculator")
    st.markdown("""This project includes input validation, BMI category colour feedback, multiple users,
SQLite storage, CSV backup/export, PDF reports, editable history, graphs, dashboard and filters.

**Formula:** BMI = weight (kg) / height squared (m).

### Developer
**Anjali Thakur**

Built with Python, Streamlit, SQLite, Pandas, Matplotlib and ReportLab.""")


st.sidebar.image("assets/bmi-reference.png", use_container_width=True)
st.sidebar.title("BMI Calculator")
st.sidebar.caption("Professional BMI Calculator")
menu = st.sidebar.radio("Navigate", ["Dashboard", "Calculator", "History", "Analytics", "About"])
st.sidebar.markdown("---\n**Developer:** Anjali Thakur\n\n**Features**\n- Calculator & categories\n- SQLite + CSV storage\n- PDF reports & graphs\n- Multiple-user history\n- Search, filters and record editing")
st.sidebar.info("Your records are stored locally in `database/bmi.db`.")
if menu == "Dashboard": dashboard_page()
elif menu == "Calculator": calculate_page()
elif menu == "History": history_page()
elif menu == "Analytics":
    st.title("BMI Analytics Dashboard"); graph.show_graph(db.get_all_records())
else: about_page()
