
def getWeekMenu(url):

    from bs4 import BeautifulSoup
    import requests
    from selenium import webdriver
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.common.keys import Keys
    from time import sleep
    import re

    gerechten = []

    browser = webdriver.PhantomJS("phantomjs-2.1.1-windows/bin/phantomjs.exe")

    url = browser.get(url)

    sleep(3)
    # wachten tot phantomjs klaar is met het uitvoeren van de javascript code
    html = browser.page_source

    scraper = BeautifulSoup(html, "lxml", from_encoding="utf-8")

    # BS maakt zoeken op html code eenvoudig

    weekMenu = scraper.find_all("div", {"class": "catering catering1"})
    # Elke dag van de week in een list zetten, deze zitten in een div op de url

    for dagMenu in weekMenu:
        dagEnMenus = []
        dagMenu = str(dagMenu)

        dagEnMenus.append(re.findall("<h2.+>(.+)</h2>", dagMenu)[0])
        # voert regex uit op de dag en datum en neemt het eerste (en enigste resultaat)
        #[0] dient om het eerste object van de list die findall teruggeeft te selecteren.
        menus = re.findall("<p>((?!\\xa0).+)</p>", dagMenu)
        extramenus = re.findall("(.+)<br", dagMenu)
        # Sommige gerechten zitten in een aparte paragraaf
        for menu in extramenus:
            menu = str(menu).lstrip()  # Tabs verwijderen
            menus.append(menu)
        for menu in menus:
            dagEnMenus.append(menu)
        # re.findall voert regex uit op de paragrafen binnen de div van een dag
        #\\xa0 is &nbsp na conversie wat een witregel is in de html, niet in list opnemen
        gerechten.append(dagEnMenus)
    return gerechten


def convertListToText(listWeekMenu):
    weekMenuText = ""

    for dagMenus in listWeekMenu:
        weekMenuText += dagMenus[0]
        weekMenuText += "\n"
        for count in range(1, len(dagMenus)):
            weekMenuText += dagMenus[count]
            weekMenuText += "\n"
        weekMenuText += "\n"
    return weekMenuText


def writeTextToFile(text):
    fileHandler = open("Gerechten.txt", 'w')
    for line in text:
        fileHandler.write(line)
    fileHandler.close()


def checkUpdated():
    import datetime
    import re

    try:
        fileHandler = open("Gerechten.txt", 'r')
    except:
        return False
    currentDay = datetime.date.today()
    # Indien er geen Gerechten.txt bestaat -> return False -> Nieuwe aanmaken
    firstLine = str(fileHandler.readline())
    # Leest eerste regel, gaat deze gebruiken voor de controle
    date = re.findall("([0-9]+)", firstLine)
    date = date[2] + "-" + date[1] + "-" + date[0]
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    # De eerste datum in de string omvormen tot een datetime object
    date = date + datetime.timedelta(days=5)
    print(date)
    print(currentDay)
    if(date > currentDay):
        # datetime objects kunnen vergeleken worden
        return True
    else:
        return False

    fileHandler.close()


def main():
    url = "http://www.pxl.be/Pub/Studenten/Voorzieningen-Student/Catering/Weekmenu-Campus-Elfde-Linie.html"

    if (checkUpdated() == False):  # Controle of tekstbestand gerechten heeft van deze week
        listWeekMenu = getWeekMenu(url)  # PXL url scrapen en een list samenstellen
        weekMenuText = convertListToText(listWeekMenu)  # list omvormen naar gestructureerde textfile
        writeTextToFile(weekMenuText)  # text wegschrijven naar Gerechten.txt


if __name__ == "__main__":
    main()