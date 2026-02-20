"""
Insight Generator module
Generates human-readable insights from data analysis using LLM
"""

import openai
import os
from typing import Dict, Optional

class InsightGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize insight generator with OpenAI API
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
    
    def generate(self, query_params: Dict, statistics: Dict, prediction: Dict) -> str:
        """
        Generate natural language insights from analysis results
        
        Args:
            query_params: Parsed query parameters
            statistics: Statistical analysis results
            prediction: Prediction results
            
        Returns:
            Human-readable insight text
        """
        
        # For demo: Generate template-based insights
        region = query_params.get("region", "the ocean")
        parameter = query_params.get("parameter", "data")
        start_year = query_params.get("start_year")
        end_year = query_params.get("end_year")
        
        insight = f"Analysis of {parameter} in {region}"
        
        if start_year and end_year:
            insight += f" from {start_year} to {end_year}"
        
        insight += ":\n\n"
        
        # Add statistics
        if statistics:
            insight += f"📊 Statistical Summary:\n"
            insight += f"- Average: {statistics.get('mean', 'N/A'):.2f}\n"
            insight += f"- Range: {statistics.get('min', 'N/A'):.2f} to {statistics.get('max', 'N/A'):.2f}\n"
            insight += f"- Data points: {statistics.get('count', 0)}\n\n"
        
        # Add prediction insights
        if prediction and prediction.get("success"):
            trend = prediction.get("trend", "stable")
            confidence = prediction.get("confidence", "unknown")
            
            insight += f"🔮 Prediction:\n"
            insight += f"- Trend: {trend.capitalize()}\n"
            insight += f"- Confidence: {confidence.capitalize()}\n"
            
            if trend == "increasing":
                insight += f"- The {parameter} shows an upward trend, indicating potential warming or environmental changes.\n"
            elif trend == "decreasing":
                insight += f"- The {parameter} shows a downward trend, which may require further investigation.\n"
            
            insight += "\n"
        
        # Add climate interpretation
        insight += self._add_climate_context(parameter, prediction)
        
        return insight
    
    def _add_climate_context(self, parameter: str, prediction: Dict) -> str:
        """
        Add climate-specific context based on parameter
        """
        
        context = "🌍 Climate Context:\n"
        
        if parameter == "temperature":
            if prediction.get("trend") == "increasing":
                context += "Rising ocean temperatures are linked to climate change and can affect marine ecosystems, coral bleaching, and sea level rise.\n"
            else:
                context += "Ocean temperature patterns are crucial indicators of climate health and marine ecosystem stability.\n"
        
        elif parameter == "salinity":
            context += "Ocean salinity changes indicate shifts in evaporation, precipitation, and ice melt patterns, which are important climate indicators.\n"
        
        elif parameter == "oxygen":
            if prediction.get("trend") == "decreasing":
                context += "⚠️ Declining oxygen levels (ocean deoxygenation) can threaten marine life and indicate ecosystem stress.\n"
            else:
                context += "Ocean oxygen levels are critical for marine biodiversity and ecosystem health.\n"
        
        else:
            context += f"The {parameter} measurements provide valuable insights into ocean health and climate patterns.\n"
        
        return context
    
    def generate_with_gpt(self, query_params: Dict, statistics: Dict, prediction: Dict) -> str:
        """
        Generate insights using OpenAI GPT (for production)
        """
        if not self.api_key:
            return self.generate(query_params, statistics, prediction)
        
        try:
            prompt = f"""
            As an ocean climate expert, provide insights on this analysis:
            
            Query: {query_params}
            Statistics: {statistics}
            Prediction: {prediction}
            
            Provide a clear, concise summary with:
            1. Key findings
            2. Trend analysis
            3. Climate implications
            4. Any warnings or notable patterns
            
            Keep it professional but accessible.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert oceanographer and climate scientist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"GPT insight generation failed: {e}")
            return self.generate(query_params, statistics, prediction)
