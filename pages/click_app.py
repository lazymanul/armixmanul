import streamlit as st
from PIL import ImageFont, Image, ImageDraw
from streamlit_image_select import image_select

fsize = 250
W = 320
H = 320
font = ImageFont.truetype("assets/NotoSansCJK-Regular.ttc", fsize)

def gen_character_image(character, W, H, font):
    """Generates image for given character    
    """
    image = Image.new('L', (W, H), color=255)
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), character, font=font)
    draw.text((w/1.5,h/2), character, anchor="mm", font=font)    
    return image


img = image_select(
    label="Select a character",
    images=[
        gen_character_image('科', W, H, font),
        gen_character_image('秩', W, H, font),
        gen_character_image('秣', W, H, font),
    ],    
    use_container_width = False,
    return_value='index'
)
st.write(img)
