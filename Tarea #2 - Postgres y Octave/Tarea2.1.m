%Estructura de control de flujo
x = 1
y = 0
z = -5

if (x > y & z < 0)
  'X es mayor a Y y Z es menor a 0'
elseif (x == y | z < 0)
  'X y Y son iguales'
else
  'Y es mayor a X'
endif

while(z < y)
'Valor de z'
z
++z
endwhile

fib = ones(1,10)
for i = 3:10
  fib(i) = fib (i-1) + fib(i-2);
endfor

fib

try
  m = [1:5;10:15]
catch
  'No se pudo ejectutar, se continúa con la ejecución normal del código'
end_try_catch

%OPERACIONES BÁSICAS CON MATRICES

H =
