PYTHON ?= python


archpkg:
	-rm -r packages/
	mkdir packages
	cp contrib/PKGBUILD packages/
	python setup.py sdist --dist-dir packages
	cd packages && makepkg -ci
