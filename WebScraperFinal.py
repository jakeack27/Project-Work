import requests
import os.path
from bs4 import BeautifulSoup

con_label = 'con'
non_label = 'non'

link_list = []
contents_list = []
'''These variables store the URLs that will be stripped '''
URL = 'https://projectavalon.net/forum4/forumdisplay.php?187-5G'
URL_CONVO = 'https://theconversation.com/four-experts-investigate-how-the-5g-coronavirus-conspiracy-theory-began-139137'
URL_BBC = 'https://www.bbc.co.uk/news/53191523'
URL_TELE = 'https://telecoms.com/503845/5g-conspiracy-theories-what-they-are-why-they-are-wrong-and-what-can-be-done/'
URL_WIRED = 'https://www.wired.com/story/the-rise-and-spread-of-a-5g-coronavirus-conspiracy-theory/'
URL_OBSE = 'https://observer.com/2020/08/extreme-5g-conspiracy-theories-where-they-come-from-covid-19/'
URL_FULL = 'https://fullfact.org/online/5g-and-coronavirus-conspiracy-theories-came/'
URL_POP = 'https://www.popularmechanics.com/technology/infrastructure/a34025852/are-5g-towers-safe/'
URL_VOX = 'https://www.vox.com/recode/2020/4/24/21231085/coronavirus-5g-conspiracy-theory-covid-facebook-youtube'
URL_EURO = 'https://www.euronews.com/2020/05/15/what-is-the-truth-behind-the-5g-coronavirus-conspiracy-theory-culture-clash'
URL_SKY = 'https://news.sky.com/story/coronavirus-father-of-three-who-searched-for-5g-conspiracy-theories-online-jailed-for-arson-attack-on-phone-mast-12002914'
URL_DRUM = 'https://www.thedrum.com/news/2020/09/23/mast-conspiracies-after-5g-s-bad-reception-can-marketing-help-it-connect'
URL_REUT = 'https://www.reuters.com/world/middle-east-africa/5g-covid-19-conspiracy-theory-baseless-fake-safricas-telecoms-regulator-says-2021-01-11/#main-content'
URL_VICE = 'https://www.vice.com/en/article/pke7yv/5g-coronavirus-conspiracy-theory-origin'

'''These variables request the page from the internet using the URLs.'''
page = requests.get(URL)
bbc_page = requests.get(URL_BBC)
convo_page = requests.get(URL_CONVO)
tele_page = requests.get(URL_TELE)
wired_page = requests.get(URL_WIRED)
obse_page = requests.get(URL_OBSE)
full_page = requests.get(URL_FULL)
pop_page = requests.get(URL_POP)
vox_page = requests.get(URL_VOX)
euro_page = requests.get(URL_EURO)
sky_page = requests.get(URL_SKY)
drum_page = requests.get(URL_DRUM)
reut_page = requests.get(URL_REUT)
vice_page = requests.get(URL_VICE)

'''These variables retrieve the content from the pages using the BeautifulSoup module. '''
soup = BeautifulSoup(page.content, 'html.parser')
bbc_soup = BeautifulSoup(bbc_page.content, 'html.parser')
convo_soup = BeautifulSoup(convo_page.content, 'html.parser')
tele_soup = BeautifulSoup(tele_page.content, 'html.parser')
wired_soup = BeautifulSoup(wired_page.content, 'html.parser')
obse_soup = BeautifulSoup(obse_page.content, 'html.parser')
full_soup = BeautifulSoup(full_page.content, 'html.parser')
pop_soup = BeautifulSoup(pop_page.content, 'html.parser')
vox_soup = BeautifulSoup(vox_page.content, 'html.parser')
euro_soup = BeautifulSoup(euro_page.content, 'html.parser') 
sky_soup = BeautifulSoup(sky_page.content, 'html.parser')
drum_soup = BeautifulSoup(drum_page.content, 'html.parser')
reut_soup = BeautifulSoup(reut_page.content, 'html.parser')
vice_soup = BeautifulSoup(vice_page.content, 'html.parser')

'''This if statement checks if the conspiracyData.txt file exists and if it doesnt
exists it creates it.'''
if os.path.exists('conspiracyData.txt'):
    print("File already exists.")
else:
    f = open("conspiracyData.txt", "x")
    print("File has been created.")

'''This line opens the file so the data can be written to the file. The file is closed
at the end of the program.'''
f = open("conspiracyData.txt", "w")


###BBC ARTICLE STRIPPING###
'''This line finds all lines that belong to class'''
bbc_results = bbc_soup.find_all('div', class_='ssrcss-uf6wea-RichTextComponentWrapper e1xue1i83')

'''This for loop loops through the bbc_results, formats it and adds to a list.'''
for i in bbc_results:
    bbc_results_formatted = i.text.strip()
    contents_list.append(bbc_results_formatted)

'''These lines join the contents of the list, remove all the contents from the
list, and replace any new lines with a space.'''
bbc_final = ' '.join(contents_list)
contents_list.clear()
bbc_final = bbc_final.replace('\n', ' ')

'''This line writes the post to the file along with the label.'''
f.write(non_label+'\t'+bbc_final+'\n')

#print(bbc_final)
#print(len(bbc_final))

###CONVO ARTICLE STRIPPING###
'''This line finds the class that contains the posts contents.'''
convo_results = convo_soup.find('div', class_='grid-ten large-grid-nine grid-last content-body content entry-content instapaper_body inline-promos')

'''This line formats the contents and replaces newlines with spaces.'''
convo_final = convo_results.text.strip().replace('\n', ' ')

'''This line writes the post to the file along with the label.'''
f.write(non_label+'\t'+convo_final+'\n')

#print(convo_final)
#print(len(convo_final))

###TELE ARTICLE STRIPPING###
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

### SKY ARTICLE STRIPPING ###
sky_results = sky_soup.find_all('p')

for i in sky_results:
    sky_results_formatted = i.text.strip()
    contents_list.append(sky_results_formatted)

sky_final = ' '.join(contents_list)
contents_list.clear()
sky_final = sky_final.replace('\n', ' ')

f.write(non_label+'\t'+sky_final+'\n')

### DRUM ARTICLE STRIPPING ###
drum_results = drum_soup.find('div', id='articleMainBody')

drum_final = drum_results.text.strip()

f.write(non_label+'\t'+drum_final+'\n')

### REUT ARTICLE STRIPPING ###
reut_results = reut_soup.find('div', class_='ArticleBody__content___2gQno2 paywall-article')

reut_final = reut_results.text.strip()

f.write(non_label+'\t'+reut_final+'\n')

### VICE ARTICLE STRIPPING ###
vice_results = vice_soup.find('div', class_='article__body-components')

vice_final = vice_results.text.strip()

f.write(non_label+'\t'+vice_final+'\n')

###### collecting all the links on the web page #######
'''These two lines ffind the part of the html where the post links are located and
then finding all the posts in the forum.'''
results = soup.find(id='thread_inlinemod_form')
post_elems = results.find_all('li', class_='threadbit')

'''This for loop selects each post and obtains its link.'''
for elems in post_elems:
    thread_link = elems.find('a', class_='title')['href']
    link_list.append(thread_link)

###### taking the first link in the list, editing and removing it ######
#print("Number of links in the list: " + str(len(link_list)))
edit = 'https://projectavalon.net/forum4/'

'''This for loop attaches an edit to each link.''' 
for i in link_list:
    first_link_unedited = i
    first_link_edited = edit + first_link_unedited

    '''These lines requests the page from each link, retriesve the content, finds
    the content, formats the content, and them writes it to the file.'''
    new_page = requests.get(first_link_edited)
    new_soup = BeautifulSoup(new_page.content, 'html.parser')
    page_content = new_soup.find('div', class_='content')
    page_content_stripped = page_content.text.strip().replace('\x92', '').replace('\x91', '').replace('\u010d', '').replace('\u0107', '').replace('\x96', '').replace('\x99', '').replace('\n', ' ').replace('\r', '').replace('/t', '')
    f.write(con_label+'\t'+page_content_stripped+'\n')

f.close()
