from django.shortcuts import render
import datetime
from cluster import get_cluster, update_access_token, access_token
from django.http import HttpResponse, JsonResponse
import urllib2
import contextlib
import json
import requests

def gen_cluster(request, number="1"):
    cluster = get_cluster(number)
    return render(request, 'main.html', {'cluster' : cluster, 'number' : number})

def beta(request):
    cluster = get_cluster('1')
    return render(request, 'beta.html', {'cluster' : cluster, 'number' : '1'})
    
def error404(request):
    return HttpResponse(render(request, '404.html'), status=404)

def get_user_data(request, username):
    if (access_token == None):
        update_access_token()
    try:
        r = requests.get('https://api.intra.42.fr/v2/users/'+username+'/?access_token=' + access_token)
        data = r.json()
    except:
        update_access_token()

    if data:
        user_data = {}
        user_data['username'] = data['login']
        user_data['name'] = data['displayname']
        user_data['pic'] = data['image_url']
        user_data['correction'] = data['correction_point']
        user_data['wallet'] = data['wallet']

        for cursus in data['cursus_users']:
            if cursus['grade']:
                user_data['role'] = cursus['grade']
                break

        for cursus in data['cursus_users']:
            if cursus['cursus_id'] == 4:
                user_data['piscine_level'] = cursus['level']
            elif cursus['cursus_id'] == 1:
                user_data['program_level'] = cursus['level']

        user_data['projects_finished'] = []
        user_data['projects_inprogress'] = []
        for project in data['projects_users']:
            if project['cursus_ids'][0] == 1:
                if project['status'] == "finished":
                    user_data['projects_finished'].append(project['project']['name'])
                elif project['status'] == "in_progress":
                    user_data['projects_inprogress'].append(project['project']['name'])
        if user_data['projects_finished']:
            user_data['projects_finished'] = ', '.join(user_data['projects_finished'])
        else:
            user_data['projects_finished'] = "-"
        user_data['projects_inprogress'] = ', '.join(user_data['projects_inprogress'])

        locations = requests.get('https://api.intra.42.fr/v2/users/'+username+'/locations/?access_token=' + access_token).json()
        for location in locations:
            if location['end_at'] == None:
                user_data['online_since'] = location['begin_at']

    return JsonResponse(user_data)
