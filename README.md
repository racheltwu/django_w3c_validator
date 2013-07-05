Django W3C Validator
================

About
-----
Django W3C Validator is a pluggable Django app that validates all your urls using the W3C validator. It is called via
a management command that crawls your domain for all internal links using Mechanize and saves them to a text file to reuse.
It then sends each url to the W3C validator and saves the results in an html file to view on your website.


Installation
------------

1. Pip install from GitHub:

        pip install git+git://github.com/racheltwu/django_w3c_validator

2. Add `django_w3c_validator` to your `INSTALLED_APPS` in your settings file:

        INSTALLED_APPS = (
            ...
            'django_w3c_validator',
            ...
        )

3. You can either set the `VALIDATOR_START_URL` variable in your settings file, or if you already have your domain set in `ALLOWED_HOSTS`
it will pull the first domain from that tuple. `VALIDATOR_START_URL` has priority, and it doesn't matter if you start with "http://" or not, nor
does it matter if you use the ".example.com" method in `ALLOWED_HOSTS` to include subdomains. Subdomain urls would be considered internal during
the crawling process and would be included to be validated.

        VALIDATOR_START_URL = 'example.com'

4. Add this url to your `urls.py` to make your validation results available at *http://yourdomain.com/validation*. You can view the crawled urls
at *http://yourdomain.com/validation/urls*

        (r'^validation', include('django_w3c_validator.urls')),


5. You can disable the javascript collapsing effect by setting `VALIDATOR_COLLAPSE` to False in your settings. It is True by default.



Usage
-----

Call the management command `validate` to validate all the internal urls on your site. The command will detect your domain name from your settings
file and proceed to crawl it for all internal links, and save all found urls to a text file to use again later. If this file
already exists, it will not crawl the site again unless you pass the `--crawl` option with the command.



Screenshot
----------

![](https://github.com/racheltwu/django_w3c_validator/raw/master/screenshot.jpg "Django W3C Validator Screenshot")
