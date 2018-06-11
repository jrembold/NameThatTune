# Library for function to facilitate the Name that tune game

import os
import subprocess
import random
from mutagen.mp3 import MP3

def getSongList(Dir):
    return [os.path.join(path,filename) for path,dirs,files in os.walk(Dir) \
            for filename in files if filename.endswith('.mp3')]

def getRandomSong(flist):
    return random.choice(flist)

def getSongChoices(flist, num):
    tmp = flist.copy()
    random.shuffle(tmp)
    return tmp[:num]

def getSongData(fname):
    data = MP3(fname)
    title = data['TIT2'].text[0]
    artist = data['TPE2'].text[0]
    album = data['TALB'].text[0]
    return {'title':title, 'artist':artist, 'album':album}

def playSong(fname):
    subprocess.Popen(['cmus-remote', '-c', '-q'])
    subprocess.Popen(['cmus-remote', '-q', fname])
    subprocess.Popen(['cmus-remote', '-n'])
    subprocess.Popen(['cmus-remote', '-p'])
