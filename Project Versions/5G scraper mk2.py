import requests
import os.path
from bs4 import BeautifulSoup

bbc_list = []
tele_list = []
link_list = []

URL_CONVO = 'https://theconversation.com/four-experts-investigate-how-the-5g-coronavirus-conspiracy-theory-began-139137'
URL_BBC = 'https://www.bbc.co.uk/news/53191523'
URL_TELE = 'https://telecoms.com/503845/5g-conspiracy-theories-what-they-are-why-they-are-wrong-and-what-can-be-done/'
URL_WIRED = 'https://www.wired.com/story/the-rise-and-spread-of-a-5g-coronavirus-conspiracy-theory/'
URL_OBSE = 'https://observer.com/2020/08/extreme-5g-conspiracy-theories-where-they-come-from-covid-19/'

bbc_page = requests.get(URL_BBC)
convo_page = requests.get(URL_CONVO)
tele_page = requests.get(URL_TELE)
wired_page = requests.get(URL_WIRED)
obse_page = requests.get(URL_OBSE)

bbc_soup = BeautifulSoup(bbc_page.content, 'html.parser')
convo_soup = BeautifulSoup(convo_page.content, 'html.parser')
tele_soup = BeautifulSoup(tele_page.content, 'html.parser')
wired_soup = BeautifulSoup(wired_page.content, 'html.parser')
obse_soup = BeautifulSoup(obse_page.content, 'html.parser')

'''
if os.path.exists('conspiracyData.txt'):
    print("This file already exists.")
else:
    f = open("conspiracyData.txt", "x")
    print("File has been created.")

#f = open("conspiracyData.txt", "w")
'''

save_path = r"C:\Users\Jake\Desktop\conspiracy_data\nons"

###BBC ARTICLE STRIPPING###
bbc_results = bbc_soup.find_all('div', class_='ssrcss-uf6wea-RichTextComponentWrapper e1xue1i83')

for i in bbc_results:
    bbc_results_formatted = i.text.strip()
    bbc_list.append(bbc_results_formatted)

bbc_list = ' '.join(bbc_list)
bbc_final = bbc_list
'''
bbc_path = os.path.join(save_path, "non_1.txt")
file = open(bbc_path, "x")
file.write(bbc_final)
file.close()
'''
#bbc_final = ""

#print(bbc_final)
#print(len(bbc_final))

###CONVO ARTICLE STRIPPING###
convo_results = convo_soup.find('div', class_='grid-ten large-grid-nine grid-last content-body content entry-content instapaper_body inline-promos')

convo_final = convo_results.text.strip()
'''
convo_path = os.path.join(save_path, "non_2.txt")
file = open(convo_path, "x")
file.write(convo_final)
file.close()
'''

#print(convo_final)
#print(len(convo_final))


###TELE ARTICLE STRIPPING###
#tele_results = tele_soup.find('div', itemprop = 'articleBody')

tele_results = tele_soup.find_all('div', itemprop='articleBody')

for i in tele_results:
    tele_results_formatted = i.text.strip()
    tele_list.append(tele_results_formatted)

tele_list = ''.join(tele_list)
tele_final = tele_list
'''
tele_path = os.path.join(save_path, "non_3.txt")
file = open(tele_path, "x")
file.write(tele_final)
file.close()
'''
#print(tele_final_text)
#print(len(tele_final_text))    

###WIRED ARTICLE STRIPPING###

wired_results = wired_soup.find('div', class_='article__chunks')

wired_final = wired_results.text.strip()
'''
wired_path = os.path.join(save_path, "non_4.txt")
file = open(wired_path, "x")
file.write(wired_final)
file.close()
'''
#print(wired_final)
#print(len(wired_final))

###OBSE ARTICLE STRIPPING###

obse_results = obse_soup.find('div', class_='entry-content')

obse_final = obse_results.text.strip()
'''
obse_path = os.path.join(save_path, "non_5.txt")
file = open(obse_path, "x")
file.write(obse_final)
file.close()
'''
#print(obse_final)
#print(len(obse_final))

con_save_path = r'C:\Users\Jake\Desktop\conspiracy_data\cons'

path_list = []

###### collecting all the links on the web page ######
URL = 'https://projectavalon.net/forum4/forumdisplay.php?187-5G'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='thread_inlinemod_form')

post_elems = results.find_all('li', class_='threadbit')

for elems in post_elems:
    thread_link = elems.find('a', class_='title')['href']
    link_list.append(thread_link)

###### generating the filename and storing it in a list ######
for i in range(0, len(link_list)):
    i = i+1
    new_file_name = "con_" + str(i) + ".txt"
    new_path_name = os.path.join(con_save_path, new_file_name)
    path_list.append(new_path_name)
    #print(new_path_name)

###### taking the first link in the list, editing and removing it ######
print("Number of links in the list: " + str(len(link_list)))
edit = 'https://projectavalon.net/forum4/'

for i in link_list:
    first_link_unedited = i
    first_link_edited = edit + first_link_unedited

###### opening the link and storing the info on the page ######
    new_page = requests.get(first_link_edited)
    new_soup = BeautifulSoup(new_page.content, 'html.parser')
    page_content = new_soup.find('div', class_='content')
    page_content_stripped = page_content.text.strip().replace('\x92', '').replace('\x91', '').replace('\u010d', '').replace('\u0107', '').replace('\x96', '').replace('\x99', '')
    current_path = path_list[0]
    file = open(current_path, "x")
    file.write(str(page_content_stripped))
    file.close()
    path_list.pop(0)

###### pre-processing the non conspiracy theory posts ######





