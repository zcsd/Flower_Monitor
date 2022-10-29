from PIL import ImageDraw
from datetime import datetime
from io import BytesIO

def draw_date_text(pil_image, font):
    draw = ImageDraw.Draw(pil_image)
    now = datetime.now()
    date_str = now.strftime("%Y/%m/%d %H:%M")
    draw.text((30, 30), date_str, font=font, fill =(0, 255, 0))
    return pil_image

def pil_to_bytes(pil_image):
    image_buf = BytesIO()
    pil_image.save(image_buf, format='JPEG')
    image_buf.seek(0)

    return image_buf
