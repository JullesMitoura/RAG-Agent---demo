import streamlit as st
from PIL import Image
import os

def process():
    dir_imgs = os.path.join(os.getcwd(), 'imgs')
    st.header("Process Informations")
    st.markdown("---")
    image = Image.open(os.path.join(dir_imgs, "TEG.png"))
    st.image(image, use_column_width=True)
  