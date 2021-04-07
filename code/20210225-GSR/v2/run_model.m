% RA, 2021-04-01

function run_model
	[~, ~, ~] = mkdir("results");
	delete("results/diary.txt");
	diary("results/diary.txt");
	diary on;
	
	close all;
	
	function [project_file] = load_model()
		project_file = sbioloadproject("nct.sbproj").m1;
	end

	m1 = load_model();
	
	sbmlexport(m1);

	% Note: to iterate species do
	%	for R = convertCharsToStrings({m1.Species.name})
		
	%%
	
	function responses = simulate(m, name)
		T = 1e4; % seconds
		set(getconfigset(m, 'active'), 'Stoptime', T);
		
		% i_ex = (~cellfun(@isempty, regexpi({m.Rules.Rule}, '^Exercise')));
		% m.Rules(i_ex).active = 0;
	
		[t, x, names] = sbiosimulate(m);
		
		responses = containers.Map();
		responses('t') = t;
		for i_ = (1 : length(names))
			responses(names{i_}) = x(:, i_);
		end
		
		[~, ~, ~] = mkdir("results");
		
		equations = m.getequations;
		save(strcat("results", "/", name), 't', 'x', 'names', 'equations', '-nocompression');
	end

	function report(responses)
		last = @(x) x(end);
		disp(['Nuclear RanGTP     (uM): ' num2str(last(responses("RanGTP_nuc")))]);
		disp(['Cytoplasmic RanGTP (nM): ' num2str(1000 * last(responses("Total cyto RanGTP")))]);
	end

	%%
	
	% Note: load the model anew for each scenario
	
	%% 
	
	disp("Baseline conditions")
	
	m1 = load_model();
	responses = simulate(m1, "Baseline");
 	report(responses);
	
	diary off;
end
