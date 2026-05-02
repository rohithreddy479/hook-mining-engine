import re

def calculate_hook_score(hook_text: str) -> int:
    score = 0
    text_lower = hook_text.lower()
    
    has_number = False
    has_curiosity = False
    
    # Contains numbers (+3)
    if re.search(r'\d', hook_text):
        has_number = True
        score += 3
        
    # Contains question mark (+2)
    if '?' in hook_text:
        score += 2
        
    # Uses emotional or strong words (+2)
    strong_words = [r'\bstop\b', r'\bfail\b', r'\bsecret\b', r'\bshocking\b']
    for word_pattern in strong_words:
        if re.search(word_pattern, text_lower):
            score += 2
            break
            
    # Uses curiosity phrasing (+3)
    curiosity_phrases = ["here's what happened", "here’s what happened", "you won't believe", "you won’t believe", "this is why"]
    if any(phrase in text_lower for phrase in curiosity_phrases):
        has_curiosity = True
        score += 3
        
    # Short and punchy (<15 words) (+1)
    word_count = len(hook_text.split())
    if 0 < word_count < 15:
        score += 1
        
    # Bonus: Number + Curiosity (+2)
    if has_number and has_curiosity:
        score += 2
        
    return min(score, 10)

def score_and_rank_hooks(hooks: list[dict]) -> list[dict]:
    for item in hooks:
        hook_text = item.get("hook", "")
        item["score"] = calculate_hook_score(hook_text)
        
    # Sort hooks in descending order of score
    hooks.sort(key=lambda x: x.get("score", 0), reverse=True)
    return hooks
