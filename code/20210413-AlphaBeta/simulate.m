% RA, 2021-05-14

function simulate
	delete("diary.txt");
	diary("diary.txt");
	diary on;
	
	close all;
	main();

	diary off;
end

function main()
	out_dir = "results/";
	[~, ~, ~] = mkdir(out_dir);
	
	scenarios = dir("scenarios/*.m");

	for n = 1:length(scenarios)
		scenario = scenarios(n);

		m = load_model();

		T = 1e6; % seconds
		set(getconfigset(m, 'active'), 'Stoptime', T);
	
		run(strcat(scenario.folder, "/", scenario.name));

		[t, x, names] = sbiosimulate(m);

		equations = m.getequations;
		save(strcat(out_dir, "/", scenario.name(1:end-2), ".mat"), 't', 'x', 'names', 'equations', '-nocompression');
	end
end
	
function [m] = load_model()
	m = sbioloadproject("alpha_beta.sbproj").m1;
end
