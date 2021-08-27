#include "cantera/thermo.h"
#include <iostream>

using namespace Cantera;
using namespace std;

// The actual code is put into a function that
// can be called from the main program.
void simple_demo()
{
    // Create a new phase
    std::unique_ptr<ThermoPhase> gas(newPhase("JP10.yaml"));
    
    // gaseous fuel species
    string fuelSpecies = "C10H16";

    // declare an array and assign values to the array
    double phi[50];
    for (int i = 0; i < 50; i++) {
        phi[i] = 0.0 + (0.4082*i);
    }

    int species = gas->nSpecies();

    // declare variables to store the data 
    double Tad[50];
    double Xeq[50];

    for (int i = 0; i < 50; i++){
        // set the state of the gas
        gas->setState_TP(1000, 101325);

        // set the equivalence ratio of gas
        gas->setEquivalenceRatio(phi[i], fuelSpecies, "O2:1.0, N2:3.76");

	// equilibrate the mixture adiabatically at constant P
        gas->equilibrate("HP","gibbs");

        // storing the resulting value of adiabatic temp and molefractions
        Tad[i] = gas->temperature();
        gas->getMoleFractions(Xeq);
        cout << "phi = " << phi[i] << "\t\t Xeq of CO = : " << Xeq[11] << "\t\t Xeq of CO2 = : " << Xeq[24] << endl;
    }   
}



// the main program just calls function simple_demo within
// a 'try' block, and catches CanteraError exceptions that
// might be thrown
int main()
{
    try {
        simple_demo();
    }
    catch (CanteraError& err) {
        std::cout << err.what() << std::endl;
    }
}


