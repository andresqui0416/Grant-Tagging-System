import re
import json
from typing import List, Dict, Set
import openai
import os
from dotenv import load_dotenv

load_dotenv()

class GrantTaggingService:
    def __init__(self):
        # Predefined tags from the requirements
        self.predefined_tags = [
            "agriculture", "aquaculture", "capacity-building", "capital", "climate",
            "community-benefit", "conservation", "cost-share", "dairy", "distribution",
            "drought", "education", "equipment", "equine", "equine-owners", "food-safety",
            "farmer", "farm-to-school", "grant", "infrastructure", "irrigation", "local-food",
            "local-government", "logistics", "marketing", "mixed-operations", "nonprofit",
            "nutrient-management", "operational", "organic-certification", "organic-transition",
            "outreach", "planning", "pilot", "producer-group", "procurement", "processing",
            "research", "resilience", "reimbursement", "rolling", "rural", "safety-net",
            "school", "seafood", "seafood-harvester", "soil", "supply-chain", "technical-assistance",
            "training", "value-added", "water", "water-storage", "working-capital", "row-crops",
            "vegetables", "fruit", "livestock", "competitive", "match-required", "public-entity-eligible",
            "individual-eligible", "rfa-open", "wi", "va", "ri", "nh", "mn", "me", "ky", "co",
            "cooperative", "for-profit", "university", "extension", "tribal", "veteran",
            "beginning-farmer", "underserved", "youth", "food-access", "nutrition", "workforce",
            "energy", "renewable-energy", "water-quality", "soil-health", "wildlife-habitat",
            "pasture", "grazing", "manure-management", "disaster-relief", "flood"
        ]
        
        # Initialize OpenAI client if API key is available
        self.openai_client = None
        if os.getenv('OPENAI_API_KEY'):
            try:
                self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            except Exception as e:
                print(f"Warning: Failed to initialize OpenAI client: {e}")
                print("Continuing without LLM-enhanced tagging...")
                self.openai_client = None
        
        # Create keyword mappings for better string matching
        self.keyword_mappings = self._create_keyword_mappings()
    
    def _create_keyword_mappings(self) -> Dict[str, List[str]]:
        """Create keyword mappings for improved string matching"""
        return {
            "agriculture": ["agriculture", "agricultural", "farming", "farm", "farmer", "farmers"],
            "education": ["education", "educational", "learning", "teach", "training", "workshop"],
            "sustainability": ["sustainable", "sustainability", "environmental", "eco-friendly"],
            "conservation": ["conservation", "conserving", "preserve", "protection"],
            "water": ["water", "irrigation", "drought", "water-storage", "water-quality"],
            "soil": ["soil", "nutrient", "nutrient-management", "soil-health"],
            "research": ["research", "studies", "investigation", "analysis"],
            "infrastructure": ["infrastructure", "facilities", "buildings", "construction"],
            "equipment": ["equipment", "machinery", "tools", "technology"],
            "marketing": ["marketing", "promotion", "advertising", "branding"],
            "local-food": ["local food", "local-food", "locally sourced", "regional"],
            "farm-to-school": ["farm to school", "farm-to-school", "school meals"],
            "organic": ["organic", "organic-certification", "organic-transition"],
            "dairy": ["dairy", "milk", "cattle", "cows"],
            "livestock": ["livestock", "animals", "cattle", "poultry", "sheep"],
            "equine": ["equine", "horse", "horses", "equestrian"],
            "seafood": ["seafood", "fish", "fishing", "aquaculture"],
            "youth": ["youth", "young", "students", "children", "kids"],
            "rural": ["rural", "countryside", "remote", "small town"],
            "disaster-relief": ["disaster", "emergency", "relief", "crisis"],
            "climate": ["climate", "weather", "environmental", "greenhouse"],
            "energy": ["energy", "renewable", "solar", "wind", "power"],
            "nutrition": ["nutrition", "healthy", "food access", "hunger"],
            "workforce": ["workforce", "employment", "jobs", "career"],
            "beginning-farmer": ["beginning farmer", "new farmer", "startup"],
            "underserved": ["underserved", "disadvantaged", "minority", "low-income"],
            "veteran": ["veteran", "military", "service member"],
            "tribal": ["tribal", "native", "indigenous", "reservation"],
            "cooperative": ["cooperative", "co-op", "collective", "partnership"],
            "nonprofit": ["nonprofit", "non-profit", "charity", "foundation"],
            "university": ["university", "college", "academic", "institution"],
            "extension": ["extension", "outreach", "advisory", "consulting"],
            "pilot": ["pilot", "test", "trial", "demonstration"],
            "competitive": ["competitive", "competition", "award", "prize"],
            "match-required": ["match", "matching", "cost-share", "co-funding"],
            "reimbursement": ["reimbursement", "reimburse", "refund", "repayment"],
            "rolling": ["rolling", "continuous", "ongoing", "open"],
            "rfa-open": ["rfa", "request for applications", "open", "available"]
        }
    
    def assign_tags(self, grant_name: str, grant_description: str) -> List[str]:
        """
        Assign relevant tags to a grant based on its name and description
        """
        # Combine name and description for analysis
        full_text = f"{grant_name} {grant_description}".lower()
        
        # Get tags from string matching
        string_match_tags = self._string_matching_tags(full_text)
        
        # Get tags from LLM analysis if available
        llm_tags = []
        if self.openai_client:
            try:
                print("Using LLM for tagging...")
                llm_tags = self._llm_tagging(grant_name, grant_description)
            except Exception as e:
                print(f"LLM tagging failed: {e}")
        
        # Combine and deduplicate tags
        all_tags = list(set(string_match_tags + llm_tags))
        
        # Filter to only include predefined tags
        valid_tags = [tag for tag in all_tags if tag in self.predefined_tags]
        
        return valid_tags
    
    def _string_matching_tags(self, text: str) -> List[str]:
        """Extract tags using string matching"""
        matched_tags = set()
        
        # Direct tag matching
        for tag in self.predefined_tags:
            if tag.replace("-", " ") in text or tag in text:
                matched_tags.add(tag)
        
        # Keyword-based matching
        for tag, keywords in self.keyword_mappings.items():
            for keyword in keywords:
                if keyword in text:
                    matched_tags.add(tag)
        
        # Special case matching for compound terms
        if "farm to school" in text or "farm-to-school" in text:
            matched_tags.add("farm-to-school")
        
        if "local food" in text or "local-food" in text:
            matched_tags.add("local-food")
        
        if "nutrient management" in text or "nutrient-management" in text:
            matched_tags.add("nutrient-management")
        
        if "organic transition" in text or "organic-transition" in text:
            matched_tags.add("organic-transition")
        
        if "organic certification" in text or "organic-certification" in text:
            matched_tags.add("organic-certification")
        
        return list(matched_tags)
    
    def _llm_tagging(self, grant_name: str, grant_description: str) -> List[str]:
        """Use OpenAI to assign tags based on semantic understanding"""
        if not self.openai_client:
            return []
        
        prompt = f"""
        Analyze this grant and assign relevant tags from the predefined list.
        
        Grant Name: {grant_name}
        Grant Description: {grant_description}
        
        Available Tags: {', '.join(self.predefined_tags)}
        
        Return only the most relevant tags (3-8 tags) as a JSON array. 
        Only use tags from the predefined list above.
        Focus on the main themes and purposes of the grant.
        
        Example format: ["agriculture", "education", "research"]
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.3
            )
            
            # Parse the JSON response
            tags_text = response.choices[0].message.content.strip()
            # Remove markdown formatting if present
            tags_text = tags_text.replace("```json", "").replace("```", "").strip()
            
            tags = json.loads(tags_text)
            return tags if isinstance(tags, list) else []
            
        except Exception as e:
            print(f"Error in LLM tagging: {e}")
            return []
    
    def get_available_tags(self) -> List[str]:
        """Return the list of available tags"""
        return self.predefined_tags
