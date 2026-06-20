import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="SurgiTrack Lite",
    page_icon="🏥",
    layout="wide"
)

FILE = "surgeries.csv"

# Create CSV if not exists
if not os.path.exists(FILE):
    df_init = pd.DataFrame(columns=[
        "Patient",
        "Age",
        "Gender",
        "Procedure",
        "Date",
        "Duration",
        "Notes"
    ])
    df_init.to_csv(FILE, index=False)

# Load data
df = pd.read_csv(FILE)

# Sidebar
st.sidebar.title("🏥 SurgiTrack Lite")

menu = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Add Case",
        "View Cases"
    ]
)

# Dashboard
if menu == "Dashboard":

    st.title("🏥 Surgeon Dashboard")

    total_cases = len(df)

    if total_cases > 0:
        avg_duration = round(
            pd.to_numeric(
                df["Duration"],
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

    st.dataframe(
        df.tail(10),
        use_container_width=True
    )

# Add Case
elif menu == "Add Case":

    st.title("➕ Add Surgery Case")

    with st.form("case_form"):

        patient = st.text_input(
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
            [
                "Male",
                "Female",
                "Other"
            ]
        )

        procedure = st.text_input(
            "Procedure"
        )

        date = st.date_input(
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

        submitted = st.form_submit_button(
            "Save Case"
        )

        if submitted:

            new_row = pd.DataFrame([{
                "Patient": patient,
                "Age": age,
                "Gender": gender,
                "Procedure": procedure,
                "Date": str(date),
                "Duration": duration,
                "Notes": notes
            }])

            updated_df = pd.concat(
                [df, new_row],
                ignore_index=True
            )

            updated_df.to_csv(
                FILE,
                index=False
            )

            st.success(
                "✅ Surgery Case Saved"
            )

# View Cases
elif menu == "View Cases":

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

    excel_file = "surgery_logbook.xlsx"

    filtered.to_excel(
        excel_file,
        index=False
    )

    with open(
        excel_file,
        "rb"
    ) as f:

        st.download_button(
            label="⬇ Download Excel",
            data=f,
            file_name="surgery_logbook.xlsx"
        )
