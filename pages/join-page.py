import base64
import fastparquet
import streamlit as st
import pandas as pd
import numpy as np


def manage_uploads(u_file):
    # # To read file as bytes:
    # bytes_data = u_file.getvalue()
    # st.write(bytes_data)
    #
    # # To convert to a string based IO:
    # stringio = StringIO(u_file.getvalue().decode("utf-8"))
    # st.write(stringio)
    #
    # # To read file as string:
    # string_data = stringio.read()
    # st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(u_file)
    return dataframe


def download_parquet(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/parquet;base64,{b64}" download="file.parquet">Download parquet file</a>'
    return href


## Reference Column Names
def common_member(ref_df, tgt_df):
    ref_columns = set(ref_df.columns.to_list())
    tgt_columns = set(tgt_df.columns.to_list())
    if ref_columns & tgt_columns:
        return list(ref_columns & tgt_columns)
    else:
        return ("No common elements")


def display_data_table(data):
    data_as_csv = data.to_csv(index=False).encode("utf-8")

    # st.sidebar.divider()
    # st.sidebar.write("Some Description | The inner join operation is used to find the "
    #                  "intersection between two tables | and [hyperlink](./) to Learn Inner Joi-")
    # st.write("DataFrame")
    return data_as_csv

col1, col2 = st.columns(2)

with col1:
    st.subheader("Reference File Upload")
    uploaded_reference_file = col1.file_uploader("Choose your Reference file", key=0)
    if uploaded_reference_file is not None:
        ref_df = manage_uploads(uploaded_reference_file)
        st.dataframe(ref_df.head().T, use_container_width=True)

with col2:
    st.subheader("Target File Upload")
    uploaded_target_file = col2.file_uploader("Choose your Target file", key=1)
    if uploaded_target_file is not None:
        tgt_df = manage_uploads(uploaded_target_file)
        st.dataframe(tgt_df.head().T)

st.sidebar.write("Options would appear once your Files are uploaded")
if uploaded_reference_file is not None and uploaded_target_file is not None:
    # Using "with" notation
    with st.sidebar:
        add_radio = st.radio(
            "Choose a shipping method",
            ("Inner-Join", "Left-Join", "Right-Join")
            # , "Full-Join"
        )
    st.info(f"You selected **{add_radio}**")
    # col3, col4 = st.columns(2)
    #
    # with col1:
    if add_radio == "Inner-Join" or "Right-Join":
        cc_id = st.selectbox("Select the common Identifier:", common_member(ref_df, tgt_df))
        inJ_df = ref_df.merge(tgt_df, how="inner", on=str(cc_id))
        rtJ_df = ref_df.merge(tgt_df, how="right", on=str(cc_id))
        data = pd.DataFrame()
        if cc_id is not None or cc_id != "No common elements":
            if add_radio == "Inner-Join":
                data = inJ_df.copy()
                if st.sidebar.button("Preview Data"):
                    st.dataframe(data.head().T)
            elif add_radio == "Right-Join":
                data = rtJ_df.copy()
                if st.sidebar.button("Preview Data"):
                    st.dataframe(data.head().T)
        else:
            st.warning("Choose a common Identifier to continue")
    if add_radio == "Left-Join":
        lfJ_df = ref_df.merge(tgt_df, how='left')
        data = lfJ_df.copy()
        if lfJ_df.shape[0] == 0:
            st.error("No Common Data! Retry with another common identifier")
        else:
            if st.sidebar.button("Preview Data"):
                st.dataframe(data.head().T)
    if data.shape[0] == 0:
        st.error("No Common Data! Retry with another common identifier")
    st.markdown("")
    st.markdown("")
    col5, col6, col7 = st.columns(3)
    with col5:
        st.write(f'The Wrangled Data: {data.shape}')
        # st.write(data.shape())
    with col6:
        data_as_csv = data.to_csv()
        st.download_button(
            label="Download data as CSV",
            data=data_as_csv,
            file_name=str(add_radio) + '_data.csv',
            mime='text/csv',
        )
    with col7:
        st.write("PlaceHolder for Parquet File Downloader")
# col5, col6 = st.sidebar.columns(2)
#                     with col5:
#                         st.download_button(
#                             label="Download data as CSV",
#                             data=myfile_as_csv,
#                             file_name='innerJoined_data.csv',
#                             mime='text/csv',
#                         )
#                     with col6:
#                         # ### Code to save df as parquet
#                         parquet_file = inJ_df.to_parquet('myfile.parquet', engine='fastparquet')
#                         # download_parquet(inJ_df)
#                         st.write('Parquet Download Placeholder')