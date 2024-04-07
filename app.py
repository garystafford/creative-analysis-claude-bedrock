# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Reference: https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages.html

"""
Shows how to run a multimodal prompt with Anthropic Claude (on demand) and InvokeModel.
"""

import json
import logging
import base64
import time
import boto3
import streamlit as st
import numpy as np
from PIL import Image

from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def run_multi_modal_prompt(
    bedrock_runtime,
    model_id,
    messages,
    max_tokens=2000,
    temperature=0.25,
    top_p=0.999,
    top_k=250,
):
    """
    Invokes a model with a multimodal prompt.
    Args:
        bedrock_runtime: The Amazon Bedrock boto3 client.
        model_id (str): The model ID to use.
        messages (JSON) : The messages to send to the model.
        max_tokens (int) : The maximum  number of tokens to generate.
    Returns:
        None.
    """

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
        }
    )

    response = bedrock_runtime.invoke_model(body=body, modelId=model_id)
    response_body = json.loads(response.get("body").read())

    return response_body


def build_request(prompt, image):
    """
    Entrypoint for Anthropic Claude multimodal prompt example.
    """

    try:

        bedrock_runtime = boto3.client(service_name="bedrock-runtime")

        model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
        input_image = image
        input_text = prompt

        # Read reference image from file and encode as base64 strings.
        with open(input_image, "rb") as image_file:
            content_image = base64.b64encode(image_file.read()).decode("utf8")

        message = {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": content_image,
                    },
                },
                {"type": "text", "text": input_text},
            ],
        }

        messages = [message]

        response = run_multi_modal_prompt(
            bedrock_runtime,
            model_id,
            messages,
            st.session_state.max_tokens,
            st.session_state.temperature,
            st.session_state.top_p,
            st.session_state.top_k,
        )
        print(json.dumps(response, indent=4))

        return response

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occurred: " + format(message))


def main():
    """
    Entrypoint for Anthropic Claude multimodal prompt example.
    """

    st.set_page_config(
        page_title="Advertising Analysis",
        # page_icon="",
    )

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
                    height: 325px;
                    font-family: 'Inter', sans-serif;
                    background-color: #777777;
                    color: #ffffff;
                }
                section[aria-label="Upload a JPG image:"] {
                    background-color: #777777;
                }
                textarea[aria-label="Analysis:"] {
                    height: 800px;
                }
                .element-container img {
                    background-color: #ffffff;
                }
                h2 {
                    color: white;
                }
                #MainMenu {
                    visibility: visible;
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
                    color: #CCC8AA;
                }
                div[class^="stSlider"] p {
                    color: #CCC8AA;
                }
                div[class^="stSlider"] label {
                    background-color: #777777;
                }
                [data-testid="stForm"] {
                    border-color: #777777;
                }
                [id="generative-ai-powered-creative-analysis"] span {
                    color: #e6e6e6;
                }
                [data-testid="stForm"] {
                    width: 800px;
                }
        </style>
        """

    st.markdown(
        custom_css,
        unsafe_allow_html=True,
    )

    if "max_tokens" not in st.session_state:
        st.session_state["max_tokens"] = 1000

    if "temperature" not in st.session_state:
        st.session_state["temperature"] = 1.0

    if "top_p" not in st.session_state:
        st.session_state["top_p"] = 0.999

    if "top_k" not in st.session_state:
        st.session_state["top_k"] = 250

    st.markdown("## Generative AI-powered Creative Analysis")

    with st.form("ad_analyze_form", border=True, clear_on_submit=False):
        st.markdown(
            "Describe the analysis task you wish to perform and upload the creative content to be analyzed. Analysis powered by Amazon Bedrock and Anthropic Claude 3 Sonnet foundational AI model."
        )
        default_prompt = """Analyze these advertisements for Mercedes-Benz C-Class Sedans, two in English and two in German. Identify at least 5 common creative elements that contribute to their success. Examine factors such as:
    1. Visual design and imagery
    2. Messaging and copywriting
    3. Use of color, typography, and branding
    4. Interactivity or multimedia components
    5. Alignment with Mercedes-Benz's brand identity and positioning

For each element, describe how it is effectively utilized across the ads and explain why it is an impactful creative choice. Provide specific examples and insights to support your analysis. The goal is to uncover the key creative strategies that make these Mercedes-Benz digital ads compelling and effective."""
        prompt = st.text_area(label="User Prompt:", value=default_prompt, height=250)

        img_file_buffer = st.file_uploader(
            "Upload a JPG, PNG, GIF, or WEBP image:", type=["jpg", "png", "webp", "gif"]
        )
        epoch_time = int(time.time())
        image_name = f"image_{epoch_time}.png"
        if img_file_buffer is not None:
            image = Image.open(img_file_buffer)
            image_path = f"_temp_images/{image_name}"
            image.save(image_path)

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.markdown("---")
            st.image(image_path, caption="")
            with st.spinner(text="Analyzing..."):
                response = build_request(prompt, image_path)
                st.text_area(
                    label="Analysis:", value=response["content"][0]["text"], height=800
                )
    st.markdown(
        "<small style='color: #888888'> Gary A. Stafford, 2024</small>",
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("### Inference Parameters")

        st.session_state.max_tokens = st.slider(
            "max_tokens", min_value=0, max_value=5000, value=2000, step=10
        )
        st.markdown("---")

        st.session_state.temperature = st.slider(
            "temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.01
        )
        st.markdown("---")

        st.session_state.top_p = st.slider(
            "top_p", min_value=0.0, max_value=1.0, value=0.999, step=0.001
        )
        st.markdown("---")

        st.session_state.top_k = st.slider(
            "top_k", min_value=0, max_value=500, value=250, step=1
        )


if __name__ == "__main__":
    main()
