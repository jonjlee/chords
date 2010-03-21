import logging
import re
import songformat
from google.appengine.ext import db

class SongModel(db.Model):
    id = db.StringProperty()
    text = db.TextProperty()
    lastmod = db.DateTimeProperty(auto_now_add=True)
    
class Songs:
    def read(self, id, format=None):
        query = db.GqlQuery("SELECT * FROM SongModel WHERE id = :id", id=id)
        results = query.fetch(1)
        
        if len(results) == 0:
            return None, None
        
        song = Song(results[0].text.split('\n'))

        if (format == 'object'):
            return song, None
        elif (format == 'text'):
            return song.text, "text/plain;annotated=true"
        elif (format == 'rtf'):
            return song.get_rtf(), "text/rtf"
        else:
            return song.get_html(), "text/html"
        
    def write(self, id, song):
        song_model = SongModel()
        song_model.id = id
        song_model.text = song.text
        song_model.put()
        
    def delete(self, id):
        query = db.GqlQuery("SELECT * FROM SongModel WHERE id = :id", id=id)
        results = query.fetch(1)
        db.delete(results)

class Song:
    def __init__(self, lines=[], meta={}):
        self.meta, self.lines = self._parse_raw_lines(lines, meta)
    
    def _set_text(self, text):
        self.meta, self.lines = self._parse_raw_lines(text.split("\n"))

    def _get_text(self, options={}):
        return songformat.get_annotated_text(self, options)

    text = property(_get_text, _set_text)

    def set_meta(self, name, value):
        self.meta[name] = value
        
    def get_meta(self, name=None):
        if (name == None):
            return self.meta
        else:
            return self.meta[name]

    def get_html(self, options={}):
        return songformat.get_html(self, options)

    def get_rtf(self, options={}):
        return songformat.get_rtf(self, options)
    
    def _parse_raw_lines(self, raw_lines, meta={}):
        lines = []
        
        i = 0
        prevmetakey = None
        for i,raw_line in enumerate(raw_lines):
            raw_line = raw_line.rstrip("\n")
            if (len(raw_line) == 0):
                break
            nv = raw_line.split(":",1)
            if len(nv) > 1:
                meta[nv[0].strip().lower()] = nv[1].strip()
                prevmetakey = nv[0].strip().lower()
            elif prevmetakey != None:
                meta[prevmetakey] += '\n' + nv[0]

        for raw_line in raw_lines[i+1:]:
            raw_line = raw_line.rstrip("\n")
            lines.append(SongLine(raw_line))
    
        return meta, lines

class SongLine:
    CHORDS = "chords"
    LYRICS = "lyrics"

    _CHORD_PATTERN = re.compile('^[0-9A-G#bmsusdiaug/ ]+$')

    def __init__(self, raw_text=""):
        self.type, self.text = self.parse_text(raw_text)
    
    def parse_text(self, raw_text):
        typ = SongLine.LYRICS
        text = raw_text
        if len(raw_text) > 0:
            if raw_text[0] == '.':
                typ,text = SongLine.CHORDS, raw_text[1:]
            elif raw_text[0] == '-':
                typ,text =SongLine.LYRICS, raw_text[1:]

        if SongLine._CHORD_PATTERN.match(raw_text):
            typ,text = SongLine.CHORDS, raw_text

        return typ,text.expandtabs()