ifeq ($(GROUP),)
	GROUP := http
endif

ifeq ($(PREFIX),)
	PREFIX := /srv/http
endif

install: src/html src/cgi-bin
	install -g $(GROUP) -d $(DESTDIR)$(PREFIX)/cgi-bin
	install -g $(GROUP) -d $(DESTDIR)$(PREFIX)/html
	install -g $(GROUP) -m 644 src/cgi-bin/* $(DESTDIR)$(PREFIX)/cgi-bin/
	install -g $(GROUP) -m 644 src/html/* $(DESTDIR)$(PREFIX)/html/
