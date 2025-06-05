import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pytesseract
import json
import re
from utils import IngredientAnalyzer, ImageProcessor
import os

# Konfigurasi halaman
st.set_page_config(
    page_title="Pet Product Safety Analyzer",
    page_icon="🐾",
    layout="wide"
)

# Inisialisasi analyzer
@st.cache_resource
def load_analyzer():
    return IngredientAnalyzer()

def main():
    st.title("🐾 Pet Product Safety Analyzer")
    st.markdown("**Sistem Analisis Keamanan Produk Perawatan Hewan**")
    
    # Sidebar untuk informasi
    with st.sidebar:
        st.header("📋 Informasi Sistem")
        st.markdown("""
        **Fungsi Utama:**
        - Deteksi label produk
        - Ekstraksi teks (OCR)
        - Analisis keamanan bahan
        
        **Format yang Didukung:**
        - JPG, PNG, JPEG
        
        **Jenis Produk:**
        - Shampoo hewan
        - Makanan ringan
        - Suplemen & obat luar
        """)
    
    # Load analyzer
    analyzer = load_analyzer()
    image_processor = ImageProcessor()
    
    # Upload gambar
    st.header("📤 Upload Gambar Produk")
    uploaded_file = st.file_uploader(
        "Pilih gambar kemasan produk", 
        type=['jpg', 'jpeg', 'png'],
        help="Upload gambar kemasan produk perawatan hewan untuk dianalisis"
    )
    
    if uploaded_file is not None:
        # Tampilkan gambar asli
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🖼️ Gambar Asli")
            image = Image.open(uploaded_file)
            st.image(image, caption="Gambar yang diupload", use_column_width=True)
        
        with col2:
            st.subheader("🔍 Preprocessing")
            # Proses gambar
            processed_image = image_processor.preprocess_image(np.array(image))
            st.image(processed_image, caption="Gambar setelah preprocessing", use_column_width=True)
        
        # Tombol untuk memproses
        if st.button("🔬 Analisis Produk", type="primary"):
            with st.spinner("Sedang menganalisis gambar..."):
                # OCR
                st.header("📝 Hasil OCR")
                ocr_text = image_processor.extract_text(np.array(image))
                
                if ocr_text.strip():
                    st.text_area("Teks yang diekstrak:", ocr_text, height=150)
                    
                    # Analisis bahan
                    st.header("🧪 Analisis Bahan")
                    analysis = analyzer.analyze_ingredients(ocr_text)
                    
                    # Tampilkan hasil dalam 3 kolom
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Bahan Berbahaya", 
                            len(analysis['dangerous']),
                            delta=f"-{len(analysis['dangerous'])}" if analysis['dangerous'] else "0"
                        )
                        
                        if analysis['dangerous']:
                            st.error("🚫 **Bahan Berbahaya Ditemukan:**")
                            for ingredient in analysis['dangerous']:
                                st.write(f"• **{ingredient['name']}** - {ingredient['reason']}")
                    
                    with col2:
                        st.metric(
                            "Bahan Aman", 
                            len(analysis['safe']),
                            delta=f"+{len(analysis['safe'])}" if analysis['safe'] else "0"
                        )
                        
                        if analysis['safe']:
                            st.success("✅ **Bahan Aman:**")
                            for ingredient in analysis['safe']:
                                st.write(f"• **{ingredient['name']}** - {ingredient['benefit']}")
                    
                    with col3:
                        st.metric(
                            "Tidak Diketahui", 
                            len(analysis['unknown']),
                            delta=f"?{len(analysis['unknown'])}" if analysis['unknown'] else "0"
                        )
                        
                        if analysis['unknown']:
                            st.warning("❓ **Bahan Tidak Diketahui:**")
                            for ingredient in analysis['unknown']:
                                st.write(f"• {ingredient}")
                    
                    # Rekomendasi
                    st.header("💡 Rekomendasi")
                    recommendation = analyzer.get_recommendation(analysis)
                    
                    if recommendation['status'] == 'dangerous':
                        st.error(f"⚠️ **{recommendation['message']}**")
                    elif recommendation['status'] == 'safe':
                        st.success(f"✅ **{recommendation['message']}**")
                    else:
                        st.info(f"ℹ️ **{recommendation['message']}**")
                    
                    # Statistik detail
                    st.header("📊 Statistik Detail")
                    total_ingredients = len(analysis['dangerous']) + len(analysis['safe']) + len(analysis['unknown'])
                    
                    if total_ingredients > 0:
                        danger_pct = (len(analysis['dangerous']) / total_ingredients) * 100
                        safe_pct = (len(analysis['safe']) / total_ingredients) * 100
                        unknown_pct = (len(analysis['unknown']) / total_ingredients) * 100
                        
                        st.write(f"**Total bahan terdeteksi:** {total_ingredients}")
                        st.write(f"**Persentase berbahaya:** {danger_pct:.1f}%")
                        st.write(f"**Persentase aman:** {safe_pct:.1f}%")
                        st.write(f"**Persentase tidak diketahui:** {unknown_pct:.1f}%")
                        
                        # Progress bar visual
                        st.progress(safe_pct / 100, text=f"Tingkat Keamanan: {safe_pct:.1f}%")
                    
                else:
                    st.error("❌ Tidak dapat mengekstrak teks dari gambar. Pastikan gambar memiliki kualitas yang baik dan teks terlihat jelas.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>🐾 Pet Product Safety Analyzer v1.0</p>
        <p><small>Sistem ini membantu menganalisis keamanan produk perawatan hewan berdasarkan komposisi bahan.</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()