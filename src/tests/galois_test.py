# import numpy as np
import galois

prim_numer = 36893488147419103183
n = 100
max_degree = 42

galois_field = galois.GF(prim_numer)
print(galois_field.properties)


random_poly = galois.Poly.Random(7, galois_field)
print(random_poly)
