import re
from util import tpl_file
from google.appengine.ext.webapp import template

def get_annotated_text(song, options):
    text = ""
    for n,v in song.meta.items():
        text += n + ": " + v + "\n"

    text += "\n"
    for line in song.lines:
        if line.type == 'chords':
            text += "."
        else:
            text += "-"
        text += line.text + "\n"

    return text

def get_html(song, options):
    LEADING_SPACES = re.compile('^( )+')
    TRAILING_SPACES = re.compile('( )+$')
    def pad_nbsp(line):
        if (len(line) == 0):
            return '&nbsp;'
        spaces = LEADING_SPACES.search(line)
        if (spaces):
            line = (len(spaces.group()) * '&nbsp;') + line[len(spaces.group()):]
        spaces = TRAILING_SPACES.search(line)
        if (spaces):
            line = line[:-len(spaces.group())] + (len(spaces.group()) * '&nbsp;')
        return line.replace('\007', '&nbsp')
        
    songtext = ''
    prevline = None
    for line in song.lines:
        if (line.type == 'lyrics'):
            text = ''
            if prevline != None and prevline.type == 'chords':
                chordline = prevline.text
                lyricline = line.text
                if (len(chordline) < len(lyricline)):
                    chordline += (len(lyricline) - len(chordline)) * ' '
                else:
                    lyricline += (len(chordline) - len(lyricline)) * '\007'
                    
                cpos = 0
                lpos = 0
                while cpos < len(chordline):
                    if chordline[cpos] != ' ':
                        text += '<i class="chord">'
                        while (cpos < len(chordline) and chordline[cpos] != ' '):
                            text += chordline[cpos]
                            cpos += 1
                        text += '</i>'
                    text += lyricline[lpos:cpos+1]
                    lpos = cpos = (cpos + 1)
            else:
                text = line.text

            songtext += "<p>" + pad_nbsp(text) + '</p>\n'

        prevline = line
    
    title = song.meta.get('title', '').replace('\n','<br/>')
    subtitle = song.meta.get('subtitle', '').replace('\n','<br/>')
    byline = song.meta.get('byline', '').replace('\n','<br/>')
    
    v = {
        'title': title,
        'subtitle': subtitle,
        'byline': byline,
        'song': songtext
    }
    return template.render(tpl_file('song.html'), v)

def get_rtf(song, options):
    raise Exception("Not yet implemented")