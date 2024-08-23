from bs4 import BeautifulSoup
import requests 
disease = 'disease_name'
letter = disease[0]

html_text = requests.get('https://www.mayoclinic.org/diseases-conditions/index?letter={}'.format(letter)).text

soup = BeautifulSoup(html_text, 'lxml')
data = soup.find('div', class_ = 'cmp-back-to-top-container__children')
contents = data.find_all('div', class_='cmp-link', attrs={'data-testid': 'cmp-button'})

disease_url = None
for content in contents:
    if  content.text.lower() == disease.lower():
        disease_url = content.find('a')['href']
        break

if disease_url:    
    html_text2 = requests.get(disease_url).text
    soup2 = BeautifulSoup(html_text2, 'lxml')

    try:
        data2 = soup2.find('div', class_ = 'content')
        content2 = data2.find('div', class_ = False)
        information = content2.find_all(['p', 'ul', 'h2', 'h3', 'h4'], class_ = False, id = False)
    except AttributeError:
        data2 = soup2.find('div', class_ = 'container-child container-child cmp-column-control__content-column')
        content2 = data2.find('article', attrs={'data-testid': 'cmp-article'})
        information = content2.find_all('section', attrs={'data-testid': 'cmp-section'})           

    with open('data/' + disease + '.txt', 'a') as f:
        for element in information:       
            f.write(element.text + '\n')

