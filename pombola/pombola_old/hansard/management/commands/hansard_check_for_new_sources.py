
# This script changed extensively when the Kenyan Parliament website changed after the 2013 Election.
#
# The previous version can be seen at:
#
#    https://github.com/mysociety/pombola/blob/7181e30519b140229e3817786e4a7440ac08288d/mzalendo/hansard/management/commands/hansard_check_for_new_sources.py

import pprint
import httplib2
import re
import datetime
import sys
import parsedatetime as pdt
from warnings import warn

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

from django.conf import settings


from django.core.management.base import NoArgsCommand

from pombola.hansard.models import Source

class NoSourcesFoundError(Exception):
    pass

class Command(NoArgsCommand):
    help = 'Check for new sources'

    # http://www.parliament.go.ke
    # /plone/national-assembly/business/hansard/copy_of_official-report-28-march-2013-pm/at_multi_download/item_files
    # ?name=Hansard%20National%20Assembly%2028.03.2013P.pdf


    def handle_noargs(self, **options):

        preferred_urls = (
            'http://www.parliament.go.ke/plone/senate/business/hansard',
            'http://www.parliament.go.ke/plone/national-assembly/business/hansard',
        )

        for url in preferred_urls:
            try:
                self.process_url(url)
            except NoSourcesFoundError:
                # We expect this error so don't do anything
                pass
            else:
                # We don't expect to get here, so produce a warning. Hopefully this is good news
                # and the preferred_urls can be the only ones we look at
                warn("Previously broken url '%s' now has sources - consider reverting #905 related changes" % url)

        # The above www.parliament.go.ke urls broke seemingly on the 29 Sept 2013
        # - instead of returning the expected list of hansard sources they return
        # "Welcome to nginx!" with a status code of 200. This was issue #905.
        #
        # Going to http://www.parliament.go.ke/ and then clicking on the "Parliamentary
        # Website" menu item takes you to http://212.49.91.136/ which appears to be the
        # site as it should be (is the nginx proxying not working?). For now we'll use
        # these links so that we continue to display recent Hansard entries and
        # hopefully if they stop working the code will warn us (either no links found,
        # or bad status code returned).
        fallback_urls = (
            'http://212.49.91.136/plone/senate/business/hansard',
            'http://212.49.91.136/plone/national-assembly/business/hansard',
        )

        for url in fallback_urls:
            try:
                self.process_url(url)
            except NoSourcesFoundError:
                warn("Could not find any Hansard sources on '%s'" % url)


    def process_url(self, url):
        """
        For the given url find or create an entry for each source in the database.

        If no sources found raise an exception.
        """

        h = httplib2.Http( settings.HTTPLIB2_CACHE_DIR )
        response, content = h.request(url)
        # print content

        # parse content
        soup = BeautifulSoup(
            content,
            convertEntities=BeautifulStoneSoup.HTML_ENTITIES
        )

        spans = soup.findAll( 'span', 'contenttype-repositoryitem summary')

        links = [ span.a for span in spans ]

        # Check that we found some links. This is to detect when the page changes or our
        # scraper breaks (see issue #905 for example). Checking that the most recent
        # source is not more that X weeks old might also be a good idea, but could lead
        # to lots of false positives as there is often a long hiatus.
        if not len(links):
            raise NoSourcesFoundError()

        for link in links:

            # print '==============='
            # print link

            href = link['href'].strip()
            # print "href: " + href

            name = ' '.join(link.contents).strip()
            # print "name: " + name

            if not Source.objects.filter(name=name).exists():

                cal = pdt.Calendar()
                # Sometimes the space is missing between before the
                # month, so insert that if it appears to be missing:
                tidied_name = re.sub(r'(\d+(st|nd|rd|th))(?=[^ ])', '\\1 ', name)
                # Commas in the name confuse parsedatetime, so strip
                # them out too:
                tidied_name = re.sub(r',', '', tidied_name)
                result = cal.parseDateText(tidied_name)
                source_date = datetime.date(*result[:3])
                # print "source_date: " + str(source_date)


                # I don't trust that we can accurately create the download link url with the
                # details that we have. Instead fetche the page and extract the url.
                download_response, download_content = h.request(href)
                download_soup = BeautifulSoup(
                    download_content,
                    convertEntities=BeautifulStoneSoup.HTML_ENTITIES
                )
                download_url = download_soup.find( id="archetypes-fieldname-item_files" ).a['href']
                # print download_url

                # create the source entry
                Source.objects.create(
                    name = name,
                    url = download_url,
                    date = source_date,
                )
