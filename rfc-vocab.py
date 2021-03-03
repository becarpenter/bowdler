#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Does target directory contain words from vocabulary file?
(this version is specific to rfc files.)
- In the vocabulary file, put one questionable word per line.
  (Parts of speech must be entered separately).
- If a word is completely unacceptable in all circumstances,
  precede it with an asterisk. (It will be flagged but not printed.)
- If word A is undesirable on its own, but OK when followed by word B,
  put "A B" on the same line, e.g. "black hole".
- If a whole phrase is undesirable, use + signs, e.g. "man+in+the+middle"
- Strings in double quotes are exempt from checking (e.g. "John White")
- Not case-sensistive
- Very short words (except "he") and blank lines are ignored
- Comments start with #
"""

#Written by Brian Carpenter, March 2021. NO rights reserved.
#The license is DWTFYWWI

#Needs Python3, tested on 3.7.

from tkinter import Tk
from tkinter.filedialog import asksaveasfile, askopenfilename, askdirectory
from tkinter.messagebox import showinfo

import time
import string
import sys
import os

class vocword:
    """Class for processed vocabulary items"""
    def __init__(self, head_word):
        self.head_word = head_word
        self.never = False
        self.OK_tail = None
        self.bad_tail = None
        self.raw = ""
        
def rf(f):
    """Return a file as a list of strings"""
    file = open(f, "r",encoding='utf-8', errors='replace')
    l = file.readlines()
    file.close()
    return l

def tname(x):
    """-> name of type of x"""
    return type(x).__name__

def nextw():
    """-> next word in target"""
    global lookahead, target
    while tname(target[lookahead]) == 'int':
        lookahead += 1
        if lookahead >= len(target):
            return "" #reached EOF
    lookahead += 1 #ready for next call
    return target[lookahead-1]
    
#Announce

Tk().withdraw() # we don't want a full GUI

T = "RFC vocabulary checker"

showinfo(title=T,
         message = "I'm going to need a vocabulary file & a target directory;\
                   only the rfc files will be checked.")

#Get file names
fn1 = None
fn2 = None
dn2 = None
while not fn1:
    fn1 = (askopenfilename(title="Select vocabulary file"))
while not dn2:
    dn2 = (askdirectory(title="Select target directory"))
                
#Read in data files

raw_vocab = rf(fn1)


#Tidy vocabulary (remove newlines, force lower case, ignore short words and comments)
raw_vocab = [x.replace('\n','').lower() for x in raw_vocab if x=='he\n' or (len(x)>3 and x[0]!="#")]

#Parse vocabulary
vocab = []
exempt = []
try:
    for v in raw_vocab:
        if v[0] == '"':
            #exempt phrase
            exempt.append(v.replace('"',''))
        elif " " in v:
            #suspect word but acceptable 2-word phrase
            head, tail = v.split(" ",1)
            newv = vocword(head)
            newv.OK_tail = tail
            vocab.append(newv)
        elif "+" in v:
            #multiword suspect phrase
            head, tail = v.split("+",1)
            newv = vocword(head)
            newv.bad_tail = tail.split("+")
            newv.raw = v.replace("+"," ")
            vocab.append(newv)
        elif v[0] == "*":
            #unprintable word
            newv = vocword(v[1:])
            newv.never = True
            vocab.append(newv)
        
        else:
            #suspect phrase
            vocab.append(vocword(v))
        if len(vocab) > 1000:
            0/0  #implausibly large vocabulary
except:
    showinfo(title=T,
         message = "Invalid vocabulary file.")
    exit()

#Select & prepare output file
showinfo(title=T,
         message = "Please select log file.")
    
result = asksaveasfile(defaultextension=".txt",
                       title="Select output file (Cancel to use standard output)")

if result:
    so = False
else:
    so = True
    result = sys.stdout
    showinfo(title=T,
         message = "Using standard output.")

print("Working on it... may take a few minutes.")

result.write("Generated at "
             + time.strftime("%Y-%m-%d %H:%M:%S UTC%z",time.localtime())+"\n")

log = []
log.append("Vocabulary '"+fn1+"' has "+str(len(vocab))+" entries & "
       +str(len(exempt))+" exempt phrases")
report = 0


#Walk the directory

for p1,p2,efiles in os.walk(dn2):
    for fn2 in efiles:
        #print(fn2)
        if not (fn2[0:3] == "rfc" and fn2[3] in "123456789"):
            continue

        raw_target = rf(dn2+'/'+fn2)

        ## Prepare target for checking:

        #Force lower case, remove exempt phrases
        for phrase in exempt:
            raw_target = [x.lower().replace(phrase,'') for x in raw_target]

        #Remove punctuation
        trans = "".maketrans('','',string.punctuation)
        raw_target = [x.replace('-',' ').replace('/',' ').translate(trans)
                      for x in raw_target]

        #Change target into a single array with interspersed line numbers
        target = []
        line_no = 0
        for l in raw_target:
            line_no += 1
            target.append(line_no)
            target += l.split()

        del raw_target

        log.append("Target '"+fn2+"' has "+str(line_no)+" lines.")

        ##print(log) #for debug

        #Find naughty words & phrases

        #We have to ignore line breaks due to multi-word cases,
        #but we have to retrieve them for logging. So we go word
        #by word, and can't use comprehensions because we sometimes
        #need to look ahead by several words.

        
        found = []
        naughty = False
        lookahead = 0

        for w in range(len(target)):
            suspect = target[w]
            if tname(suspect) == 'int':
                #New line - anything to log?
                if found != []:
                    naughty = True
                    out = "Line "+str(badline)+" contains: "
                    for word in found:
                        out += word+", "
                    log.append(out[:-2])
                
                #skip line number
                #(ideally we'd also skip footer & header in RFC format)
                line_no = suspect
                found = []
                continue
               
            for word in vocab:
                if word.head_word == suspect or word.head_word+"s" == suspect:
                    if word.OK_tail:
                        #check if OK couple
                        lookahead = w + 1
                        if not word.OK_tail in nextw():
                            #not the right 2nd word
                            badline = line_no
                            found.append(word.head_word)
                            report += 1
                    elif word.bad_tail:
                        #check if naughty tuple
                        clean = False
                        lookahead = w +1
                        for tail in word.bad_tail:
                            if not tail in nextw():
                                #not the tuple
                                clean = True
                                break
                        if not clean:
                            #the whole tuple is here
                            badline = line_no
                            found.append(word.raw)
                            report += 1
                    else:
                        #stand-alone word, mark it as found
                        badline = line_no
                        if word.never:
                            found.append("Unacceptable word")
                        else:
                            found.append(word.head_word)
                        report += 1
        if not naughty:
            log.pop() #don't log title of clean file
            
                
if not report:
    log.append("No words from vocabulary found")
else:
    log.append("Total words flagged: "+str(report))

for line in log:
    result.write(line+"\n")
if not so:
    result.close()

print("Exiting...")

showinfo(title=T,
         message = "Log file written.")


Tk().destroy()  #hopefully avoids GUI hangups

