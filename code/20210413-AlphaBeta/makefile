default:
	@cat makefile
	
all: simulate plot


simulate:
	~/Documents/*/*/*/matlab -nodisplay -nosplash -nojvm -r "simulate; exit;"

plot:
	. ../venv/*/activate && cd python && python plot.py


