# bowdler
 A simple Python3 tool to log questionable terminology in a draft or RFC.

- It needs two input files, a vocabulary and the target document (preferably plain text,
but an HTML or even XML2RFC file is usually OK)
- It generates an output log file (or sends the log to standard output if you prefer)
- Uses Tk to provide a simple GUI
- Tested on Windows 10 and Linux with Python 3.7

The vocabulary file is plain text:

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

The program is bowdler.py

An example vocabulary file is rudewords.txt
