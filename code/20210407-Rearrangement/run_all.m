% RA, 2021-04-07

function run_all
	[~, ~, ~] = mkdir("results");
	delete("results/diary.txt");
	diary("results/diary.txt");
	diary on;
	
	close all;
	
	main();

	diary off;
end

function main()
	m = load_model();
	sbmlexport(m);

	T = 1e4; % seconds
	set(getconfigset(m, 'active'), 'Stoptime', T);

	[t, x, names] = sbiosimulate(m);

	name = ['default'];

	equations = m.getequations;
	save(strcat("results", "/", name, ".mat"), 't', 'x', 'names', 'equations', '-nocompression');
end
	
function [m] = load_model()
	m = sbioloadproject("IBB_ImpB_rearrangement.sbproj").m1;
end

