import cv2
import numpy as np
import pytesseract
import re
import json
from typing import Dict, List, Tuple

class ImageProcessor:
    """Kelas untuk pemrosesan gambar dan OCR"""
    
    def __init__(self):
        # Konfigurasi Tesseract (sesuaikan path jika diperlukan)
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows
        pass
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocessing gambar untuk meningkatkan akurasi OCR
        """
        # Convert ke grayscale jika berwarna
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image.copy()
        
        # Resize jika terlalu kecil
        height, width = gray.shape
        if width < 800:
            scale = 800 / width
            new_width = int(width * scale)
            new_height = int(height * scale)
            gray = cv2.resize(gray, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        
        # Gaussian blur untuk mengurangi noise
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        
        # Threshold untuk mendapatkan binary image
        _, threshold = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Morphological operations untuk membersihkan noise
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def detect_label_area(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Deteksi area label menggunakan contour detection (opsional)
        Returns: List of (x, y, w, h) bounding boxes
        """
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if len(image.shape) == 3 else image
        
        # Edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours berdasarkan area dan aspect ratio
        label_areas = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 5000:  # Minimum area threshold
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h
                
                # Label biasanya memiliki aspect ratio tertentu
                if 0.5 <= aspect_ratio <= 3.0:
                    label_areas.append((x, y, w, h))
        
        return label_areas
    
    def extract_text(self, image: np.ndarray, preprocess: bool = True) -> str:
        """
        Ekstraksi teks menggunakan OCR
        """
        if preprocess:
            processed_image = self.preprocess_image(image)
        else:
            processed_image = image
        
        # Konfigurasi OCR
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789()[]{}.,;:-_+%/ '
        
        try:
            # Ekstraksi teks
            text = pytesseract.image_to_string(processed_image, config=custom_config, lang='eng')
            return text.strip()
        except Exception as e:
            print(f"Error dalam OCR: {e}")
            return ""

class IngredientAnalyzer:
    """Kelas untuk analisis keamanan bahan"""
    
    def __init__(self):
        self.dangerous_ingredients = self._load_dangerous_ingredients()
        self.safe_ingredients = self._load_safe_ingredients()
    
    def _load_dangerous_ingredients(self) -> Dict[str, str]:
        """Load daftar bahan berbahaya"""
        return {
            # Surfaktan berbahaya
            'sodium lauryl sulfate': 'Dapat menyebabkan iritasi kulit dan mata',
            'sls': 'Dapat menyebabkan iritasi kulit dan mata',
            'sodium laureth sulfate': 'Dapat menyebabkan iritasi kulit',
            'sles': 'Dapat menyebabkan iritasi kulit',
            
            # Pengawet berbahaya
            'paraben': 'Dapat menyebabkan gangguan hormonal',
            'methylparaben': 'Dapat menyebabkan gangguan hormonal',
            'propylparaben': 'Dapat menyebabkan gangguan hormonal',
            'formaldehyde': 'Karsinogen dan dapat menyebabkan iritasi',
            'formalin': 'Karsinogen dan dapat menyebabkan iritasi',
            
            # Pewarna buatan
            'artificial color': 'Dapat menyebabkan alergi',
            'fd&c': 'Pewarna buatan yang dapat berbahaya',
            'tartrazine': 'Dapat menyebabkan reaksi alergi',
            
            # Bahan kimia lainnya
            'triclosan': 'Dapat mengganggu sistem endokrin',
            'dea': 'Berpotensi karsinogen',
            'diethanolamine': 'Berpotensi karsinogen',
            'propylene glycol': 'Dapat menyebabkan iritasi pada hewan sensitif',
            'mineral oil': 'Dapat menyumbat pori-pori',
            'petrolatum': 'Dapat menyumbat pori-pori',
            
            # Alkohol berbahaya
            'isopropyl alcohol': 'Dapat menyebabkan kekeringan berlebihan',
            'denatured alcohol': 'Dapat menyebabkan iritasi',
            
            # Fragrances
            'artificial fragrance': 'Dapat menyebabkan alergi',
            'synthetic fragrance': 'Dapat menyebabkan alergi',
        }
    
    def _load_safe_ingredients(self) -> Dict[str, str]:
        """Load daftar bahan aman"""
        return {
            # Bahan alami
            'aloe vera': 'Menenangkan dan melembabkan kulit',
            'coconut oil': 'Melembabkan dan antibakteri alami',
            'olive oil': 'Melembabkan dan kaya antioksidan',
            'jojoba oil': 'Melembabkan dan tidak menyumbat pori',
            'shea butter': 'Melembabkan dan anti-inflamasi',
            'oatmeal': 'Menenangkan kulit sensitif',
            'chamomile': 'Anti-inflamasi dan menenangkan',
            'lavender': 'Aromaterapi dan antibakteri',
            'tea tree oil': 'Antibakteri dan antijamur alami',
            'vitamin e': 'Antioksidan dan melindungi kulit',
            'vitamin c': 'Antioksidan dan memperbaiki kulit',
            
            # Surfaktan alami
            'coco glucoside': 'Surfaktan alami yang lembut',
            'decyl glucoside': 'Surfaktan alami yang lembut',
            'sodium cocoyl isethionate': 'Surfaktan lembut dari kelapa',
            
            # Pengawet alami
            'tocopherol': 'Vitamin E sebagai pengawet alami',
            'rosemary extract': 'Antioksidan dan pengawet alami',
            'grapefruit seed extract': 'Antimikroba alami',
            
            # Bahan lainnya
            'glycerin': 'Humektan alami yang melembabkan',
            'panthenol': 'Pro-vitamin B5 untuk kesehatan kulit',
            'allantoin': 'Menenangkan dan memperbaiki kulit',
            'hyaluronic acid': 'Melembabkan intensif',
            'ceramide': 'Memperkuat barrier kulit',
        }
    
    def _clean_text(self, text: str) -> str:
        """Membersihkan teks untuk analisis"""
        # Convert ke lowercase
        text = text.lower()
        
        # Hapus karakter khusus kecuali yang diperlukan
        text = re.sub(r'[^\w\s&,.-]', ' ', text)
        
        # Normalisasi spasi
        text = ' '.join(text.split())
        
        return text
    
    def _extract_ingredients_section(self, text: str) -> str:
        """Ekstrak bagian ingredients dari teks"""
        text_lower = text.lower()
        
        # Pattern untuk mencari section ingredients
        patterns = [
            r'ingredients?[:\-\s]+(.*?)(?:directions?|instructions?|caution|warning|$)',
            r'composition[:\-\s]+(.*?)(?:directions?|instructions?|caution|warning|$)',
            r'contents?[:\-\s]+(.*?)(?:directions?|instructions?|caution|warning|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_lower, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Jika tidak ditemukan section khusus, gunakan seluruh teks
        return text
    
    def analyze_ingredients(self, text: str) -> Dict[str, List]:
        """
        Analisis bahan-bahan dalam teks
        Returns: Dictionary dengan kategori dangerous, safe, unknown
        """
        cleaned_text = self._clean_text(text)
        ingredients_text = self._extract_ingredients_section(cleaned_text)
        
        # Split ingredients berdasarkan koma dan kata penghubung
        ingredients_list = re.split(r'[,;]|\band\b|\bor\b', ingredients_text)
        ingredients_list = [ing.strip() for ing in ingredients_list if ing.strip()]
        
        dangerous = []
        safe = []
        unknown = []
        found_ingredients = set()  # Untuk menghindari duplikasi
        
        # Analisis setiap ingredient
        for ingredient in ingredients_list:
            ingredient = ingredient.strip()
            if len(ingredient) < 2:  # Skip ingredient yang terlalu pendek
                continue
            
            # Cek bahan berbahaya
            found_dangerous = False
            for dangerous_name, reason in self.dangerous_ingredients.items():
                if dangerous_name in ingredient.lower():
                    if dangerous_name not in found_ingredients:
                        dangerous.append({
                            'name': dangerous_name.title(),
                            'found_in': ingredient,
                            'reason': reason
                        })
                        found_ingredients.add(dangerous_name)
                        found_dangerous = True
                        break
            
            if found_dangerous:
                continue
            
            # Cek bahan aman
            found_safe = False
            for safe_name, benefit in self.safe_ingredients.items():
                if safe_name in ingredient.lower():
                    if safe_name not in found_ingredients:
                        safe.append({
                            'name': safe_name.title(),
                            'found_in': ingredient,
                            'benefit': benefit
                        })
                        found_ingredients.add(safe_name)
                        found_safe = True
                        break
            
            if not found_safe and not found_dangerous:
                # Filter ingredient yang mungkin bukan nama bahan
                if len(ingredient) > 3 and not re.match(r'^\d+%?$', ingredient):
                    unknown.append(ingredient.title())
        
        return {
            'dangerous': dangerous,
            'safe': safe,
            'unknown': list(set(unknown))  # Remove duplicates
        }
    
    def get_recommendation(self, analysis: Dict[str, List]) -> Dict[str, str]:
        """
        Memberikan rekomendasi berdasarkan hasil analisis
        """
        dangerous_count = len(analysis['dangerous'])
        safe_count = len(analysis['safe'])
        total_known = dangerous_count + safe_count
        
        if dangerous_count == 0 and safe_count > 0:
            return {
                'status': 'safe',
                'message': f'Produk ini terlihat aman dengan {safe_count} bahan yang bermanfaat untuk hewan.'
            }
        elif dangerous_count > 0 and dangerous_count >= safe_count:
            return {
                'status': 'dangerous',
                'message': f'Hati-hati! Produk ini mengandung {dangerous_count} bahan berbahaya. Pertimbangkan untuk mencari alternatif yang lebih aman.'
            }
        elif dangerous_count > 0 and safe_count > dangerous_count:
            return {
                'status': 'caution',
                'message': f'Produk ini mengandung {dangerous_count} bahan berbahaya dan {safe_count} bahan aman. Gunakan dengan hati-hati dan pantau reaksi hewan.'
            }
        else:
            return {
                'status': 'unknown',
                'message': 'Tidak cukup informasi untuk menentukan keamanan produk. Konsultasikan dengan dokter hewan.'
            }

# Fungsi utility tambahan
def save_analysis_results(results: dict, filename: str = "analysis_results.json"):
    """Menyimpan hasil analisis ke file JSON"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Hasil analisis disimpan ke {filename}")
    except Exception as e:
        print(f"Error menyimpan file: {e}")

def load_custom_ingredients_db(filename: str = "ingredients_db.json") -> dict:
    """Load database bahan kustom dari file JSON"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {filename} tidak ditemukan, menggunakan database default")
        return {}
    except Exception as e:
        print(f"Error loading database: {e}")
        return {}