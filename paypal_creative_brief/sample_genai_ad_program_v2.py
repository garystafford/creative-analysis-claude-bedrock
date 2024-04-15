from PIL import Image, ImageDraw, ImageFont

for idx, generated_image in enumerate(
    [
        # "generated_images/paypal_creative_brief/paypal_generated_image_v1.png",
        # "generated_images/paypal_creative_brief/paypal_generated_image_v2.png",
        # "pgenerated_images/aypal_creative_brief/paypal_generated_image_v3.png",
        "generated_images/paypal_creative_brief/paypal_generated_image_v4.png",
        "generated_images/paypal_creative_brief/paypal_generated_image_v5.png",
        "generated_images/paypal_creative_brief/paypal_generated_image_v6.png",
    ]
):
    # Create a new image with the desired dimensions
    width, height = 400, 500
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)

    # Load fonts
    headline_font = ImageFont.truetype(
     
        "/Users/garystafford/Library/Fonts/Montserrat-Bold.ttf", 38
    )
    copy_font = ImageFont.truetype(
        "/Users/garystafford/Library/Fonts/Montserrat-Regular.ttf", 20
    )
    cta_font = ImageFont.truetype(
        "/Users/garystafford/Library/Fonts/Montserrat-SemiBold.ttf", 20
    )

    # Headline
    headline = "Join PayPal Today"

    headline_width, headline_height = draw.textbbox((0, 0), headline, font=headline_font)[
        2:
    ]
    headline_x = (width - headline_width) / 2
    headline_y = 20
    draw.text((headline_x, headline_y), headline, font=headline_font, fill="#7C15FF")

    # Ad Copy
    ad_copy = (
        "     Whether it's your allowance\n               or a part-time gig,\nPayPal keeps your money moving."
    )
    copy_width, copy_height = draw.textbbox((0, 0), ad_copy, font=copy_font)[2:]
    copy_x = (width - copy_width) / 2
    copy_y = headline_y + headline_height + 10
    draw.text((copy_x, copy_y), ad_copy, font=copy_font, fill="#000000")

    # Call to Action
    cta = "Join PayPal Today"
    cta_width, cta_height = draw.textbbox((0, 0), cta, font=cta_font)[2:]
    cta_x = (width - cta_width) / 2
    cta_y = height - cta_height - 30
    draw.rectangle(
        (cta_x - 10, cta_y - 10, cta_x + cta_width + 10, cta_y + cta_height + 10),
        fill="#7C15FF",
        outline="#7C15FF",
    )
    draw.text((cta_x, cta_y), cta, font=cta_font, fill="white")

    # Imagery
    image = Image.open(generated_image)
    image = image.resize((400, 240))
    image_x = (width - image.width) / 2
    image_y = copy_y + copy_height + 20
    img.paste(image, (int(image_x), int(image_y)))

    # Save the image
    img.save(f"generated_ads/paypal_generated_ad_v2_{idx + 1}.jpg")
