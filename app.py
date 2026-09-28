import streamlit as st
import requests
from PIL import Image
import io
import re
import urllib.parse

st.set_page_config(page_title="Free Sourcing Engine", layout="wide")

st.title("🚀 Free Sourcing Engine")
st.write("Vind continu en 100% gratis leveranciers op basis van je Temu-foto's of product-links.")

# Twee tabbladen voor screenshot of link
tab1, tab2 = st.tabs(["📸 Screenshot Uploaden", "🔗 Temu Link Plakken"])

# --- DE AUTOMATISCHE GOOGLE LENS METHODE ---
def start_google_lens_sourcing(image_url, product_image):
    st.write("---")
    st.subheader("📦 Gevonden Groothandel Leveranciers")
    
    if image_url:
        # We zetten de afbeeldingslink om naar een formaat dat Google begrijpt
        encoded_url = urllib.parse.quote_plus(image_url)
        google_lens_url = f"https://lens.google.com/uploadbyurl?url={encoded_url}"
        
        st.success("🎯 Product succesvol gekoppeld aan de visuele zoekmachine!")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            if product_image:
                st.image(product_image, caption="Geanalyseerd product van de link", width=250)
        with col2:
            st.markdown("### Vind de exacte fabriek")
            st.write("Klik op de onderstaande knop. Google scant de foto direct over heel Alibaba en AliExpress om exact dezelfde verpakking te vinden.")
            # Deze knop opent DIRECT de live Google Lens pagina met de exacte matches
            st.link_button("🔍 VIND EXACTE LEVERANCIERS VIA GOOGLE LENS", google_lens_url)
    else:
        st.error("Kon geen automatische zoeklink genereren.")

# --- TAB 1: SCREENSHOT UPLOADEN ---
with tab1:
    st.write("Sleep hier je Temu-screenshot naartoe")
    uploaded_file = st.file_uploader("Kies een afbeelding...", type=["jpg", "png", "jpeg", "avif"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)

# --- TAB 2: LINK PLAKKEN (Werkt automatisch voor elk product!) ---
with tab2:
    st.write("Plak hier direct de Temu product-link:")
    temu_url = st.text_input("Product URL", placeholder="https://temu.com...")

    if st.button("Zoek Leverancier via Link"):
        if temu_url:
            with st.spinner("Productpagina analyseren en foto isoleren..."):
                try:
                    # We gebruiken headers om blokkades van Temu te voorkomen
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                    }
                    response = requests.get(temu_url, headers=headers, timeout=15)
                    html_content = response.text
                    
                    # We zoeken de unieke afbeeldings-URL op de Temu pagina
                    img_urls = re.findall(r'(https://img\.kwcdn\.com/[^\s"\'>]+\.jpg)', html_content)
                    if not img_urls:
                        img_urls = re.findall(r'(https://img\.kwcdn\.com/[^\s"\'>]+\.jpeg)', html_content)

                    if img_urls:
                        exact_img_url = img_urls[0]
                        
                        # Download de foto voor de weergave in de app
                        img_response = requests.get(exact_img_url, headers=headers, timeout=15)
                        image_from_link = Image.open(io.BytesIO(img_response.content))
                        
                        # Start de Google Lens module met de echte afbeeldingslink
                        start_google_lens_sourcing(exact_img_url, image_from_link)
                    else:
                        st.error("Kon de productfoto niet automatisch uitlezen. Gebruik de screenshot module.")
                        
                except Exception as e:
                    st.error(f"Fout bij verwerken van de link: {e}")
        else:
            st.warning("Voer eerst een geldige Temu link in.")

