from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import datapipe
import json

def index(request):
	return render(request, 'datapipe/index.html')
	
@csrf_exempt # was causing error due to session cookie not present
def submit(request):
	submission = json.loads(request.body.decode('utf-8'))
	datapipe.start_job(submission['emailInput'], submission['classOne'])
	return HttpResponse(status=202) # 202 = request accepted
