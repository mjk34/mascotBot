import random, requests
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
from typing import Iterable, Union
from dateutil import parser
from pytz import timezone

est = timezone('EST')

"""Replaces a character in all string of a list"""
def replaceList (list_of_strings:list, old:str, new:str) -> list:
    for i in range(len(list_of_strings)):
        list_of_strings[i] = list_of_strings[i].replace(old, new)
    return list_of_strings

"""Fetches each line of a text file in a list"""
def fetchContentList (filename) -> list:
    lines = []
    with open(f'./messages/{filename}', 'r') as file:
        lines = file.readlines()
    return replaceList(lines, '\n', '')

"""Fetches today's date"""
def today () -> str:
    time = datetime.now(est)
    return str(time.strftime('%m-%d-%y'))

"""Fetches the current monday"""
def thisMonday () -> str:
    today = datetime.now(est)
    weekday =  datetime.weekday(today)

    if weekday == 0: return str(today.strftime('%m-%d-%y'))
    else: 
        monday = today + timedelta(days=-weekday)
        return str(monday.strftime('%m-%d-%y'))

"""Checks if the designated monday is the current monday"""
def checkMonday (block_date) -> bool:
    block_datetime = parser.parse(block_date)
    block_week = datetime.weekday(block_datetime)
    block_monday = ''

    if block_week == 0: 
        block_monday = str(block_datetime.strftime('%m-%d-%y'))
    else:
        temp_monday = block_datetime + timedelta(days=-block_week)
        block_monday = str(temp_monday.strftime('%m-%d-%y'))

    if block_monday == thisMonday(): return True
    return False

"""Randomly generate luck based on values 1-1001"""
def dailyLuck () -> Iterable[Union[int, str]]:
    luck = random.randint(1, 1006)
    cred_amount, cred_status = 0, ''

    if luck <= 350: 
        cred_amount = random.randint(100, 250)
        cred_status = '*Nyani desu...*'
    if luck > 350 and luck <= 600: 
        cred_amount = random.randint(250, 400)
        cred_status = '*Very Nyice*.'
    if luck > 600 and luck <= 800: 
        cred_amount = random.randint(400, 500)
        cred_status = '**P-Poggerz!**,'
    if luck > 800 and luck <= 1000:
        cred_amount = random.randint(500, 700)
        cred_status = '***Nyaaaa!!***,'
    if luck > 1000:
        cred_amount = 2000
        cred_status = 'RNJesus has blessed you, '
    return cred_amount, cred_status

"""Randomly generate fortune readings from fortune-api"""
def dailyFortune () -> str:
    response = requests.get('https://fungenerators.com/random/fortune-cookie/')
    soup = BeautifulSoup(response.content, 'html.parser')
    contents = soup.find('h2').get_text()

    return str('\"' + contents + '\"')

"""Fetch discord user's Name by Id"""
async def getName(id, client) -> str:
    user_object = await client.fetch_user(id)
    return str(user_object.name)

if __name__ == '__main__':
    print(checkMonday('9-13-2022'))
    print(checkMonday('9-12-2022'))