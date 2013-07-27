from django.http import HttpResponse
from django.shortcuts import render

from viz.models import Author, Script

def home( request ):
    return render( request, 'viz/illuminate.html' )

def illuminator( request ):
    return render( request, 'viz/illuminator.js' )

def script_data( request, field ):
    s = Script.objects.all()[0]
    result = ''
    if field == 'scenes':
        result = s.scenes
    elif field == 'script':
        result = s.script
    elif field == 'noun_types':
        result = s.noun_types
    elif field == 'presences':
        result = s.presences
    elif field == 'presence_ns':
        result = s.presence_ns
    elif field == 'presence_sn':
        result = s.presence_sn
    elif field == 'interactions':
        result = s.interactions
    elif field == 'interaction_ns':
        result = s.interaction_ns
    elif field == 'interaction_sn':
        result = s.interaction_sn

    return HttpResponse( result, mimetype="application/json" )
