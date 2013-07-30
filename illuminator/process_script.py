import json
import os
import re
import sys

from django import forms;

from illuminator.load import *
from illuminator.parse import *

from viz.models import Author
from viz.models import Script

def process_script( script, title, draft, parse_mode=STRICT ):

    content_type = script.content_type
    if content_type == 'text/plain':
        pass
    elif content_type == 'application/pdf':
        pass
    else:
        print "ERROR - unsupported content type" + content_type
        return -1

    script_lines = load_txt( body=script, lines_per_page = 56 )

    script = parse_script_lines( script_lines )

    compute_presence_and_interactions( script_lines, script, parse_mode=parse_mode )

    noun_types = {}
    for noun in presence_ns:
        noun_types[noun] = presence_ns[noun]['noun_type']

    a = Author.objects.all()[0]

    s = Script( author=a, title=title, draft=draft, is_public=True, 
                scenes=json.dumps(script), script=json.dumps(script_lines), 
                noun_types=json.dumps(noun_types), 
                presences=json.dumps(presences), 
                presence_ns=json.dumps(presence_ns), 
                presence_sn=json.dumps(presence_sn), 
                interactions=json.dumps(interactions), 
                interaction_ns=json.dumps(interaction_ns), 
                interaction_sn=json.dumps(interaction_sn) )

    s.save()

    reset_parser_state()

    return s.id
