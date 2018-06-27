clean:
	find . -name '*.pyc' -exec rm '{}' \;
	find . -name '*.pyo' -exec rm '{}' \;

reqs:
	pip-compile --output-file ./requirements.txt ./requirements.in

dist:
	rm -Rf ./dist/*
	python setup.py sdist

deploy: bump dist
	ansible-playbook ./sync.yml -l vanyli -v

bump:
	python -c "from  ndbattle.cli import bump_version; bump_version()"

static:
	lessc ./ndbattle/project_static/less/master.less ./ndbattle/project_static/css/master.css


.PHONY: clean dist deploy bump static reqs
