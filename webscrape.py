from bs4 import BeautifulSoup
import pandas as pd
import requests

search_terms = [f'python%20developer', f'java%20developer', f'C%2B%2B%20Developer']
job_terms = ['Python Developer', 'Java Developer', 'C++ Developer']

def extract(page, term):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}
    url = f'https://www.indeed.com/jobs?q={term}&l=Minnesota&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'lxml')
    return soup


def transform(soup):
    listings = soup.find_all('div', class_='slider_container')
    for item in listings:
        job_title = item.find('h2').find(class_=None).text
        company = item.find('span', class_='companyName').text
        try:
            salary = item.find('span', class_='salary-snippet').text
        except:
            salary = ''
        summary = item.find('div', class_='job-snippet').text.strip().replace('\n',' ')

        job = {
            'title': job_title,
            'company': company,
            'salary': salary,
            'summary': summary
        }
        joblist.append(job)
    return

def get_salary(listing):
    temp = listing['salary'].replace(',', '').replace('$', '') #gets rid of extra symbols in numbers
    salary_range = [int(i) for i in temp.split() if i.isdigit()]
    final_salary = 0
    for num in salary_range:
        final_salary += num
    if len(salary_range) != 0:
        return final_salary // len(salary_range)
    return 0


def find_avg_salary():
    avg_salary = num_salary = 0
    for listing in joblist:
        if listing['salary'] != '':
            salary = get_salary(listing)
            avg_salary += salary
            num_salary = num_salary + 1
            if salary < 1000:
                salary *= 2000 # turn hourly wage into yearly wage
    avg_salary_job = {
        'title': 'Average Salary',
        'company': '',
        'salary': round(avg_salary//num_salary, -3),
        'summary': '' 
    }
    return avg_salary_job

for i in range (len(search_terms)):
    joblist = []

    # get first 5 pages of listings
    for page in range(0, 40, 10):
        print(f'Getting data on page: {page//10}')
        c = extract(page, search_terms[i])
        transform(c)
    joblist.append(find_avg_salary())

    job_listings_csv = pd.DataFrame(joblist)
    job_listings_csv.to_csv(f'{job_terms[i]}.csv')

    job_listings_excel = pd.DataFrame(joblist)
    job_listings_excel.to_excel(f'{job_terms[i]}.xlsx')