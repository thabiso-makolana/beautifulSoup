from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

myurl = "https://stackoverflow.com/questions/415511/how-to-get-the-current-time-in-python"

# Create a request with a User-Agent header to avoid being blocked
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
req = Request(url=myurl, headers=headers)
html = urlopen(req).read()
soupified = BeautifulSoup(html, "html.parser")

# Updated selectors for current Stack Overflow HTML structure
question_container = soupified.find("div", {"data-questionid": "415511"})
if not question_container:
    question_container = soupified.find("div", {"id": "question"})
    
questiontext = question_container.find("div", {"class": "s-prose"})

print("Question: \n", questiontext.get_text().strip())

# Find the accepted answer or the first answer
accepted_answer = soupified.find("div", {"class": "answer", "itemprop": "acceptedAnswer"})
if not accepted_answer:
    accepted_answer = soupified.find("div", {"class": "answer"})

answertext = accepted_answer.find("div", {"class": "s-prose"})
print("Best answer: \n", answertext.get_text().strip())