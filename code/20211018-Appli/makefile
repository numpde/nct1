default:
	@cat makefile

all: clear_scenarios populate_scenarios simulate plot plot_ss chkp_new chkp_index upload

clear_scenarios:
	mkdir -p cleared
	rm -rf cleared/* && mv scenarios results python/plot python/plot_ss cleared || exit 0

populate_scenarios:
	mkdir -p scenarios
	. ../venv/*/activate && cd python && python populate_scenarios.py
	git add scenarios/*.m

simulate:
	~/Documents/*/*2021b/*/matlab -nodisplay -nosplash -nojvm -r "simulate; exit;"
	git add results/*.mat

plot:
	. ../venv/*/activate && cd python && python plot.py
	git add python/plot/*

plot_ss:
	. ../venv/*/activate && cd python && python plot_ss.py
	git add python/plot_ss/*

chkp_new:
	mkdir -p checkpoint
	d=checkpoint/$$(date +"%Y%m%d-%H%M%S"); mkdir $$d && cp -r *.sbproj model.html *.m scenarios results python/plot python/plot_ss $$d/; echo "$$d<br><a href='model.html'>base model</a>, <a href='scenarios/index.html'>scenarios</a>, <a href='plot/index.html'>time-course</a>, <a href='plot_ss/index.html'>steady-state</a><br>" > $$d/index.html; git add $$d && git commit $$d -m "$$d" && git commit . -m "checkpoint" && git log -n 1 --pretty=format:"<a href='https://github.com/numpde/nct1/tree/%H/$$(dirname $$(git ls-files --full-name | head -n 1))'>permalink</a><br>" >> $$d/index.html;

chkp_index:
	cd checkpoint; echo > index.html; for i in 20*; do echo "<a href='$$i'>$$i</a><br>" >> index.html; done; git add index.html; git commit index.html -m "checkpoint index";

upload:
	git commit *.sbproj *.m python/*.py -m "iteration" || true
	git commit scenarios results python/plot -m "scenarios" || true
	git add checkpoint/* || true
	git commit checkpoint -m "checkpoint" || true
	git push || git push || git push

