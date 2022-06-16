# Importation des librairies

import http.client, urllib
from selenium import webdriver
import time
import datetime


# Envoyer la notification via Pushover

def send_notification(link,price,name,size,title,avis):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.parse.urlencode({
        "token": "",
        "user": "",
        "message":
          "\U0001F45F" + title + " \n\U0001F4B0 " + price + " \n\U0001F4CF " + size +" EU " + "\n\U0001FAAA " + name + "\n\U00002B50" + avis +" \n\U0001F517 " + link,
        "title": "Nouvelle annonce Vinted",
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
    return print("Notification sent")


# Afficher la liste de façon plus harmonieuse

def print_list(l):
    for x in l:
        print(x)


# Test d'égalité de deux listes pour le premier élement, et renvoie les éléments en trop 

def equality(l1,l2):
    l=[]
    for x in l1:
        status=True
        for y in l2:
            if x[0]==y[0]:
                status=False
        if status:
            l.append(x)     
    return l


# Fonction qui permet de scraper toutes les informations d'une recherche vinted

def search():
    articles = driver.find_elements_by_css_selector('div.feed-grid__item:not(.feed-grid__item--full-row)')
    l=[]
    for article in articles:
        links_selector = article.find_elements_by_css_selector('a')[1]
        link = links_selector.get_attribute('href')
        title = links_selector.get_attribute('title').split(", ")[0]
        price_selector = article.find_element_by_css_selector('h3')
        price = price_selector.text
        name_selector = article.find_elements_by_css_selector('h4')[0]
        name = name_selector.text
        size_selector = article.find_elements_by_css_selector('h4')[2]
        size = size_selector.text
        l.append([link,price,name,size,title])
    return l


# Fonction qui à partir d'un lien article renvoie le nombre d'étoiles de l'acheteur.

def check_stars(link):
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get(link)
    time.sleep(0.5)
    button = driver.find_element_by_id("onetrust-accept-btn-handler")
    button.click()
    article = driver.find_element_by_css_selector('div.Rating_rating__rOUZx')
    stars = article.get_attribute('aria-label')
    driver.quit()
    if stars == None:
        return "Pas d'évaluation"
    else:
        return stars.split(" ")[2] + "/5"


# Fonction qui vérifie la date de l'annonce pour savoir si elle est vraiment nouvelle

def check_date(link):
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get(link)
    time.sleep(0.5)
    button = driver.find_element_by_id("onetrust-accept-btn-handler")
    button.click()
    article = driver.find_element_by_css_selector('time.relative')
    time_vinted = article.get_attribute('datetime')
    temps = datetime.datetime(int(time_vinted[0:4]),int(time_vinted[5:7]),int(time_vinted[8:10]),int(time_vinted[11:13]),int(time_vinted[14:16]))
    seconds = datetime.datetime.timestamp(temps)
    today = time.time()
    driver.quit()
    if today-seconds > 2*3600:
        return False
    else:
        return True


# Lancement du navigateur

driver = webdriver.Chrome("chromedriver.exe")
driver.get('YOUR LINK')

time.sleep(0.5)

# Accepter les cookies

button = driver.find_element_by_id("onetrust-accept-btn-handler")
button.click()

# Initialisation de la liste de départ pour éviter d'envoyer les notifications de toutes les paires nouvelles

new_list = search()
old_list = new_list.copy()[1:]
time.sleep(2)
driver.refresh()
time.sleep(2)


# Boucle qui va lancer la recherche de façon permanente

while True:
    
    new_list = search()
    print(equality(new_list, old_list))
    
    # Envoie de la notification pour chaque nouvelle annonce avec les informations correspondantes
    
    if equality(new_list, old_list) != []:
        for element in equality(new_list, old_list):
            if check_date(element[0]):
                send_notification(element[0],element[1],element[2],element[3],element[4],check_stars(element[0]))
        old_list = old_list + equality(new_list, old_list)
    
    time.sleep(60)
    
    driver.refresh()
    
    time.sleep(2)
