from bs4 import BeautifulSoup
import requests

class GoogleSearch:
    """ class to initiate a query to google.com. Require only keyword.
    Initiation of this class is not yet queried to google.com"""
    def __init__(self, keyword):
        kwd = keyword.strip()
        self.query = "q=%s" % (kwd.replace(" ", "+"))
        self.is_final_page = False
        self.current_page = 1
        self.current_html_page = ''
        self.search_result = []
        self.google = "http://www.google.com/search?"

    def start_search(self, max_page=1):
        # method to start send query to google. Search start from page 1.
        # max_page determine how many result expected
        # hint: 10 result per page for google
        for page in range(1, (max_page + 1)):
            start = "start=%s" % str((page - 1) * 10)
            url = "%s%s&%s" % (self.google, self.query, start)
            self._execute_search_request(url)
            self.current_page += 1

    def more_search(self, more_page):
        # method to add more result to an already exist result
        # more_page determine how many result page 
        # should be added to the current result
        next_page = self.current_page + 1
        top_page = more_page + self.current_page
        for page in range(next_page, (top_page + 1)):
            start = "start=%s" % str((page - 1) * 10)
            url = "%s%s&%s" % (self.google, self.query, start)
            self._execute_search_request(url)
            self.current_page += 1

    def _execute_search_request(self, url):
        # method to execute the query to google. The specified page and keyword
        # must already included in the url.
        self.request_page = requests.get(url)
        #self.request_page.raise_for_status()
        self.current_html_page = self.request_page.text
        soup = BeautifulSoup(self.current_html_page, "html5lib")
        results = soup.find_all('a', class_=False)
        links = []  # store the final url of search result, 10 links
        
        # this loop filter the search result links inside the search page
        for target in results:
            # filter only link from search result shoul be appended
            if (target.get('href').find("/url?q") == 0) and not \
                    (target.get('href').find("/url?q=http://webcache.googleusercontent.com") == 0) and not (target.get('href').find("/url?q=/settings/") ==0):
                start_index = target.get('href').find('http')
                end_index = target.get('href').find('&sa')

                # slice the desired url into ideal link, and append 
                # it to reserved list variable
                links.append(target.get('href')[start_index:end_index])

        # this loop inspect if the current page is the final page
        for href in results:
            fnl = 'repeat the search with the omitted results included'
            if href.get_text() == fnl:
                self.is_final_page = True
            else:
                pass

        # send the final url link to class reserved variable
        for link in links:
            self.search_result.append(link)
