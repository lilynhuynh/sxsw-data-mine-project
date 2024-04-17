print("Booting Drivers...")
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Function that gets the specific XPATH - DO NOT USE EVER PLEASE
def getElementXPATH(ELXPATH,delay):
    try:
        # Wait for the element with the XPATH
        el = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH,ELXPATH)))
    except TimeoutException:
        print("Timed Out")
        el =None
    return el

# Function that returns a list of elements with that class name
def getElementClass(ELXPATH, delay):
    try:
        # Wait for the element with the class name
        el = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CLASS_NAME,ELXPATH)))
    except TimeoutException:
        print("Timed Out")
        el =None
    return el

# Function that takes a specific string and and returns the next sibling
def getElementText(ELXPATH, val, delay):
    try:
        # Wait for the element with the class name
        el = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CLASS_NAME,ELXPATH)))
        par_el = 0
        for item in el:
            if item.text == val:
                par_el = item.find_element(By.XPATH, "..")
        next_el = par_el.find_element(By.CLASS_NAME, "item-text")
        el = next_el

    except TimeoutException:
        print("Timed Out")
        el =None
    return el

# Sifts through given URL and returns a URL list of all links for each event
html = ""
URLLIST = []

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)
URL = "https://schedule.sxsw.com/2024/search/event?filters=event%2Fevent_type%3ASession%3Btype%3Aevent%3Bevent%2Ftheme%3AArtificial+Intelligence%7CAdvertising+%26+Brand+Experience%7CCreator+Economy%7CCulture%7CMusic+%26+Tech%7CTech+Industry%7CStartups%7CWorkplace%7CXR+%26+Metaverse%7CGovernment+%26+Civic+Engagement%7CHealth+%26+MedTech%3Bevent%2Fformat%3AFeatured+Session%7CFireside+Chat%7CMeet+Up%7CPanel%7CPresentation%7CShort+Form"
driver.get(URL)
print("finding each url")

for i in range(2,10): # Currently set to search up to 10 elements (ALWAYS START AT 2)
    XPATH= '/html/body/main/div/div/div[1]/section/div[2]/div['+str(i)+']/div/div[3]/div[1]/div/h4/a'
    element = getElementXPATH(XPATH, 3)
    if element != None:
        URLLIST.append([element.get_attribute('href'),element.text]) # element.text = title
        print("found: " + element.get_attribute('href'))
output = []

# Goes through the created URL list of links and scrapes for all the needed data
for x in URLLIST :

    # GET TITLE
    URL = x[0]
    driver.get(URL)

    # OUTPUT STRINGS IF PROPERTY FOUND
    dateOut = "\n\nDate: "
    timeOut = "\n\nTime: "
    presOut = "\n\nPresenter: "
    orgOut = "\n\nOrganization: "
    desOut = "\n\nDescription: "
    tagOut = "\n\nTag: "
    trackOut = "\n\nTrack: "
    formOut = "\n\nFormat: "
    confOut = "\n\nConference: "

    # GET DATE
    eventDate = getElementClass("sv-event--date", 3)
    if eventDate != None:
        strDate = ""
        for date in eventDate:
            strDate += date.find_element(By.TAG_NAME, 'p').text
        dateOut += strDate
    else:
        timeOut += "N/A"

    # GET TIME
    # Next Steps: filter out events that are before 9:30 AM
    eventTime = getElementClass("sv-event--time", 3)
    if eventTime != None:
        strTime = ""
        for time in eventTime:
            strTime += time.find_element(By.TAG_NAME, 'p').text
        timeOut += strTime
    else:
        timeOut += "N/A"

    # GET PRESENTER(S)
    eventPres = getElementClass("sve-person-name", 3)
    if eventPres != None:
        strPres = ""
        for name in eventPres:
            strPres += name.text + "; " # divided by semicolon
        presOut += strPres[:-2]
    else:
        presOut += "N/A"
        
    # GET ORGANIZATION
    eventOrg = getElementClass("sve-person-org", 3)
    if eventOrg != None:
        strOrg = ""
        for org in eventOrg:
            if org.text not in strOrg:
                strOrg += org.text + "; " # divided by semicolon
        orgOut += strOrg[:-2]

    # GET DESCRIPTION/ABSTRACT
    # Note: Bro we need to skip the first p elem bc the italic <i> info is unnecessary
    eventDes = getElementClass("sv-event--description", 3)
    if eventDes != None:
        strDes = ""
        for elem in eventDes:
            strDes += elem.text
        desOut += strDes
    else:
        desOut += "N/A"
        
    # GET TAGS
    eventTag = getElementClass("sv-event--tag", 3)
    if eventTag != None:
        strTag = ""
        for tag in eventTag:
            if tag.tag_name == 'a':
                strTag += tag.text + ', '
        tagOut += strTag[:-2]
    else:
        tagOut += "N/A"
    
    # GET TRACK
    findTrack = getElementText("item-label", "Track:", 3)
    if findTrack != None:
        strTrack = findTrack.text
        trackOut += strTrack
    else:
        trackOut += "N/A"

    # GET FORMAT
    eventForm = getElementText("item-label", "Format:", 3)
    if eventForm != None:
        strForm = eventForm.text
        formOut += strForm
    else:
        formOut += "N/A"


    output.append(x[1] + dateOut + timeOut + presOut + orgOut + desOut + tagOut + trackOut + formOut + confOut)

# NEEDED ITEMS: (+ -> completed)
# +Title
# +Time
# +Presenter(s)
# +Organization
# +Abstract(Desc)
# +Tags
# +Track
# +Format
# Conference (e.g. music, edu)
# Codes (S&P) - ignore for now

# Wait for it to process
for x in output:
    print(x+"\n"+"--------------------------\n")

driver.quit()