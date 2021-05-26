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
	d=checkpoint/$$(date +"%Y%m%d-%H%M%S"); mkdir $$d && cp -r *.sbproj model.html *.m scenarios results python/plot $$d/; echo "$$d<br><a href='model.html'>base model</a>, <a href='scenarios/index.html'>scenarios</a>, <a href='plot/index.html'>figures</a><br>" > $$d/index.html; git add $$d && git commit $$d -m "$$d" && git commit . -m "checkpoint" && git log -n 1 --pretty=format:"<a href='https://github.com/numpde/nct1/tree/%H/$$(dirname $$(git ls-files --full-name | head -n 1))'>permalink</a><br>" >> $$d/index.html;

chkp_index:
	cd checkpoint; echo > index.html; for i in 2021*; do echo "<a href='$$i'>$$i</a><br>" >> index.html; done; git commit index.html -m "checkpoint index";

upload:
	git commit alpha_beta.sbproj *.m python/*.py -m "iteration" || true
	git commit scenarios results python/plot -m "scenarios" || true
	git add checkpoint/* || true
	git commit checkpoint -m "checkpoint" || true
	git push || git push || git push

