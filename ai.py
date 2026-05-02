import json
import os
import re
from google import genai
from google.genai import types

def get_fallback_hooks() -> list[dict]:
    return [
        {
            "hook": "He turned down $15M from AI companies — here's what happened next",
            "category": "curiosity",
            "reason": "Creates curiosity gap and uses a strong financial number"
        },
        {
            "hook": "Stop making this common mistake before it costs you your business",
            "category": "bold statement",
            "reason": "Instills urgency and challenges the reader's current practices"
        },
        {
            "hook": "Why do 90% of startups fail within the first year?",
            "category": "question",
            "reason": "Directly engages the reader with a surprising statistic and invites them to find the answer"
        }
    ]

def generate_viral_hooks(post_titles: list[str]) -> list[dict]:
    if not post_titles:
        return get_fallback_hooks()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return get_fallback_hooks()

    # Initialize client using new SDK
    client = genai.Client(api_key=api_key)
    
    titles_text = "\n".join([f"- {title}" for title in post_titles])

    prompt = f"""You are a viral content expert.
Your goal is to transform standard post titles into highly engaging viral hooks.
Keep hooks short, punchy, and scroll-stopping. Avoid generic outputs.

CRITICAL INSTRUCTIONS:
- You must generate AT LEAST 10 hooks.
- Do NOT return empty output under any circumstances.
- If the input titles are weak, you must still generate strong, high-quality hooks based on the topics.

For each hook, generate:
- "hook": The rewritten hook in an engaging viral format.
- "category": Must be strictly one of: "curiosity", "question", or "bold statement".
- "reason": A specific psychological reason why this hook works.

You must output STRICTLY a JSON object with a single key "hooks" containing an array of objects.
Example output format:
{{
  "hooks": [
    {{
      "hook": "He turned down $15M from AI companies — here's what happened next",
      "category": "curiosity",
      "reason": "Creates curiosity gap and uses a strong financial number"
    }}
  ]
}}

Transform these post titles into viral hooks:
{titles_text}
"""

    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash-latest',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        result_text = response.text
        
        # Logging raw output for debugging
        print("--- RAW AI RESPONSE ---")
        print(result_text)
        print("-----------------------")
        
        if not result_text:
            print("Warning: Received empty response from Gemini.")
            return get_fallback_hooks()
            
        # Strip code blocks in case the model wraps the JSON response
        cleaned_text = result_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
        cleaned_text = cleaned_text.strip()
            
        result = json.loads(cleaned_text)
        hooks = result.get("hooks", [])
        
        if not hooks:
            return get_fallback_hooks()
            
        return hooks
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing failed. Parse error: {e}")
        # Advanced regex fallback to extract just the array
        try:
            match = re.search(r'\[\s*\{.*?\}\s*\]', result_text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except Exception:
            pass
        return get_fallback_hooks()
    except Exception as e:
        print(f"Error in AI processing: {e}")
        return get_fallback_hooks()
