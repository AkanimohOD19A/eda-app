## TODO
# Basic Distribution EDA_Page
# Numerical EDA_Page
# Categorical EDA_Page
# Correlation_Matrix EDA_Page
# ChatGPT Advisory for ML-Commitment

### Libraries come here
import streamlit as st
import numpy as np
import pandas as pd
import pyarrow
import plotly.express as px

### Placeholder Data
df = pd.read_csv("./dta/sample_data.csv")

### Page components come here
#### > Handles
st.sidebar.title("Page Handles")

uploaded_file = st.sidebar.file_uploader("Choose a File {.csv, .parquet}", type=["csv", "parquet"])

### Read Uploaded data
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".parquet"):
            df = pd.read_parquet(uploaded_file)
        else:
            st.error("Provide an acceptable file extension")
    except UnicodeDecodeError:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, encoding="ISO-8859-1", header=None, delim_whitespace=True)



### Functions come here
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
numeric_df = df.select_dtypes(include=numerics)
numeric_columns = numeric_df.columns.tolist()
category_df = df.drop(columns=numeric_columns)
category_columns = category_df.columns.tolist()

### Basic Analytics
shape = df.shape
null_values = sum(df.isnull().sum())

#### > Exploration Page
st.header("Exploratory Data Analysis")
st.markdown("Simple Data Visualization/Exploration Tool for quickly Probing, Visualizing and Analyzing Data Sets")

st.divider()
st.markdown('#### Univariate Analysis')
# st.markdown("<h5 style='text-align: center;'>Univariate Analysis</h5>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    num_option = st.selectbox("Select Distribution of a Numerical Variable", numeric_columns)
    fig = px.histogram(df, x=num_option, opacity=0.75)
    fig.update_layout(bargap=0.2, uniformtext_minsize=12, uniformtext_mode='hide')
    st.plotly_chart(fig, use_container_width=True)
with col2:
    cat_option = st.selectbox("Select Distribution of a Categorical Variable", category_columns)
    fig = px.histogram(df, x=cat_option)
    fig.update_layout(bargap=0.2)
    st.plotly_chart(fig, use_container_width=True)
st.divider()

st.markdown('#### Bivariate Analysis')
st.write("Distribution of the Selected Columns")
col3, col4, col5 = st.columns(3)
with col3:
    num_option1 = st.selectbox("Select Numerical Variable", numeric_columns)
with col4:
    numeric_columns_x = numeric_df.drop(columns=num_option1).columns.tolist()
    num_option2 = st.selectbox("Select another Numerical Variable", numeric_columns_x)
with col5:
    cat_option1 = st.selectbox("Select a Categorical Identifier", category_columns)
fig = px.histogram(df, x=num_option2, y=num_option1, color=cat_option1,
                   marginal="box",  # or violin, rug
                   hover_data=df.columns)
st.plotly_chart(fig, use_container_width=True)
st.divider()

st.subheader("Data Page")
st.warning("Check the **Editable Dataframes** option on the side widget to enable you change your values")

### Option to edit data
Editable_Status = {0: "No", 1: "Yes"}
if st.sidebar.checkbox("Would you like to edit your data"):
    edit_df = st.experimental_data_editor(df, use_container_width=True)
    # edit_df.to_csv('./dta/edit_data.csv')
    # df = pd.read_csv("./dta/edit_data.csv")
    Editable_Status = Editable_Status[1]
else:
    st.dataframe(df, use_container_width=True)
    Editable_Status = Editable_Status[0]

st.sidebar.divider()

s_Col1, s_Col2, s_Col3 = st.sidebar.columns(3)
with s_Col1:
    st.markdown("### DATA SHAPE")
    st.write(shape)

with s_Col2:
    st.markdown("### EDITABLE STATUS")
    st.write(Editable_Status)

with s_Col3:
    st.markdown("### NULL VALUES")
    st.write(null_values)
