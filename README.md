Leadsheet
==============
Leadsheet converts audio music files into leadsheets printing the chords. 
The leadsheet is written or printed using [Lilypond](http://www.lilypond.org) format. 

Install
---------------------
Requires Python3

    pip install --upgrade pip
    pip install numpy
    pip install --trusted-host pypi.python.org -r requirements.txt

Required Vamp Plugins can be downloaded from [https://www.vamp-plugins.org/download.html] and must be extracted to the directory $HOME/vamp
- nnls-chroma
- vamp-example-plugins

Usage
---------------------
    ./vmpt-leadsheet.py InputAudioFile + [OutputLilypondFile] 