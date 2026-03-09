PYTHON ?= python3

.PHONY: help sorting oscillator

help:
	@printf "Available targets:\n"
	@printf "  make sorting    Run the sorting benchmark toy project\n"
	@printf "  make oscillator Run the harmonic oscillator toy project\n"

sorting:
	$(PYTHON) -m projects.algorithms.sorting_lab.run

oscillator:
	$(PYTHON) -m projects.physics.harmonic_oscillator.run
