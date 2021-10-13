% RA, 2021-05-14

function simulate
	delete("diary.txt");
	diary("diary.txt");
	diary on;
	
	close all;
	
	try
		fid = fopen('model.html', 'wt');
		fprintf(fid, evalc("model_to_html(load_model())"));
		fclose(fid);
		
		main()
	catch ex
		disp(" ")
		disp("main() failed:")
		disp(ex.identifier)
		disp(ex.message)
	end

	diary off;
end

function main()
	out_dir = "results/";
	[~, ~, ~] = mkdir(out_dir);
	
	scenarios = dir("scenarios/*.m");

	for n = 1:length(scenarios)
		scenario = scenarios(n);
		script = strcat(scenario.folder, "/", scenario.name);
		
		disp(strcat("Running scenario: ", scenario.name));

		m = load_model();

		T = 1e6; % seconds
		set(getconfigset(m, 'active'), 'Stoptime', T);
	
		run(script);

		[t, x, names] = sbiosimulate(m);

		equations = m.getequations;
		save(strcat(out_dir, "/", scenario.name(1:end-2), ".mat"), 't', 'x', 'names', 'equations', '-nocompression');
	end
end
	
function [m] = load_model()
	m = sbioloadproject("alpha_beta.sbproj").m1;
end
