PYTHON ?= python


install:
	$(PYTHON) setup.py build
	$(PYTHON) setup.py install --skip-build -O1 --root=$(DESTDIR)

archpkg:
	-rm -r packages/
	mkdir packages
	umask 0022 && $(PYTHON) setup.py sdist --dist-dir packages
	cp contrib/PKGBUILD packages/
	cd packages && makepkg -ci

