from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render
from username_search.forms import SearchForm
import MySQLdb
import pywikibot
import requests.utils
import re
import urllib.parse


def index(request):
    context = {}
    context['form'] = SearchForm()
    return render(request, 'index.html', context)


def docs(request):
    context = {}
    return render(request, 'docs.html', context)


def search(request):
    context = {}
    form = SearchForm(request.GET)
    context['form'] = form
    if form.is_valid():
        # Clear out any old data just in case
        pywikibot.config.authenticate = {}

        # Load up the site
        site_kwargs = {'code': 'en', 'fam': 'wikipedia'}
        wiki_url = form.cleaned_data.get('wiki_url')
        base_url = "https://"+wiki_url+"/wiki/"
        if wiki_url:
            site_kwargs = {'url': base_url}
        try:
            site = pywikibot.Site(**site_kwargs)
        except pywikibot.exceptions.SiteDefinitionError:
            form.add_error('wiki_url',
                "Unable to find this wiki. Please check the domain and "
                "try again. You provided "+wiki_url+", so we expected "
                +base_url+" to be recognized by pywikibot - but it "
                "wasn't."
            )
            return render(request, 'index.html', context)

        # Set up authentication
        if request.user.is_authenticated:
            # TODO If it is possible to have more than one auth, we should try
            # all of them, or clear them out somehow.
            auths = request.user.social_auth.all()
            auth = auths[0]
            sitebasename = requests.utils.urlparse(site.base_url('')).netloc
            pywikibot.config.authenticate[sitebasename] = (
                settings.SOCIAL_AUTH_MEDIAWIKI_KEY,
                settings.SOCIAL_AUTH_MEDIAWIKI_SECRET,
                auth.extra_data['access_token']['oauth_token'],
                auth.extra_data['access_token']['oauth_token_secret'],
            )
            userinfo = site.getuserinfo(force=True)
            if userinfo['name'] != request.user.username:
                auth.delete()
                pywikibot.config.authenticate = {}
                messages.error(request, "We weren't able to log in to the "
                               "wiki. If you need more revisions or to scan "
                               "deleted revisions, please log in again.")
                logout(request)

        # Query mariadb for the list of users
        dbname = site.dbName()
        db = MySQLdb.Connect(host=dbname+".web.db.svc.eqiad.wmflabs",
                             user=settings.MYSQL_USER,
                             passwd=settings.MYSQL_PASS,
                             db=dbname+"_p")
        c = db.cursor()
        c.execute("SELECT * FROM user WHERE user_name REGEXP %s",
                  (form.cleaned_data.get('to_search'),))
        users = [{'user_id': x[0], 'user_name': x[1], 'user_created': x[12],
                  'edit_count': x[14]} for x in c.fetchall()]

        context['users'] = users

        indexphp = 'https:' + site.siteinfo['server'] + site.siteinfo['script']
        context['indexphp'] = indexphp

        # Clean up
        pywikibot.config.authenticate = {}

        return render(request, 'username_search/search.html', context)

    return render(request, 'index.html', context)
