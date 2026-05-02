import requests

def fetch_reddit_posts(niche: str) -> list[str]:
    # Using Reddit search to support multi-word niches
    url = "https://www.reddit.com/search.json"
    params = {
        "q": niche,
        "limit": 20,
        "sort": "top"
    }
    # Reddit requires a custom User-Agent to avoid rate limiting or blocking
    headers = {
        "User-Agent": "HookMiningEngineBot/1.0"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        posts = []
        for child in data.get("data", {}).get("children", []):
            title = child.get("data", {}).get("title")
            if title:
                posts.append(title)
                
        return posts
    except Exception as e:
        print(f"Error fetching Reddit posts: {e}")
        return []
