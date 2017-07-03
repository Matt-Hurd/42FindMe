from django.shortcuts import render
from cluster import *
from django.http import HttpResponse, JsonResponse


def error404(request):
    return HttpResponse(render(request, '404.html'), status=404)

def gen_cluster(request, number="1"):
    cluster = get_cluster(number)
    return render(request, 'main.html', {'cluster': cluster, 'number': '1', 'online': online})
#    return render(request, '503.html')

def get_user_data(request, username):
    if (access_token == None):
        update_access_token()
    data = user_data_storage[username]

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
                user_data['piscine_level'] = '{0:,.2f}'.format(cursus['level'])
            elif cursus['cursus_id'] == 1:
                user_data['program_level'] = '{0:,.2f}'.format(cursus['level'])

        user_data['projects_finished'] = []
        user_data['projects_inprogress'] = []
        for project in data['projects_users']:
            if project['cursus_ids'][0] == 1:
                if project['status'] == "finished":
                    user_data['projects_finished'].append(project['project']['name'])
                elif project['status'] == "in_progress":
                    user_data['projects_inprogress'].append(project['project']['name'])
        user_data['projects_finished'] = ', '.join(user_data['projects_finished']) if user_data[
            'projects_finished'] else "-"
        user_data['projects_inprogress'] = ', '.join(user_data['projects_inprogress']) if user_data[
            'projects_inprogress'] else "-"

        locations = user_locations[username]
        for location in locations:
            if location['end_at'] == None:
                user_data['online_since'] = location['begin_at']

    return JsonResponse(user_data)
