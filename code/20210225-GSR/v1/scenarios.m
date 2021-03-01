% RA, 2021-02-26

function scenarios
	close all;

	m1 = sbioloadproject("GSR_v1.sbproj").m1;

	index_of = containers.Map();
	for s = (1 : length(m1.Species))
		index_of(m1.Species(s).Name) = s;
	end

	% Note: to iterate species do
	%	for R = convertCharsToStrings({m1.Species.name})
	
	function responses = simulate(m)
		responses = {};

		T = 1000; % seconds
		set(getconfigset(m, 'active'), 'Stoptime', T);
		
		i_ex = (~cellfun(@isempty, regexpi({m.Rules.Rule}, '^Exercise')));
		
		m.Rules(i_ex).active = 0;
	
		[t, x] = sbiosimulate(m);
		for r = (1 : length(m.Species))
			responses{r} = x(end, r);
		end
		
		m.Rules(i_ex).active = 1;
		sdo = sbiosimulate(m);
		
% 		sdo.Name
		
		%responses{r + 1} = m.Parameters({m.Parameters.Name} == "Exercise").Value;
		responses{r + 1} = sdo.Data(end, sdo.DataNames == "Exercise");
	end

	function report(m, responses)
		disp(['Nuclear RanGTP     (uM): ' num2str(responses{index_of("RanGTP_nuc")})]);
		disp(['Cytoplasmic RanGTP (nM): ' num2str(1000 * responses{index_of("Total cyto RanGTP")})]);
		disp(['Dynamic capacity (uM/s): ' num2str(responses{end})]);
	end
	
	%% 
	
	disp("Standard conditions")
	
	m1 = sbioloadproject("GSR_v1.sbproj").m1;
	responses = simulate(m1);
	report(m1, responses);
	
	%% 
	
	disp("Omission of RanBP1")
	
	m1 = sbioloadproject("GSR_v1.sbproj").m1;
	
	s = (~cellfun(@isempty, regexpi({m1.Rules.Rule}, '^\[RanBP1\]')));
	m1.Rules(s).active = 0;
	
	responses = simulate(m1);
	
	report(m1, responses);
	
	%%
	
	disp("200% RCC1")
	
	m1 = sbioloadproject("GSR_v1.sbproj").m1;
	
	s = ({m1.Parameters.Name} == "RCC1_total");
	m1.Parameters(s).Value = 2 * m1.Parameters(s).Value;

	responses = simulate(m1);
	
	report(m1, responses);
	
	
	%% 
	
	disp("50% RCC1")
	
	m1 = sbioloadproject("GSR_v1.sbproj").m1;
	
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
