import streamlit as st
import subprocess
import os

# Automatische Playwright browser installatie voor de Streamlit server
@st.cache_resource
def install_playwright_browsers():
    try:
        # Controleer of de browser al bestaat, zo niet, installeer hem
        if not os.path.exists("/home/appuser/.cache/ms-playwright"):
            with st.spinner("Systeem configureert de browser voor de eerste keer, een moment geduld..."):
                subprocess.run(["python", "-m", "playwright", "install", "chromium"], check=True)
    except Exception as e:
        st.error(f"Fout bij installeren browser: {e}")

# Voer de installatie uit
install_playwright_browsers()

from playwright.sync_api import sync_playwright
from PIL import Image
import io

st.title("🚀 Free Sourcing Engine")
st.write("Vind continu en 100% gratis Alibaba-leveranciers op basis van je Temu-foto's of product-links.")

# Maak twee tabbladen aan in Streamlit voor een nette layout
tab1, tab2 = st.tabs(["📸 Screenshot Uploaden", "🔗 Temu Link Plakken"])

# --- TAB 1: SCREENSHOT UPLOADEN ---
with tab1:
    st.write("Sleep hier je Temu-screenshot naartoe")
    uploaded_file = st.file_uploader("Kies een afbeelding...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Geüploade afbeelding', use_column_width=True)
        st.info("Hier kun je jouw bestaande functie aanroepen om te zoeken op Alibaba!")

# --- TAB 2: LINK PLAKKEN ---
with tab2:
    st.write("Plak hier direct de Temu product-link:")
    temu_url = st.text_input("Product URL", placeholder="https://temu.com...")

    if st.button("Zoek Leverancier via Link"):
        if temu_url:
            with st.spinner("Temu pagina laden en foto ophalen..."):
                try:
                    # Start Playwright op de achtergrond
                    with sync_playwright() as p:
                        browser = p.chromium.launch(headless=True)
                        page = browser.new_page()
                        
                        # Ga naar de Temu link
                        page.goto(temu_url, timeout=60000)
                        
                        # Wacht tot de pagina geladen is
                        page.wait_for_selector("img", timeout=15000)
                        
                        # Maak een screenshot van de geladen pagina om de foto te pakken
                        screenshot_bytes = page.screenshot(full_page=False)
                        browser.close()
                    
                    # Zet de gemaakte screenshot om naar een PIL Image
                    image_from_link = Image.open(io.BytesIO(screenshot_bytes))
                    
                    st.success("Productfoto succesvol opgehaald!")
                    st.image(image_from_link, caption='Gevonden productfoto', use_column_width=True)
                    st.info("Hier stuur je deze foto door naar je Alibaba zoek-engine!")
                    
                except Exception as e:
                    st.error(f"Er ging iets mis bij het ophalen van de link: {e}")
        else:
            st.warning("Voer eerst een geldige Temu link in.")

