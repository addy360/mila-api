import requests
from bs4 import BeautifulSoup


class Page:
    def __init__(self, url):
        self.URL = url

    def get_response(self):
        try:
            with requests.get(self.URL) as response:
                return response
        except Exception as e:
            exit(1)

    def get_soup(self, html):
        return BeautifulSoup(html, features="html.parser")

    def get_page(self):
        return self.get_response().text

    def get_content(self):
        return self.get_response().content


class MillardAyo(Page):
    def __init__(self):
        super().__init__('https://millardayo.com/')
        self.BASE_URL = 'https://millardayo.com'
        self.posts = []
        self.cached_posts = {}
        self.next_page_url = None

    def parse_post_details(self, post_detail_html):
        soup = self.get_soup(post_detail_html)
        post_header = soup.select_one('div#post-header>h1').text
        post_content = soup.select_one('div.post-section')
        post_detail = post_content.text.strip()
        return {"post_header": post_header, "post_content": post_content, "post_detail": post_detail}

    def get_post_details(self, post_url):
        self.URL = post_url
        post_html = self.get_res()
        self.parse_post_details(post_html)

    def user_choice(self, next_page_url=None):
        choice = 2
        try:
            post_url = self.posts[int(choice)-1]['post_link']
            self.get_post_details(post_url)
        except Exception:
            return False

    def parse_next_page(self, next_page_url: str):

        # TODO caching for easier backward navigation
        # self.cached_posts[self.URL] = self.posts
        self.posts = []
        self.URL = self.BASE_URL + next_page_url

        self.parse_result()

    def print_posts(self, posts):
        for i, post in enumerate(posts):
            title = post.h2.a.text
            link: str = post.h2.a['href']
            self.posts.append({'post_title': title,
                               'post_link': link.replace(self.BASE_URL, '')})
        return self.posts

    def parse_result(self):
        html_result = self.get_res()
        soup = self.get_soup(html_result)
        list_posts = soup.find_all('li', class_="infinite-post")
        next_page_url = soup.select(
            'div.pagination>a:not(.inactive)')[-2]['href']

        self.print_posts(list_posts)
        self.next_page_url = next_page_url.replace(self.BASE_URL, '')
        # self.user_choice(next_page_url)

    def get_res(self):
        res = self.get_page()
        return res

    def run(self):
        self.parse_result()
