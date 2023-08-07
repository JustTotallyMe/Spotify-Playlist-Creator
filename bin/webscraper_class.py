from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


class WebScrapeForBBC:
    def __init__(self):
        self.options = Options()
        self.options.add_argument('-headless')
        self.browser = Firefox(options=self.options)

    def GetSongListAsDict(self, url):
        self.browser.get(url)
        divsOnPage = self.browser.find_elements(by=By.TAG_NAME, value='div')
        output = {}

        for div in divsOnPage:
            if div.get_attribute('class') == 'sc-u-antialiased':
                for ul in div.find_elements(by=By.TAG_NAME, value='ul'):
                    if 'sc-c-scrollable-list__list' in ul.get_attribute('class'):
                        for trackDiv in ul.find_elements(by=By.TAG_NAME, value='div'):
                            for track in trackDiv.find_elements(by=By.TAG_NAME, value='div'):
                                if track.get_attribute('title') != "":
                                    trackArtAndName = track.text.split('\n')
                                    output[trackArtAndName[0]] = trackArtAndName[1]

        return output

    def GetCorrectUrl(self):
        self.browser.get("https://www.bbc.co.uk/sounds/tag/dance")
        spansOnPage = self.browser.find_elements(by=By.TAG_NAME, value="span")
        newUrl = ''
        for i in spansOnPage:
            if 'Bass Show' in i.get_attribute('innerHTML'):
                blub = i.find_elements(By.XPATH, value='..')[0]

                while blub.get_attribute('class') != 'sc-c-playable-list-card__link sc-o-link sc-u-flex-grow':
                    blub = blub.find_elements(By.XPATH, '..')[0]

                newUrl = blub.get_attribute('href')
                break

        self.browser.get(newUrl)
        ulsOnPage = self.browser.find_elements(By.TAG_NAME, 'ul')
        for i in ulsOnPage:
            if i.get_attribute('class') == 'sc-o-scrollable__list':
                if len(i.find_elements(By.XPATH, './li')) > 3:
                    return i.find_elements(By.XPATH, './li')[2].find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
                else:
                    return newUrl
