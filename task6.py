from pyDatalog import pyDatalog
pyDatalog.create_terms('X, Y, Z, contains, part_of')

# EDB
+ contains('Car', 'Engine')
+ contains('Engine', 'Piston')
+ contains('Piston', 'Ring')

# IDB
part_of(Y, X) <= contains(X, Y)
part_of(Y, X) <= contains(X, Z) & part_of(Y, Z)

print("Everything that is part of a Car:")
print(part_of(X, 'Car'))

print("Objects that contain a Ring")
print(part_of('Ring', X))
