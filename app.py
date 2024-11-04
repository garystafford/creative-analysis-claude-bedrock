# Author: Gary A. Stafford
# Modified: 2024-10-25
# Shows how to use Anthropic Claude 3 multimodal family model prompt on Amazon Bedrock.

import base64
import datetime
import json
import logging
from io import StringIO
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List, Optional, Tuple, Union

import boto3
import pymupdf
import pyperclip
import streamlit as st
from botocore.exceptions import ClientError
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from PIL import Image

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

################### Constants ###################
AWS_REGIONS: str = ["us-west-2", "us-east-1"]

DEFAULT_AWS_REGION: int = AWS_REGIONS[0]

# model ids: https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html
MODELS: list[str] = [
    "anthropic.claude-3-5-sonnet-20241022-v2:0",  # currently only available in us-west-2!
    "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "anthropic.claude-3-haiku-20240307-v1:0",
    "anthropic.claude-3-sonnet-20240229-v1:0",
    "anthropic.claude-3-opus-20240229-v1:0",
]

DEFAULT_MODEL_ID: int = MODELS[0]

DEFAULT_MAX_TOKENS: int = 2048
DEFAULT_TEMPERATURE: float = 0.2
DEFAULT_TOP_P: float = 0.999
DEFAULT_TOP_K: int = 250

DEFAULT_SYSTEM_PROMPT: str = """You are an experienced Creative Director at a top-tier advertising agency. You are an expert at advertising analysis, the process of examining advertising to understand its effects on consumers."""

DEFAULT_USER_PROMPT: str = """Analyze these four print advertisements for Mercedes-Benz sedans, two in English and two in German. Identify at least 5 common creative elements that contribute to their success. Examine factors such as:
    1. Visual design and imagery
    2. Messaging and copywriting
    3. Use of color, typography, and branding
    4. Interactivity or multimedia components
    5. Alignment with Mercedes-Benz's brand identity and positioning

For each element, describe how it is effectively utilized across the ads and explain why it is an impactful creative choice. Provide specific examples and insights to support your analysis. The goal is to uncover the key creative strategies that make these Mercedes-Benz ads compelling and effective.

Important: if no ads were provided, do not produce the analysis."""
#################################################


def invoke_model(
    model_id: str,
    system_prompt: str,
    messages: List[dict],
    max_tokens: int,
    temperature: float,
    top_p: float,
    top_k: int,
) -> Optional[dict]:
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

    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime", region_name=st.session_state.aws_region
    )

    try:
        response = bedrock_runtime.invoke_model(body=body, modelId=model_id)
        logger.debug("Response: %s", response)
        return json.loads(response["body"].read())
    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        st.error(f"A client error occurred: {message}")
        return None


def compose_message(user_prompt: str, file_paths: List[dict]) -> List[dict]:
    """
    Composes a message dictionary for a user prompt and optional file paths.
    Args:
        user_prompt (str): The text prompt provided by the user.
        file_paths (List[dict]): A list of dictionaries, each containing:
            - "file_path" (str): The path to the file.
            - "file_type" (str): The MIME type of the file.
    Returns:
        List[dict]: A list containing a single message dictionary. The message dictionary
        includes the user prompt as text and optionally includes images encoded in base64
        if file paths are provided.
    """

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


def is_pdf_image_based(uploaded_file: Union[NamedTemporaryFile, StringIO]) -> bool:
    """
    Determines if a PDF file is image-based (i.e., contains no text content).
    Args:
        uploaded_file (Union[NamedTemporaryFile, StringIO]): The uploaded PDF file to check.
            It can be a NamedTemporaryFile or a StringIO object.
    Returns:
        bool: True if the PDF is image-based (contains no text content), False otherwise.
    """

    is_image_based = True

    with NamedTemporaryFile(suffix="pdf") as temp:
        temp.write(uploaded_file.getvalue())
        temp.seek(0)
        doc = pymupdf.open(temp.name)

    for page in doc:
        text = page.get_text()
        if text.strip():  # Check if there is any text content
            is_image_based = False
            break

    doc.close()
    return is_image_based


def convert_pdf_to_images(
    uploaded_file: Union[NamedTemporaryFile, StringIO]
) -> List[Path]:
    """
    Convert a PDF file to a list of images, one for each page.

    Args:
        uploaded_file (Union[NamedTemporaryFile, StringIO]): The uploaded PDF file to be converted.

    Returns:
        List[Path]: A list of paths to the generated image files, one for each page of the PDF.
    """

    images = []
    zoom = 4
    mat = pymupdf.Matrix(zoom, zoom)

    with NamedTemporaryFile(suffix="pdf") as temp:
        temp.write(uploaded_file.getvalue())
        temp.seek(0)
        doc = pymupdf.open(temp.name)

        for i, page in enumerate(doc):
            image = page.get_pixmap()
            image_path = Path(f"_temp_images/page_{i}.png")
            image.save(image_path)
            images.append(image_path)
        doc.close()

    return images


def extract_text_from_pdf_pymupdf(
    uploaded_file: Union[NamedTemporaryFile, StringIO]
) -> str:
    """
    Extracts text from a PDF file using PyMuPDF.
    Args:
        uploaded_file (Union[NamedTemporaryFile, StringIO]): The uploaded PDF file,
        which can be a NamedTemporaryFile or a StringIO object.
    Returns:
        str: The extracted text from the PDF.
    """

    with NamedTemporaryFile(suffix="pdf") as temp:
        temp.write(uploaded_file.getvalue())
        temp.seek(0)
        doc = pymupdf.open(temp.name)
        extract_text = "".join(page.get_text() for page in doc)
        return extract_text


def extract_text_from_pdf_docling(
    uploaded_file: Union[NamedTemporaryFile, StringIO]
) -> str:
    """
    Extracts text from a PDF file using OCR and table structure recognition.

    Args:
        uploaded_file (Union[NamedTemporaryFile, StringIO]): The uploaded PDF file to be processed.

    Returns:
        str: The extracted text from the PDF in Markdown format.

    This function uses a document conversion pipeline with OCR and table structure options enabled
    to extract text from the provided PDF file. The extracted text is then exported to Markdown format.
    """

    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.do_cell_matching = True

    doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    with NamedTemporaryFile(suffix="pdf") as temp:
        temp.write(uploaded_file.getvalue())
        temp.seek(0)
        conv_result = doc_converter.convert(temp.name)
        extract_text = conv_result.document.export_to_markdown()
        return extract_text


def extract_text_from_text(uploaded_file: Union[NamedTemporaryFile, StringIO]) -> str:
    """
    Extracts text content from an uploaded file.
    This function takes an uploaded file, which can be either a NamedTemporaryFile or a StringIO object,
    and extracts its text content as a string.
    Args:
        uploaded_file (Union[NamedTemporaryFile, StringIO]): The uploaded file from which to extract text.
    Returns:
        str: The extracted text content of the uploaded file.
    """

    extract_text = StringIO(uploaded_file.getvalue().decode("utf-8"))
    return extract_text.getvalue()


def save_image(
    uploaded_file: Union[NamedTemporaryFile, StringIO], file_paths: List[dict]
) -> None:
    """
    Save an uploaded image file to a temporary directory and update the file paths list.
    Args:
        uploaded_file (Union[NamedTemporaryFile, StringIO]): The uploaded image file.
        file_paths (List[dict]): A list to store file path information dictionaries.
    Returns:
        None
    Raises:
        None
    Logs:
        - Error if the file size exceeds 5MB.
        - Info when the image is successfully saved.
    Notes:
        - The function checks if the uploaded file size exceeds 5MB and logs an error if it does.
        - The image is saved in a temporary directory named "_temp_images".
        - The file path and type are appended to the `file_paths` list.
    """

    if uploaded_file.size > 5 * 1024 * 1024:  # 5MB
        logger.error("File size exceeds 5MB limit")
        st.error("File size exceeds 5MB limit")
        return
    image = Image.open(uploaded_file)
    image_path = Path("_temp_images") / uploaded_file.name
    image_path.parent.mkdir(exist_ok=True)
    image.save(image_path)
    file_paths.append(
        {
            "file_path": str(image_path),
            "file_type": uploaded_file.type,
        }
    )
    logger.info("Image saved: %s (%s)", image_path, uploaded_file.type)


def display_inference_summary() -> str:
    """
    Generates a summary of inference parameters and results from the session state.

    Returns:
        str: A formatted string containing the inference parameters and results.
            The summary includes:
            - aws_region: The AWS region used for inference.
            - model_id: The ID of the model used for inference.
            - max_tokens: The maximum number of tokens allowed in the inference.
            - temperature: The temperature setting for the inference.
            - top_p: The top-p sampling parameter for the inference.
            - top_k: The top-k sampling parameter for the inference.
            - uploaded_media_type: The type of media uploaded for inference.
            - analysis_time_sec: The time taken for the analysis in seconds.
            - input_tokens: The number of input tokens used in the inference.
            - output_tokens: The number of output tokens generated by the inference.
    """
    return f"""
Inference Parameters:
• aws_region: {st.session_state.aws_region}
• model_id: {st.session_state.model_id}
• max_tokens: {st.session_state.max_tokens}
• temperature: {st.session_state.temperature}
• top_p: {st.session_state.top_p}
• top_k: {st.session_state.top_k}
• uploaded_media_type: {st.session_state.media_type}

Inference Results:
• analysis_time_sec: {st.session_state.analysis_time}
• input_tokens: {st.session_state.input_tokens}
• output_tokens: {st.session_state.output_tokens}"""


def display_sidebar() -> None:
    """
    Displays the sidebar in the Streamlit application with various inference parameters.
    The sidebar includes:
    - A selectbox for selecting AWS regions.
    - A selectbox for selecting model IDs from the Anthropic Claude 3 family of models.
    - A slider for setting the maximum number of tokens.
    - A slider for setting the temperature.
    - A slider for setting the top_p parameter.
    - A slider for setting the top_k parameter.
    Additionally, it displays an inference summary at the bottom of the sidebar.
    """

    with st.sidebar:
        st.markdown("### Inference Parameters")
        st.session_state.aws_regions = st.selectbox(
            label="aws_region:",
            options=AWS_REGIONS,
        )
        st.session_state.model_id = st.selectbox(
            label="model_id (Anthropic Claude 3 family of models):",
            options=MODELS,
        )
        st.session_state.max_tokens = st.slider(
            "max_tokens", min_value=0, max_value=5000, value=DEFAULT_MAX_TOKENS, step=10
        )
        st.session_state.temperature = st.slider(
            "temperature",
            min_value=0.0,
            max_value=1.0,
            value=DEFAULT_TEMPERATURE,
            step=0.05,
        )
        st.session_state.top_p = st.slider(
            "top_p", min_value=0.0, max_value=1.0, value=DEFAULT_TOP_P, step=0.01
        )
        st.session_state.top_k = st.slider(
            "top_k", min_value=0, max_value=500, value=DEFAULT_TOP_K, step=1
        )

        st.markdown("---")

        # display inference summary
        inference_summary = display_inference_summary()
        st.text(inference_summary)


def handle_form_submission() -> Tuple[bool, Optional[List], List[dict], Optional[str]]:
    """
    Handles the form submission for analyzing uploaded content using Generative AI models.

    This function creates a form using Streamlit to collect user inputs, including system and user prompts,
    and files to be analyzed. It processes the uploaded files based on their types and extracts relevant
    information to be used in the analysis.

    Returns:
        Tuple[bool, Optional[List], List[dict], Optional[str]]:
            - A boolean indicating whether the form was submitted.
            - A list of uploaded files, if any.
            - A list of dictionaries containing file paths and types for image files.
            - Extracted text from the uploaded files, if applicable.
    """

    with st.form("ad_analyze_form", border=True, clear_on_submit=False):
        st.markdown(
            "Describe the role you want the model to play, the task you wish to perform, and upload the content to be analyzed. The Generative AI-based analysis is powered by Amazon Bedrock and Anthropic Claude 3 family of foundation models."
        )

        system_prompt_default = DEFAULT_SYSTEM_PROMPT
        user_prompt_default = DEFAULT_USER_PROMPT

        st.session_state.system_prompt = st.text_area(
            "System Prompt:", value=system_prompt_default, height=50
        )
        st.session_state.user_prompt = st.text_area(
            "User Prompt:", value=user_prompt_default, height=250
        )

        uploaded_files = st.file_uploader(
            "Upload JPG, PNG, GIF, WEBP, PDF, CSV, MD, or TXT files:",
            type=["jpg", "jpeg", "png", "gif", "webp", "pdf", "csv", "md", "txt"],
            accept_multiple_files=True,
        )

        file_paths: List[dict] = []
        extract_text: Optional[str] = None

        if uploaded_files:
            for uploaded_file in uploaded_files:
                logger.info(
                    "Uploaded file: %s (%s)", uploaded_file.name, uploaded_file.type
                )
                st.session_state.media_type = uploaded_file.type
            match uploaded_file.type:
                case "text/csv" | "text/plain" | "application/octet-stream":
                    extract_text = extract_text_from_text(uploaded_file)
                    st.session_state.user_prompt += f"\n\n{extract_text}"
                case "application/pdf":
                    is_image: bool = is_pdf_image_based(uploaded_file)
                    logging.info("is_image: %s", is_image)
                    if is_pdf_image_based(uploaded_file):
                        images = convert_pdf_to_images(uploaded_file)
                        for image in images:
                            file_paths.append(
                                {
                                    "file_path": str(image),
                                    "file_type": "image/png",
                                }
                            )
                    else:
                        extract_text = extract_text_from_pdf_pymupdf(uploaded_file)
                        st.session_state.user_prompt += f"\n\n{extract_text}"
                case "image/jpeg" | "image/png" | "image/webp" | "image/gif":
                    save_image(uploaded_file, file_paths)
                case _:
                    st.error("Invalid file type. Please upload a valid file type.")
            logger.info("Prompt: %s", st.session_state.user_prompt)

        submitted = st.form_submit_button("Submit")

    return submitted, uploaded_files, file_paths, extract_text


def main() -> None:
    """
    Main function to set up and run the Streamlit application for Generative AI-powered Multimodal Analysis.

    This function performs the following tasks:
    1. Sets the page configuration with a title and icon.
    2. Reads and applies custom CSS from a file.
    3. Initializes session state variables with default values if they are not already set.
    4. Displays the main title of the application.
    5. Handles form submission and processes uploaded files.
    6. If a form is submitted and a user prompt is provided, it:
        - Displays a separator.
        - Displays a sample of the file contents or images based on the uploaded file type.
        - Shows a spinner while analyzing the input.
        - Composes a message and invokes the AI model for analysis.
        - Displays the model's response in a text area.
        - Updates session state with analysis time and token usage.
        - Copies the response to the clipboard.
    7. Displays a footer with author information.
    8. Displays the sidebar of the application.
    """

    st.set_page_config(page_title="Multimodal Analysis", page_icon="analysis.png")

    with open("css.txt") as css_file:
        custom_css = css_file.read()
    st.markdown(custom_css, unsafe_allow_html=True)

    session_vars = {
        "aws_region": DEFAULT_AWS_REGION,
        "system_prompt": DEFAULT_SYSTEM_PROMPT,
        "user_prompt": DEFAULT_USER_PROMPT,
        "model_id": DEFAULT_MODEL_ID,
        "max_tokens": DEFAULT_MAX_TOKENS,
        "temperature": DEFAULT_TEMPERATURE,
        "top_p": DEFAULT_TOP_P,
        "top_k": DEFAULT_TOP_K,
        "media_type": None,
        "analysis_time": 0,
        "input_tokens": 0,
        "output_tokens": 0,
    }
    for var, value in session_vars.items():
        if var not in st.session_state:
            st.session_state[var] = value

    st.markdown("## Generative AI-powered Multimodal Analysis")

    # display form and handle form submission
    submitted, uploaded_files, file_paths, extract_text = handle_form_submission()

    if submitted and st.session_state.user_prompt:
        st.markdown("---")
        if uploaded_files:
            if uploaded_files[0].type in [
                "text/csv",
                "text/plain",
                "application/pdf",
            ]:
                # st.markdown(f"Sample of file contents:\n\n{extract_text[0:250]}...")
                st.markdown(f"")
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
                    analysis = st.text_area(
                        "Model Response:",
                        value=response["content"][0]["text"],
                        height=800,
                    )
                    st.session_state.analysis_time = (
                        end_time - start_time
                    ).total_seconds()
                    st.session_state.input_tokens = response["usage"]["input_tokens"]
                    st.session_state.output_tokens = response["usage"]["output_tokens"]
                    pyperclip.copy(analysis)
                    st.success("Response copied to clipboard.")
                else:
                    st.error("An error occurred during the analysis")
            else:
                st.error("An error occurred constructing the analysis request")
    st.markdown(
        "<small style='color: #888888'> Gary A. Stafford, 2024</small>",
        unsafe_allow_html=True,
    )

    # display sidebar
    display_sidebar()


if __name__ == "__main__":
    main()
