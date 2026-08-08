pkg load database

% Definición de categorías
bajoPeso = "Bajo peso";
pesoNormal = "Peso normal";
sobrePeso = "Sobrepeso";

% Conexión a PostgreSQL
conn = pq_connect(setdbopts('dbname', 'postgres', ...
'host', 'localhost', ...
'port', '5432', ...
'user', 'postgres', ...
'password', 'mafer123'));

while true
    % Mostrar opciones
    disp("Menú:");
    disp("1. Calcular IMC y guardar información");
    disp("2. Leer información del archivo");
    disp("3. Borrar información del archivo");
    disp("4. Salir");

    opcion = input("Ingrese la opción deseada: ");

    if !(1 <= opcion && opcion <= 4)
        disp("Opción no válida. Intente de nuevo.");
        continue;
    end

    switch opcion
        case 1
            % Entrada de datos
            nombre = input("Ingrese su nombre: ", "s");
            peso = input("Ingrese su peso en kilogramos: ");
            altura = input("Ingrese su altura en metros: ");

            % Cálculo del IMC
            imc = peso / (altura^2);

            % Clasificación
            if imc < 18.5
                categoria = bajoPeso;
            elseif imc < 25
                categoria = pesoNormal;
            else
                categoria = sobrePeso;
            end

            % Mostrar resultados
            fprintf("Hola %s, tu IMC es: %.2f\n", nombre, imc);
            fprintf("Categoría: %s\n", categoria);

            % Guardar en archivo
            archivo = fopen("imc.txt", "w");
            fprintf(archivo, "Nombre: %s\nPeso: %.2f kg\nAltura: %.2f m\nIMC: %.2f\nCategoría: %s\n", ...
                    nombre, peso, altura, imc, categoria);
            fclose(archivo);
            disp("Información guardada en 'imc.txt'");

            % Guardar en PostgreSQL
            query = sprintf(["INSERT INTO imc (nombre, peso, altura, imc, categoria) VALUES (" ...
                "'%s', %.2f, %.2f, %.2f, '%s');"], ...
                nombre, peso, altura, imc, categoria);
            pq_exec_params(conn, query);
            disp("Información guardada en PostgreSQL.");

        case 2
            % Leer información del archivo
            archivo = fopen("imc.txt", "r");
            if archivo == -1
                disp("No existe el archivo 'imc.txt'");
            else
                while ~feof(archivo)
                    linea = fgetl(archivo);
                    disp(linea);
                end
                fclose(archivo);
            end

        case 3
            % Borrar archivo
            if exist("imc.txt", "file")
                delete("imc.txt");
                disp("Archivo 'imc.txt' eliminado.");
            else
                disp("No existe el archivo 'imc.txt'.");
            end

        case 4
            % Salir
            disp("¡Gracias por usar el programa!");
            break;
    end
end

% Cerrar conexión a PostgreSQL
pq_close(conn);

