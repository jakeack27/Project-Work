import requests
import os.path
from bs4 import BeautifulSoup

con_label = 'con'
non_label = 'non'

link_list = []
contents_list = []

URL_CONVO = 'https://theconversation.com/four-experts-investigate-how-the-5g-coronavirus-conspiracy-theory-began-139137'
URL_BBC = 'https://www.bbc.co.uk/news/53191523'
URL_TELE = 'https://telecoms.com/503845/5g-conspiracy-theories-what-they-are-why-they-are-wrong-and-what-can-be-done/'
URL_WIRED = 'https://www.wired.com/story/the-rise-and-spread-of-a-5g-coronavirus-conspiracy-theory/'
URL_OBSE = 'https://observer.com/2020/08/extreme-5g-conspiracy-theories-where-they-come-from-covid-19/'
URL_FULL = 'https://fullfact.org/online/5g-and-coronavirus-conspiracy-theories-came/'
URL_POP = 'https://www.popularmechanics.com/technology/infrastructure/a34025852/are-5g-towers-safe/'
URL_VOX = 'https://www.vox.com/recode/2020/4/24/21231085/coronavirus-5g-conspiracy-theory-covid-facebook-youtube'
URL_NPR = 'https://www.npr.org/2020/07/10/889037310/anatomy-of-a-covid-19-conspiracy-theory?t=1617104419213'
URL_EURO = 'https://www.euronews.com/2020/05/15/what-is-the-truth-behind-the-5g-coronavirus-conspiracy-theory-culture-clash'
URL_SKY = 'https://news.sky.com/story/coronavirus-father-of-three-who-searched-for-5g-conspiracy-theories-online-jailed-for-arson-attack-on-phone-mast-12002914'

bbc_page = requests.get(URL_BBC)
convo_page = requests.get(URL_CONVO)
tele_page = requests.get(URL_TELE)
wired_page = requests.get(URL_WIRED)
obse_page = requests.get(URL_OBSE)
full_page = requests.get(URL_FULL)
pop_page = requests.get(URL_POP)
vox_page = requests.get(URL_VOX)
npr_page = requests.get(URL_NPR)
euro_page = requests.get(URL_EURO)
sky_page = requests.get(URL_SKY)

bbc_soup = BeautifulSoup(bbc_page.content, 'html.parser')
convo_soup = BeautifulSoup(convo_page.content, 'html.parser')
tele_soup = BeautifulSoup(tele_page.content, 'html.parser')
wired_soup = BeautifulSoup(wired_page.content, 'html.parser')
obse_soup = BeautifulSoup(obse_page.content, 'html.parser')
full_soup = BeautifulSoup(full_page.content, 'html.parser')
pop_soup = BeautifulSoup(pop_page.content, 'html.parser')
vox_soup = BeautifulSoup(vox_page.content, 'html.parser')
npr_soup = BeautifulSoup(npr_page.content, 'html.parser')
euro_soup = BeautifulSoup(euro_page.content, 'html.parser') 
sky_soup = BeautifulSoup(sky_page.content, 'html.parser')

if os.path.exists('scraperTest.txt'):
    print("This file already exists.")
else:
    f = open("scraperTest.txt", "x")
    print("File has been created.")

f = open("scraperTest.txt", "w")


###BBC ARTICLE STRIPPING###
bbc_list = []
bbc_results = bbc_soup.find_all('div', class_='ssrcss-uf6wea-RichTextComponentWrapper e1xue1i83')

for i in bbc_results:
    bbc_results_formatted = i.text.strip()
    contents_list.append(bbc_results_formatted)

#contents_list = ' '.join(contents_list)
bbc_final = ' '.join(contents_list)
contents_list.clear()
bbc_final = bbc_final.replace('\n', ' ')

f.write(non_label+'\t'+bbc_final+'\n')

#print(bbc_final)
#print(len(bbc_final))

###CONVO ARTICLE STRIPPING###
convo_results = convo_soup.find('div', class_='grid-ten large-grid-nine grid-last content-body content entry-content instapaper_body inline-promos')

convo_final = convo_results.text.strip().replace('\n', ' ')

f.write(non_label+'\t'+convo_final+'\n')

#print(convo_final)
#print(len(convo_final))

###TELE ARTICLE STRIPPING###
tele_list = []
tele_results = tele_soup.find_all('div', itemprop='articleBody')

for i in tele_results:
    tele_results_formatted = i.text.strip()
    contents_list.append(tele_results_formatted)

tele_final = ''.join(contents_list)
contents_list.clear()
tele_final = tele_final.replace('\n', ' ')

f.write(non_label+'\t'+tele_final+'\n')

#print(tele_final)
#print(len(tele_final))    

###WIRED ARTICLE STRIPPING###

wired_results = wired_soup.find('div', class_='article__chunks')

wired_final = wired_results.text.strip().replace('\n', ' ')

f.write(non_label+'\t'+wired_final+'\n')

#print(wired_final)
#print(len(wired_final))

###OBSE ARTICLE STRIPPING###

obse_results = obse_soup.find('div', class_='entry-content')

obse_final = obse_results.text.strip().replace('\n', ' ')

f.write(non_label+'\t'+obse_final+'\n')

#print(obse_final)
#print(len(obse_final))

###FULL ARTICLE STRIPPING###

full_results = full_soup.find('article')

full_final = full_results.text.strip().replace('\n', ' ')

f.write(non_label+'\t'+full_final+'\n')

#print(full_final)

###EURO ARTICLE STRIPPING###
#euro_list = []
euro_results = euro_soup.find_all('p')

for i in euro_results:
    euro_results_formatted = i.text.strip()
    contents_list.append(euro_results_formatted)

euro_final = ' '.join(contents_list)
contents_list.clear()
euro_final = euro_final.replace('\n', ' ')

f.write(non_label+'\t'+euro_final+'\n')

#print(euro_final)

###pop article stripping###
#pop_list = []
pop_results = pop_soup.find_all('p', class_='body-text')

for i in pop_results:
    pop_results_formatted = i.text.strip()
    contents_list.append(pop_results_formatted)

pop_final = ' '.join(contents_list)
contents_list.clear()
pop_final = pop_final.replace('\n', ' ').replace('\u27a1', '')

f.write(non_label+'\t'+pop_final+'\n')
#print(pop_final)


###VOX ARTICLE STRIPPING###

vox_results = vox_soup.find('div', class_='c-entry-content')

vox_final = vox_results.text.strip().replace('\n', ' ')

f.write(non_label+'\t'+vox_final+'\n')

#print(vox_final)

###NPR ARTICLE STRIPPING###

#npr_results = npr_soup.find('div', class_='storytext storylocation linkLocation')
#print(npr_results.text.strip())

### SKY ARTICLE STRIPPING ###
#sky_list = []
sky_results = sky_soup.find_all('p')

for i in sky_results:
    sky_results_formatted = i.text.strip()
    contents_list.append(sky_results_formatted)

sky_final = ' '.join(contents_list)
contents_list.clear()
sky_final = sky_final.replace('\n', ' ')

f.write(non_label+'\t'+sky_final+'\n')

f.close()




