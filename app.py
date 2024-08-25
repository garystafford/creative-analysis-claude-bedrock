# Author: Gary A. Stafford
# Modified: 2024-04-25
# Shows how to use Anthropic Claude 3 multimodal family model prompt on Amazon Bedrock.

import base64
import datetime
import json
import logging
from io import StringIO
from pathlib import Path
from tempfile import NamedTemporaryFile

import boto3
import pymupdf
import streamlit as st
from botocore.exceptions import ClientError
from PIL import Image

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def invoke_model(
    model_id,
    system_prompt,
    messages,
    max_tokens,
    temperature,
    top_p,
    top_k,
):
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "system": system_prompt,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
        }
    )

    bedrock_runtime = boto3.client(service_name="bedrock-runtime")

    try:
        response = bedrock_runtime.invoke_model(body=body, modelId=model_id)
        logger.debug("Response: %s", response)
        return json.loads(response["body"].read())
    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        st.error(f"A client error occurred: {message}")
        return None


def compose_message(user_prompt, file_paths):
    message = {"role": "user", "content": [{"type": "text", "text": user_prompt}]}

    if file_paths:
        for file_path in file_paths:
            with open(file_path["file_path"], "rb") as image_file:
                content_image = base64.b64encode(image_file.read()).decode("utf8")
                message["content"].append(
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": file_path["file_type"],
                            "data": content_image,
                        },
                    }
                )

    messages = [message] if message else []
    return messages


def extract_text_from_pdf(uploaded_file):
    with NamedTemporaryFile(suffix="pdf") as temp:
        temp.write(uploaded_file.getvalue())
        temp.seek(0)
        doc = pymupdf.open(temp.name)
        extract_text = "".join(page.get_text() for page in doc)
        return extract_text


def extract_text_from_text(uploaded_file):
    extract_text = StringIO(uploaded_file.getvalue().decode("utf-8"))
    return extract_text.getvalue()


def save_image(uploaded_file, file_paths):
    if uploaded_file.size > 5 * 1024 * 1024:
        logger.error("File size exceeds 5MB limit")
        st.error("File size exceeds 5MB limit")
        return
    image = Image.open(uploaded_file)
    file_path = Path("_temp_images") / uploaded_file.name
    file_path.parent.mkdir(exist_ok=True)
    image.save(file_path)
    file_paths.append(
        {
            "file_path": str(file_path),
            "file_type": uploaded_file.type,
        }
    )
    logger.info("Image saved: %s (%s)", file_path, uploaded_file.type)


def main():
    st.set_page_config(page_title="Multimodal Analysis", page_icon="analysis.png")

    custom_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400&display=swap');
        html, body, p, li, a, h1, h2, h3, h4, h5, h6, table, td, th, div, form, input, button, textarea, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        .block-container {
            padding-top: 32px;
            padding-bottom: 32px;
            padding-left: 0;
            padding-right: 0;
        }
        textarea[class^="st-"] {
            font-family: 'Inter', sans-serif;
            color: #ffffff;
            background-color: #777777;
        }
        textarea[aria-label="System Prompt:"] {
            height: 50px;
        }
        textarea[aria-label="User Prompt:"] {
            height: 400px;
        }
        textarea[aria-label="Analysis:"] {
            height: 600px;
        }
        section[aria-label="Upload JPG, PNG, GIF, WEBP, PDF, CSV, or TXT files:"] {
            background-color: #777777;
        }
        .element-container img { # uploaded image preview
            background-color: #ffffff;
        }
        h2 { # main headline
            color: white;
        }
        MainMenu {
            visibility: hidden;
        }
        footer {
            visibility: hidden;
        }
        header {
            visibility: hidden;
        }
        p, div, h1, h2, h3, h4, h5, h6, button, section, label, input, small[class^="st-"] {
            color: #ffffff;
        }
        button, section, label, input {
            background-color: #555555;
        }
        button[class^="st-"] {
            background-color: #777777;
            color: #ffffff;
            border-color: #ffffff;
        }
        hr span {
            color: #ffffff;
        }
        div[class^="st-"] {
            color: #ccc8aa;
        }
        div[class^="stSlider"] p {
            color: #ccc8aa;
        }
        div[class^="stSlider"] label {
            background-color: #777777;
        }
        div[data-testid="stSidebarUserContent"] {
            padding-top: 40px;
        }
        div[class="row-widget stSelectbox"] label {
            background-color: #777777;
        }
        label[data-testid="stWidgetLabel"] p {
            color: #ccc8aa;
        }
        div[data-baseweb="select"] div {
            font-size: 14px;
        }
        div[data-baseweb="select"] li {
            font-size: 12px;
        }
        [data-testid="stForm"] {
            border-color: #777777;
        }
        h2[id="generative-ai-powered-multimodal-analysis"] {
            color: #e6e6e6;
            font-size: 34px;
        }
        [data-testid="stForm"] {
            width: 850px;
        }
    </style>
    """

    st.markdown(custom_css, unsafe_allow_html=True)

    session_vars = {
        "system_prompt": None,
        "user_prompt": None,
        "model_id": "anthropic.claude-3-5-sonnet-20240620-v1:0",
        "analysis_time": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "max_tokens": 1000,
        "temperature": 1.0,
        "top_p": 0.999,
        "top_k": 250,
        "media_type": None,
    }

    for var, value in session_vars.items():
        if var not in st.session_state:
            st.session_state[var] = value

    st.markdown("## Generative AI-powered Multimodal Analysis")

    with st.form("ad_analyze_form", border=True, clear_on_submit=False):
        st.markdown(
            "Describe the role you want the model to play, the task you wish to perform, and upload the content to be analyzed. The Generative AI-based analysis is powered by Amazon Bedrock and Anthropic Claude 3 family of foundation models."
        )

        system_prompt_default = """You are an experienced Creative Director at a top-tier advertising agency. You are an expert at advertising analysis, the process of examining advertising to understand its effects on consumers."""
        user_prompt_default = """Analyze these four print advertisements for Mercedes-Benz sedans, two in English and two in German. Identify at least 5 common creative elements that contribute to their success. Examine factors such as:
    1. Visual design and imagery
    2. Messaging and copywriting
    3. Use of color, typography, and branding
    4. Interactivity or multimedia components
    5. Alignment with Mercedes-Benz's brand identity and positioning

For each element, describe how it is effectively utilized across the ads and explain why it is an impactful creative choice. Provide specific examples and insights to support your analysis. The goal is to uncover the key creative strategies that make these Mercedes-Benz ads compelling and effective.

Important: if no ads were provided, do not produce the analysis."""

        st.session_state.system_prompt = st.text_area(
            "System Prompt:", value=system_prompt_default, height=50
        )
        st.session_state.user_prompt = st.text_area(
            "User Prompt:", value=user_prompt_default, height=250
        )

        uploaded_files = st.file_uploader(
            "Upload JPG, PNG, GIF, WEBP, PDF, CSV, or TXT files:",
            type=["jpg", "png", "webp", "pdf", "gif", "csv", "txt"],
            accept_multiple_files=True,
        )

        file_paths = []
        extract_text = None

        if uploaded_files:
            for uploaded_file in uploaded_files:
                st.session_state.media_type = uploaded_file.type
                if uploaded_file.type in ["text/csv", "text/plain"]:
                    extract_text = extract_text_from_text(uploaded_file)
                    st.session_state.user_prompt += f"\n\n{extract_text}"
                elif uploaded_file.type == "application/pdf":
                    extract_text = extract_text_from_pdf(uploaded_file)
                    st.session_state.user_prompt += f"\n\n{extract_text}"
                elif uploaded_file.type in [
                    "image/jpeg",
                    "image/png",
                    "image/webp",
                    "image/gif",
                ]:
                    save_image(uploaded_file, file_paths)
                else:
                    st.error("Invalid file type. Please upload a valid file type.")

            logger.info("Prompt: %s", st.session_state.user_prompt)

        submitted = st.form_submit_button("Submit")

        if submitted and st.session_state.user_prompt:
            st.markdown("---")
            if uploaded_files:
                if uploaded_files[0].type in [
                    "text/csv",
                    "text/plain",
                    "application/pdf",
                ]:
                    st.markdown(f"Sample of file contents:\n\n{extract_text[0:500]}...")
                else:
                    for file_path in file_paths:
                        st.image(file_path["file_path"], caption="", width=400)

            with st.spinner(text="Analyzing..."):
                start_time = datetime.datetime.now()
                messages = compose_message(st.session_state.user_prompt, file_paths)
                if messages:
                    response = invoke_model(
                        st.session_state.model_id,
                        st.session_state.system_prompt,
                        messages,
                        st.session_state.max_tokens,
                        st.session_state.temperature,
                        st.session_state.top_p,
                        st.session_state.top_k,
                    )
                    end_time = datetime.datetime.now()
                    if response:
                        st.text_area(
                            "Analysis:",
                            value=response["content"][0]["text"],
                            height=800,
                        )
                        st.session_state.analysis_time = (
                            end_time - start_time
                        ).total_seconds()
                        st.session_state.input_tokens = response["usage"][
                            "input_tokens"
                        ]
                        st.session_state.output_tokens = response["usage"][
                            "output_tokens"
                        ]
                    else:
                        st.error("An error occurred during the analysis")
                else:
                    st.error("An error occurred constructing the analysis request")

    st.markdown(
        "<small style='color: #888888'> Gary A. Stafford, 2024</small>",
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("### Inference Parameters")
        st.session_state.model_id = st.selectbox(
            "model_id",
            options=[
                "anthropic.claude-3-5-sonnet-20240620-v1:0",
                "anthropic.claude-3-haiku-20240307-v1:0",
                "anthropic.claude-3-sonnet-20240229-v1:0",
                "anthropic.claude-3-opus-20240229-v1:0",
            ],
        )

        st.session_state.max_tokens = st.slider(
            "max_tokens", min_value=0, max_value=5000, value=2000, step=10
        )
        st.session_state.temperature = st.slider(
            "temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.05
        )
        st.session_state.top_p = st.slider(
            "top_p", min_value=0.0, max_value=1.0, value=0.999, step=0.01
        )
        st.session_state.top_k = st.slider(
            "top_k", min_value=0, max_value=500, value=250, step=1
        )

        st.markdown("---")

        st.text(
            f"""• model_id: {st.session_state.model_id}
• max_tokens: {st.session_state.max_tokens}
• temperature: {st.session_state.temperature}
• top_p: {st.session_state.top_p}
• top_k: {st.session_state.top_k}
⎯
• uploaded_media_type: {st.session_state.media_type}
⎯
• analysis_time_sec: {st.session_state.analysis_time}
• input_tokens: {st.session_state.input_tokens}
• output_tokens: {st.session_state.output_tokens}
"""
        )


if __name__ == "__main__":
    main()
