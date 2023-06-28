import openai
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
TOKEN = os.getenv('OPENAI_TOKEN')

openai.api_key  = TOKEN

def get_completion(messages, temperature=0, max_tokens=500, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    token_dict = {
        'prompt_tokens':response['usage']['prompt_tokens'],
        'completion_tokens':response['usage']['completion_tokens'],
        'total_tokens':response['usage']['total_tokens'],
    }
    content = response.choices[0].message["content"]
    return content, token_dict

delimiter = '####'
system_message = f"""
As ChatGPT, your task is to categorize each query (within {delimiter}) \
and identify the most appropriate engineering team to handle it. \
Provide your output in json format with the keys: \
- primary category
- secondary category
Plus, add your reasoning in a bullet style.

Primary categories: Infra, Ad Exchange System, Data Engineering, \
AI, Data Analysis, Web Backend, Web Frontend, Product, Miscellaneous.

Always make sure to match secondary categories with their respective primary categories as specified.

Data-related queries (loss, recovery, anomalies) should go to Data Engineering.
For CPM or ad issues, consider:
- Dashboard value-setting problems - Web Frontend
- Incorrectly set value/number - Ad Exchange System

Payment, budget, or revenue queries primarily belong to Web Backend.

If the query requires adding new feature which doesn't exist, it belongs to Product.

The primary objective of the Data Analysis team is to provide deep insights and thorough analysis.
They are not responsible for addressing bugs or errors.

For ambiguous queries, request more context.\
Aim for smooth team operations.

Web backend secondary categories:
Advertisers' Budget (charging...)
Media's Revenue Calculation
Tax or Payment related issues
Sever-related tasks for internal dashboards
Content Review and Approval System

Web Frontend secondary categories:
Client-related tasks for internal dashboards
UI issues(HTML, CSS)
Widgets
inserting conversion scripts

Infra secondary categories:
VPN authorization
Cloud management
Cloud deployment system (Spinnaker...)
Cloud-related tasks

Data Engineering secondary categories:
Providing reasons for void clicks and invalid revenue
Fixing Database management
Fixing Data storage, processing and loading
Fixing Statistics
Data recovery from loss
Fraud Detection

AI secondary categories:
Machine Learning
creating DSP model
Targeting algorithms

Data Analysis secondary categories:
Analyzing data for giving long-term business insights
Extracting data for requests
Business Intelligence Tools(redash...)

Ad Exchange System secondary categories:
Ad Campaign & Content pool
CPM setting
DSP integration
Ad exchange server
Kubernetes

Product
Review Possibilities before creating new feature
Refining specification

Miscellaneous
Other ambiguous questions
"""

user_message = f"""\
Invalid Click Refund Rate 조정

현재 제공되는 무효 클릭 보상률을 80% → 40%로 변경. 
무효클릭 보상이 매달 15일에 일어나므로 가능하면 그 전에 변경되어, 이 비용을 절약할 수 있으면 좋겠습니다. 월 약 1천만원 수준의 비용을 아낄 수 있는 것으로 예상하고 있습니다.
"""
messages =  [  
{'role':'system', 
 'content': system_message},    
{'role':'user', 
 'content': f"{delimiter}{user_message}{delimiter}"},  
]

temperature = 0
max_tokens = 1000
response, token_dict = get_completion(messages, temperature, max_tokens)
print(response)
print(token_dict)