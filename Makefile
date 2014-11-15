ALL:
	python -m compileall *
clean:
	find . -name '*.pyc' -delete
