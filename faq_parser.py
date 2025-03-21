import requests
from bs4 import BeautifulSoup
from vector_store import VectorStore


def scrape_faq(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    faqs = []
    
    # Adjusting selectors based on actual HTML structure
    faq_section = soup.find('section', class_='faq-wrap')
    if not faq_section:
        print(f"FAQ section not found on {url}.")
        return None
    
    faq_items = faq_section.find_all('li')  # Finding all FAQ list items
    
    for item in faq_items:
        question = item.find('strong')  # Find the question inside <strong>
        answer = item.find('p', class_='para')  # Find the answer inside <p class='para'>
        
        if question and answer:
            faqs.append({"question": question.get_text(strip=True), "answer": answer.get_text(strip=True)})
    
    if not faqs:
        print(f"No FAQs found on {url}. Check the HTML structure.")
    
    return faqs

urls = [
    "https://aranya.gov.in/aranyacms/(S(kk0ft5sbjw5x0b1cg0nycyng))/English/IndividualService.aspx?X+lcPlkH9QY=",
    "https://aranya.gov.in/aranyacms/(S(kk0ft5sbjw5x0b1cg0nycyng))/English/IndividualService.aspx?u15HOwzBSyuVSOgOGs9sAQ==",
    "https://aranya.gov.in/aranyacms/(S(kk0ft5sbjw5x0b1cg0nycyng))/English/IndividualService.aspx?SrB+W5OgJfH92gViz24j0w=="
]

all_faqs = {}

for url in urls:
    faqs = scrape_faq(url)
    if faqs:
        all_faqs[url] = faqs

doc = []
# Print extracted FAQs
for url, faqs in all_faqs.items():
    print(f"FAQs from {url}:")
    for faq in faqs:
        print("Q : ", faq['question'])
        print("A : ", faq['answer'])


