default:
	@cat makefile
	
all: populate_scenarios simulate plot


populate_scenarios:
	. ../venv/*/activate && cd python && python populate_scenarios.py

simulate:
	~/Documents/*/*/*/matlab -nodisplay -nosplash -nojvm -r "simulate; exit;"

plot:
	. ../venv/*/activate && cd python && python plot.py


