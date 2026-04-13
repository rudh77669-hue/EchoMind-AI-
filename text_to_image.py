from PIL import Image, ImageDraw, ImageFont
import textwrap

def text_to_image(user_input):
    if not user_input:
        return "No text Provided"
    
    # Image size
    width, height = 1200, 600
    
    # 🎨 Gradient background
    image = Image.new("RGB", (width, height), "#1e3c72")
    for y in range(height):
        r = 30 + int((y/height)*40)
        g = 60 + int((y/height)*50)
        b = 114 + int((y/height)*70)
        for x in range(width):
            image.putpixel((x, y), (r, g, b))
    
    draw = ImageDraw.Draw(image)

    # ✅ Font selection (English / Hindi)
    if all(ord(c) < 128 for c in user_input):  
        font_path = "C:/Users/rudh7/OneDrive/Desktop/Echomind Ai+/Noto_Sans,Noto_Sans_Devanagari/Noto_Sans/static/NotoSans-Regular.ttf"
    else:
        font_path = "C:/Users/rudh7/OneDrive/Desktop/Echomind Ai+/Noto_Sans,Noto_Sans_Devanagari/Noto_Sans_Devanagari/static/NotoSansDevanagari-Regular.ttf"
        
    try:
        # Dynamic font size fit
        font_size = 60
        while font_size > 10:
            font = ImageFont.truetype(font_path, font_size)
            bbox = draw.textbbox((0, 0), user_input, font=font)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
            if text_width <= width - 100 and text_height <= height - 100:
                break
            font_size -= 2

        # Wrap text
        wrapped_text = textwrap.fill(user_input, width=20)
        bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, spacing=6)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        text_x = (width - text_width) / 2
        text_y = (height - text_height) / 2

        # 📦 Rounded rectangle background for text
        padding = 30
        rect_x1, rect_y1 = text_x - padding, text_y - padding
        rect_x2, rect_y2 = text_x + text_width + padding, text_y + text_height + padding
        draw.rounded_rectangle([rect_x1, rect_y1, rect_x2, rect_y2], radius=25, fill=(255,255,255,230))

        # ✨ Drop shadow text
        shadow_offset = 3
        draw.multiline_text((text_x+shadow_offset, text_y+shadow_offset), wrapped_text, font=font, fill="gray", spacing=6)

        # Main text
        draw.multiline_text((text_x, text_y), wrapped_text, fill="black", font=font, spacing=6)

        # Save
        output_path = "text_to_image.png"
        image.save(output_path)
        image.show()
        return output_path

    except IOError:
        return "⚠️ Font file not found", 500
