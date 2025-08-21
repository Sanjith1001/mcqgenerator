import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.mcqgenerator import generate_evaluate_chain
# from mcqgenerator.logger import logging

# Load response schema (if needed)
with open("response.json", "r") as f:
    RESPONSE_JSON = json.load(f)

st.title("MCQs Creator Application with LangChain 🦜⛓️")

# Create a form using st.form
with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or txt file")
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
    subject = st.text_input("Insert Subject", max_chars=20)
    tone = st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")

    button = st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                text = read_file(uploaded_file)

                response = generate_evaluate_chain(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    }
                )

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error while generating MCQs.")
            else:
                if isinstance(response, dict):
                    quiz = response.get("quiz") or response.get("data")

                    if quiz is not None:
                        table_data = get_table_data(quiz)

                        if table_data:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1

                            # ✅ Style for line breaks, wrapping, and row height
                            styled_df = df.style.set_properties(**{
                                "white-space": "pre-line",
                                "line-height": "1.5",
                                "max-width": "300px",
                            })

                            row_height = 50
                            table_height = min(max(len(df) * row_height, 300), 1000)

                            st.dataframe(styled_df, use_container_width=True, height=table_height)

                            st.text_area(label="Review", value=response.get("review", ""))

                        else:
                            st.error("Error parsing quiz data into table.")
                    else:
                        st.error("No quiz data found in response.")
                        st.write("Full response object:", response)
                else:
                    st.write(response)
