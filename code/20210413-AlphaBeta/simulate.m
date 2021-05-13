% RA, 2021-05-14

function simulate
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
	%sbmlexport(m);

	T = 1e6; % seconds
	set(getconfigset(m, 'active'), 'Stoptime', T);
	
	for hydro = [1e-5, 1e-4, 1e-3, 0.01, 0.1]
		r = m.Reactions({m.Reactions.Name} == "hydrolysis2");
		k = r.KineticLaw;
		p_hydro = k.Parameters({k.Parameters.Name} == "kf");
		p_hydro.Value = hydro;

		[t, x, names] = sbiosimulate(m);
		
		condition = str2mat(strcat("k_{hydrolysis} = ", num2str(p_hydro.Value), ", ", p_hydro.Units));
		disp(condition)

		filename = strcat("default");
		filename = strcat(filename, "__", "hydro=", num2str(p_hydro.Value));

		equations = m.getequations;
		save(strcat("results", "/", filename, ".mat"), 't', 'x', 'names', 'equations', 'condition', 'hydro', '-nocompression');
	end
end
	
function [m] = load_model()
	m = sbioloadproject("alpha_beta.sbproj").m1;
end
