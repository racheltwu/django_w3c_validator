import requests
import time
import re
from os import path
from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings
from BeautifulSoup import BeautifulSoup
from mechanize import Browser, RobotExclusionError


class Command(BaseCommand):
    help = 'Crawls to find all internal urls, and validates them using W3C standard set in page doctype.'
    option_list = BaseCommand.option_list + (
        make_option('--crawl',
            action='store_true',
            dest='crawl',
            default=False,
            help='Crawl site to find all urls. Uses last crawl results by default.'),
        )
    def handle(self, *args, **options):
        template_dir = path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))), 'templates')
        time_start = time.time()
        validate_urls(get_urls(options['crawl'], template_dir), template_dir)
        duration = time.gmtime(time.time() - time_start)
        print 'Finished in {hour}h {min}m {sec}s'.format(hour=duration.tm_hour, min=duration.tm_min, sec=duration.tm_sec)


def get_urls(should_crawl, template_dir):
    """Fetches existing or crawls for new urls"""
    crawled_urls_file = path.join(template_dir, 'crawled-urls.txt')
    if path.exists(crawled_urls_file) and not should_crawl:
        print 'Fetching already found urls...'
        return open(crawled_urls_file, 'r').read().split('\n')
    urls = sorted(crawl_urls())
    with open(crawled_urls_file, 'w') as file:
        for url in urls:
            file.write(url + '\n')
    return urls


def crawl_urls():
    """Returns a set of unique crawled internal url strings"""
    print 'Crawling for urls...'
    domain = getattr(settings, 'VALIDATOR_START_URL', settings.ALLOWED_HOSTS[0])
    domain = re.sub(r'^http://|^[^\w]+|[^\w]+$', '', domain)
    urls = set()
    visited_pages = set()
    internal = '^/.*$|.*' + domain + '.*$'
    br = Browser()

    def crawl_url(url):
        """Crawls one url collecting urls and recursively visits each url it finds"""
        try:
            br.open(url)
        except RobotExclusionError:
            return
        except Exception as e:
            print e + ' - ' + url
            return
        if not br.viewing_html():
            return
        time.sleep(1)
        urls.add(url)
        print url
        visited_pages.add(url)
        current_page_urls = []
        for url in br.links(url_regex=internal):
            current_page_urls.append(url.absolute_url)
        for url in current_page_urls:
            if url not in visited_pages:
                crawl_url(url)

    crawl_url('http://' + domain)
    return urls


def validate_urls(urls, template_dir):
    """Validates a list of urls using the online W3C validator, saving results to html file"""
    print 'Validating urls now...'
    with open(path.join(template_dir, 'validation-results.html'), 'w') as file:
        for url in urls:
            print url
            html = requests.post('http://validator.w3.org/check', {'uri': url})
            time.sleep(1)
            results = BeautifulSoup(html.text).find('div', {'id': 'result'})
            if not results:
                continue
            del results['id']
            results['class'] = 'results'
            for img in results.findAll('img'):
                if not img['alt'] in ['Error', 'Warning', 'Info']:
                    img.extract()
            for element_with_id in results.findAll(True, {'id': True}):
                del element_with_id['id']
            for p in results.findAll('p', {'class': re.compile('helpwanted|backtop')}):
                p.extract()
            results = str(results)
            results = results.replace('images/info_icons/', '{{ STATIC_URL }}django_w3c_validator/')
            if not re.search('Congratulations', results):
                file.write('<div class="results-wrapper">\n')
                file.write('<h1>' + url + '</h1>\n')
                file.write(results)
                file.write('</div>\n')
