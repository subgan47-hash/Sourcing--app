import streamlit as st
from playwright.sync_api import sync_playwright
import time
from PIL import Image

# Prachtige, schone lay-out
st.set_page_config(page_title="Free Sourcing Engine", page_icon="🚀", layout="centered")
st.title("🚀 Free Sourcing Engine")
st.write("Vind continu en 100% gratis Alibaba-leveranciers op basis van je Temu-foto's.")

# Foto uploader
uploaded_file = st.file_uploader("Sleep hier je Temu-screenshot naartoe", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Jouw zoekafbeelding", width=200)
    
    with st.spinner("🔄 Browser start op en scant Alibaba gratis... (10-15 seconden)"):
        try:
            # Sla de geüploade foto tijdelijk op voor het script
            temp_path = "temp_search_img.jpg"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            # Start de gratis browser-automatisering
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto("https://alibaba.com")
                time.sleep(2)
                
                # Simuleer de gratis consumenten-zoekopdracht
                page.click("text=Search by Image")
                page.set_input_files("input[type='file']", temp_path)
                page.wait_for_selector(".search-result-grid", timeout=15000)
                
                # Haal de data live van het scherm
                leveranciers = page.locator(".supplier-name").all_text_contents()[:3]
                prijzen = page.locator(".elements-title-normal").all_text_contents()[:3]
                
                browser.close()
            
            # Toon de resultaten in een mooie tabel layout
            st.success("✨ Resultaten succesvol opgehaald!")
            for i in range(len(leveranciers)):
                with st.container():
                    st.subheader(f"Optie {i+1}: {leveranciers[i] if i < len(leveranciers) else 'Fabriek'}")
                    st.write(f"💰 Richtprijs: {prijzen[i] if i < len(prijzen) else 'Zie website'}")
                    st.markdown("---")
                    
        except Exception as e:
            st.error(f"Er ging iets mis of Alibaba vraagt om een handmatige verificatie: {e}")

