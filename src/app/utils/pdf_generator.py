from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
import base64
from PIL import Image as PILImage
from typing import List, Dict, Any
import tempfile

class PDFGenerator:
    """Utility class for generating PDF reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.custom_styles = self._create_custom_styles()
        
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        custom_styles = {}
        
        # Section Title
        section_title = ParagraphStyle(
            'SectionTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            textColor=colors.HexColor('#2C3E50')
        )
        
        # Subsection Title
        subsection_title = ParagraphStyle(
            'SubsectionTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=15,
            textColor=colors.HexColor('#34495E')
        )
        
        # Body Text
        body_text = ParagraphStyle(
            'BodyText',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=10,
            leading=14
        )
        
        # List Item
        list_item = ParagraphStyle(
            'ListItem',
            parent=self.styles['Normal'],
            fontSize=11,
            leftIndent=20,
            spaceAfter=5
        )
        
        custom_styles.update({
            'SectionTitle': section_title,
            'SubsectionTitle': subsection_title,
            'BodyText': body_text,
            'ListItem': list_item
        })
        
        return custom_styles

    def add_base64_image(self, base64_str: str, width: int = 500) -> Image:
        """Convert base64 image to ReportLab Image"""
        try:
            img_data = base64.b64decode(base64_str)
            img_buffer = BytesIO(img_data)
            img = PILImage.open(img_buffer)
            
            # Save to temporary file
            temp_img = BytesIO()
            img.save(temp_img, format='PNG')
            temp_img.seek(0)
            
            return Image(temp_img, width=width)
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return None

    def generate_customer_discovery_pdf(self, data: Dict[str, Any], output_path: str):
        """Generate PDF for customer discovery analysis"""
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        
        # Title
        story.append(Paragraph(f"Customer Discovery Analysis: {data['primary_domain']}", 
                             self.custom_styles['SectionTitle']))
        story.append(Spacer(1, 20))
        
        # Market Size
        story.append(Paragraph("Total Market Size", self.custom_styles['SubsectionTitle']))
        story.append(Paragraph(f"${data['total_market_size']:,}", 
                             self.custom_styles['BodyText']))
        
        # Ideal Customer Profile
        story.append(Paragraph("Ideal Customer Profile", 
                             self.custom_styles['SubsectionTitle']))
        story.append(Paragraph(data['ideal_customer_profile']['insights'], 
                             self.custom_styles['BodyText']))
        
        # Market Niches
        story.append(Paragraph("Market Niches", self.custom_styles['SubsectionTitle']))
        for niche in data['niches']:
            story.append(Paragraph(f"• {niche['name']}", 
                                 self.custom_styles['ListItem']))
            story.append(Paragraph(niche['description'], 
                                 self.custom_styles['BodyText']))
        
        doc.build(story)
        return output_path

    def generate_market_analysis_pdf(self, data: Dict[str, Any], output_path: str):
        """Generate PDF for market analysis"""
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        
        # Title
        story.append(Paragraph("Market Analysis Report", 
                             self.custom_styles['SectionTitle']))
        story.append(Spacer(1, 20))
        
        # Original Query
        story.append(Paragraph("Analysis Query", self.custom_styles['SubsectionTitle']))
        story.append(Paragraph(data['original_query'], 
                             self.custom_styles['BodyText']))
        
        # Comprehensive Report
        story.append(Paragraph("Market Analysis", 
                             self.custom_styles['SubsectionTitle']))
        story.append(Paragraph(data['comprehensive_report'], 
                             self.custom_styles['BodyText']))
        
        doc.build(story)
        return output_path

    def generate_competitive_analysis_pdf(self, data: Dict[str, Any], output_path: str):
        """Generate PDF for competitive analysis"""
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        
        # Title
        story.append(Paragraph(f"Competitive Analysis: {data['product_name']}", 
                             self.custom_styles['SectionTitle']))
        story.append(Spacer(1, 20))
        
        # Competitors
        story.append(Paragraph("Competitor Analysis", 
                             self.custom_styles['SubsectionTitle']))
        for competitor in data['competitors']:
            story.append(Paragraph(f"• {competitor['name']}", 
                                 self.custom_styles['ListItem']))
            story.append(Paragraph(competitor['description'], 
                                 self.custom_styles['BodyText']))
            story.append(Paragraph("Key Differentiators:", 
                                 self.custom_styles['BodyText']))
            for diff in competitor['key_differentiators']:
                story.append(Paragraph(f"  - {diff}", 
                                     self.custom_styles['ListItem']))
        
        # Product Derivatives
        story.append(Paragraph("Product Derivatives", 
                             self.custom_styles['SubsectionTitle']))
        for derivative in data['derivatives']:
            story.append(Paragraph(f"• {derivative['name']}", 
                                 self.custom_styles['ListItem']))
            story.append(Paragraph(derivative['description'], 
                                 self.custom_styles['BodyText']))
            story.append(Paragraph(f"Target Market: {derivative['target_market']}", 
                                 self.custom_styles['BodyText']))
        
        doc.build(story)
        return output_path

    def generate_product_evolution_pdf(self, data: Dict[str, Any], output_path: str):
        """Generate PDF for product evolution strategy"""
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        
        # Title
        story.append(Paragraph("Product Evolution Strategy", 
                             self.custom_styles['SectionTitle']))
        story.append(Spacer(1, 20))
        
        # Vision and Goals
        story.append(Paragraph("Overall Vision", self.custom_styles['SubsectionTitle']))
        story.append(Paragraph(data['overall_vision'], 
                             self.custom_styles['BodyText']))
        
        story.append(Paragraph("Long-term Goals", 
                             self.custom_styles['SubsectionTitle']))
        for goal in data['long_term_goals']:
            story.append(Paragraph(f"• {goal}", self.custom_styles['ListItem']))
        
        # Evolution Phases
        story.append(Paragraph("Evolution Phases", 
                             self.custom_styles['SubsectionTitle']))
        for phase in data['phases']:
            story.append(Paragraph(f"Phase: {phase['name']}", 
                                 self.custom_styles['ListItem']))
            story.append(Paragraph(phase['description'], 
                                 self.custom_styles['BodyText']))
            story.append(Paragraph("Key Features:", 
                                 self.custom_styles['BodyText']))
            for feature in phase['key_features']:
                story.append(Paragraph(f"  - {feature}", 
                                     self.custom_styles['ListItem']))
        
        # Visuals
        if data.get('visuals'):
            story.append(Paragraph("Visualization Insights", 
                                 self.custom_styles['SubsectionTitle']))
            if img := self.add_base64_image(data['visuals']['img']):
                story.append(img)
            story.append(Paragraph("Analysis:", self.custom_styles['BodyText']))
            story.append(Paragraph(data['visuals']['reason'], 
                                 self.custom_styles['BodyText']))
            story.append(Paragraph("Key Insights:", 
                                 self.custom_styles['BodyText']))
            for insight in data['visuals']['insights']:
                story.append(Paragraph(f"• {insight}", 
                                     self.custom_styles['ListItem']))
        
        doc.build(story)
        return output_path

    def combine_pdfs(self, pdf_paths: List[str], output_path: str):
        """Combine multiple PDFs into a single report"""
        from PyPDF2 import PdfMerger
        
        merger = PdfMerger()
        for pdf in pdf_paths:
            merger.append(pdf)
            
        with open(output_path, "wb") as output_file:
            merger.write(output_file)
        
        return output_path
