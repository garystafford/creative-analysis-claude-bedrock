from PIL import Image, ImageDraw, ImageFont

for idx, generated_image in enumerate(
    [
        "generated_images/paypal_generated_image_v1.png",
        "generated_images/paypal_generated_image_v2.png",
        "generated_images/paypal_generated_image_v3.png",
        # "generated_images/paypal_generated_image_v4.png",
        # "generated_images/paypal_generated_image_v5.png",
        # "generated_images/paypal_generated_image_v6.png",
    ]
):
    # Create a new image with the desired dimensions
    width, height = 400, 500
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)

    # Load fonts
    headline_font = ImageFont.truetype(
        "/Users/garystafford/Library/Fonts/Montserrat-Bold.ttf", 36
    )
    copy_font = ImageFont.truetype(
        "/Users/garystafford/Library/Fonts/Montserrat-Regular.ttf", 18
    )
    cta_font = ImageFont.truetype(
        "/Users/garystafford/Library/Fonts/Montserrat-SemiBold.ttf", 20
    )

    # Headline
    headline = "Your Money,\nYour Control"

    headline_width, headline_height = draw.textbbox((0, 0), headline, font=headline_font)[
        2:
    ]
    headline_x = (width - headline_width) / 2
    headline_y = 20
    draw.text((headline_x, headline_y), headline, font=headline_font, fill="#0C9C00")

    # Ad Copy
    ad_copy = (
        "Take charge of your finances with PayPal.\n     No complexities, just convenience."
    )
    copy_width, copy_height = draw.textbbox((0, 0), ad_copy, font=copy_font)[2:]
    copy_x = (width - copy_width) / 2
    copy_y = headline_y + headline_height + 20
    draw.text((copy_x, copy_y), ad_copy, font=copy_font, fill="#000000")

    # Call to Action
    cta = "Download the App"
    cta_width, cta_height = draw.textbbox((0, 0), cta, font=cta_font)[2:]
    cta_x = (width - cta_width) / 2
    cta_y = height - cta_height - 30
    draw.rectangle(
        (cta_x - 10, cta_y - 10, cta_x + cta_width + 10, cta_y + cta_height + 10),
        fill="#0C9C00",
        outline="#0C9C00",
    )
    draw.text((cta_x, cta_y), cta, font=cta_font, fill="white")

    # Imagery
    image = Image.open(generated_image)
    image = image.resize((400, 240))
    image_x = (width - image.width) / 2
    image_y = copy_y + copy_height + 20
    img.paste(image, (int(image_x), int(image_y)))

    # Save the image
    img.save(f"generated_ads/paypal_generated_ad_v1_{idx + 1}.jpg")
