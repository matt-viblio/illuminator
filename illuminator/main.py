#!/usr/bin/python

import json
import os
import re
import sys

from load import *
from parse import *
from reports import *

scripts = [
    ( 'Ghostbusters', 'scripts/g.txt' ),
    ( 'The Big Lebowski', 'scripts/b1.txt' ),
    ( 'Canaan Road', 'scripts/Chappell.txt' ),
    ( 'Clerks', 'scripts/clerks.txt' ),
    ( 'Indiana Jones and the Last Crusade', 'scripts/indiana-crusade.txt' ),
    ( 'M.I.A. 3-4-13', 'scripts/MIA.txt' ),
    ( 'The Matrix', 'scripts/matrix.txt' ),
    ( 'Chinatown', 'scripts/chinatown.txt' ),
    ( 'Dune', 'scripts/dune.txt' ),
    ( 'Highlander', 'scripts/highlander.txt' ),
    ( 'Terminator 2', 'scripts/t2.txt' ),
    ( 'Sample', 'scripts/g1.txt' ),
    ]

#script_file = 'foo.txt'
#script_file = 'foo1.txt'
#script_file = 'g.txt'
#script_file = 'g1.txt'
#script_file = 'b1.txt'
#script_file = 'Chappell.txt'
#script_file = 'c1.txt'

def output_json( var, file_name, outdir='.' ):
    if not os.path.isdir( outdir ):
        os.makedirs( outdir )

    output = open( outdir+'/'+file_name, 'w' )
    json.dump( var, output, sort_keys=True, indent=4 )
    output.close()

def process_script( script, parse_mode=STRICT ):
    name = script[0]
    script_file = script[1]

    print "Working on:", name

    outdir = 'output/' + re.sub( r'\s+', '_', name.lower() )

    script_lines = load_txt( script_file=script_file, lines_per_page = 56 )

    script = parse_script_lines( script_lines )

    output_json( script_lines, 'script-text.json', outdir )
    output_json( script, 'script-structure.json', outdir )

    compute_presence_and_interactions( script_lines, script, parse_mode=parse_mode )

    noun_types = {}
    for noun in presence_ns:
        noun_types[noun] = presence_ns[noun]['noun_type']

    output_json( presences, 'presences.json', outdir )
    output_json( presence_ns, 'presence_ns.json', outdir )
    output_json( presence_sn, 'presence_sn.json', outdir )
    output_json( interactions, 'interactions.json', outdir )
    output_json( interaction_ns, 'interaction_ns.json', outdir )
    output_json( interaction_sn, 'interaction_sn.json', outdir )
    output_json( noun_types, 'noun_types.json', outdir )

    presence_png = presence_plot( script_lines, map( lambda x: x[0], top_presences( top_n=8, noun_types=[CHARACTER] ) ), "Top 8 Character Presence in "+name )
    f = open( outdir+'/character_presence.png', 'w' )
    f.write( presence_png.getvalue() )
    presence_png.close()
    presence_png = None
    f.close()

    f = open( outdir+'/presence.csv', 'w' )
    f.write( get_presence_csv() )
    f.close()

    f = open( outdir+'/interaction.csv', 'w' )
    f.write( get_interaction_csv() )
    f.close()

    output_top_presences( top_presences( top_n=5, noun_types=[CHARACTER] ), outdir+'/top5_characters.csv' )
    output_top_presences( top_presences( top_n=5, presence_types=[DISCUSS] ), outdir+'/top5_speakers.csv' )
    output_top_presences( top_presences( top_n=5, noun_types=[LOCATION] ), outdir+'/top5_locations.csv' )
#    output_top_presences( top_presences( top_n=5, noun_types=[THING] ), outdir+'/top5_things.csv' )

    output_top_interactions( top_interactions( top_n=5, interaction_types=[SETTING] ), outdir+'/top5_hangouts.csv' )
    output_top_interactions( top_interactions( top_n=5, noun_types=[ ( CHARACTER, CHARACTER ) ] ), outdir+'/top5_bffs.csv' )
#    output_top_interactions( top_interactions( top_n=5, noun_types=[ (CHARACTER, THING ) ] ), outdir+'/top5_tools.csv' )
    output_top_interactions( top_interactions( top_n=5, interaction_types=[DISCUSS] ), outdir+'/top5_speakers.csv' )

def output_top_presences( presences, filename ):
    f = open( filename, 'w' )
    f.write("name,noun_type,appearances\n")
    for p in presences:
        f.write( ','.join( [ p[0], p[1], str( p[2] ) ] ) )
        f.write( "\n" )
    f.close()

def output_top_interactions( interactions, filename ):
    f = open( filename, 'w' )
    f.write("name1,name2,interactions\n")
    for i in interactions:
        f.write( ','.join( [ i[0], i[1], str( i[2] ) ] ) )
        f.write( "\n" )
    f.close()

for script in scripts:
    process_script( script, parse_mode=STRICT )
    reset_parser_state()
    


'''

I am having a closure / scope issue or something, my charts are all
screwed up after the first one, and it doesn't happen when we generate
them one at a time. - Figure out why my one approach wasn't working.

It appears the first scrip's datastructure just keeps getting used
over and over.

Reports:

5. Then once this is done, start a "vizualization" library, and print
out some graphs, yeah!

a. Presence by scene / page / text offset or something for top chatacters.

b. Interactions by scene.

c. Interaction webs for top characters.

PDF reader inserts non-UTF8 strings with accents and stuff, which breaks JSON encoding.


---

Thing about FUZZY detection and things.  In strict mode we never
detect things.  In fuzzy mode we can blow up and detect AND, IN,
etc. as nouns.  

Maybe the POS tagging has some value after all, or a simpler thing
that just rejects coordinating conjunctions like AND and IN as
standalone nouns?


'''
