# Author: Gary A. Stafford
# Modified: 2024-10-25
# Build sample ads 9-12 for PayPal using generated images 9-12
# Requires https://fonts.google.com/specimen/Montserrat to be installed

from PIL import Image, ImageDraw, ImageFont

# Change to your font path!
FONT_PATH = "~/Library/Fonts"


def main() -> None:
    headline_font = ImageFont.truetype(f"{FONT_PATH}/Montserrat-Bold.ttf", 27)
    copy_font = ImageFont.truetype(f"{FONT_PATH}/Montserrat-Regular.ttf", 20)
    cta_font = ImageFont.truetype(f"{FONT_PATH}/Montserrat-SemiBold.ttf", 20)
<<<<<<< Updated upstream

    for idx, generated_image in enumerate(
        [
            "generated_images/paypal_generated_image_v9.png",
            "generated_images/paypal_generated_image_v10.png",
            "generated_images/paypal_generated_image_v11.png",
            "generated_images/paypal_generated_image_v12.png",
        ]
    ):
        # Create a new image with the desired dimensions
        width, height = 400, 500
        img = Image.new("RGB", (width, height), color="white")
        draw = ImageDraw.Draw(img)

        # Headline
        headline = "Freedom to Earn, Anytime"

        headline_width, headline_height = draw.textbbox(
            (0, 0), headline, font=headline_font
        )[2:]
        headline_x = (width - headline_width) / 2
        headline_y = 20
        draw.text(
            (headline_x, headline_y),
            headline,
            font=headline_font,
            fill="#157FFF",
            align="center",
        )

        # Ad Copy
        ad_copy = "Unlock financial independence\nwith PayPal's virtual wallet.\nReceive money whenever, wherever."
        copy_width, copy_height = draw.textbbox((0, 0), ad_copy, font=copy_font)[2:]
        copy_x = (width - copy_width) / 2
        copy_y = headline_y + headline_height + 10
        draw.text(
            (copy_x, copy_y), ad_copy, font=copy_font, fill="#000000", align="center"
        )

        # Call to Action
        cta = "Sign Up Now"
        cta_width, cta_height = draw.textbbox((0, 0), cta, font=cta_font)[2:]
        cta_x = (width - cta_width) / 2
        cta_y = height - cta_height - 30
        draw.rectangle(
            (cta_x - 10, cta_y - 10, cta_x + cta_width + 10, cta_y + cta_height + 10),
            fill="#157FFF",
            outline="#157FFF",
        )
        draw.text((cta_x, cta_y), cta, font=cta_font, fill="white")

=======
    width, height = 400, 500
    headline = "Freedom to Earn, Anytime"
    ad_copy = "Unlock financial independence\nwith PayPal's virtual wallet.\nReceive money whenever, wherever."
    cta = "Sign Up Now"
    primary_color = "#157FFF"
    secondary_color = "#000000"

    for idx, generated_image in enumerate(
        [
            "generated_images/paypal_generated_image_v9.png",
            "generated_images/paypal_generated_image_v10.png",
            "generated_images/paypal_generated_image_v11.png",
            "generated_images/paypal_generated_image_v12.png",
        ]
    ):
        # Create a new image with the desired dimensions
        img = Image.new("RGB", (width, height), color="white")
        draw = ImageDraw.Draw(img)

        # Headline
        headline_width, headline_height = draw.textbbox(
            (0, 0), headline, font=headline_font
        )[2:]
        headline_x = (width - headline_width) / 2
        headline_y = 20
        draw.text(
            (headline_x, headline_y),
            headline,
            font=headline_font,
            fill=primary_color,
            align="center",
        )

        # Ad Copy
        copy_width, copy_height = draw.textbbox((0, 0), ad_copy, font=copy_font)[2:]
        copy_x = (width - copy_width) / 2
        copy_y = headline_y + headline_height + 10
        draw.text(
            (copy_x, copy_y), ad_copy, font=copy_font, fill=secondary_color, align="center"
        )

        # Call to Action
        cta_width, cta_height = draw.textbbox((0, 0), cta, font=cta_font)[2:]
        cta_x = (width - cta_width) / 2
        cta_y = height - cta_height - 30
        draw.rectangle(
            (cta_x - 10, cta_y - 10, cta_x + cta_width + 10, cta_y + cta_height + 10),
            fill=primary_color,
            outline=primary_color,
        )
        draw.text((cta_x, cta_y), cta, font=cta_font, fill="white")

>>>>>>> Stashed changes
        # Imagery
        image = Image.open(generated_image)
        image = image.resize((400, 250))
        image_x = (width - image.width) / 2
        image_y = copy_y + copy_height + 25
        img.paste(image, (int(image_x), int(image_y)))

        # Border for entire image
        draw.rectangle([0, 0, width - 1, height - 1], outline="#999999", width=1)

        # Save the image
        image_path = f"generated_ads/paypal_generated_ad_v3_{idx + 1}.png"
        img.save(image_path, format="PNG")

        # Notify user
        print(f"Generated ad: {image_path}")

<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
if __name__ == "__main__":
    main()
