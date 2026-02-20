"""
Query Parser module
Converts natural language queries into structured JSON using LLM
"""

import openai
import os
import json
from typing import Dict, Optional

class QueryParser:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the query parser with OpenAI API
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
    
    def parse(self, user_query: str) -> Dict:
        """
        Parse natural language query into structured format
        
        Args:
            user_query: Natural language query from user
            
        Returns:
            Dictionary with region, parameter, start_year, end_year
        """
        
        # For demo/hackathon: Simple keyword extraction
        # In production: Use OpenAI GPT to parse
        
        query_lower = user_query.lower()
        
        # Extract parameters
        params = {
            "region": self._extract_region(query_lower),
            "parameter": self._extract_parameter(query_lower),
            "start_year": self._extract_year(query_lower, "start"),
            "end_year": self._extract_year(query_lower, "end")
        }
        
        return params
    
    def _extract_region(self, query: str) -> Optional[str]:
        """Extract region from query"""
        regions = {
            "indian ocean": "Indian Ocean",
            "pacific": "Pacific Ocean",
            "atlantic": "Atlantic Ocean",
            "arctic": "Arctic Ocean",
            "southern": "Southern Ocean"
        }
        
        for key, value in regions.items():
            if key in query:
                return value
        
        return None
    
    def _extract_parameter(self, query: str) -> Optional[str]:
        """Extract parameter from query"""
        parameters = {
            "temperature": "temperature",
            "temp": "temperature",
            "salinity": "salinity",
            "salt": "salinity",
            "oxygen": "oxygen",
            "pressure": "pressure"
        }
        
        for key, value in parameters.items():
            if key in query:
                return value
        
        return None
    
    def _extract_year(self, query: str, year_type: str) -> Optional[int]:
        """Extract years from query"""
        import re
        
        # Find all 4-digit numbers that look like years
        years = re.findall(r'\b(19\d{2}|20\d{2})\b', query)
        
        if not years:
            return None
        
        years = [int(y) for y in years]
        
        if year_type == "start":
            return min(years)
        elif year_type == "end":
            return max(years)
        
        return None
    
    def parse_with_gpt(self, user_query: str) -> Dict:
        """
        Parse query using OpenAI GPT (for production)
        """
        if not self.api_key:
            return self.parse(user_query)
        
        try:
            system_prompt = """You are an ocean data query parser. 
            Convert natural language queries into structured JSON with these fields:
            - region (e.g., "Indian Ocean", "Pacific Ocean")
            - parameter (e.g., "temperature", "salinity", "oxygen")
            - start_year (integer)
            - end_year (integer)
            
            Return only valid JSON."""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                temperature=0
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"GPT parsing failed: {e}")
            return self.parse(user_query)
