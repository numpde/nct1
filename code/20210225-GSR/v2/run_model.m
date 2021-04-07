% RA, 2021-04-01

function run_model
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
	
	
	
	return
	
	%% 
	
	disp("Omission of RanBP1")
	
	m1 = load_model();
	
	s = (~cellfun(@isempty, regexpi({m1.Rules.Rule}, '^\[RanBP1\]')));
	m1.Rules(s).active = 0;
	
	responses = simulate(m1);
	
	report(m1, responses);
	
	%%
	
	disp("200% RCC1")
	
	m1 = load_model();
	
	s = ({m1.Parameters.Name} == "RCC1_total");
	m1.Parameters(s).Value = 2 * m1.Parameters(s).Value;

	responses = simulate(m1);
	
	report(m1, responses);
	
	
	%% 
	
	disp("50% RCC1")
	
	m1 = load_model();
	
	s = ({m1.Parameters.Name} == "RCC1_total");
	m1.Parameters(s).Value = 0.5 * m1.Parameters(s).Value;

	responses = simulate(m1);
	
	report(m1, responses);
	
	%% 
	
	disp("10% RCC1")
	
	m1 = sbioloadproject("GSR_v1.sbproj").m1;
	
	s = ({m1.Parameters.Name} == "RCC1_total");
	m1.Parameters(s).Value = 0.1 * m1.Parameters(s).Value;

	responses = simulate(m1);
	
	report(m1, responses);
	
	%% 
	
	disp("1% RCC1")
	
	m1 = sbioloadproject("GSR_v1.sbproj").m1;
	
	s = ({m1.Parameters.Name} == "RCC1_total");
	m1.Parameters(s).Value = 0.01 * m1.Parameters(s).Value;

	responses = simulate(m1);
	
	report(m1, responses);
	
	%% 
	
	disp("GTP:GDP = 500:0")
	
	m1 = sbioloadproject("GSR_v1.sbproj").m1;
	
	s = ({m1.Parameters.Name} == "GTP");
	d = ({m1.Parameters.Name} == "GDP");
	m1.Parameters(d).Value = 0 * m1.Parameters(s).Value;

	responses = simulate(m1);
	
	report(m1, responses);
	
	%% 
	
	disp("GTP:GDP = 500:50")
	
	m1 = sbioloadproject("GSR_v1.sbproj").m1;
	
	s = ({m1.Parameters.Name} == "GTP");
	d = ({m1.Parameters.Name} == "GDP");
	m1.Parameters(d).Value = 0.1 * m1.Parameters(s).Value;

	responses = simulate(m1);
	
	report(m1, responses);		
	
	%% 
	
	disp("GTP:GDP = 500:500")
	
	m1 = sbioloadproject("GSR_v1.sbproj").m1;
	
	s = ({m1.Parameters.Name} == "GTP");
	d = ({m1.Parameters.Name} == "GDP");
	m1.Parameters(d).Value = 1 * m1.Parameters(s).Value;

	responses = simulate(m1);
	
	report(m1, responses);
	
	%%
	
	disp("Saturating NTF2")
	
	m1 = sbioloadproject("GSR_v1.sbproj").m1;
	
	s = ({m1.Parameters.Name} == "kPerm_NTF2--RanGDP");
	d = ({m1.Parameters.Name} == "kPerm_RanGDP");
	m1.Parameters(d).Value = m1.Parameters(s).Value;

	responses = simulate(m1);
	
	report(m1, responses);
	
	%%
	
	disp("Omission of NTF2")
	
	m1 = sbioloadproject("GSR_v1.sbproj").m1;
	
	s = ({m1.Parameters.Name} == "kPerm_RanGTP");
	d = ({m1.Parameters.Name} == "kPerm_RanGDP");
	m1.Parameters(d).Value = m1.Parameters(s).Value;

	responses = simulate(m1);
	
	report(m1, responses);
	
	%%
	
	disp("200% RanGAP")
	
	m1 = sbioloadproject("GSR_v1.sbproj").m1;
	
	i = ({m1.Parameters.Name} == "RanGAP");
	m1.Parameters(i).Value = 2 * m1.Parameters(i).Value;

	responses = simulate(m1);
	
	report(m1, responses);
	
	%%
	
	disp("50% RanGAP")
	
	m1 = sbioloadproject("GSR_v1.sbproj").m1;
	
	i = ({m1.Parameters.Name} == "RanGAP");
	m1.Parameters(i).Value = 0.5 * m1.Parameters(i).Value;

	responses = simulate(m1);
	
	report(m1, responses);
	
	%%
	
	disp("50% permeability for RanGTP")
	
	m1 = sbioloadproject("GSR_v1.sbproj").m1;
	
	i = ({m1.Parameters.Name} == "kPerm_RanGTP");
	m1.Parameters(i).Value = 0.5 * m1.Parameters(i).Value;

	responses = simulate(m1);
	
	report(m1, responses);
	
	%%
	
	disp("200% permeability for RanGTP")
	
	m1 = sbioloadproject("GSR_v1.sbproj").m1;
	
	i = ({m1.Parameters.Name} == "kPerm_RanGTP");
	m1.Parameters(i).Value = 2 * m1.Parameters(i).Value;

	responses = simulate(m1);
	
	report(m1, responses);
	
	%%
	
	disp("400% permeability for RanGTP")
	
	m1 = sbioloadproject("GSR_v1.sbproj").m1;
	
	i = ({m1.Parameters.Name} == "kPerm_RanGTP");
	m1.Parameters(i).Value = 4 * m1.Parameters(i).Value;

	responses = simulate(m1);
	
	report(m1, responses);
	
end
