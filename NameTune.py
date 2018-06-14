# Library for function to facilitate the Name that tune game

import os
import subprocess
import random
import time
from picker import pick
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
    try:
        title = data['TIT2'].text[0]
    except:
        title = 'Unknown Title'
    try:
        artist = data['TPE1'].text[0]
    except:
        artist = 'Unknown Artist'
    try:
        album = data['TALB'].text[0]
    except:
        album = 'Unknown Album'
    return {'title':title, 'artist':artist, 'album':album, 'length':data.info.length}

def playSong(fname):
    subprocess.Popen(['cmus-remote', '-c', '-q'])
    subprocess.Popen(['cmus-remote', '-q', fname])
    time.sleep(1)
    subprocess.Popen(['cmus-remote', '-n'])
    subprocess.Popen(['cmus-remote', '-p'])

class PlayGame():
    def __init__(self):
        self.directory = None
        self.song_list = None
        self.song_fnames = None
        self.allsongs = None
        self.mode = None
        self.rounds = None
        self.totalscore = 0
        self.round = 1
        self.optcount = 5

        self.readConf()
        self.getMode()
        self.getNumRounds()
        self.getAllSongs()
        while self.round <= self.rounds:
            self.playRound()
        print(f'Your total score was {self.totalscore:02f}!')

    def readConf(self):
        with open('NtT.conf') as f:
            d = dict(line.rstrip().split('=') for line in f)
        self.directory = d['Directory'].strip()
        self.optcount = int(d['NumChoices'].strip())

    def getMode(self):
        title='Please select which mode you would like to play:'
        opts = {'Name the Tune':'title',
                'Name the Artist':'artist',
                'Name the Album':'album'}
        choice,idx = pick(list(opts.keys()), title, indicator='->')
        self.mode = opts[choice]

    def getNumRounds(self):
        self.rounds = int(input('How many rounds would you like? '))

    def getAllSongs(self):
        self.allsongs = getSongList(self.directory)
    
    def genOptions(self, n, mode):
        self.song_fnames = getSongChoices(self.allsongs,n)
        self.song_list = [getSongData(i)[mode] \
                for i in self.song_fnames ]

    def playRound(self):
        self.genOptions(self.optcount, self.mode)
        realpick = self.song_list[0]
        realfname = self.song_fnames[0]
        realdata = getSongData(realfname)
        random.shuffle(self.song_list)
        playSong(realfname)
        starttime = time.time()

        title = f'Round {self.round}: Guess the {self.mode}!'
        choice = None
        while choice != realpick:
            choice, idx = pick(self.song_list, title, indicator='->')
            self.song_list.remove(choice)
        elapsedtime = time.time()-starttime
        score = max(100*(1-*elapsedtime/realdata['length']) - (4-len(self.song_list))*20, 0)
        print('You guessed it!')
        print(f'Your score was {score:0.2f}')
        input('Press enter to continue to next round...')
        self.totalscore += score
        self.round += 1



if __name__ == '__main__':
    game = PlayGame()
