# Entrap Met Star

This is a regex pattern-matching module for use with the DFI text mining framework.

:pencil: It uses a system call to Python, since i didn't like the thought of having to convert regular expressions from Python-compatible syntax, to R-compatible syntax ("\\\s"). Might change this in the future by implementing some sort of translator. :blush:

:pencil: Most of what precedes the "process data" comment in the ems.R script is boilerplate, relating to the DFI implementation. The interesting manipulation goes on in the extRegexDf function, and its related functions located in the lib folder.

:wrench: This script depends on stringr, glue, redux and jsonlite.

:warning: Additionally, you need to install [DBgratia](https://github.com/peder2911/DB_gratia), which is the collection of redis-communication functions i am using to make all of these scripts less verbose.

EMS is a working title, and is a secret anagram :ghost:



