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
