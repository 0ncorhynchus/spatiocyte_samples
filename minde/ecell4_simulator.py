#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ecell4 import *
import csv

duration = 100 #sec

with species_attributes():
    cytoplasm | {'radius': '1e-8', 'D': '0'}
    MinDatp | MinDadp | {'radius': '1e-8', 'D': '16e-12', 'location': 'cytoplasm'}
    MinEE_C | {'radius': '1e-8', 'D': '10e-12', 'location': 'cytoplasm'}
    membrane | {'radius': '1e-8', 'D': '0', 'location': 'cytoplasm'}
    MinD | MinEE_M | MinDEE | MinDEED | {'radius': '1e-8', 'D': '0.02e-12', 'location': 'membrane'}

with reaction_rules():
    membrane + MinDatp > MinD | 2.2e-8
    MinD + MinDatp > MinD + MinD | 3e-20
    MinD + MinEE_C > MinDEE | 5e-19
    MinDEE > MinEE_M + MinDadp | 1
    MinDadp > MinDatp | 5
    MinDEE + MinD > MinDEED | 5e-15
    MinDEED > MinDEE + MinDadp | 1
    MinEE_M > MinEE_C | 0.83

m = get_model()

f = spatiocyte.SpatiocyteFactory(1e-8)
w = f.create_world(Real3(4.6e-6, 1.1e-6, 1.1e-6))
w.bind_to(m)

rod = Rod(3.5e-6, 0.51e-6, w.edge_lengths()*0.5)
w.add_structure(Species('cytoplasm'), rod)
w.add_structure(Species('membrane'), rod.surface())
w.add_molecules(Species('MinDadp'), 1300)
w.add_molecules(Species('MinDEE'), 700)

sim = f.create_simulator(m, w)
alpha = reduce(lambda x, y: min(x, sim.calculate_alpha(y)), m.reaction_rules())
sim.set_alpha(alpha)

obs = FixedIntervalNumberObserver(0.01, ('MinEE_M', 'MinD', 'MinDEE', 'MinDEED'))
sim.run(duration, obs)

with open('ecell4_data.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(obs.data())
