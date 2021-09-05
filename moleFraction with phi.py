# Variation of equilibrium products mole fractions (mainly CO2 CO and NOx) with different phi.

import matplotlib.pyplot as plt 
import cantera as ct
import numpy as np
import sys
import csv

# Edit these parameters to change the initial temperature, the pressure, and
# the phases in the mixture.

T = 1000.0
P = 101325.0 

# phases
gas = ct.Solution('JP10.yaml')
carbon = ct.Solution('graphite.yaml')

# the phases that will be included in the calculation, and their initial moles
mix_phases = [(gas, 1.0), (carbon, 0.0)]

# gaseous fuel species
fuel_species = 'C10H16'

# equivalence ratio range
npoints = 50
phi = np.linspace(0,20,npoints)

mix = ct.Mixture(mix_phases)

# create some arrays to hold the data
tad = np.zeros(npoints)
xeq = np.zeros((mix.n_species, npoints))

xeq_CO = np.zeros(npoints)
xeq_CO2 = np.zeros(npoints)

for i in range(npoints):
    # set the gas state
    gas.set_equivalence_ratio(phi[i], fuel_species, 'O2:1.0, N2:3.76')

    # create a mixture of 1 mole of gas, and 0 moles of solid carbon.
    mix = ct.Mixture(mix_phases)
    mix.T = T
    mix.P = P

    # equilibrate the mixture adiabatically at constant P
    mix.equilibrate('HP', solver='gibbs', max_steps=1000)

    tad[i] = mix.T
    xeq[:, i] = mix.species_moles
    xeq_CO[i] = xeq[11,i]
    xeq_CO2[i] = xeq[24,i]
    print('At phi = {0:12.4g}, Xco = {1:12.4g}, Xco2 = {2:12.4g}'.format(phi[i], xeq_CO[i], xeq_CO2[i]))
    


# write output CSV file for importing into Excel
csv_file = 'molefraction_with_phi.csv'
with open(csv_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['phi', 'T (K)'] + mix.species_names)
    for i in range(npoints):
        writer.writerow([phi[i], tad[i]] + list(xeq[:, i]))
print('Output written to {0}'.format(csv_file))

if '--plot' in sys.argv:
    plt.plot(phi, xeq_CO)
    plt.plot(phi, xeq_CO2)   
    plt.ylim([0,1])
    plt.xlim([0,2])
    plt.xlabel('Equivalence ratio')
    plt.ylabel('Mole fraction')
    plt.legend(['CO','CO2'])
    plt.show()   
        
    









