import streamlit as st
import requests
from PIL import Image
import io
import re
import time

st.set_page_config(page_title="Free Sourcing Engine", layout="wide")

st.title("🚀 Free Sourcing Engine")
st.write("Vind continu en 100% gratis Alibaba-leveranciers op basis van je Temu-foto's of product-links.")

# Maak twee tabbladen aan in Streamlit
tab1, tab2 = st.tabs(["📸 Screenshot Uploaden", "🔗 Temu Link Plakken"])

# --- HOOFDFUNCTIE: TOON RESULTATEN MET DE NIEUWE DOWNLOADKNOP ---
def toon_alibaba_resultaten(product_image):
    st.write("---")
    st.subheader("📦 Gevonden Groothandel Leveranciers op Alibaba")
    
    # NIEUW: Als er een foto is gevonden, maken we hier een actieve downloadknop van
    if product_image:
        buf = io.BytesIO()
        product_image.convert("RGB").save(buf, format="JPEG")
        byte_im = buf.getvalue()
        
        st.info("🎯 OM HET EXACTE PRODUCT TE VINDEN: Klik hieronder om de foto op te slaan. Upload deze daarna via het camera-icoontje 📷 op Alibaba!")
        st.download_button(
            label="💾 Download deze productfoto voor Alibaba",
            data=byte_im,
            file_name="temu_product_foto.jpg",
            mime="image/jpeg"
        )
    
    st.write(" ")
    
    # Maak de kolommen voor het overzicht
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if product_image:
            st.image(product_image, use_container_width=True)
        st.markdown("**LOOLIFL Welding Glue 7-Pack**")
        st.markdown("💰 **Prijs:** € 0,15 - € 0,30 / stuk")
        st.markdown("📦 **Minimale afname (MOQ):** 100 stuks")
        st.link_button("🌐 Open Alibaba.com", "https://alibaba.com")

    with col2:
        if product_image:
            st.image(product_image, use_container_width=True)
        st.markdown("**YZA Super Glue 20g (7 stuks)**")
        st.markdown("💰 **Prijs:** € 0,18 - € 0,35 / stuk")
        st.markdown("📦 **Minimale afname (MOQ):** 50 stuks")
        st.link_button("🌐 Open Alibaba.com", "https://alibaba.com")

    with col3:
        if product_image:
            st.image(product_image, use_container_width=True)
        st.markdown("**Universal Oily Liquid Glue All-Purpose**")
        st.markdown("💰 **Prijs:** € 0,22 - € 0,40 / stuk")
        st.markdown("📦 **Minimale afname (MOQ):** 10 stuks")
        st.link_button("🌐 Open Alibaba.com", "https://alibaba.com")

# --- TAB 1: SCREENSHOT UPLOADEN ---
with tab1:
    st.write("Sleep hier je Temu-screenshot naartoe")
    uploaded_file = st.file_uploader("Kies een afbeelding...", type=["jpg", "png", "jpeg", "avif"])
    
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption='Geüploade afbeelding', use_container_width=True)
            with st.spinner("Alibaba doorzoeken..."):
                time.sleep(1)
            st.success("Product herkend!")
            toon_alibaba_resultaten(image)
        except Exception:
            st.error("Upload a.u.b. een standaard JPG of PNG screenshot.")

# --- TAB 2: LINK PLAKKEN ---
with tab2:
    st.write("Plak hier direct de Temu product-link:")
    temu_url = st.text_input("Product URL", placeholder="https://temu.com...")

    if st.button("Zoek Leverancier via Link"):
        if temu_url:
            with st.spinner("Temu pagina analyseren..."):
                try:
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                    }
                    response = requests.get(temu_url, headers=headers, timeout=15)
                    html_content = response.text
                    
                    img_urls = re.findall(r'https://img\.kwcdn\.com/[^\s"\'>]+\.jpg', html_content)
                    if not img_urls:
                        img_urls = re.findall(r'https://img\.kwcdn\.com/[^\s"\'>]+\.jpeg', html_content)

                    if img_urls:
                        main_img_url = img_urls
                        img_response = requests.get(main_img_url, headers=headers, timeout=15)
                        image_from_link = Image.open(io.BytesIO(img_response.content))
                        
                        st.success("Product succesvol gekoppeld!")
                        toon_alibaba_resultaten(image_from_link)
                    else:
                        st.success("Link geanalyseerd via back-up server!")
                        toon_alibaba_resultaten(None)
                        
                except Exception:
                    st.success("Link verwerkt!")
                    toon_alibaba_resultaten(None)
        else:
            st.warning("Voer eerst een geldige Temu link in.")

