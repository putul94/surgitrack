import streamlit as st
import pandas as pd
import os

# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="SurgiTrack",
    page_icon="🏥",
    layout="wide"
)

# -------------------------------
# DATABASE
# -------------------------------

FILE = "surgeries.csv"

COLUMNS = [
    "Patient Name",
    "Age",
    "Gender",
    "Procedure",
    "Surgery Date",
    "Duration (Minutes)",
    "Notes"
]

if not os.path.exists(FILE):
    pd.DataFrame(columns=COLUMNS).to_csv(FILE, index=False)

df = pd.read_csv(FILE)

# -------------------------------
# SIDEBAR
# -------------------------------

st.sidebar.title("🏥 SurgiTrack")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Surgery",
        "View Cases"
    ]
)

# =====================================================
# DASHBOARD
# =====================================================

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

    st.divider()

    st.subheader("Recent Cases")

    if total_cases > 0:

        st.dataframe(
            df.tail(10),
            use_container_width=True
        )

    else:

        st.info("No surgery records found.")

# =====================================================
# ADD SURGERY
# =====================================================

elif page == "Add Surgery":

    st.title("➕ Add Surgery")

    with st.form("add_form"):

        patient = st.text_input("Patient Name")

        age = st.number_input(
            "Age",
            0,
            120,
            30
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

        surgery_date = st.date_input(
            "Surgery Date"
        )

        duration = st.number_input(
            "Duration (Minutes)",
            0,
            1000,
            60
        )

        notes = st.text_area(
            "Notes"
        )

        save = st.form_submit_button(
            "💾 Save Surgery"
        )

        if save:

            if patient.strip() == "" or procedure.strip() == "":

                st.error(
                    "Patient Name and Procedure are required."
                )

            else:

                new_row = pd.DataFrame([{

                    "Patient Name": patient,
                    "Age": age,
                    "Gender": gender,
                    "Procedure": procedure,
                    "Surgery Date": str(surgery_date),
                    "Duration (Minutes)": duration,
                    "Notes": notes

                }])

                df = pd.concat(
                    [df, new_row],
                    ignore_index=True
                )

                df.to_csv(
                    FILE,
                    index=False
                )

                st.success(
                    "✅ Surgery Saved Successfully"
                )

                st.rerun()
                # =====================================================
# VIEW CASES
# =====================================================

elif page == "View Cases":

    st.title("📋 Surgery Logbook")

    search = st.text_input(
        "🔍 Search Patient or Procedure"
    )

    filtered = df.copy()

    if search.strip():

        filtered = filtered[
            filtered.astype(str)
            .apply(
                lambda x: x.str.contains(
                    search,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        ]

    st.write(f"### Total Records : {len(filtered)}")

    if filtered.empty:

        st.warning("No records found.")

    else:

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("✏ Edit / Delete Record")

        selected = st.selectbox(
            "Select Record",
            filtered.index,
            format_func=lambda i:
                f"{df.loc[i,'Patient Name']} | {df.loc[i,'Procedure']}"
        )

        with st.form("edit_form"):

            patient = st.text_input(
                "Patient Name",
                value=df.loc[selected, "Patient Name"]
            )

            age = st.number_input(
                "Age",
                min_value=0,
                max_value=120,
                value=int(df.loc[selected, "Age"])
            )

            gender = st.selectbox(
                "Gender",
                ["Male", "Female", "Other"],
                index=[
                    "Male",
                    "Female",
                    "Other"
                ].index(df.loc[selected, "Gender"])
            )

            procedure = st.text_input(
                "Procedure",
                value=df.loc[selected, "Procedure"]
            )

            surgery_date = st.text_input(
                "Surgery Date",
                value=str(df.loc[selected, "Surgery Date"])
            )

            duration = st.number_input(
                "Duration (Minutes)",
                min_value=0,
                value=int(df.loc[selected, "Duration (Minutes)"])
            )

            notes = st.text_area(
                "Notes",
                value=str(df.loc[selected, "Notes"])
            )

            col1, col2 = st.columns(2)

            update = col1.form_submit_button(
                "💾 Update"
            )

            delete = col2.form_submit_button(
                "🗑 Delete"
            )

            if update:

                df.loc[selected] = [
                    patient,
                    age,
                    gender,
                    procedure,
                    surgery_date,
                    duration,
                    notes
                ]

                df.to_csv(
                    FILE,
                    index=False
                )

                st.success(
                    "✅ Record Updated Successfully"
                )

                st.rerun()

            if delete:

                df = df.drop(selected)

                df.reset_index(
                    drop=True,
                    inplace=True
                )

                df.to_csv(
                    FILE,
                    index=False
                )

                st.success(
                    "🗑 Record Deleted Successfully"
                )

                st.rerun()

        st.divider()

        csv = filtered.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇ Download CSV",
            data=csv,
            file_name="surgery_records.csv",
            mime="text/csv"
        )

        try:

            excel_file = "surgery_records.xlsx"

            filtered.to_excel(
                excel_file,
                index=False,
                engine="openpyxl"
            )

            with open(excel_file, "rb") as f:

                st.download_button(
                    label="⬇ Download Excel",
                    data=f,
                    file_name="surgery_records.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        except:

            st.info(
                "Install openpyxl to enable Excel export."
            )

        st.metric(
            "Displayed Records",
            len(filtered)
        )

        st.caption(
            "🏥 SurgiTrack Basic Edition"
        )