# Generative AI-powered Multimodal Analysis

Simple Streamlit [application](app.py) used for demonstrating [Anthropic Claude 3](https://www.anthropic.com/news/claude-3-family) family of model's multimodal prompting on [Amazon Bedrock](https://aws.amazon.com/bedrock): Haiku, Sonnet, and Opus. The app was originally created for AdTech, MarTech, and Advertising Agencies that need to analyze advertising and generate new creative concepts. To start, describe the analysis task you wish to perform and optionally upload the content to be analyzed. The app currently supports uploading multiple JPG, PNG, GIF, WebP, PDF, CSV, or TXT files. The analysis is powered by Amazon Bedrock and Anthropic Claude 3 foundational AI model. The Streamlit application calls the [Anthropic Claude Messages API](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages.html); refer to this link for all inference parameters.

![Screenshot](screenshot_app.png)

## Media Types Supported

Currently, this app supports the following media-types for uploading:

- image/jpeg - natively supported by Bedrock/Anthropic
- image/png - natively supported by Bedrock/Anthropic
- image/webp - natively supported by Bedrock/Anthropic
- image/gif - natively supported by Bedrock/Anthropic
- text/plain - content of file is added into prompt as raw text
- text/csv - content of file is added into prompt as raw text (a little hacky right now...)
- application/pdf - content of file is added into prompt as raw text (a little hacky right now...)

## Start Application

```sh
python3 -m pip install virtualenv -Uq
virtualenv claude-streamlit-venv
python3 -m venv claude-streamlit-venv

source claude-streamlit-venv/bin/activate

python3 -m pip install -r requirements.txt -Uq

streamlit run app.py \
    --server.runOnSave true \
    --theme.base "light" \
    --theme.backgroundColor "#333333" \
    --theme.primaryColor "#CCC8AA" \
    --theme.secondaryBackgroundColor "#777777" \
    --ui.hideTopBar "true" \
    --client.toolbarMode "minimal"
```

## Samples Advertisements

<table>
    <tr>
        <td width=384><image src="mercedes_benz_ads/ad1.jpeg"></td>
        <td width=384><image src="mercedes_benz_ads/ad2.jpeg"></td>
    </tr>
    <tr>
        <td width=384><image src="mercedes_benz_ads/ad3.jpeg"></td>
        <td width=384><image src="mercedes_benz_ads/ad4.jpeg"></td>
    </tr>
</table>

## Samples Prompts

### 1. Generate an Analysis of Print Advertisements for Mercedes-Benz

Provides an analysis of the four uploaded print advertisements for Mercedes-Benz.

Upload (4) JPEGs:

- [ad1.jpeg](mercedes_benz_ads/ad1.jpeg)
- [ad2.jpeg](mercedes_benz_ads/ad2.jpeg)
- [ad3.jpeg](mercedes_benz_ads/ad3.jpeg)
- [ad4.jpeg](mercedes_benz_ads/ad4.jpeg)

Prompt:

```text
Analyze these four print advertisements for Mercedes-Benz sedans, two in English and two in German. Identify at least 5 common creative elements that contribute to their success. Examine factors such as:
    1. Visual design and imagery
    2. Messaging and copywriting
    3. Use of color, typography, and branding
    4. Interactivity or multimedia components
    5. Alignment with Mercedes-Benz's brand identity and positioning

For each element, describe how it is effectively utilized across the ads and explain why it is an impactful creative choice. Provide specific examples and insights to support your analysis. The goal is to uncover the key creative strategies that make these Mercedes-Benz ads compelling and effective.

Important: if no ads were provided, do not produce the analysis.
```

### 2. Generate Better Prompts using Prompt Optimization

Asking the foundation model to optimize the user's sub-optimal initial prompt.

Upload (4) JPEGs:

- [ad1.jpeg](mercedes_benz_ads/ad1.jpeg)
- [ad2.jpeg](mercedes_benz_ads/ad2.jpeg)
- [ad3.jpeg](mercedes_benz_ads/ad3.jpeg)
- [ad4.jpeg](mercedes_benz_ads/ad4.jpeg)

Prompt:

```text
You are an expert at optimizing large language model prompts for marketing analysts. Given the following marketing analyst’s task description and the accompanying advertising samples, your job is to create a concise and effective positive prompt that will provide effective responses from a large language model. Based on the content provided, suggest a concise list of key elements to focus on in the analysis.

Analyze these English and German print advertisements and find some common creative elements.
```

### 3. Generate New Creative Concepts from Analysis of Print Advertisements for Mercedes-Benz

Using the resulting analysis to design a new 'Large Leaderboard' size digital advertisement appearing on the 'Modern Luxury | Manhattan' website for Mercedes-Benz C-Class Sedans, targeting young affluent urban couples between 25-35 years old.

Upload (2) PDFs:

- [Ad_Specs_Modern_Luxury.pdf](manhattan_ad_specs/Ad_Specs_Modern_Luxury.pdf)
- [Advertise_Info_Modern_Luxury.pdf](manhattan_ad_specs/Advertise_Info_Modern_Luxury.pdf)

Prompt:

```text
Based on the following analysis of four successful Mercedes-Benz print advertisements, describe a new and compelling design for a 'Large Leaderboard' size digital advertisement appearing on the 'Modern Luxury | Manhattan' website for Mercedes-Benz C-Class Sedans, targeting young affluent urban couples between 25 and 35 years old. Use the 'Modern Luxury | Manhattan' online ad specs as a reference for the layout described in this PDF. Include the size of the ad in the response.

The provided Mercedes-Benz sedan advertisements effectively utilize several creative elements that contribute to their compelling and impactful nature. Here are five key strategies employed across these ads:

1. Striking Visual Imagery: The ads feature stunning, high-quality photography that showcases the vehicles in dynamic and aspirational settings. The use of motion blur, lighting effects, and dramatic angles creates a sense of movement and energy, capturing the performance and luxury of the Mercedes-Benz brand. The cars are prominently displayed, allowing viewers to appreciate their sleek designs and premium aesthetics.

2. Emphasis on Innovation and Perfection: The messaging and copywriting consistently reinforce Mercedes-Benz's commitment to innovation and the pursuit of perfection. Phrases like "The only thing that's not relative. Perfection," "Glam turismo," and "Das Beste kennt keine Alternative" (The best knows no alternative) position the brand as a leader in automotive excellence and cutting-edge technology.

3. Consistent Branding and Typography: The ads maintain a strong brand identity through the consistent use of the Mercedes-Benz logo, color palette, and typography. The iconic three-pointed star and the brand's signature tagline, "The best or nothing," are prominently featured, reinforcing brand recognition and association with luxury and quality. The clean, modern typography complements the brand's sophisticated image.

4. Evocative Copywriting: The ads employ evocative and aspirational copywriting that appeals to the target audience's desires for luxury, performance, and exclusivity. Phrases like "A class ahead," "The all new C-Class Coupé is more than just a head turner," and "DISTRONIC PLUS. Gefahren minus" (DISTRONIC PLUS. Dangers minus) highlight the vehicles' advanced features and capabilities, while also tapping into emotional drivers.

5. Attention to Detail and Craftsmanship: The ads showcase the vehicles' meticulous attention to detail and craftsmanship, reflecting Mercedes-Benz's commitment to quality. Close-up shots highlight the sleek lines, premium materials, and intricate design elements, reinforcing the brand's reputation for exceptional engineering and craftsmanship.

By effectively combining these creative elements, the Mercedes-Benz ads create a compelling and aspirational brand experience that aligns with the company's positioning as a leader in luxury and innovation. The ads effectively communicate the brand's values and the vehicles' desirable attributes, appealing to the target audience's desires and reinforcing Mercedes-Benz's premium brand identity.
```

### 4a. Summerize Contents of a Text File

Upload (1) TXT file:

- [mercedes_benz_info.txt](mercedes_benz_ads/mercedes_benz_info.txt)

Prompt:

```text
Provides a concise summary of this document.
```

### 4b. Query Data in CSV File

The model cannot correctly add up large volumes of numbers. It will provide an answer, but that answer is likely not correct. This prompt writes a program that can correctly calculate the answer.

Source of dataset: [https://www.kaggle.com/datasets/yasserh/advertising-sales-dataset](https://www.kaggle.com/datasets/yasserh/advertising-sales-dataset)

Upload (1) CSV file:

- [Advertising_Budget_and_Sales.csv](/csv_data/Advertising_Budget_and_Sales.csv)

Prompts:

```text
Based on the Advertising Budget and Sales CSV file, write a Python program to calculate the total sales. Use the Pandas package.
```

```text
Based on the Advertising Budget and Sales CSV file, write a Java program to calculate the total sales.
```

```text
Based on the Advertising Budget and Sales CSV file, write a Node.js program to calculate the grand total of all TV, radio, and newspaper ad budgets. Use the csv-parser package.
```

```text
Based on the Advertising Budget and Sales CSV file, write a Python program to calculate the ratio of the grand total of TV, radio, and newspaper ad budgets to sales for ID 100. Use the Pandas package.
```

### 5. Generate New Creative Concepts Based on Analysis of a Creative Brief 

Analyze a creative brief for PayPal and generate three ideas for new ads. Output a structured response as well-formatted JSON that an be easily ingested into a downstream system.

Upload (1) WebP file:

- [paypal-creative-brief-1-2048.webp](/paypal_creative_brief/paypal-creative-brief-1-2048.webp)

Prompt:

```text
You are a Creative Director for a leading advertising agency. Based on the following Creative Brief for PayPal, develop three compelling online digital advertisements. In your response, include a unique ad ID (UUID), headline, ad copy, call to action, and description of imagery for each. The ad copy should be 20 words or less.

Format the response as a series of JSON objects according to the template below.

{
    "advertisements": [
        {
            "id": "",
            "headline": "",
            "ad_copy": "",
            "call_to_action": "",
            "imagery": ""
        },
        {
            "id": "",
            "headline": "",
            "ad_copy": "",
            "call_to_action": "",
            "imagery": ""
        },
        {
            "id": "",
            "headline": "",
            "ad_copy": "",
            "call_to_action": "",
            "imagery": ""
        }
    ]
}
```

### 6. Generate a Layout Design for an Ad Based on Generated Creative Concepts

As a Graphic Designer, describe the layout of the advertisement, based on the content generated in example 5, above.

Upload (1) WebP file:

- [paypal-creative-brief-1-2048.webp](/paypal_creative_brief/paypal-creative-brief-1-2048.webp)

Prompt:

```text
You are a talented Graphic Designer for a leading advertising agency. Based on the following headline, ad copy, call to action, and description of imagery, describe the design for a compelling online digital advertisement. The advertisement should be designed in a tall, portrait format, with a width of 300 pixels and a height of 600 pixels. The Creative Brief for PayPal is included for reference.

{
    "id": "3e67f83a-5f3e-4b4f-8653-b1c3c6b7147e",
    "headline": "Your Money, Your Control",
    "ad_copy": "Take charge of your finances with PayPal. No complexities, just convenience.",
    "call_to_action": "Download the App",
    "imagery": "The ad depicts a teenager's hand holding a smartphone with the PayPal app open, showcasing the ease of managing money on the go."
}
```

### 7. Generate Ads Programmatically Based on Generated Creative Concepts

Generate a Python program, which uses the [PILLOW](https://pypi.org/project/pillow/) package to create a compelling online digital advertisement based on the content generated in example 5, above.

Upload (1) WebP file:

- [paypal-creative-brief-1-2048.webp](/paypal_creative_brief/paypal-creative-brief-1-2048.webp)

Prompt:

```text
You are a talented Graphic Designer and Python developer for a leading advertising agency. Write a Python program using the PILLOW package to create a compelling online digital advertisement based on the following headline, ad copy, call to action, and imagery description. The advertisement should be designed in a tall, portrait format, with a width of 400 pixels and a height of 600 pixels. The Creative Brief for PayPal is included for reference.

{
    "id": "3e67f83a-5f3e-4b4f-8653-b1c3c6b7147e",
    "headline": "Your Money, Your Control",
    "ad_copy": "Take charge of your finances with PayPal. No complexities, just convenience.",
    "call_to_action": "Download the App",
    "imagery": "The ad depicts a teenager's hand holding a smartphone with the PayPal app open, showcasing the ease of managing money on the go."
}
```

#### Examples Ads Built from Generated Python Program

All images were created on Amazon Bedrock using the recently announced Amazon Titan Image Generator G1 foundation model.

![Ads](/paypal_creative_brief/nine_up_ads.png)

## Example Response from Foundation Model

Example response body from Claude 3 Sonnet model on Bedrock. Note that responses also include input and output token counts, which are useful for estimating costs.

```json
{
  "id": "msg_017ntpirxuSGXfJMN1afGAXR",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Here is a concise and effective positive prompt for analyzing the common creative elements across these Mercedes-Benz print advertisements, some in English and some in German:\n\n\"Examine the visual design, messaging, and marketing approaches used across these Mercedes-Benz vehicle print ads. Identify recurring creative strategies, themes, and techniques employed to promote the brand's luxury automotive offerings to potential customers. Discuss how the ads aim to create desire and appeal through their imagery, copy, and overall artistic execution, while being mindful to objectively analyze the marketing without subjective judgement or bias.\""
    }
  ],
  "model": "claude-3-sonnet-28k-20240229",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 1662,
    "output_tokens": 124
  }
}
```

```json
{
  "id": "msg_01A6TxmM18XGTFJ6vMk7xnCg",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "These Mercedes-Benz print advertisements showcase several compelling creative elements that contribute to their effectiveness in promoting the brand's luxury sedans:\n\n1. Striking visual imagery: All four ads feature high-quality, dramatic photography that showcases the vehicles in stylish and aspirational settings. The use of dynamic lighting, motion blur effects, and urban/futuristic backdrops creates a sense of sophistication and excitement around the cars.\n\n2. Impactful copywriting: The ads employ concise, evocative taglines and headlines that reinforce Mercedes-Benz's brand positioning around perfection, innovation, and superior performance. Examples include \"The only thing that's not relative. Perfection.\" and \"Glam turismo.\" The German copy like \"Das Beste kennt keine Alternative\" also conveys a premium, uncompromising message.\n\n3. Consistent branding elements: The iconic Mercedes-Benz tri-star logo is prominently featured in each ad, along with the brand's signature typography and color palette of silver, black, and blue tones. This strong brand identity ties the campaigns together cohesively.\n\n4. Focus on design and styling: The ads highlight the sleek, modern designs of the featured C-Class and S-Class models through artistic angles and attention to detail on elements like the sculpted bodies, alloy wheels, and LED lighting accents.\n\n5. Aspirational lifestyle positioning: While showcasing the vehicles themselves, the ads also subtly convey an aspirational, luxurious lifestyle through the sophisticated urban settings, use of motion and speed, and overall premium aesthetic. This aligns with Mercedes-Benz's high-end brand identity.\n\nOverall, these print ads leverage striking visuals, compelling copy, consistent branding, design-focused vehicle depictions, and an aspirational luxury positioning to create a cohesive, impactful campaign that effectively promotes Mercedes-Benz's premium sedan offerings."
    }
  ],
  "model": "claude-3-sonnet-28k-20240229",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 1743,
    "output_tokens": 417
  }
}
```

---

_The contents of this repository represent my viewpoints and not of my past or current employers, including Amazon Web Services (AWS). All third-party libraries, modules, plugins, and SDKs are the property of their respective owners._
