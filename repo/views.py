from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.conf import settings
from repo.models import Repo
from django.core.cache import cache

# Geo IP and Geo Location modules
from Lib.Locations import get_region, get_country_code
from Lib.Locations import get_loc
from geopy import distance

def closest_mirrors(location):
    '''Using the longitude and latitude from get_log
    return a list of the cloest repos'''
    repo_list = []
    repos = Repo.objects.all()
    for r in repos:
        if r.enabled:
            place, visitor_cords = location
            longitude = r.longitude
            latitude = r.latitude
            dist = distance.distance(visitor_cords, (longitude, latitude)).miles
            repo_list.append((dist, place, r.repo))
    return sorted(repo_list)

def index(request):
    '''Top level view tied to our HTTP view'''

    # first things first, lets be sure they have
    # the correct GET data
    try:
        release = request.GET['release']
        arch = request.GET['arch']
    except KeyError:
        raise Http404
    
    # get requesters IP address, then get their
    # country code with GeoIP
    remote_addr = request.META['REMOTE_ADDR']

    # check if this remote address has a cache
    if cache.get(remote_addr):
        repo_list = cache.get(remote_addr)
    if cache.get(remote_addr+'_loc'):
        location = cache.get(remote_addr+'_loc')
    else:
        location = None

    # if we have a cache skip to the end,
    # else run our lookups
    try:
        repo_list
    except NameError:
        # using the requestors ip address
        # lets attempt to get a region
        region = get_region(remote_addr)

        if region:
        # if we successfully pulled a region
        # lets construct a region + country code
            country_code = ' '.join(region.values())
        else:
            # using the requestors ip address
            # lets pull a country code
            country_code = get_country_code(remote_addr)
        
        # If we successfully pulled a country code
        # lets give a repo list sorted by locations
        if country_code:
            # Since we have a country_code lets
            # get the longitude and latitude
            location = get_loc(country_code)
            
            if not location:
            # if we did not get a country code the IP address
            # is not yet in the GeoIP.dat and we need to
            # improvise
                return HttpResponse('Failed to lookup Address %s' % remote_addr)
            # if we recieved our location lets get closest mirrors
            else:
                repo_list = closest_mirrors(location)

    # set our cache (or refresh or cache)
    cache.set(remote_addr, repo_list, 300)
    cache.set(remote_addr+'_loc', location[0], 300)

    # return the list to the template
    return render(request, 
                   'repos.html',
                   {'location': location, 'repo_list': repo_list, 'release': release, 'arch': arch}, 
                   content_type="text/plain"
                  )
