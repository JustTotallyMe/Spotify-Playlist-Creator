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