# bowdler
 A simple Python3 tool to log questionable terminology in a draft or RFC.
 
**PLEASE NOTE:**

The IESG (the IETF's steering group) has issued a formal statement about inclusive language [https://www.ietf.org/about/groups/iesg/statements/on-inclusive-language/]. The tool in this repository has no purpose except logging the use of certain words or phrases in text files.

The tool:

- Needs two input files, a vocabulary and the target document (preferably plain text,
but an HTML or even XML2RFC file is usually OK)
- Generates an output log file (or sends the log to standard output if you prefer)
- Uses Tk to provide a simple GUI
- Has been tested on Windows 10 and Linux, both with Python 3.7

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

The alternative version, rfc-vocab.py, does the same thing but applies it to a whole directory of rfcs.

(Dr Thomas Bowdler was a 19th century British medical doctor famous for publishing an expurgated version of Shakespeare's plays. Whether this was a good or bad thing has been debated ever since. This software offers no judgment, simply information.)

