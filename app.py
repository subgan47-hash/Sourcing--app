import streamlit as st
import requests
from PIL import Image
import io
import re

st.title("🚀 Free Sourcing Engine")
st.write("Vind continu en 100% gratis Alibaba-leveranciers op basis van je Temu-foto's of product-links.")

# Maak twee tabbladen aan in Streamlit
tab1, tab2 = st.tabs(["📸 Screenshot Uploaden", "🔗 Temu Link Plakken"])

# --- TAB 1: SCREENSHOT UPLOADEN ---
with tab1:
    st.write("Sleep hier je Temu-screenshot naartoe")
    uploaded_file = st.file_uploader("Kies een afbeelding...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Geüploade afbeelding', use_container_width=True)
        st.info("Hier kun je jouw bestaande functie aanroepen om te zoeken op Alibaba!")

# --- TAB 2: LINK PLAKKEN ---
with tab2:
    st.write("Plak hier direct de Temu product-link:")
    temu_url = st.text_input("Product URL", placeholder="https://temu.com...")

    if st.button("Zoek Leverancier via Link"):
        if temu_url:
            with st.spinner("Temu pagina analyseren..."):
                try:
                    # We bootsen een normale browser na zodat Temu ons niet blokkeert
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                    }
                    response = requests.get(temu_url, headers=headers, timeout=15)
                    html_content = response.text
                    
                    # We zoeken in de code naar de link van de afbeelding
                    img_urls = re.findall(r'https://img\.kwcdn\.com/[^\s"\'>]+\.jpg', html_content)
                    
                    if not img_urls:
                        img_urls = re.findall(r'https://img\.kwcdn\.com/[^\s"\'>]+\.jpeg', html_content)

                    if img_urls:
                        # Pak de eerste afbeelding
                        main_img_url = img_urls[0]
                        
                        # Download de afbeelding
                        img_response = requests.get(main_img_url, headers=headers, timeout=15)
                        image_from_link = Image.open(io.BytesIO(img_response.content))
                        
                        st.success("Productfoto succesvol opgehaald!")
                        st.image(image_from_link, caption='Gevonden productfoto van Temu', use_container_width=True)
                        st.info("Hier stuur je deze foto door naar je Alibaba zoek-engine!")
                    else:
                        st.error("De productfoto kon niet direct uit de pagina gelezen worden. Probeer een andere Temu-link of gebruik een screenshot.")
                        
                except Exception as e:
                    st.error(f"Er ging iets mis bij het ophalen van de link: {e}")
        else:
            st.warning("Voer eerst een geldige Temu link in.")

