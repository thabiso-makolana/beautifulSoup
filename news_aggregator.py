import requests
from bs4 import BeautifulSoup
import time

def scrape_bbc_news():
    # Send a GET request to BBC News
    url = "https://www.bbc.com/news"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            print("\nTOP STORIES FROM BBC NEWS:")
            print("=" * 50)
            
            # The BBC News site has headline elements that we can target directly
            headlines = soup.find_all(['h1', 'h2', 'h3'])
            
            top_stories = []
            for headline in headlines:
                headline_text = headline.text.strip()
                if headline_text and len(headline_text) > 10 and len(headline_text) < 100:
                    # Filter out navigation and other non-story headlines
                    if not any(x in headline_text.lower() for x in ['bbc', 'sign in', 'search', 'menu', 'more from bbc']):
                        top_stories.append(headline_text)
            
            # Remove duplicates while preserving order
            unique_stories = []
            for story in top_stories:
                if story not in unique_stories:
                    unique_stories.append(story)
            
            # Display top stories (limit to 10)
            for i, story in enumerate(unique_stories[:10], 1):
                print(f"{i}. {story}")
                print("-" * 50)
            
            # Try to find category sections
            print("\nNEWS BY CATEGORY:")
            print("=" * 50)
            
            categories = ['World', 'UK', 'Business', 'Technology', 'Science']
            
            for category in categories:
                print(f"\n{category.upper()} NEWS:")
                
                # Method 1: Try to find category section headings
                category_section = None
                for heading in soup.find_all(['h2', 'h3']):
                    if category.lower() in heading.text.lower():
                        category_section = heading.parent
                        break
                
                category_stories = []
                
                # Method 2: Use keyword matching on stories
                for story in unique_stories:
                    # This is simplified categorization based on keywords
                    if any(keyword.lower() in story.lower() for keyword in [
                        category.lower(), 
                        category[:4].lower(),
                        # Common keywords for each category
                        *{
                            'World': ['country', 'nation', 'international', 'foreign'],
                            'UK': ['britain', 'british', 'england', 'scotland', 'wales', 'london'],
                            'Business': ['company', 'market', 'economy', 'trade', 'finance'],
                            'Technology': ['tech', 'digital', 'computer', 'ai', 'robot', 'app'],
                            'Science': ['research', 'study', 'scientist', 'discovery']
                        }.get(category, [])
                    ]):
                        category_stories.append(story)
                
                if category_stories:
                    for i, story in enumerate(category_stories[:3], 1):
                        print(f"{i}. {story}")
                        print("-" * 40)
                else:
                    print("No relevant stories found in this category.")
                    print("-" * 40)
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        
        # Fallback to demonstrate structure with sample data
        print("\nUsing sample data for demonstration:")
        sample_stories = [
            "Ukraine and Russia in deadlock at peace talks",
            "Climate protests disrupt major cities worldwide",
            "Tech giants face new regulations in European Union",
            "Scientists discover potential new treatment for cancer",
            "Global economy shows signs of recovery despite inflation",
            "New AI breakthrough could transform healthcare",
            "UK announces major infrastructure investment plan",
            "Space mission discovers evidence of water on distant planet",
            "Business leaders call for action on climate change",
            "Technology firms announce major job cuts amid economic uncertainty"
        ]
        
        print("\nTOP STORIES (SAMPLE DATA):")
        print("=" * 50)
        for i, story in enumerate(sample_stories, 1):
            print(f"{i}. {story}")
            print("-" * 50)

if __name__ == "__main__":
    scrape_bbc_news()