% RA, 2022-01-17

% UNFINISHED

function simulate_effective
	out_dir = "results_effective";
	[~, ~, ~] = mkdir(out_dir);
	
	initiate(out_dir)
	main(out_dir)
	finalize(out_dir)
end

function main(out_dir)
	for ImpB = [0, 0.34]
		for RanBP1 = [0, 0.2]
			for RanGAP = [0.01]

				[m, t_react] = config_model(ImpB, RanBP1, RanGAP);

				obj = sbiosimulate(m);
				t = obj.Time;
				x = obj.Data;
				names = obj.DataNames;

				name = strcat("ImpB=", num2str(ImpB), "_", "RanBP1=", num2str(RanBP1), "_", "RanGAP=", num2str(RanGAP));

				equations = m.getequations;
				save(strcat(out_dir, "/", name, ".mat"), 't', 'x', 'names', 'equations', 'ImpB', 'RanBP1', 'RanGAP', 't_react', '-nocompression');
			end
		end
	end
end

function [m, T] = config_model(ImpB, RanBP1, RanGAP)
	m = load_models().m2;
	
	% Conditions from Fig. 4A
	
	m.Species({m.Species.Name} == "Ran·GTP").InitialAmount = 0.25;
	
	m.Species({m.Species.Name} == "ImpB").InitialAmount = ImpB;
	m.Species({m.Species.Name} == "RanBP1").InitialAmount = RanBP1;
	m.Species({m.Species.Name} == "RanGAP").InitialAmount = RanGAP;
	
	m.Events({m.Events.Name} == "Add ImpB").Active = false;
	m.Events({m.Events.Name} == "Add RanBP1").Active = false;
	
	m.Events({m.Events.Name} == "Dilution").Active = false;
	m.Events({m.Events.Name} == "Add RanGAP").Active = false;

	T = 3600;
	cs = getconfigset(m, 'active');
	set(cs, 'Stoptime', T);
end


function [mm, names] = load_models()
	mm = sbioloadproject("rangap-sequence.sbproj");
	names = fieldnames(mm);
end

function initiate(out_dir)
	delete(strcat(out_dir, "/diary.txt"));
	diary(strcat(out_dir, "/diary.txt"));
	diary on;
	
	close all;
	
	[mm, fields] = load_models();
	for fn = {fields{:}}
		sbmlexport(mm.(fn{1}))
	end
end


function finalize(out_dir)
	diary off;
end
