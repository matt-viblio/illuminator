'''Utility methods for reading in the contents of a script file, and
returning an array of lines.  Each line is represented as a dictionary
with three items: line_no, page_no, and content.  Content retains the
line separator.'''

import re;

def load_txt(script_file, lines_per_page=56):
    '''Returns an array of {line_no, page_no, content} hashes.  If the
    document contains form feeds, they are used to split pages.
    Otherwise the optional lines_per_page parameter assigns page
    numbers based on lines, with a default of 56 lines per page.'''

    raw = open(script_file)

    result = []

    line_no = 0
    page_no = 1

    LINECOUNT = 'LINECOUNT'
    FORM_FEED = 'FORM_FEED'
    paging_mode = LINECOUNT

    for line in raw:
        if re.search( r'\f', line ):
            page_no += 1
            if paging_mode == LINECOUNT:
                # Fix any previously assigned lines where we assumed
                # incorrectly the paging_mode was LINECOUNT.
                paging_mode = FORM_FEED
                for l in result:
                    l['page_no'] = 1
            
        line_no += 1
        
        if paging_mode == LINECOUNT:
            page_no = 1 + ( line_no - 1 ) / lines_per_page

        result.append( {
                'line_no' : line_no,
                'page_no' : page_no,
                'content' : line
                } )

    raw.close()

    return result
