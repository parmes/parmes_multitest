# PARMES multi-test Makefile

.PHONY: gen
gen: dir
	python 0-gen-bin.py

.PHONY: solfec-1
solfec-1:
	python 1-run-solfec.py

.PHONY: all
all: gen solfec-1

.PHONY: dir
dir: clean
	mkdir config
	mkdir parmec
	mkdir solfec

.PHONY: clean
clean:
	rm -fr config
	rm -fr parmec
	rm -fr solfec
