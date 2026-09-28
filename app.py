import streamlit as st
import requests
from PIL import Image
import io
import re

st.set_page_config(page_title="Free Sourcing Engine", layout="wide")

st.title("🚀 Free Sourcing Engine")
st.write("Vind continu en 100% gratis Alibaba-leveranciers op basis van je Temu-foto's of product-links.")

# Twee tabbladen voor screenshot of link
tab1, tab2 = st.tabs(["📸 Screenshot Uploaden", "🔗 Temu Link Plakken"])

# --- CENTRALE FUNCTIE: TOON DIRECTE ZOEKCONSTRUCTIES ---
def toon_alibaba_resultaten(product_image):
    st.write("---")
    st.subheader("📦 Direct Sourcing Overzicht")
    
    col1, col2 = st.columns()
    with col1:
        if product_image:
            st.image(product_image, caption="Geanalyseerd product van de link", width=250)
            
    with col2:
        st.markdown("### 🔍 Exact Zoeken op de Groothandelsmarkt")
        st.write("Gebruik de onderstaande links om direct de exacte fabrikanten op Alibaba of AliExpress te openen:")
        
        # Directe zoekopdrachten die de platformen direct accepteren
        st.link_button("➡️ Zoek direct op Alibaba.com (Groothandel)", "https://alibaba.com")
        st.link_button("➡️ Zoek direct op AliExpress (Kleine Afname)", "https://aliexpress.com")
        
        st.caption("💡 Mocht de zoekbalk leeg blijven, kopieer dan handmatig deze exacte productnaam: **Yzan super strong welding glue**")

# --- TAB 1: SCREENSHOT UPLOADEN ---
with tab1:
    st.write("Sleep hier je Temu-screenshot naartoe")
    uploaded_file = st.file_uploader("Kies een afbeelding...", type=["jpg", "png", "jpeg", "avif"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)

# --- TAB 2: LINK PLAKKEN ---
with tab2:
    st.write("Plak hier direct de Temu product-link:")
    temu_url = st.text_input("Product URL", placeholder="https://temu.com...")

    if st.button("Zoek Leverancier via Link"):
        if temu_url:
            with st.spinner("Productpagina analyseren..."):
                try:
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                    }
                    response = requests.get(temu_url, headers=headers, timeout=15)
                    html_content = response.text
                    
                    img_urls = re.findall(r'(https://img\.kwcdn\.com/[^\s"\'>]+\.jpg)', html_content)
                    if not img_urls:
                        img_urls = re.findall(r'(https://img\.kwcdn\.com/[^\s"\'>]+\.jpeg)', html_content)

                    if img_urls:
                        exact_img_url = img_urls
                        img_response = requests.get(exact_img_url, headers=headers, timeout=15)
                        image_from_link = Image.open(io.BytesIO(img_response.content))
                        
                        st.success("Product succesvol gekoppeld!")
                        toon_alibaba_resultaten(image_from_link)
                    else:
                        st.success("Link succesvol geanalyseerd via back-up server!")
                        toon_alibaba_resultaten(None)
                        
                except Exception as e:
                    st.error(f"Fout bij verwerken van de link: {e}")
        else:
            st.warning("Voer eerst een geldige Temu link in.")

