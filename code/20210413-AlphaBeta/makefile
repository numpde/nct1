default:
	@cat makefile

all: populate_scenarios simulate plot chkp_new chkp_index upload

populate_scenarios:
	. ../venv/*/activate && cd python && python populate_scenarios.py
	git add scenarios/*.m

simulate:
	~/Documents/*/*/*/matlab -nodisplay -nosplash -nojvm -r "simulate; exit;"
	git add results/*.mat

plot:
	. ../venv/*/activate && cd python && python plot.py
	git add python/plot/*

chkp_new:
	d=checkpoint/$$(date +"%Y%m%d-%H%M%S"); mkdir $$d && cp -r *.sbproj simulate.m scenarios results python/plot  $$d/;

chkp_index:
	cd checkpoint; echo > index.html; for i in 2021*; do echo "<a href='$$i/scenarios/index.html'>$$i</a>: <a href='$$i/plot/index.html'>figures</a> <br>" >> index.html; done

upload:
	git commit alpha_beta.sbproj *.m python/*.py -m "iteration" || true
	git commit scenarios results python/plot -m "scenarios" || true
	git add checkpoint/* || true
	git commit checkpoint -m "checkpoint" || true
	git push || git push || git push
