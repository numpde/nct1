% RA, 2021-04-06

% function run_all	
	[~, ~, ~] = mkdir("results");
	delete("results/diary.txt");
	diary("results/diary.txt");
	diary on;
	
	close all;

	m = load_model();
	
	sbmlexport(m);

	index_of = containers.Map();
	for s = (1 : length(m.Species))
		index_of(m.Species(s).Name) = s;
	end
	
	%%
	
	for v = [1, 1e-1, 1e-2, 1e-3]
		m = load_model();
	
		E = m.Compartments({m.Compartments.Name} == "envelope");
		E.Value = E.Value * v;
		X = m.Species({m.Species.Name} == "Vacant NPC");
		X.Value = X.Value / v;
		
		T = 1e5; % seconds
		set(getconfigset(m, 'active'), 'Stoptime', T);
		
		[t, x, names] = sbiosimulate(m);
		
		name = ['v=' num2str(v)];
		
		equations = m.getequations;
		save(strcat("results", "/", name, ".mat"), 't', 'x', 'names', 'equations', '-nocompression');
		
		disp(strcat("NPC count", " = ", num2str(E.Value), " ", E.Unit, " x ", num2str(X.Value), " ", X.Units))
		for name = ["Cargo ratio", "Total ImpB ratio", "Total ImpB in envelope"]
			O = m.Observables({m.Observables.name} == name);
			disp(strcat(name, " = ", num2str(x(end, names == name)), " ", O.Units))
		end
		
		disp(" ");
	end

	diary off;
% end
	
function [m] = load_model()
	m = sbioloadproject("onestage_conveyor.sbproj").m1;
end

