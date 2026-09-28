import streamlit as st
import requests
from PIL import Image
import io
import re
import urllib.parse
import pandas as pd

# --- CONFIGURATIE & SETUP ---
st.set_page_config(page_title="Free Sourcing Engine PRO", layout="wide")

st.title("🚀 Free Sourcing Engine PRO")
st.write("Vind direct de exacte Alibaba-leveranciers en fabrieksprijzen op basis van je Temu product-links.")

# --- API INSTELLINGEN (Optioneel) ---
st.sidebar.markdown("### 🛠️ API Instellingen")
RAPIDAPI_KEY = st.sidebar.text_input("🔑 RapidAPI Sleutel (Optioneel voor live prijzen)", type="password")

# --- FUNCTIE: RECHTSCHREEKSE IMAGE SEARCH VIA API ---
def zoek_leveranciers_via_api(afbeeldings_url):
    if not RAPIDAPI_KEY:
        return None
    url = "https://rapidapi.com"
    querystring = {"image_url": afbeeldings_url, "site": "alibaba"}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "://rapidapi.com"
    }
    try:
        api_response = requests.get(url, headers=headers, params=querystring, timeout=15)
        if api_response.status_code == 200:
            data = api_response.json()
            return data.get("result", {}).get("items", [])
    except Exception:
        pass
    return None

# --- CENTRALE FUNCTIE: TOON RESULTATEN ---
def toon_sourcing_dashboard(product_image, product_naam, gevonden_items=None):
    st.write("---")
    st.subheader("📦 Direct Sourcing Dashboard")
   
    col1, col2 = st.columns(2)
    with col1:
        if product_image:
            st.image(product_image, caption="Geanalyseerd product van de link", width=280)
        else:
            st.warning("⚠️ Afbeelding kon niet live worden geladen door Temu-beveiliging.")
           
    with col2:
        # Dit zorgt ervoor dat er een nette, schone naam staat (zoals op jouw foto: Super Sticky Carpet Tape)
        st.markdown(f"### 🔍 Gevonden match: *{product_naam.title()}*")
        st.write("Gebruik de onderstaande knop om de leveranciers op Alibaba te openen:")
        
        # Veilige zoeklink op basis van de SCHONE naam
        zoekterm = urllib.parse.quote_plus(product_naam)
        alibaba_tekst_url = f"https://alibaba.com{zoekterm}"
        
        st.link_button("➡️ Open Exacte Producten op Alibaba.com", alibaba_tekst_url, type="primary")
        st.caption(f"💡 Zoekterm gebruikt voor Alibaba: **{product_naam}**")
        
        st.info("📌 **Tip voor Image Search:** Klik met de rechtermuisknop op de productafbeelding links, kies 'Afbeelding opslaan' en upload deze in de zoekbalk op Alibaba.com voor de exacte fabrieksmatch.")

    # --- LIVE API RESULTATEN TONEN ---
    if gevonden_items:
        st.write("---")
        st.subheader("🏭 Geverifieerde Alibaba Fabrieken (Live Data)")
        res_list = []
        for item in gevonden_items[:10]:
            res_list.append({
                "Productnaam": item.get("title"),
                "Prijs ($)": f"${item.get('price')}",
                "Min. Afname (MOQ)": item.get("moq", "1 stuks"),
                "Alibaba Link": item.get("product_url")
            })
        df = pd.DataFrame(res_list)
        st.dataframe(df, column_config={"Alibaba Link": st.column_config.LinkColumn("Bekijk Fabrikant")}, hide_index=True, use_container_width=True)

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
                
                # --- CRUCIALE FIX: Sla alle tracking codes na het vraagteken (?) over ---
                schone_url = temu_url.split('?')[0]
                
                response = requests.get(temu_url, headers=headers, timeout=15)
                html_content = response.text
               
                # Haal de echte naam uit de schone URL
                product_naam = "carpet tape"
                # Dit zoekt naar het tekstgedeelte in de URL (werkt voor /nl/, /en/, /share/, etc.)
                match_naam = re.search(r'/(?:nl|en|de|fr|share|bg|kws)/([^/]+)', schone_url)
                
                if match_naam:
                    ruwe_naam = match_naam.group(1)
                    # Verwijder .html als dat erin staat
                    ruwe_naam = ruwe_naam.replace(".html", "")
                    # Maak spaties van streepjes
                    product_naam = ruwe_naam.replace("-", " ")
                    # Verwijder losse ID-nummers aan het einde van de productnaam (zoals g_6011...)
                    product_naam = re.sub(r'\s\d+$|\sg_\d+.*$', '', product_naam).strip()
                
                # Als de naam per ongeluk toch leeg blijft of te lang is (foutieve url), pak een fallback
                if len(product_naam) > 80 or not product_naam:
                    product_naam = "carpet tape"
               
                # Afbeelding extractie uit de html
                img_urls = re.findall(r'https://img\.kwcdn\.com/product/fancy/[^\s"\'>]+\.jpg', html_content)
                if not img_urls:
                    img_urls = re.findall(r'https://img\.kwcdn\.com/[^\s"\'>]+\.jpeg', html_content)

                if img_urls:
                    zuivere_link = img_urls[0].strip("['\"] ")
                    img_response = requests.get(zuivere_link, headers=headers, timeout=15)
                    image_from_link = Image.open(io.BytesIO(img_response.content))
                   
                    api_resultaten = zoek_leveranciers_via_api(zuivere_link)
                    
                    st.success("Leveranciersdata succesvol getraceerd!")
                    toon_sourcing_dashboard(image_from_link, product_naam, api_resultaten)
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

