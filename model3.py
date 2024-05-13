from openai import OpenAI
from fastapi import FastAPI, Body
import os


api_key = os.getenv('OPEN_AI_API')

client = OpenAI(api_key=f"{api_key}")


def check_resume() -> str :
  response = client.chat.completions.create(
  model="gpt-3.5-turbo-0125",
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": "You are a expert in predicting sales in json format"},
    {"role": "user", "content": "the dataset below is of a company . predict the sales of this company for the next 30 days\n\n\"Date\": [\"2024-05-01\", \"2024-05-02\", \"2024-05-03\", \"2024-05-04\", \"2024-05-05\", \"2024-05-06\", \"2024-05-07\", \"2024-05-08\", \"2024-05-09\", \"2024-05-10\", \"2024-05-11\", \"2024-05-12\", \"2024-05-13\", \"2024-05-14\", \"2024-05-15\", \"2024-05-16\", \"2024-05-17\", \"2024-05-18\", \"2024-05-19\", \"2024-05-20\", \"2024-05-21\", \"2024-05-22\", \"2024-05-23\", \"2024-05-24\", \"2024-05-25\", \"2024-05-26\", \"2024-05-27\", \"2024-05-28\", \"2024-05-29\", \"2024-05-30\"],\"Price per unit_x\": [ 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030],\"Volume_x\": [2010, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100, 2110, 2120, 2130, 2140, 2150, 2160, 2170, 2180, 2190, 2200, 2210, 2220, 2230, 2240, 2250, 2260, 2270, 2280, 2290, 2300],\"Price per unit_y\": [1501, 1502, 1503, 1504, 1505, 1506, 1507, 1508, 1509, 1510, 1511, 1512, 1513, 1514, 1515, 1516, 1517, 1518, 1519, 1520, 1521, 1522, 1523, 1524, 1525, 1526, 1527, 1528, 1529, 1530\",Volume_y\": [ 3010, 3020, 3030, 3040, 3050, 3060, 3070, 3080, 3090, 3100, 3110, 3120, 3130, 3140, 3150, 3160, 3170, 3180, 3190, 3200, 3210, 3220, 3230, 3240, 3250, 3260, 3270, 3280, 3290, 3300],\"Price per unit\": [ 2501, 2502, 2503, 2504, 2505, 2506, 2507, 2508, 2509, 2510, 2511, 2512, 2513, 2514, 2515, 2516, 2517, 2518, 2519, 2520, 2521, 2522, 2523, 2524, 2525, 2526, 2527, 2528, 2529, 2530],\"Volume\": [4010, 4020, 4030, 4040, 4050, 4060, 4070, 4080, 4090, 4100, 4110, 4120, 4130, 4140, 4150, 4160, 4170, 4180, 4190, 4200, 4210, 4220, 4230, 4240, 4250, 4260, 4270, 4280, 4290, 4300],\"Sales\": [501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530]\n\nOnly give met he sales values aloung with the date nothing else\n"}
  ]
)
  return(response.choices[0].message.content)
    
  
  


