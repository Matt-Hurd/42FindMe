from django.shortcuts import render
import datetime
from cluster import get_cluster
from django.http import HttpResponse

def gen_cluster(request, number="1"):
    cluster = get_cluster(number)
    return render(request, 'main.html', {'cluster' : cluster, 'number' : number})

def beta(request):
    cluster = get_cluster('1')
    return render(request, 'beta.html', {'cluster' : cluster, 'number' : '1'})
    
def error404(request):
    return HttpResponse(render(request, '404.html'), status=404)