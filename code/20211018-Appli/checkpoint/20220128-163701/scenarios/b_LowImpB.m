% Autogenerated by populate_scenarios.py on UTC-20220128-143547.

c = m.Compartments({m.Compartments.Name} == "C");
assert(1 == length(c));
assert(c.Units == "picoliter");
c.Value = 1;

c = [m.Species.Parent];
s = m.Species(({m.Species.Name} == "CAS(c)") & ({c.Name} == "C"));
assert(1 == length(s));
assert(s.Units == "uM");
s.Value = 1;

c = [m.Species.Parent];
s = m.Species(({m.Species.Name} == "CAS(n)") & ({c.Name} == "C"));
assert(1 == length(s));
assert(s.Units == "uM");
s.Value = 1;

c = [m.Species.Parent];
s = m.Species(({m.Species.Name} == "Ran·GTP(n)") & ({c.Name} == "C"));
assert(1 == length(s));
assert(s.Units == "uM");
s.Value = 3;

c = [m.Species.Parent];
s = m.Species(({m.Species.Name} == "NPC(c)") & ({c.Name} == "C"));
assert(1 == length(s));
assert(s.Units == "uM");
s.Value = 0.01;

c = [m.Species.Parent];
s = m.Species(({m.Species.Name} == "NPC") & ({c.Name} == "C"));
assert(1 == length(s));
assert(s.Units == "uM");
s.Value = 1;

c = [m.Species.Parent];
s = m.Species(({m.Species.Name} == "NPC(n)") & ({c.Name} == "C"));
assert(1 == length(s));
assert(s.Units == "uM");
s.Value = 0.01;

c = [m.Species.Parent];
s = m.Species(({m.Species.Name} == "ImpB(c)") & ({c.Name} == "C"));
assert(1 == length(s));
assert(s.Units == "uM");
s.Value = 0.5;

c = [m.Species.Parent];
s = m.Species(({m.Species.Name} == "ImpB(n)") & ({c.Name} == "C"));
assert(1 == length(s));
assert(s.Units == "uM");
s.Value = 0.5;

c = [m.Species.Parent];
s = m.Species(({m.Species.Name} == "ImpA(c)") & ({c.Name} == "C"));
assert(1 == length(s));
assert(s.Units == "uM");
s.Value = 4;

c = [m.Species.Parent];
s = m.Species(({m.Species.Name} == "ImpA(n)") & ({c.Name} == "C"));
assert(1 == length(s));
assert(s.Units == "uM");
s.Value = 4;

r = m.Reactions({m.Reactions.Name} == "hydrolysis of Ran·GTP·ImpB·NPC");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kf");
assert(1 == length(p));
assert(p.Units == "1/s");
p.Value = 0.1;

r = m.Reactions({m.Reactions.Name} == "hydrolysis of ImpA·CAS·Ran·GTP·NPC");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kf");
assert(1 == length(p));
assert(p.Units == "1/s");
p.Value = 1e-2;

r = m.Reactions({m.Reactions.Name} == "CAS with Ran");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kf");
assert(1 == length(p));
assert(p.Units == "1/uM/s");
p.Value = 0.01;

r = m.Reactions({m.Reactions.Name} == "CAS with Ran");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kr");
assert(1 == length(p));
assert(p.Units == "1/s");
p.Value = 0.015;

r = m.Reactions({m.Reactions.Name} == "CAS with NPC(c)");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kf");
assert(1 == length(p));
assert(p.Units == "1/uM/s");
p.Value = 1e-3;

r = m.Reactions({m.Reactions.Name} == "CAS with NPC(c)");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kr");
assert(1 == length(p));
assert(p.Units == "1/s");
p.Value = 1e-4;

r = m.Reactions({m.Reactions.Name} == "CAS with NPC(n)");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kf");
assert(1 == length(p));
assert(p.Units == "1/uM/s");
p.Value = 1e-3;

r = m.Reactions({m.Reactions.Name} == "CAS with NPC(n)");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kr");
assert(1 == length(p));
assert(p.Units == "1/s");
p.Value = 1e-4;

r = m.Reactions({m.Reactions.Name} == "CAS·Ran with ImpA");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kf");
assert(1 == length(p));
assert(p.Units == "1/uM/s");
p.Value = 0.1;

r = m.Reactions({m.Reactions.Name} == "CAS·Ran with ImpA");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kr");
assert(1 == length(p));
assert(p.Units == "1/s");
p.Value = 1e-4;

r = m.Reactions({m.Reactions.Name} == "Complex CAS with NPC(c)");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kf");
assert(1 == length(p));
assert(p.Units == "1/uM/s");
p.Value = 1e-3;

r = m.Reactions({m.Reactions.Name} == "Complex CAS with NPC(c)");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kr");
assert(1 == length(p));
assert(p.Units == "1/s");
p.Value = 1e-5;

r = m.Reactions({m.Reactions.Name} == "Complex CAS with NPC(n)");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kf");
assert(1 == length(p));
assert(p.Units == "1/uM/s");
p.Value = 1e-3;

r = m.Reactions({m.Reactions.Name} == "Complex CAS with NPC(n)");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kr");
assert(1 == length(p));
assert(p.Units == "1/s");
p.Value = 1e-5;

r = m.Reactions({m.Reactions.Name} == "Replenish NLS");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kf");
assert(1 == length(p));
assert(p.Units == "1/s");
p.Value = 0;

r = m.Reactions({m.Reactions.Name} == "Passive diffusion");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "k_diff");
assert(1 == length(p));
assert(p.Units == "1/s");
p.Value = 0;

r = m.Reactions({m.Reactions.Name} == "Ran gradient");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "k_pump");
assert(1 == length(p));
assert(p.Units == "1/s");
p.Value = 1e-2;

