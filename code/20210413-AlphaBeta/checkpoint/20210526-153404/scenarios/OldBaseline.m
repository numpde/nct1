% Autogenerated by populate_scenarios.py on UTC-20210526-133233.

s = m.Species({m.Species.Name} == "CAS(c)");
assert(s.Units == "uM");
s.Value = 1;

s = m.Species({m.Species.Name} == "ΔCAS(c)");
assert(s.Units == "uM");
s.Value = 0;

s = m.Species({m.Species.Name} == "Ran·GTP(n)");
assert(s.Units == "uM");
s.Value = 3;

s = m.Species({m.Species.Name} == "NPC");
assert(s.Units == "uM");
s.Value = 1;

r = m.Reactions({m.Reactions.Name} == "hydrolysis of Ran·GTP·ImpB·NPC");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kf");
assert(p.Units == "1/s");
p.Value = 0.1;

r = m.Reactions({m.Reactions.Name} == "hydrolysis of ImpA·CAS·Ran·GTP·NPC");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kf");
assert(p.Units == "1/s");
p.Value = 0.1;

r = m.Reactions({m.Reactions.Name} == "CAS with Ran");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kf");
assert(p.Units == "1/uM/s");
p.Value = 0.01;

r = m.Reactions({m.Reactions.Name} == "CAS with Ran");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kr");
assert(p.Units == "1/s");
p.Value = 0.0048;

r = m.Reactions({m.Reactions.Name} == "CAS with NPC");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kf");
assert(p.Units == "1/uM/s");
p.Value = 1e-3;

r = m.Reactions({m.Reactions.Name} == "CAS with NPC");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kr");
assert(p.Units == "1/s");
p.Value = 1e-3;

r = m.Reactions({m.Reactions.Name} == "CAS·Ran with ImpA");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kf");
assert(p.Units == "1/uM/s");
p.Value = 0.1;

r = m.Reactions({m.Reactions.Name} == "Complex CAS with NPC");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kf");
assert(p.Units == "1/uM/s");
p.Value = 1e-3;

r = m.Reactions({m.Reactions.Name} == "Complex CAS with NPC");
k = r.KineticLaw;
p = k.Parameters({k.Parameters.Name} == "kr");
assert(p.Units == "1/s");
p.Value = 1e-4;

