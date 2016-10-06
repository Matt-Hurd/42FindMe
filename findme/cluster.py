import requests
import sys
import urllib2
import contextlib
import json
import os
import copy
import threading
from secrets import secret, uid
import time
import settings

access_token = None
cluster_layout = None
user_data_storage = {}
user_locations = {}

def update_access_token():
    global access_token
    
    r = requests.post("https://api.intra.42.fr/oauth/token", data={'grant_type': 'client_credentials', 'client_id': uid, 'client_secret': secret}, verify=False)
    r.raise_for_status()
    access_token = r.text[17:81]

booting = 1

def get_locations():
    if (access_token == None):
        update_access_token()
    else:
        try:
            with contextlib.closing(urllib2.urlopen('https://api.intra.42.fr/v2/campus/7/locations?access_token=' + access_token)) as x:
                    json.load(x)["error"] == "Not authorized"
        except:
            update_access_token()
    
    url = 'http://api.intra.42.fr/v2/campus/7/locations?access_token=%s&per_page=100&filter[active]=true&page=' % (access_token)
    locations = []
    x = 1
    page = 1
    while x:
        with contextlib.closing(urllib2.urlopen(url + "&page=" + str(page))) as x:
            result = json.load(x)
            if not result:
                x = 0
            locations += result
        page += 1
    
    clean = {}
    
    for l in locations:
        clean[l["host"]] = l["user"]["login"]
    
    if not booting:
        for u in clean.values():
            if u not in user_data_storage.keys():
                with contextlib.closing(urllib2.urlopen('https://api.intra.42.fr/v2/users/'+u+'/?access_token=' + access_token)) as x:
                    user_data_storage[u] = json.load(x)
                with contextlib.closing(urllib2.urlopen('https://api.intra.42.fr/v2/users/'+u+'/locations/?access_token=' + access_token)) as x:
                    user_locations[u] = json.load(x)
    return clean

class Location:
    def __init__(self, name, display, user, active):
        self.name = name
        self.user = user
        self.display = display
        self.active = active
       

def build_clusters():
    global cluster_layout
    if cluster_layout == None:
        cluster_layout = {}
    for c in os.listdir(settings.STATICFILES_DIRS[0] + "/findme/layouts/"):
        with open(settings.STATICFILES_DIRS[0] + "/findme/layouts/" + c, "rb") as f:
            x = [z.split(',') for z in f.read().split('\n')]
            cnum = c.split('.')[0]
            if not cnum in cluster_layout.keys():
                cluster_layout[cnum] = []
                for row in range(len(x)):
                    cluster_layout[cnum].append([])
                    if len(x[row]) > 1:
                        for column in range(len(x[row])):
                            n = x[row][column].strip()
                            if 'e1z1r' in n:
                                cluster_layout[cnum][row].append(Location(n, n.split('p')[1], '', 0))
                            elif 'Bocal' in n:
                                cluster_layout[cnum][row].append(Location(n, "B-" + n.split('-')[2], '', 0))
                            elif n and (n[0] == 'x' or n[0].lower() == 'r'):
                                cluster_layout[cnum][row].append(Location('', '' if not n or n[0].lower() != 'r' else n, '', 'blank'))
                            else:
                                cluster_layout[cnum][row].append(Location('', '', '', ''))

def update_clusters():
    locs = get_locations()
    build_clusters()
    for cluster in cluster_layout.values():
        for row in cluster:
            for l in row:
                if l.active != 'blank' and l.name in locs:
                    l.active = 'active'
                    l.user = locs[l.name]
                elif l.active != 'blank':
                    l.active = 'empty'
                    l.user = '';
    return cluster_layout
    
def get_cluster(x):
    return cluster_layout[x]
    

def update_loc_storage():
    if not booting:
        for u in get_locations().values():
            with contextlib.closing(urllib2.urlopen('https://api.intra.42.fr/v2/users/'+u+'/?access_token=' + access_token)) as x:
                user_data_storage[u] = json.load(x)
            with contextlib.closing(urllib2.urlopen('https://api.intra.42.fr/v2/users/'+u+'/locations/?access_token=' + access_token)) as x:
                user_locations[u] = json.load(x)
    
def update_loop():
    threading.Timer(60.0, update_loop).start()
    print("[%s] Updating locations" % time.strftime("%Y-%m-%d %H:%M:%S"))
    update_clusters()
    
def update_location_storage_loop():
    threading.Timer(300.0, update_location_storage_loop).start()
    print("[%s] Updating projects" % time.strftime("%Y-%m-%d %H:%M:%S"))
    update_loc_storage()
update_loop()
update_location_storage_loop()
booting = 0