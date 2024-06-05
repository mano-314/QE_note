F_constant  = 9.648533212331 * 10000 # C/mol 
R_constant  = 8.314462618153         # J/K/mol 
ry2ev       = 13.6057039763
temperature = 298.15
pH          = 14 

ts_H2       = -0.404
A_H2        = -2.33023715 * ry2ev + ts_H2
A_H2O       = -34.68690840 * ry2ev
A_H3O       = -35.49605484 * ry2ev

Ezp_H2      = 0.271 
Ezp_H2O     = 0.558 
Ezp_H3O     = 0.891 

G_L         = 0.5 * (A_H2+Ezp_H2) + A_H2O + Ezp_H2O
G_R         = A_H3O + Ezp_H3O

U_SHE       = -(G_L-G_R)

pH =14 
U_RHE_14 = U_SHE - 2.303 * R_constant / F_constant * temperature * pH 

pH =10
U_RHE_10 = U_SHE - 2.303 * R_constant / F_constant * temperature * pH 

print('E(H+/H2)[vs. E_vac] (eV) = {:6.3f}'.format(U_SHE))
print('E(H+/H2)[vs. E_vac] (eV) = {:6.3f}'.format(U_RHE_14) + "  pH=14")
print('E(H+/H2)[vs. E_vac] (eV) = {:6.3f}'.format(U_RHE_10) + "  pH=10")
            
