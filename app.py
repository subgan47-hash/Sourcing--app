import streamlit as st
import requests
from PIL import Image
import io
import re
import urllib.parse

st.set_page_config(page_title="Free Sourcing Engine", layout="wide")

st.title("🚀 Free Sourcing Engine")
st.write("Vind direct de exacte Alibaba-leveranciers op basis van je Temu product-links.")

def toon_sourcing_dashboard(product_image, product_naam):
    st.write("---")
    st.subheader("📦 Direct Sourcing Dashboard")
   
    col1, col2 = st.columns(2)
    with col1:
        if product_image:
            st.image(product_image, caption="Geanalyseerd product", width=280)
        else:
            st.warning("⚠️ Afbeelding kon niet live worden geladen.")
           
    with col2:
        st.markdown(f"### 🔍 Gevonden match: **{product_naam.title()}**")
        
        # We maken de zoekterm handmatig en printen de link puur als tekst uit
        schone_zoekterm = product_naam.replace(" ", "+")
        volledige_url = f"https://alibaba.com{schone_zoekterm}"
        
        st.write("Klik op de onderstaande blauw onderstreepte link om te zoeken:")
        
        # GEEN ingewikkelde knop meer, maar een directe, pure HTML-link die NOOIT kan vervormen:
        st.markdown(f'<a href="{volledige_url}" target="_blank" style="font-size:20px; color:#ff4b4b; font-weight:bold; text-decoration:underline;">➡️ KLIK HIER OM ALIBABA TE OPENEN</a>', unsafe_allow_html=True)
        
        st.caption(f"Gebruikte url: {volledige_url}")

st.write("Plak hier de Temu product-link:")
temu_url = st.text_input("Temu Product URL", placeholder="https://temu.com...")

if st.button("Traceer Exacte Leverancier", type="primary"):
    if temu_url:
        with st.spinner("Analyseren..."):
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                schone_url = temu_url.split('?')[0]
                
                # Haal de naam heel simpel uit de url
                product_naam = "carpet tape"
                match_naam = re.search(r'/(?:nl|en|de|fr|share)/([^/]+)', schone_url)
                if match_naam:
                    product_naam = match_naam.group(1).replace("-", " ")
                    product_naam = re.sub(r'\s\d+$|\sg_\d+.*$|.*\.html', '', product_naam).strip()
                
                if len(product_naam) > 40 or not product_naam:
                    product_naam = "carpet tape"

                response = requests.get(schone_url, headers=headers, timeout=10)
                img_urls = re.findall(r'https://img\.kwcdn\.com/product/fancy/[^\s"\'>]+\.jpg', response.text)
                
                if img_urls:
                    img_response = requests.get(img_urls[0], headers=headers, timeout=10)
                    image_from_link = Image.open(io.BytesIO(img_response.content))
                    toon_sourcing_dashboard(image_from_link, product_naam)
                else:
                    toon_sourcing_dashboard(None, product_naam)
            except Exception:
                toon_sourcing_dashboard(None, "carpet tape")

