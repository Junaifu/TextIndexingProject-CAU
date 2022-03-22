import os
from urllib.parse import quote

from bs4 import BeautifulSoup
import requests

BASE_URL = 'http://www.imsdb.com'
SCRIPTS_DIR = 'scripts_Tony'


def clean_script(text):
    text = text.replace('Back to IMSDb', '')
    text = text.replace('''<b><!--
</b>if (window!= top)
top.location.href=location.href
<b>// -->
</b>
''', '')
    text = text.replace('''          Scanned by http://freemoviescripts.com
          Formatting by http://simplyscripts.home.att.net
''', '')
    return text.replace(r'\r', '')

def get_genres(page_html):
    tableDetail = page_html.find_all('table', class_="script-details")[0]
    genreInTableDetail = tableDetail.find_all("a", href=lambda href: href and "/genre" in href)
    genres = []
    for a in genreInTableDetail:
        genres.append(a.text)
    print(genres)
    return genres

def get_writers(page_html):
    tableDetail = page_html.find_all('table', class_="script-details")[0]
    writerInTableDetail = tableDetail.find_all("a", href=lambda href: href and "/writer" in href)
    writers = []
    for a in writerInTableDetail:
        writers.append(a.text)
    print(writers)
    return writers


def get_script(relative_link):
    tail = relative_link.split('/')[-1]
    print('fetching %s' % tail)
    script_front_url = BASE_URL + quote(relative_link)
    front_page_response = requests.get(script_front_url)
    front_soup = BeautifulSoup(front_page_response.text, "html.parser")
    try:
        script_link = front_soup.find_all('p', align="center")[0].a['href']
    except IndexError:
        print('%s has no script :(' % tail)
        return None, None

    genres = get_genres(front_soup)
    writers = get_writers(front_soup)
    if script_link.endswith('.html'):
        title = script_link.split('/')[-1].split(' Script')[0]
        script_url = BASE_URL + script_link
        script_soup = BeautifulSoup(requests.get(script_url).text, "html.parser")
        script_text = script_soup.find_all('td', {'class': "scrtext"})[0].get_text()
        script_text = clean_script(script_text)
        return title + "@" + ",".join(genres) + "@" + ",".join(writers) , script_text
    else:
        print('%s is a pdf :(' % tail)
        return None, None


if __name__ == "__main__":
    response = requests.get('https://imsdb.com/all-scripts.html')
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    counter = 824
    paragraphs = soup.find_all('p')[counter:]
    for p in paragraphs:
        relative_link = p.a['href']
        title, script = get_script(relative_link)
        if not script:
            continue

        with open(os.path.join(SCRIPTS_DIR, title.strip('.html') + '.txt'), 'w', encoding="utf-8") as outfile:
            outfile.write(script)
