from django.shortcuts import render
import datetime
from cluster import get_cluster
from django.http import HttpResponse

# cluster = get_cluster()
def gen_cluster(request, number="1"):
    cluster = get_cluster(number)
    return render(request, 'main.html', {'cluster' : cluster, 'number' : number})
    
def error404(request):
    return HttpResponse(render(request, '404.html'), status=404)