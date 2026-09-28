import streamlit as st
from playwright.sync_api import sync_playwright
from PIL import Image
import io

st.title("🚀 Free Sourcing Engine")
st.write("Vind continu en 100% gratis Alibaba-leveranciers op basis van je Temu-foto's of product-links.")

# Maak twee tabbladen aan in Streamlit voor een nette layout
tab1, tab2 = st.tabs(["📸 Screenshot Uploaden", "🔗 Temu Link Plakken"])

# --- TAB 1: SCREENSHOT UPLOADEN (Je bestaande functie) ---
with tab1:
    st.write("Sleep hier je Temu-screenshot naartoe")
    uploaded_file = st.file_uploader("Kies een afbeelding...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Geüploade afbeelding', use_column_width=True)
        st.info("Hier kun je jouw bestaande functie aanroepen om te zoeken op Alibaba!")
        # Hier komt jouw code: zoek_op_alibaba(image)

# --- TAB 2: LINK PLAKKEN (De nieuwe, betere optie!) ---
with tab2:
    st.write("Plak hier direct de Temu product-link:")
    temu_url = st.text_input("Product URL", placeholder="https://temu.com...")

    if st.button("Zoek Leverancier via Link"):
        if temu_url:
            with st.spinner("Temu pagina laden en foto ophalen..."):
                try:
                    # Start Playwright op de achtergrond om de foto van Temu te pakken
                    with sync_playwright() as p:
                        # Gebruik 'chromium' (onzichtbare browser)
                        browser = p.chromium.launch(headless=True)
                        page = browser.new_page()
                        
                        # Ga naar de Temu link
                        page.goto(temu_url, timeout=60000)
                        
                        # Wacht tot de hoofdafbeelding van het product geladen is
                        # Temu gebruikt vaak een specifieke class of img tag voor de hoofd-productfoto
                        page.wait_for_selector("img", timeout=10000)
                        
                        # We maken een screenshot van de specifieke productfoto, 
                        # of van het hele scherm als fallback
                        screenshot_bytes = page.screenshot(full_page=False)
                        browser.close()
                    
                    # Zet de gemaakte screenshot om naar een PIL Image zodat jouw engine ermee kan werken
                    image_from_link = Image.open(io.BytesIO(screenshot_bytes))
                    
                    st.success("Productfoto succesvol opgehaald!")
                    st.image(image_from_link, caption='Gevonden productfoto', use_column_width=True)
                    
                    st.info("Hier stuur je deze 'image_from_link' door naar je Alibaba zoek-engine!")
                    # Hier komt jouw code: zoek_op_alibaba(image_from_link)
                    
                except Exception as e:
                    st.error(f"Er ging iets mis bij het ophalen van de link: {e}")
        else:
            st.warning("Voer eerst een geldige Temu link in.")

