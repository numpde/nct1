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
	m = load_model();
	%sbmlexport(m);

	T = 1e6; % seconds
	set(getconfigset(m, 'active'), 'Stoptime', T);
	
	setup{1}.folder = "results1";
	setup{1}.hydrolysis = ["hydrolysis1"];
	
	setup{2}.folder = "results2";
	setup{2}.hydrolysis = ["hydrolysis2"];
	
	setup{3}.folder = "results12";
	setup{3}.hydrolysis = ["hydrolysis1", "hydrolysis2"];
	
	for i = 1:length(setup)
		disp(setup{i}.folder)
		
		for hydro = [1e-5, 1e-4, 1e-3, 0.01, 0.1]
			for name = setup{i}.hydrolysis
				r = m.Reactions({m.Reactions.Name} == name);
				k = r.KineticLaw;
				p_hydro = k.Parameters({k.Parameters.Name} == "kf");
				p_hydro.Value = hydro;
			end

			[t, x, names] = sbiosimulate(m);

			equations = m.getequations;

			condition = str2mat(strcat("k_{hydrolysis} = ", num2str(p_hydro.Value), ", ", p_hydro.Units));
			disp(condition)

			filename = strcat("default");
			filename = strcat(filename, "__", "hydro=", num2str(p_hydro.Value));
			
			[~, ~, ~] = mkdir(setup{i}.folder);
			save(strcat(setup{i}.folder, "/", filename, ".mat"), 't', 'x', 'names', 'equations', 'condition', 'hydro', '-nocompression');
		end
	end
end
	
function [m] = load_model()
	m = sbioloadproject("alpha_beta.sbproj").m1;
end
