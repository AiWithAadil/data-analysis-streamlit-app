import streamlit as st
import pandas as pd
import os
from io import BytesIO

# 🎨 Set up the Streamlit app
st.set_page_config(page_title="📊 Data Spot", layout="wide")
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>🚀 Data Spot</h1>", 
    unsafe_allow_html=True
)
st.markdown("<h5 style='text-align: center;'>✨ Transform your CSV & Excel files with built-in Data Cleaning & Visualization! 📈</h5>", unsafe_allow_html=True)
st.markdown("---")

# 🎯 Sidebar for file upload
st.sidebar.header("📂 Upload Files")
upload_files = st.sidebar.file_uploader(
    "📤 Upload CSV or Excel files:", 
    type=["csv", "xlsx"], 
    accept_multiple_files=True
)

# 🏗️ Process Each Uploaded File
if upload_files:
    for file in upload_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.sidebar.error(f"❌ File type not accepted: {file_ext}")
            continue

        # ℹ️ File Information
        st.sidebar.subheader("📄 File Info")
        st.sidebar.write(f"**📜 Name:** {file.name}")
        st.sidebar.write(f"**📦 Size:** {file.size / 1024:.2f} KB")
        st.sidebar.write(f"**🔢 Rows:** {df.shape[0]} | **📊 Columns:** {df.shape[1]}")

        # 📌 UI Layout
        tab1, tab2, tab3, tab4 = st.tabs(["👀 Preview", "🧹 Cleaning", "📊 Visualization", "🔄 Conversion"])

        # 📊 Data Preview Tab
        with tab1:
            st.subheader("👀 Data Preview")
            st.dataframe(df.head(10))

        # 🧹 Data Cleaning Tab
        with tab2:
            st.subheader("🧹 Data Cleaning Options")

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🗑️ Remove Duplicates ({file.name})"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates Removed!")

            with col2:
                if st.button(f"🩹 Fill Missing Values ({file.name})"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing Values Filled!")

            # 🎯 Column Selection
            st.subheader("🎯 Select Columns to Keep")
            columns = st.multiselect(f"🛠️ Choose Columns ({file.name})", df.columns, default=df.columns)
            if columns:
                df = df[columns]

        # 📊 Data Visualization Tab
        with tab3:
            st.subheader("📊 Data Visualization")
            numeric_cols = df.select_dtypes(include='number').columns

            if st.checkbox(f"📉 Show Charts ({file.name})"):
                if len(numeric_cols) > 1:
                    st.bar_chart(df[numeric_cols].iloc[:, :2])
                    st.line_chart(df[numeric_cols].iloc[:, :2])
                else:
                    st.warning("⚠️ Not enough numeric columns for visualization!")

        # 🔄 File Conversion Tab
        with tab4:
            st.subheader("🔄 Convert File Format")
            conversion_type = st.radio(f"🔄 Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
            if st.button(f"💾 Convert {file.name}"):

                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"

                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                buffer.seek(0)

                # 📥 Download button
                st.download_button(
                    label=f"📥 Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )

st.sidebar.success("🎉 Ready to process your data!")  
