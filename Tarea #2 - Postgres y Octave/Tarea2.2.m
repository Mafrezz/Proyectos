%FUNCIONES
[x,b] = hipotenusa(2,2)

%GRAFICAS
x = [-3:0.1:1]; %Rango,saltos,rango
x = linspace(-3,1,50) %De donde, a donde, cuantos puntos
plot(x,funcion(x), 'LineStyle',':');
title('Titulo')
ylabel('Eje y')
xlabel('Eje x')

x = [-3:0.1:1]; %Rango,saltos,rango
x = linspace(-3,1,50) %De donde, a donde, cuantos puntos
stem(x,funcion(x), 'LineStyle',':');
title('Titulo')
ylabel('Eje y')
xlabel('Eje x')
legend('Funcion')

%FUNCION SENO Y COSENO
x = [0:0.1:4*pi];
y1 = sin(x);
y2 = cos(x);
hold on;
p1 = plot(x,y1);
p2 = plot(x,y2);
set(p1, 'Color', 'green', 'LineWidth', 2);
set(p2, 'Color', 'blue', 'LineWidth', 1);
ylabel('Eje y');
xlabel('Eje x');
title('Seno y Coseno');
legend('Seno', 'Coseno');
hold off;

