"""
Export Formats - CSV, Excel, JSON, PDF exports
"""
import os
import json
import csv
from typing import Dict, List, Optional
from datetime import datetime
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except:
    PANDAS_AVAILABLE = False


class ExportManager:
    """Export data in various formats"""
    
    def export_to_csv(self, data: List[Dict], filename: str) -> str:
        """Export data to CSV"""
        if not data:
            return "No data to export"
        
        filepath = os.path.join("exports", filename)
        os.makedirs("exports", exist_ok=True)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        
        return filepath
    
    def export_to_excel(self, data: Dict[str, List[Dict]], filename: str) -> str:
        """Export data to Excel"""
        if not PANDAS_AVAILABLE:
            return "Pandas not available. Install with: pip install pandas openpyxl"
        
        filepath = os.path.join("exports", filename)
        os.makedirs("exports", exist_ok=True)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            for sheet_name, sheet_data in data.items():
                df = pd.DataFrame(sheet_data)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        return filepath
    
    def export_to_json(self, data: Dict, filename: str) -> str:
        """Export data to JSON"""
        filepath = os.path.join("exports", filename)
        os.makedirs("exports", exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        
        return filepath
    
    def export_to_pdf(self, data: Dict, filename: str) -> str:
        """Export data to PDF (simplified)"""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            
            filepath = os.path.join("exports", filename)
            os.makedirs("exports", exist_ok=True)
            
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            story.append(Paragraph("JARVIS Export Report", styles['Title']))
            story.append(Spacer(1, 12))
            
            for key, value in data.items():
                story.append(Paragraph(f"<b>{key}:</b> {str(value)}", styles['Normal']))
                story.append(Spacer(1, 6))
            
            doc.build(story)
            return filepath
        except ImportError:
            return "ReportLab not available. Install with: pip install reportlab"
    
    def export_report(self, report_type: str, data: Dict, 
                     format: str = "json") -> str:
        """Export a report in specified format"""
        filename = f"{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
        
        if format == "csv":
            if isinstance(data, list):
                return self.export_to_csv(data, filename)
            else:
                return self.export_to_csv([data], filename)
        elif format == "excel":
            if isinstance(data, dict):
                return self.export_to_excel(data, filename)
            else:
                return self.export_to_excel({"Sheet1": [data] if not isinstance(data, list) else data}, filename)
        elif format == "json":
            return self.export_to_json(data, filename)
        elif format == "pdf":
            return self.export_to_pdf(data, filename)
        else:
            return f"Unsupported format: {format}"
