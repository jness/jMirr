import pygeoip
from geopy import geocoders 

def get_region(ip):
    '''Simple function to return the region name
    and country code'''
    gi = pygeoip.GeoIP('data/GeoLiteCity.dat')
    # region_by_addr does not return None
    # it excepts on unable to itter
    try:
        region = gi.region_by_addr(ip)
    except TypeError:
        return False
    else:
        return region

def get_country_code(ip):
    '''Simple function to return a country code
    from an IP address.'''
    gi = pygeoip.GeoIP('data/GeoIP.dat')
    country_code = gi.country_code_by_addr(ip)
    # If we fail to lookup IP default to US
    if not country_code:
        country_code = 'US'
    return country_code

def get_loc(country_code):
    '''Using the country_code from get_country_code
    return the Place and longitude and latitude.'''
    g = geocoders.Google()
    location = g.geocode(country_code)
    return location
