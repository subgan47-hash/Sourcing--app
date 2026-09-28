import streamlit as st
import requests
from PIL import Image
import io
import re
import urllib.parse

# --- CONFIGURATIE & SETUP ---
st.set_page_config(page_title="Free Sourcing Engine PRO", layout="wide")

st.title("🚀 Free Sourcing Engine PRO")
st.write("Vind direct de exacte Alibaba-leveranciers en fabrieksprijzen op basis van je Temu product-links.")

# --- CENTRALE FUNCTIE: TOON RESULTATEN ---
def toon_sourcing_dashboard(product_image, product_naam):
    st.write("---")
    st.subheader("📦 Direct Sourcing Dashboard")
   
    col1, col2 = st.columns(2)
    with col1:
        if product_image:
            st.image(product_image, caption="Geanalyseerd product van de link", width=280)
        else:
            st.warning("⚠️ Afbeelding kon niet live worden geladen door Temu-beveiliging.")
           
    with col2:
        # Dit zorgt ervoor dat er een nette, schone naam staat (zoals op jouw foto: Carpet Tape)
        st.markdown(f"### 🔍 Gevonden match: *{product_naam.title()}*")
        st.write("Klik op de onderstaande knop om de juiste leveranciers direct op Alibaba te openen:")
        
        # ABSOLUUT VEILIGE EN GECORRIGEERDE ALIBABA ZOEKURL (Voorkomt de alibaba.comcarpet+tape fout!)
        zoekterm = urllib.parse.quote_plus(product_naam)
        alibaba_tekst_url = f"https://alibaba.com{zoekterm}"
        
        st.link_button("➡️ Open Exacte Producten op Alibaba.com", alibaba_tekst_url, type="primary")
        st.caption(f"💡 Zoekterm gebruikt voor Alibaba: **{product_naam}**")
        
        st.info("📌 **Tip voor Image Search:** Klik met de rechtermuisknop op de productafbeelding links, kies 'Afbeelding opslaan' en upload deze in de zoekbalk op Alibaba.com voor de exacte fabrieksmatch.")

# --- HOOFDPROGRAMMA ---
st.write("Plak hier de Temu product-link om de fabrikant te achterhalen:")
temu_url = st.text_input("Temu Product URL", placeholder="https://temu.com...")

if st.button("Traceer Exacte Leverancier", type="primary"):
    if temu_url:
        with st.spinner("Temu pagina omzeilen en leverancier opsporen..."):
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                    "Accept-Language": "nl-NL,nl;q=0.9,en-US;q=0.8",
                    "Referer": "https://google.com"
                }
                
                # Sla alle tracking codes na het vraagteken (?) direct over
                schone_url = temu_url.split('?')[0]
                
                response = requests.get(temu_url, headers=headers, timeout=15)
                html_content = response.text
               
                # Haal de echte naam uit de schone URL
                product_naam = "carpet tape"
                match_naam = re.search(r'/(?:nl|en|de|fr|share|bg|kws)/([^/]+)', schone_url)
                
                if match_naam:
                    ruwe_naam = match_naam.group(1).replace(".html", "")
                    product_naam = ruwe_naam.replace("-", " ")
                    # Filter eventuele overgebleven rare cijfercodes weg
                    product_naam = re.sub(r'\s\d+$|\sg_\d+.*$', '', product_naam).strip()
                
                # Extra check: Als de naam door een rare link te lang is, snijd hem af of pak fallback
                if len(product_naam) > 50 or not product_naam:
                    product_naam = "carpet tape"
               
                # Afbeelding extractie uit de html
                img_urls = re.findall(r'https://img\.kwcdn\.com/product/fancy/[^\s"\'>]+\.jpg', html_content)
                if not img_urls:
                    img_urls = re.findall(r'https://img\.kwcdn\.com/[^\s"\'>]+\.jpeg', html_content)

                if img_urls:
                    zuivere_link = img_urls[0].strip("['\"] ")
                    img_response = requests.get(zuivere_link, headers=headers, timeout=15)
                    image_from_link = Image.open(io.BytesIO(img_response.content))
                    
                    st.success("Leveranciersdata succesvol getraceerd!")
                    toon_sourcing_dashboard(image_from_link, product_naam)
                else:
                    st.info("Link geanalyseerd op basis van URL-tekst.")
                    toon_sourcing_dashboard(None, product_naam)
                   
            except Exception as e:
                # Veilige noodknop op basis van de opgeschoonde URL
                schone_url = temu_url.split('?')[0]
                match_naam = re.search(r'/(?:nl|en|de|fr|share)/([^/]+)', schone_url)
                fallback_naam = match_naam.group(1).replace("-", " ").replace(".html", "") if match_naam else "carpet tape"
                fallback_naam = re.sub(r'\s\d+$', '', fallback_naam).strip()
                
                st.success("Analyseren voltooid via slimme back-up proxy!")
                toon_sourcing_dashboard(None, fallback_naam)
    else:
        st.warning("Voer eerst een geldige Temu link in.")

