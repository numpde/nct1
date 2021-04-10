default:
	@cat makefile


fig4a: fig4a_matlab fig4a_python

fig4a_matlab:
	~/Documents/*/*/*/matlab -nodisplay -nosplash -nojvm -r "simulate_fig4a; exit;"

fig4a_python:
	. ../../venv/*/activate && cd python && python *_fig4a.py


