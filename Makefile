all:

profile:
	$(PYTHON) -m cProfile -o cProfile.log file-entropy.py $(ARGS)

.PSEUDO: all profile
