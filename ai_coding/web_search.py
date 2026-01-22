"""
Web Search Integration for Real-time Information
"""
from typing import Dict, List, Optional
import requests
import os


class WebSearch:
    """Web search integration"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GOOGLE_SEARCH_API_KEY')
        self.search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
        self.api_url = "https://www.googleapis.com/customsearch/v1"
    
    def search(self, query: str, num_results: int = 5) -> Dict:
        """Search the web"""
        if not self.api_key or not self.search_engine_id:
            return {
                'success': False,
                'error': 'Search API not configured. Set GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_ENGINE_ID'
            }
        
        params = {
            'key': self.api_key,
            'cx': self.search_engine_id,
            'q': query,
            'num': num_results
        }
        
        try:
            response = requests.get(self.api_url, params=params, timeout=10)
            result = response.json()
            
            if 'items' in result:
                items = []
                for item in result['items']:
                    items.append({
                        'title': item.get('title'),
                        'link': item.get('link'),
                        'snippet': item.get('snippet')
                    })
                
                return {
                    'success': True,
                    'query': query,
                    'results': items,
                    'total': len(items)
                }
            else:
                return {
                    'success': False,
                    'error': 'No results found'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def search_and_summarize(self, query: str, llm=None) -> Dict:
        """Search and summarize results"""
        search_result = self.search(query)
        
        if not search_result.get('success'):
            return search_result
        
        if not llm:
            return search_result
        
        # Summarize results
        results_text = "\n".join([
            f"{i+1}. {r['title']}: {r['snippet']}"
            for i, r in enumerate(search_result['results'])
        ])
        
        prompt = f"""Summarize these search results for the query: {query}

Results:
{results_text}

Provide a concise summary."""
        
        try:
            summary = llm.chat(prompt)
            return {
                'success': True,
                'query': query,
                'summary': summary,
                'results': search_result['results']
            }
        except:
            return search_result
