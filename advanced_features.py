"""
Advanced Features untuk Pet Product Safety Analyzer
Fitur tambahan untuk pengembangan lebih lanjut
"""

import cv2
import numpy as np
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageDraw, ImageFont
import json
import requests
from datetime import datetime

class AdvancedImageProcessor:
    """Pemrosesan gambar tingkat lanjut"""
    
    def __init__(self):
        self.yolo_model = None  # Placeholder untuk YOLO model
    
    def detect_labels_with_yolo(self, image: np.ndarray) -> List[Dict]:
        """
        Deteksi label menggunakan YOLO (memerlukan model training)
        Ini adalah placeholder untuk implementasi YOLO
        """
        # Placeholder implementation
        # Dalam implementasi nyata, Anda perlu:
        # 1. Train YOLO model dengan dataset label produk
        # 2. Load model yang sudah di-train
        # 3. Deteksi object dengan confidence score
        
        dummy_detections = [
            {
                'class': 'ingredient_label',
                'confidence': 0.85,
                'bbox': [100, 100, 300, 200],
                'area': 20000
            }
        ]
        return dummy_detections
    
    def enhance_image_quality(self, image: np.ndarray) -> np.ndarray:
        """
        Meningkatkan kualitas gambar untuk OCR yang lebih baik
        """
        # Denoising
        denoised = cv2.fastNlMeansDenoising(image)
        
        # Sharpening
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(denoised, -1, kernel)
        
        # Contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(sharpened)
        
        return enhanced
    
    def segment_text_regions(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Segmentasi area teks menggunakan EAST text detector
        """
        # Placeholder untuk EAST text detection
        # Implementasi nyata memerlukan model EAST yang pre-trained
        
        height, width = image.shape[:2]
        
        # Dummy text regions
        text_regions = [
            (50, 50, 200, 30),   # (x, y, w, h)
            (50, 100, 250, 40),
            (50, 160, 180, 25)
        ]
        
        return text_regions

class DatabaseManager:
    """Manajemen database bahan kimia"""
    
    def __init__(self):
        self.db_file = "ingredients_db.json"
        self.api_endpoints = {
            'pubchem': 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}/JSON',
            'chemspider': 'https://www.chemspider.com/Search.asmx/SimpleSearch'
        }
    
    def search_ingredient_online(self, ingredient_name: str) -> Dict:
        """
        Mencari informasi bahan secara online
        """
        try:
            # Contoh pencarian di PubChem
            url = self.api_endpoints['pubchem'].format(ingredient_name)
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'found': True,
                    'source': 'PubChem',
                    'data': data,
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Error searching online: {e}")
        
        return {'found': False}
    
    def update_database_from_research(self, research_data: Dict):
        """
        Update database berdasarkan penelitian terbaru
        """
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                current_db = json.load(f)
            
            # Merge new research data
            for category, ingredients in research_data.items():
                if category in current_db:
                    current_db[category].update(ingredients)
                else:
                    current_db[category] = ingredients
            
            # Save updated database
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(current_db, f, indent=2, ensure_ascii=False)
            
            print("Database updated successfully")
            
        except Exception as e:
            print(f"Error updating database: {e}")

class AnimalSpecificAnalyzer:
    """Analisis spesifik berdasarkan jenis hewan"""
    
    def __init__(self):
        self.animal_profiles = {
            'cat': {
                'metabolism': 'slow',
                'skin_pH': 6.2,
                'sensitivity': 'high',
                'toxic_compounds': ['parabens', 'essential_oils', 'propylene_glycol']
            },
            'dog': {
                'metabolism': 'fast',
                'skin_pH': 6.5,
                'sensitivity': 'medium',
                'toxic_compounds': ['xylitol', 'grapes', 'chocolate']
            },
            'rabbit': {
                'metabolism': 'fast',
                'skin_pH': 6.0,
                'sensitivity': 'very_high',
                'toxic_compounds': ['cedar', 'pine', 'citrus_oils']
            },
            'bird': {
                'metabolism': 'very_fast',
                'skin_pH': 5.8,
                'sensitivity': 'extreme',
                'toxic_compounds': ['teflon', 'aerosols', 'fragrances']
            }
        }
    
    def analyze_for_specific_animal(self, ingredients: List[str], animal_type: str) -> Dict:
        """
        Analisis keamanan untuk jenis hewan tertentu
        """
        if animal_type not in self.animal_profiles:
            return {'error': f'Animal type {animal_type} not supported'}
        
        profile = self.animal_profiles[animal_type]
        results = {
            'animal_type': animal_type,
            'specific_warnings': [],
            'safety_score': 0,
            'recommendations': []
        }
        
        dangerous_count = 0
        safe_count = 0
        
        for ingredient in ingredients:
            ingredient_lower = ingredient.lower()
            
            # Check against animal-specific toxic compounds
            for toxic in profile['toxic_compounds']:
                if toxic in ingredient_lower:
                    results['specific_warnings'].append({
                        'ingredient': ingredient,
                        'warning': f'Sangat berbahaya untuk {animal_type}',
                        'severity': 'critical'
                    })
                    dangerous_count += 1
                    break
            else:
                safe_count += 1
        
        # Calculate safety score
        total_ingredients = len(ingredients)
        if total_ingredients > 0:
            results['safety_score'] = (safe_count / total_ingredients) * 100
        
        # Generate recommendations
        if results['safety_score'] < 50:
            results['recommendations'].append(f'Tidak disarankan untuk {animal_type}')
        elif results['safety_score'] < 80:
            results['recommendations'].append(f'Gunakan dengan hati-hati pada {animal_type}')
        else:
            results['recommendations'].append(f'Relatif aman untuk {animal_type}')
        
        return results

class ReportGenerator:
    """Generator laporan analisis"""
    
    def __init__(self):
        self.template_path = "report_template.html"
    
    def generate_pdf_report(self, analysis_results: Dict, output_path: str = "analysis_report.pdf"):
        """
        Generate laporan PDF
        """
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            
            # Create PDF document
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.darkblue,
                alignment=1  # Center alignment
            )
            story.append(Paragraph("Pet Product Safety Analysis Report", title_style))
            story.append(Spacer(1, 0.5*inch))
            
            # Analysis Summary
            summary_data = [
                ['Category', 'Count', 'Percentage'],
                ['Dangerous Ingredients', len(analysis_results.get('dangerous', [])), ''],
                ['Safe Ingredients', len(analysis_results.get('safe', [])), ''],
                ['Unknown Ingredients', len(analysis_results.get('unknown', [])), '']
            ]
            
            summary_table = Table(summary_data)
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Detailed Analysis
            if analysis_results.get('dangerous'):
                story.append(Paragraph("Dangerous Ingredients Found:", styles['Heading2']))
                for ingredient in analysis_results['dangerous']:
                    story.append(Paragraph(f"• {ingredient['name']}: {ingredient['reason']}", styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
            
            # Build PDF
            doc.build(story)
            print(f"PDF report generated: {output_path}")
            
        except ImportError:
            print("ReportLab not installed. Install with: pip install reportlab")
        except Exception as e:
            print(f"Error generating PDF report: {e}")
    
    def generate_visualization(self, analysis_results: Dict, save_path: str = "analysis_chart.png"):
        """
        Generate visualisasi hasil analisis
        """
        try:
            # Data untuk pie chart
            categories = ['Dangerous', 'Safe', 'Unknown']
            values = [
                len(analysis_results.get('dangerous', [])),
                len(analysis_results.get('safe', [])),
                len(analysis_results.get('unknown', []))
            ]
            
            colors = ['#ff6b6b', '#4ecdc4', '#ffd93d']
            
            # Create pie chart
            plt.figure(figsize=(10, 8))
            
            # Main pie chart
            plt.subplot(2, 2, 1)
            plt.pie(values, labels=categories, colors=colors, autopct='%1.1f%%', startangle=90)
            plt.title('Ingredient Safety Distribution')
            
            # Bar chart
            plt.subplot(2, 2, 2)
            plt.bar(categories, values, color=colors)
            plt.title('Ingredient Count by Category')
            plt.ylabel('Number of Ingredients')
            
            # Safety score gauge (placeholder)
            plt.subplot(2, 2, 3)
            safety_score = 75  # Placeholder
            plt.bar(['Safety Score'], [safety_score], color='green' if safety_score > 70 else 'orange' if safety_score > 40 else 'red')
            plt.ylim(0, 100)
            plt.title('Overall Safety Score')
            plt.ylabel('Score (%)')
            
            # Timeline or trends (placeholder)
            plt.subplot(2, 2, 4)
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
            safety_trend = [65, 70, 68, 75, 78]  # Placeholder data
            plt.plot(months, safety_trend, marker='o', color='blue')
            plt.title('Safety Trend Over Time')
            plt.ylabel('Safety Score')
            
            plt.tight_layout()
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"Visualization saved: {save_path}")
            
        except Exception as e:
            print(f"Error generating visualization: {e}")

class BatchProcessor:
    """Pemrosesan batch untuk multiple gambar"""
    
    def __init__(self, analyzer, image_processor):
        self.analyzer = analyzer
        self.image_processor = image_processor
    
    def process_batch(self, image_paths: List[str]) -> List[Dict]:
        """
        Proses multiple gambar sekaligus
        """
        results = []
        
        for i, image_path in enumerate(image_paths):
            print(f"Processing image {i+1}/{len(image_paths)}: {image_path}")
            
            try:
                # Load image
                image = cv2.imread(image_path)
                if image is None:
                    print(f"Error loading image: {image_path}")
                    continue
                
                # Extract text
                text = self.image_processor.extract_text(image)
                
                # Analyze ingredients
                analysis = self.analyzer.analyze_ingredients(text)
                
                # Compile results
                result = {
                    'image_path': image_path,
                    'extracted_text': text,
                    'analysis': analysis,
                    'timestamp': datetime.now().isoformat()
                }
                
                results.append(result)
                
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
                results.append({
                    'image_path': image_path,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        
        return results
    
    def save_batch_results(self, results: List[Dict], output_file: str = "batch_results.json"):
        """
        Simpan hasil batch processing
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"Batch results saved to: {output_file}")
        except Exception as e:
            print(f"Error saving batch results: {e}")

# Example usage functions
def example_advanced_usage():
    """
    Contoh penggunaan fitur advanced
    """
    print("🔬 Advanced Features Demo")
    print("-" * 30)
    
    # Initialize components
    advanced_processor = AdvancedImageProcessor()
    db_manager = DatabaseManager()
    animal_analyzer = AnimalSpecificAnalyzer()
    report_generator = ReportGenerator()
    
    # Example ingredient list
    ingredients = ['sodium lauryl sulfate', 'aloe vera', 'paraben', 'coconut oil']
    
    # Animal-specific analysis
    cat_analysis = animal_analyzer.analyze_for_specific_animal(ingredients, 'cat')
    print(f"Cat Analysis: {cat_analysis}")
    
    # Generate visualization
    analysis_results = {
        'dangerous': [{'name': 'SLS', 'reason': 'Irritant'}],
        'safe': [{'name': 'Aloe Vera', 'benefit': 'Soothing'}],
        'unknown': ['Unknown Compound']
    }
    
    report_generator.generate_visualization(analysis_results)
    
    print("✅ Advanced features demo completed")

if __name__ == "__main__":
    example_advanced_usage()
