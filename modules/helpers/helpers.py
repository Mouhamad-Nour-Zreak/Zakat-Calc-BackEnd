from modules.questioning.QuestionEngine import QuestionEngine
from Data.questions import questions
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class Helper:
    @staticmethod
    def ask(id,type=str,*args):
        question_engine = QuestionEngine(questions[id],args)
        question_engine.reset()
        question_engine.run()
        return type(question_engine.get_collector().get(questions[id]['key']))

    @staticmethod
    def thaw_frozen(obj):
        """
        Recursively converts frozen containers (frozendict, frozenlist) to their mutable equivalents.
        Handles nested structures of any combination of frozen/mutable containers.
        
        Args:
            obj: Input data structure that may contain frozendicts and frozenlists
            
        Returns:
            A new structure with all frozen containers converted to regular mutable ones
        """
        if isinstance(obj, dict) or hasattr(obj, 'items'):  
            return {key: Helper.thaw_frozen(value) for key, value in obj.items()}

        elif isinstance(obj, list) or hasattr(obj, '__class__') and obj.__class__.__name__ == 'frozenlist':
            return [Helper.thaw_frozen(item) for item in obj]

        elif isinstance(obj, tuple):
            if any(hasattr(item, '__class__') and item.__class__.__name__ in ('frozendict', 'frozenlist') for item in obj):
                return tuple(Helper.thaw_frozen(item) for item in obj)
            return obj

        elif isinstance(obj, set):
            if any(hasattr(item, '__class__') and item.__class__.__name__ in ('frozendict', 'frozenlist') for item in obj):
                return {Helper.thaw_frozen(item) for item in obj}
            return obj

        return obj

    @staticmethod
    def get_metal_price(symbol = "XAU"):
        if symbol == "XAU":
            return {"price_gram_24k" : 109}
        if symbol == "XAG":
            return {"price_gram_24k": 1.25}
        if symbol not in ["XAU","XAG"]:
            return None
        api_key = os.getenv("GOLD_API_KEY")
        if not api_key:
            raise ValueError("GOLD_API_KEY not found in environment variables")

        curr = "USD"
        date = ""

        url = f"https://www.goldapi.io/api/{symbol}/{curr}{date}"

        headers = {
            "x-access-token": api_key,
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()  # Better to return parsed JSON
        except requests.exceptions.RequestException as e:
            print("Error:", str(e))
            return None
