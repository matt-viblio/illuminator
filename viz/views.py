from django.http import HttpResponse
from django.shortcuts import render, redirect

from viz.models import Author, Script

def other( request ):
    return redirect( '/1/' )

def submit( request ):
    return redirect( '/' + request.GET['script_id']+'/' )

def home( request, script_id ):
    script_id = int( script_id )
    scripts = []
    title = 'Select Script From Right to Begin'
    for script in Script.objects.order_by('title'):
        scripts.append( { 'title': script.title, 'script_id': script.id } )
        if script.id == script_id:
            title = script.title
    return render( request, 'viz/illuminate.html', { 'current_id': script_id, 'scripts': scripts, 'title': title } )

def illuminator( request, script_id ):
    print "GOT CALLED", script_id
    return render( request, 'viz/illuminator.js', { 'script_id':script_id } )

def script_data( request, script_id, field ):
    print "SCRIPT DATA GOT CALLED", script_id, field
    s = Script.objects.filter( id=int( script_id ) )[0]
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
