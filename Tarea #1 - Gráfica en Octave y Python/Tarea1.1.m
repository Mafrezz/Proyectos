#OBJETOS NUMERICOS
375
3.75e2
3.75E2
0x177

#RANGOS NUMERICOS
#numero_inicial:salto:numero_final
1:10
1:0.5:10
1:1.6:10

#MATRICES
M = [1, 2, 3; 4, 5, 6; 7, 8, 9]
M = [1:4;5:8]

#STRINGS-Cadena de caracteres
'Cadena de string'
"Cadena de string"
"\\"
"\a" #sonido de windows

#ESTRUCTURAS
x = struct()
x.secuencia = 1:5
x.matriz = [1,2;4,5]
x.string = 'Secuencia'
x.estructura = struct()
x.estructura.numero = 0x177
x.estructura.letra = 'A'

#OPERADORES
x = 2
y = 3
x + y
x - y
x * y
x / y
++x %x = x+1
--x %x = x-1

#OPERADORES de Comparación
x < y
x <= y
x == y
x > y
x >= y
x != y

#OPERADORES Boleanos
x = 1
y = 0
x & y
x | y
not(x)
