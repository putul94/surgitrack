import streamlit as st
import pandas as pd
import os

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="SurgiTrack",
    page_icon="🏥",
    layout="wide"
)

# -----------------------
# DATABASE FILE
# -----------------------
FILE = "surgeries.csv"

if not os.path.exists(FILE):
    df = pd.DataFrame(columns=[
        "Patient Name",
        "Age",
        "Gender",
        "Procedure",
        "Surgery Date",
        "Duration (Minutes)",
        "Notes"
    ])
    df.to_csv(FILE, index=False)

# -----------------------
# LOAD DATA
# -----------------------
df = pd.read_csv(FILE)

# -----------------------
# SIDEBAR
# -----------------------
st.sidebar.title("🏥 SurgiTrack")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Add Surgery", "View Cases"]
)

# =======================
# DASHBOARD
# =======================
if page == "Dashboard":

    st.title("🏥 SurgiTrack Dashboard")

    total_cases = len(df)

    if total_cases > 0:
        avg_duration = round(
            pd.to_numeric(
                df["Duration (Minutes)"],
                errors="coerce"
            ).mean(),
            2
        )
    else:
        avg_duration = 0

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Surgeries",
        total_cases
    )

    col2.metric(
        "Average Duration",
        f"{avg_duration} min"
    )

    st.subheader("Recent Cases")

    if total_cases > 0:
        st.dataframe(
            df.tail(10),
            use_container_width=True
        )
    else:
        st.info("No surgery records found.")

# =======================
# ADD SURGERY
# =======================
elif page == "Add Surgery":

    st.title("➕ Add Surgery Case")

    with st.form("surgery_form"):

        patient_name = st.text_input(
            "Patient Name"
        )

        age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=30
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )

        procedure = st.text_input(
            "Procedure"
        )

        surgery_date = st.date_input(
            "Surgery Date"
        )

        duration = st.number_input(
            "Duration (Minutes)",
            min_value=0,
            value=60
        )

        notes = st.text_area(
            "Notes"
        )

        submit = st.form_submit_button(
            "Save Case"
        )

        if submit:

            new_case = pd.DataFrame([{
                "Patient Name": patient_name,
                "Age": age,
                "Gender": gender,
                "Procedure": procedure,
                "Surgery Date": str(surgery_date),
                "Duration (Minutes)": duration,
                "Notes": notes
            }])

            updated_df = pd.concat(
                [df, new_case],
                ignore_index=True
            )

            updated_df.to_csv(
                FILE,
                index=False
            )

            st.success(
                "✅ Surgery Case Saved Successfully"
            )

# =======================
# VIEW CASES
# =======================
elif page == "View Cases":

    st.title("📋 Surgery Logbook")

    search = st.text_input(
        "Search Patient or Procedure"
    )

    filtered = df.copy()

    if search:
        filtered = df[
            df.astype(str)
            .apply(
                lambda x: x.str.contains(
                    search,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        ]

    st.dataframe(
        filtered,
        use_container_width=True
    )

    # Excel Export
    excel_file = "surgery_logbook.xlsx"

    filtered.to_excel(
        excel_file,
        index=False,
        engine="openpyxl"
    )

    with open(excel_file, "rb") as f:

        st.download_button(
            label="⬇ Download Excel",
            data=f,
            file_name="surgery_logbook.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )