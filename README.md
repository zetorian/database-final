# Final project 
for UND database class

# structure

## Web facing
### this structure should allow it to be copied / linked directly to most default apache web servers.

src/ -> active web server stuffs.

src/html -> html, actually displayed to the client

src/cgi-bin -> cgi python scripts, retrieve active data from user submitted forms and from database for display.

## Internal use

extra/ -> management scripts, helpful, but not needed during operation of the system and should not be available to remote users.


# MakeFile

The included makefile will assist in testing with an active web system. It will install the files into the http root for rapid testing, assuming everything is correctly configured.

Two environment variables are needed, PREFIX and GROUP. 
PREFIX is the prefix of your webserver root, i.e. /srv/http
GROUP is the group under which your webserver runs, i.e. http

set them like this ```PREFIX="/var/http" GROUP="root" sudo make install```
