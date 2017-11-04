# PARMES multi-test Makefile

.PHONY: gen
gen:
	python 0-gen-bin.py

.PHONY: solfec-1
solfec-1:
	python 1-run-solfec.py

.PHONY: all
all: gen solfec-1

.PHONY: clean
clean:
	rm -fr config
	rm -fr parmec
	rm -fr solfec
	rm -fr run.sh
