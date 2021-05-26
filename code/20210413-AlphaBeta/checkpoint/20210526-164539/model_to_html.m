% model_to_html(m)
%	Usage:
%
%	fid = fopen('model.html', 'wt');
%	fprintf(fid, evalc("model_to_html(sbioloadproject('model.sbproj').m1)"));
%	fclose(fid);
%
%	RA, 2021-05-22, The Unlicense

function model_to_html(m)
	assert(class(m) == "SimBiology.Model")

	%%
	
	disp(strcat("Model name: ", m.Name))
	
	br()
	
	disp(datestr(datetime))
	
	br()
	br()
	
	%%
	
	disp("Model parameters")
	
	disp("<table border='1px'>")
	line({"Parameter", "BoundaryCondition", "ConstantValue", "Value", "Units", "Notes"})
	for i = (1 : length(m.Parameters))
		p = m.Parameters(i);
		line({p.Name, p.BoundaryCondition, p.ConstantValue, p.Value, p.Units, p.Notes})
	end
	disp("</table>")
	
	br()
	br()
	
	%%
	
	disp("Compartments")
	
	disp("<table border='1px'>")
	line({"Name", "ConstantCapacity", "Capacity", "CapacityUnits", "Notes"})
	for i = (1 : length(m.Compartments))
		c = m.Compartments(i);
		line({c.Name, c.ConstantCapacity, c.Capacity, c.CapacityUnits, c.Notes})
	end
	disp("</table>")
	
	br()
	br()
	
	%%
	
	disp("Species")
	
	disp("<table border='1px'>")
	line({"Compartment", "Name", "ConstantAmount", "InitialAmount", "InitialAmountUnits", "Notes"})
	for i = (1 : length(m.Species))
		s = m.Species(i);
		line({s.Parent.Name, s.Name, s.ConstantAmount, s.InitialAmount, s.InitialAmountUnits, s.Notes})
	end
	disp("</table>")
	
	br()
	br()
	
	%%
	
	disp("Reaction parameters")

	disp("<table border='1px'>")
	line({"ReactionName", "Reaction", "Parameter", "ConstantValue", "Value", "Units", "Notes"})
	for i = (1 : length(m.Reactions))
		r = m.Reactions(i);
		k = r.KineticLaw;
		for j = (1 : length(k.Parameters))
			p = k.Parameters(j);
			line({r.Name, r.Reaction, p.Name, p.ConstantValue, p.Value, p.Units, p.Notes})
		end
	end
	disp("</table>")
	
	br()
	br()
	
	%%
	
	disp("Reactions")

	disp("<table border='1px'>")
	line({"Name", "Active", "Reversible", "Reaction", "ReactionRate", "Notes"})
	for i = (1 : length(m.Reactions))
		r = m.Reactions(i);
		line({r.Name, r.Active, r.Reversible, r.Reaction, r.ReactionRate, r.Notes})
	end
	disp("</table>")
	
	br()
	br()
	
	%%
	
	disp("Equations dump")
	disp("<pre>")
	disp(m.getequations())
	disp("</pre>")
	
	return
	
	%%
	
	% How to use:
	
	html = evalc("model_to_html(m)");
	
	fid = fopen('model.html', 'wt');
	fprintf(fid, html);
	fclose(fid);
end

function line(arr)
	disp("<tr>")
	for na = (1 : length(arr))
		disp("<td>")
		if islogical(arr{na})
			if arr{na}
				disp("true")
			else
				disp("false")
			end
		else
			disp(arr{na})
		end
		disp("</td>")
	end
	disp("</tr>")
end

function br()
	disp("<br>")
end
