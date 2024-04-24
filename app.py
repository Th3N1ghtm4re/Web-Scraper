from flask import Flask, render_template, redirect, url_for, request
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

app = Flask(__name__)

def scrape_urls(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = []
        files = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith("http"):
                urls.append(href)
            elif href.startswith("/"):
                urls.append(urljoin(url, href))
                
        for link in soup.find_all('a', href=re.compile(r'.+\.(pdf|doc|docx|txt|csv|xls|xlsx|ppt|pptx|jpg|jpeg|png|gif|xml|html|htm|mp4|mp3|waf|ico|exe|zip|rar|tar|gz|7z|apk|ipa|deb|rpm|bat|sh|py|java|cpp|c|dll|lib|obj|pdb|class|jar|bak)$')):
            href = link['href']
            if href.startswith("http"):
                files.append(href)
            elif href.startswith("/"):
                files.append(urljoin(url, href))
                
        return {'urls': urls, 'files': files}
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    if request.method == 'POST':
        url = request.form['url']
        return redirect(url_for('scrape_result', url=url))
    return redirect(url_for('index'))

@app.route('/scrape/<path:url>')
def scrape_result(url):
    results = scrape_urls(url)
    urls = results['urls']
    files = results['files']
    return render_template('scrape.html', urls=urls, files=files)

if __name__ == '__main__':
    app.run(port=5002)
