from django.db import models
from Lib.Locations import get_region, get_country_code
from Lib.Locations import get_loc

from urlparse import urlparse
from socket import gethostbyname

class Repo(models.Model):
    owner = models.CharField(max_length='75')
    email = models.CharField(max_length='75')
    repo = models.CharField(max_length='200')
    location = models.CharField(max_length='25', editable=False)
    longitude = models.CharField(max_length='25', editable=False)
    latitude = models.CharField(max_length='25', editable=False)
    enabled = models.BooleanField()

    def save(self):
        '''custom save function to pull geoip'''

        # only perform lookup on new entry
        if not self.id:
            # extract the domain from Repo URL
            # and then resolve said domain
            domain = urlparse(self.repo).hostname
            ip = gethostbyname(domain)

            # attempt to pull the region information
            # from ip address
            region = get_region(ip)
            if region:
                country_code = ' '.join(region.values())
            else:
                # else fall back to country only
                country_code = get_country_code(ip)

            # get the longitude and latitute
            country, cords = get_loc(country_code)

            # set the location value and save
            self.location = country
            self.longitude = cords[0]
            self.latitude = cords[1]
        super(Repo, self).save()
