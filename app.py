from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input, pdf_cotent, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode(),  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


## Streamlit App

st.set_page_config(page_title="Applicant Tracking System")
st.header("Applicant Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")

# submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("Percentage match")

input_prompt1 = """
As an experienced HR professional with expertise in any one job role of the following: Data Science, Full Stack Web Development, Big Data Engineering, DevOps, or Data Analysis, your task is to review the provided resume against the job description for these roles. Please provide a detailed professional evaluation of the candidate's profile, focusing on the following aspects:

1. Alignment with Job Description:
   - Does the candidate's experience and skills match the requirements listed in the job description?
   - Are the candidate's qualifications and past roles relevant to the job they are applying for?
   
2. Strengths:
   - Highlight key skills and experiences that make the candidate a strong fit for the role.
   - Mention any notable achievements or projects that demonstrate the candidate's capabilities.
   
3. Weaknesses:
   - Identify any gaps in experience or skills that may be crucial for the job.
   - Point out areas where the candidate may need further development or training.

4. Overall Suitability:
   - Provide a summary of the candidate's overall fit for the role.
   - Recommend whether the candidate should be considered for the next stage of the hiring process.

Please ensure that your evaluation is thorough and considers both technical and soft skills relevant to the job role.
"""

input_prompt3 = """
You are an advanced ATS (Applicant Tracking System) with comprehensive knowledge and expertise in any one job role of the following: Data Science, Big Data Engineering, DevOps, Data Analysis, or Full Stack Web Development. Utilizing your deep understanding of ATS functionality, your task is to meticulously evaluate the provided resume against the specified job description.

1. Percentage Match: Calculate and provide the overall percentage match of the resume against the job description.
2. Missing Keywords: Identify and list the keywords and skills that are missing from the resume but are essential as per the job description.
3. Strengths and Weaknesses: Offer a detailed analysis highlighting the strengths and weaknesses of the candidate in relation to the job requirements.
4. Final Thoughts: Provide a professional summary and evaluation of whether the candidate's profile aligns with the job requirements, including any recommendations for improvement.

Ensure that your evaluation is thorough, objective, and based on the specific criteria outlined in the job description.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("Summary of your Resume")
        st.write(response)
    else:
        st.write("Please uplaod the resume.")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("Review:")
        st.write(response)
    else:
        st.write("Please uplaod the resume.")
