import requests
from zipfile import ZipFile
from io import BytesIO
import pandas as pd
from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

TOP_1M_DOMAINS = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
TOP_1M_DOMAINS_FILE = 'top-1m.csv'

# получаем файл
def get_data():
    top_doms = requests.get(TOP_1M_DOMAINS, stream = True)
    zipfile = ZipFile(BytesIO(top_doms.content))
    top_data = zipfile.read(TOP_1M_DOMAINS_FILE).decode('utf-8')
    
    with open(TOP_1M_DOMAINS_FILE, 'w') as f:
        f.write(top_data)

# находим топ-10 доменных зон по численности доменов
def get_stat_top_doms():
    top_doms = pd.read_csv(TOP_1M_DOMAINS_FILE, names=['rank', 'domain'])
    top_doms['zone'] = top_doms.domain.str.split('.').str[-1]
    top_10_doms = top_doms.zone.value_counts().head(10).reset_index().rename(columns={'index':'zone', 'zone':'count'})
    
    with open('top_10_doms.csv', 'w') as f:
        f.write(top_10_doms.to_csv(index=False, header=False))
        
# найти домен с самым длинным именем (если их несколько, то взять только первый в алфавитном порядке)
def get_stat_long_dom():
    top_doms = pd.read_csv(TOP_1M_DOMAINS_FILE, names=['rank', 'domain'])
    top_doms['length'] = top_doms.domain.str.len()
    longest_dom = top_doms.sort_values('length', ascending=False).head(1)
    
    with open('longest_dom.csv', 'w') as f:
        f.write(longest_dom.to_csv(index=False, header=False))
    
# На каком месте находится домен airflow.com?
def get_stat_domain_place():
    top_doms = pd.read_csv(TOP_1M_DOMAINS_FILE, names=['rank', 'domain'])
    top_doms['length'] = top_doms.domain.str.len()
    top_doms = top_doms.sort_values('length', ascending=False).reset_index(drop=True)
    dom_place = top_doms.query("domain == 'airflow.com'").reset_index().rename(columns={'index':'place'})
    dom_place = dom_place[['domain', 'place']]
    if dom_place.empty:
        result = 'Not in the list'
    else:
        result = dom_place.place
    print(result)
    
    with open('dom_place.txt', 'w') as f:
        f.write(str(result))

def print_data(ds):
    with open('top_10_doms.csv', 'r') as f:
        top_10 = f.read()
    with open('longest_dom.csv', 'r') as f:
        longest_dom = f.read()
    with open('dom_place.txt', 'r') as r:
        dom_place = d.read()
    date = ds    
    
    print(f'Top 10 domain zones for date {date}')
    print(top_10)
    print(f'Longest domain name for date {date}')
    print(longest_dom)
    print(f'"airflow.com" in long domain name rating for date {date}')
    print(dom_place)
        
default_args = {
    'owner': 'a.tarabin',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=3),
    'start_date': datetime(2023, 5, 10),
    'schedule_interval': '/3, *, *, *, *'
    }

dag = DAG('at_dag_l_2', default_args = default_args)        
        
t1 = PythonOperator(task_id = 'get_data',
                    python_callable = get_data,
                    dag = dag)  

t2 = PythonOperator(task_id = 'get_stat_top_doms',
                    python_callable = get_stat_top_doms,
                    dag = dag)

t3 = PythonOperator(task_id = 'get_stat_long_dom',
                    python_callable = get_stat_long_dom,
                    dag = dag)

t4 = PythonOperator(task_id = 'get_stat_domain_place',
                    python_callable = get_stat_domain_place,
                    dag = dag)

t5 = PythonOperator(task_id = 'print_data',
                    python_callable = print_data,
                    dag = dag)

t1 >> [t2,t3,t4] >> t5