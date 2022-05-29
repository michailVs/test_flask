import requests
from bs4 import BeautifulSoup

ITEMS = 100

headers = {
    'Host': 'hh.ru',
    'User-Agent': 'Safari',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}


def extract_max_page(url):
    hh_request = requests.get(url, headers=headers)
    # print(hh_request)
    soup = BeautifulSoup(hh_request.text, 'html.parser')

    pages = []

    pagenator = soup.find_all("span", {'class': 'pager-item-not-in-short-range'})

    for page in pagenator:
        pages.append(int(page.find("a").text))
    return pages[-1]


def extract_job(html):
    title = html.find('a').text
    link = html.find('a')['href']
    # location = html.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})
    return {
        'title': title,
        'link': link
    }


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f'Headhunter: парсинг страницы {page}')
        result = requests.get(f'{url}&page={page}', headers=headers)
        # print(result.status_code)
        bsoup = BeautifulSoup(result.text, 'html.parser')
        results = bsoup.find_all('div', {'class': 'vacancy-serp-item'})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(keyword):
    url = f'https://hh.ru/search/vacancy?area=1&text={keyword}&currency_code=RUR&L_save_area=true&page=0&items_on_page={ITEMS}'
    max_page = extract_max_page(url)
    jobs = extract_jobs(max_page, url)
    return jobs
