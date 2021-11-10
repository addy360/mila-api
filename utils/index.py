from django.core.mail import send_mail
from django.conf import settings
from bs4.element import ResultSet
import requests
from bs4 import BeautifulSoup


def get_base_server_addr(request):
    protocal = "https" if request.is_secure() else "http"
    return f"{protocal}://{request.get_host()}"


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

    def remove_base_url(self, url):
        return url.replace(self.BASE_URL, '')

    def remove_uni_chars(self, text):
        text = text.replace('\n', '')
        return text.replace('\r', '')

    def parse_post_details(self, post_detail_html):
        soup = self.get_soup(post_detail_html)
        try:
            post_feature_image = soup.select_one(
                'div#featured-image img')['src']

            post_header = soup.select_one('div#post-header>h1').text
            post_content = soup.select_one('div.post-section')
            post_images = []
            videos = []
            for image in post_content.select('img'):
                post_images.append(image['src'])
            for video in post_content.select('iframe'):
                videos.append(video['src'])
            post_detail = post_content.text.strip()
            post_detail = post_detail.split("Related")
            post_detail.pop()
            post_detail = "".join(post_detail)
            data = {"post_feature_image": post_feature_image, "post_header": self.remove_uni_chars(post_header),
                    "post_detail": self.remove_uni_chars(post_detail), "post_images": post_images, 'videos': videos}

        except:
            data = None
        return data

    def get_post_details(self, post_url):
        self.URL = self.BASE_URL + "/" + post_url
        post_html = self.get_res()
        return self.parse_post_details(post_html)

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

    def print_posts(self, posts: ResultSet):
        for i, post in enumerate(posts):
            category = post.select_one('div.blog-layout1-text>h3').text
            thumbnail = post.img['src']
            title = post.h2.a.text
            link: str = post.h2.a['href']
            self.posts.append({'category': category, 'post_title': title,
                               'post_link': self.remove_base_url(link), "thumbnail": thumbnail})
        return self.posts

    def parse_result(self):
        html_result = self.get_res()
        soup = self.get_soup(html_result)
        list_posts = soup.find_all('li', class_="infinite-post")
        try:
            next_page_url = soup.select(
                'div.pagination>a:not(.inactive)')[-2]['href']
        except:
            next_page_url = "/"

        self.print_posts(list_posts)
        self.next_page_url = next_page_url.replace(self.BASE_URL, '')

    def get_res(self):
        res = self.get_page()
        return res

    def run(self):
        self.parse_result()


def send_email_to_admin(subject, message, from_email):
    to_email = settings.DEFAULT_TO_EMAIL
    print(to_email)
    send_mail(subject=subject, message=message,
              recipient_list=[to_email], from_email=from_email)
