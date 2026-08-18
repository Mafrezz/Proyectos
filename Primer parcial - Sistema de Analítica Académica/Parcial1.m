function Parcial1()

% ============================================================
% SISTEMA DE ANALITICA ACADEMICA
% OCTAVE + POSTGRESQL
% ============================================================


% ============================================================
% CARGAR PAQUETE DATABASE
% ============================================================

pkg load database;


% ============================================================
% CONFIGURACION
% ============================================================

max_tareas = 25;
max_parcial1 = 16;
max_parcial2 = 17;
max_parcial3 = 17;
max_examen = 25;

nota_aprobacion = 61;

archivo = 'notas.txt';


% ============================================================
% CONEXION A POSTGRESQL
% ============================================================

bd_disponible = false;
conn = [];


try

    conn = pq_connect(setdbopts( ...
        'dbname', 'postgres', ...
        'host', 'localhost', ...
        'port', '5432', ...
        'user', 'postgres', ...
        'password', 'mafer123'));

    bd_disponible = true;

    disp(' ');
    disp('Conexion con PostgreSQL establecida.');

catch

    bd_disponible = false;

    disp(' ');
    disp('PostgreSQL no disponible.');
    disp('Los registros se almacenaran en notas.txt.');

end


% ============================================================
% CREAR TABLA SI NO EXISTE
% ============================================================

if bd_disponible

    query_crear = ['CREATE TABLE IF NOT EXISTS notas_academicas (', ...
        'id SERIAL PRIMARY KEY, ', ...
        'carnet VARCHAR(30), ', ...
        'nombre VARCHAR(100), ', ...
        'tareas NUMERIC(5,2), ', ...
        'parcial1 NUMERIC(5,2), ', ...
        'parcial2 NUMERIC(5,2), ', ...
        'parcial3 NUMERIC(5,2), ', ...
        'examen_final NUMERIC(5,2), ', ...
        'nota_exacta NUMERIC(6,2), ', ...
        'nota_final INTEGER, ', ...
        'estado VARCHAR(20)', ...
        ');'];

    try

        pq_exec_params(conn, query_crear);

    catch

        disp('Advertencia: no se pudo verificar la tabla.');

    end

end


% ============================================================
% MENU PRINCIPAL
% ============================================================

opcion = 0;


while opcion ~= 4

    disp(' ');
    disp('==============================================');
    disp('       SISTEMA DE ANALITICA ACADEMICA');
    disp('==============================================');
    disp('1. Ingresar datos del estudiante');
    disp('2. Historial de datos');
    disp('3. Dashboard de graficas');
    disp('4. Salir');
    disp('==============================================');


    entrada = input( ...
        'Seleccione una opcion: ', 's');


    opcion = str2double(entrada);


    % ========================================================
    % VALIDAR OPCION
    % ========================================================

    if isnan(opcion) || ...
       opcion < 1 || ...
       opcion > 4 || ...
       opcion ~= fix(opcion)

        disp('ERROR: Seleccione una opcion entre 1 y 4.');

        opcion = 0;

        continue;

    end


    % ========================================================
    % OPCIONES
    % ========================================================

    switch opcion


        % ====================================================
        % OPCION 1: INGRESAR DATOS
        % ====================================================

        case 1

            disp(' ');
            disp('============= INGRESO DE DATOS =============');


            % =================================================
            % CARNET
            % =================================================

            while true

                carnet = strtrim(input( ...
                    'Ingrese el carnet: ', 's'));


                if length(carnet) == 9 && ...
                   ~isempty(regexp( ...
                   carnet, ...
                   '^[0-9]{9}$', ...
                   'once'))

                    break;

                else

                    disp( ...
                        'ERROR: El carnet debe contener exactamente 9 numeros.');

                end

            end


            % =================================================
            % NOMBRE
            % =================================================

            while true

                nombre = strtrim(input( ...
                    'Ingrese el nombre: ', 's'));


                if ~isempty(nombre) && ...
                   ~isempty(regexp( ...
                   nombre, ...
                   '^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+$', ...
                   'once'))

                    break;

                else

                    disp( ...
                        'ERROR: El nombre solo puede contener letras y espacios.');

                end

            end


            % =================================================
            % INGRESAR NOTAS
            % =================================================

            tareas = PedirNota( ...
                'Tareas (0-25): ', ...
                max_tareas);


            parcial1 = PedirNota( ...
                'Parcial 1 (0-16): ', ...
                max_parcial1);


            parcial2 = PedirNota( ...
                'Parcial 2 (0-17): ', ...
                max_parcial2);


            parcial3 = PedirNota( ...
                'Parcial 3 (0-17): ', ...
                max_parcial3);


            examen_final = PedirNota( ...
                'Examen Final (0-25): ', ...
                max_examen);


            % =================================================
            % CALCULAR NOTA EXACTA
            % =================================================

            nota_exacta = ...
                tareas + ...
                parcial1 + ...
                parcial2 + ...
                parcial3 + ...
                examen_final;


            % =================================================
            % REDONDEO
            % =================================================

            nota_final = ...
                RedondeoIngenieria(nota_exacta);


            % =================================================
            % DETERMINAR ESTADO
            % =================================================

            if nota_final >= nota_aprobacion

                estado = 'Aprobado';

            else

                estado = 'Reprobado';

            end


            % =================================================
            % MOSTRAR RESULTADO
            % =================================================

            disp(' ');
            disp('==============================================');
            disp('              RESULTADO ACADEMICO');
            disp('==============================================');

            fprintf('Carnet:       %s\n', carnet);
            fprintf('Nombre:       %s\n', nombre);
            fprintf('Tareas:       %.2f / 25\n', tareas);
            fprintf('Parcial 1:    %.2f / 16\n', parcial1);
            fprintf('Parcial 2:    %.2f / 17\n', parcial2);
            fprintf('Parcial 3:    %.2f / 17\n', parcial3);
            fprintf('Examen Final: %.2f / 25\n', examen_final);
            fprintf('Nota exacta:  %.2f\n', nota_exacta);
            fprintf('Nota final:   %d\n', nota_final);
            fprintf('Estado:       %s\n', estado);

            disp('==============================================');


            % =================================================
            % GUARDAR EN ARCHIVO
            % =================================================

            fileID = fopen(archivo, 'a');


            if fileID == -1

                disp('ERROR: No se pudo abrir notas.txt.');

            else

                fprintf(fileID, ...
                    '========================================\n');

                fprintf(fileID, ...
                    'REGISTRO ACADEMICO\n');

                fprintf(fileID, ...
                    '========================================\n');

                fprintf(fileID, ...
                    'Carnet: %s\n', carnet);

                fprintf(fileID, ...
                    'Nombre: %s\n', nombre);

                fprintf(fileID, ...
                    'Tareas: %.2f\n', tareas);

                fprintf(fileID, ...
                    'Parcial 1: %.2f\n', parcial1);

                fprintf(fileID, ...
                    'Parcial 2: %.2f\n', parcial2);

                fprintf(fileID, ...
                    'Parcial 3: %.2f\n', parcial3);

                fprintf(fileID, ...
                    'Examen Final: %.2f\n', examen_final);

                fprintf(fileID, ...
                    'Nota exacta: %.2f\n', nota_exacta);

                fprintf(fileID, ...
                    'Nota final: %d\n', nota_final);

                fprintf(fileID, ...
                    'Estado: %s\n', estado);

                fprintf(fileID, ...
                    '========================================\n\n');

                fclose(fileID);


                disp('Registro guardado en notas.txt.');


                % =================================================
                % GUARDAR EN POSTGRESQL
                % =================================================

                if bd_disponible

                    carnet_sql = ...
                        strrep(carnet, '''', '''''');

                    nombre_sql = ...
                        strrep(nombre, '''', '''''');


                    query = sprintf([ ...
                        'INSERT INTO notas_academicas ', ...
                        '(carnet, nombre, tareas, parcial1, ', ...
                        'parcial2, parcial3, examen_final, ', ...
                        'nota_exacta, nota_final, estado) ', ...
                        'VALUES (''%s'', ''%s'', %.2f, %.2f, ', ...
                        '%.2f, %.2f, %.2f, %.2f, %d, ''%s'');'], ...
                        carnet_sql, ...
                        nombre_sql, ...
                        tareas, ...
                        parcial1, ...
                        parcial2, ...
                        parcial3, ...
                        examen_final, ...
                        nota_exacta, ...
                        nota_final, ...
                        estado);


                    try

                        resultado = ...
                            pq_exec_params(conn, query);


                        if isempty(resultado)

                            disp( ...
                                'Advertencia: no se pudo guardar en PostgreSQL.');

                        else

                            disp( ...
                                'Registro guardado en PostgreSQL.');

                        end


                    catch

                        disp( ...
                            'Advertencia: no se pudo guardar en PostgreSQL.');

                    end

                else

                    disp( ...
                        'PostgreSQL no esta disponible.');

                end

            end


        % ====================================================
        % OPCION 2: HISTORIAL
        % ====================================================

        case 2

            MostrarHistorialArchivo();


        % ====================================================
        % OPCION 3: DASHBOARD
        % ====================================================

        case 3

            GenerarGraficasArchivo();


        % ====================================================
        % OPCION 4: SALIR
        % ====================================================

        case 4

            disp(' ');
            disp('==============================================');
            disp('Programa finalizado.');
            disp('Gracias por utilizar el Sistema de Analitica Academica.');
            disp('==============================================');

    end

end


endfunction


% ============================================================
% FUNCION PARA INGRESAR NOTAS
% ============================================================

function nota = PedirNota(mensaje, maximo)

    while true

        entrada = input(mensaje, 's');

        valor = str2double(entrada);


        if isnan(valor)

            disp( ...
                'ERROR: Debe ingresar un valor numerico.');


        elseif valor < 0 || valor > maximo

            fprintf( ...
                'ERROR: La nota debe estar entre 0 y %.2f.\n', ...
                maximo);


        else

            nota = valor;

            break;

        end

    end

endfunction


% ============================================================
% FUNCION PARA REDONDEO DE INGENIERIA
% ============================================================

function resultado = RedondeoIngenieria(valor)

    parte_entera = floor(valor);

    parte_decimal = valor - parte_entera;


    if parte_decimal >= 0.5

        resultado = parte_entera + 1;

    else

        resultado = parte_entera;

    end

endfunction


% ============================================================
% FUNCION PARA OBTENER DATOS DEL ARCHIVO
% ============================================================

function valor = ObtenerValor(texto, etiqueta)

    valor = '';

    posicion = strfind(texto, etiqueta);


    if isempty(posicion)

        return;

    end


    inicio = posicion(1) + length(etiqueta);

    resto = texto(inicio:end);

    salto = strfind(resto, char(10));


    if isempty(salto)

        valor = strtrim(resto);

    else

        valor = strtrim( ...
            resto(1:salto(1)-1));

    end

endfunction


% ============================================================
% FUNCION PARA MOSTRAR HISTORIAL
% ============================================================

function MostrarHistorialArchivo()

    fileID = fopen('notas.txt', 'r');


    if fileID == -1

        disp(' ');
        disp('No existe el archivo notas.txt.');
        disp('No hay registros disponibles.');

        return;

    end


    contenido = fread( ...
        fileID, ...
        '*char')';


    fclose(fileID);


    if isempty(strtrim(contenido))

        disp(' ');
        disp('No existen registros.');

        return;

    end


    bloques = strsplit( ...
        contenido, ...
        '========================================');


    disp(' ');
    disp('================ HISTORIAL =================');

    disp('======================================================================');


    fprintf( ...
        '%-15s %-25s %-10s %-8s %-8s %-8s %-10s %-8s %-12s\n', ...
        'Carnet', ...
        'Nombre', ...
        'Tareas', ...
        'P1', ...
        'P2', ...
        'P3', ...
        'Examen', ...
        'Final', ...
        'Estado');


    disp('======================================================================');


    for i = 1:length(bloques)

        bloque = strtrim(bloques{i});


        if isempty(bloque)

            continue;

        end


        if isempty(strfind(bloque, 'Carnet:'))

            continue;

        end


        carnet = ObtenerValor( ...
            bloque, 'Carnet:');

        nombre = ObtenerValor( ...
            bloque, 'Nombre:');

        tareas = ObtenerValor( ...
            bloque, 'Tareas:');

        parcial1 = ObtenerValor( ...
            bloque, 'Parcial 1:');

        parcial2 = ObtenerValor( ...
            bloque, 'Parcial 2:');

        parcial3 = ObtenerValor( ...
            bloque, 'Parcial 3:');

        examen = ObtenerValor( ...
            bloque, 'Examen Final:');

        nota_final = ObtenerValor( ...
            bloque, 'Nota final:');

        estado = ObtenerValor( ...
            bloque, 'Estado:');


        fprintf( ...
            '%-15s %-25s %-10s %-8s %-8s %-8s %-10s %-8s %-12s\n', ...
            carnet, ...
            nombre, ...
            tareas, ...
            parcial1, ...
            parcial2, ...
            parcial3, ...
            examen, ...
            nota_final, ...
            estado);

    end


    disp('======================================================================');

endfunction


% ============================================================
% FUNCION PARA GENERAR DASHBOARD
% ============================================================

function GenerarGraficasArchivo()

    fileID = fopen('notas.txt', 'r');


    if fileID == -1

        disp(' ');
        disp('No existe el archivo notas.txt.');

        return;

    end


    contenido = fread( ...
        fileID, ...
        '*char')';


    fclose(fileID);


    if isempty(strtrim(contenido))

        disp(' ');
        disp( ...
            'No existen registros para generar las graficas.');

        return;

    end


    bloques = strsplit( ...
        contenido, ...
        '========================================');


    nombres = {};

    notas = [];

    tareas = [];

    parcial1 = [];

    parcial2 = [];

    parcial3 = [];

    examenes = [];

    aprobados = 0;

    reprobados = 0;


    for i = 1:length(bloques)

        bloque = strtrim(bloques{i});


        if isempty(bloque)

            continue;

        end


        if isempty(strfind(bloque, 'Carnet:'))

            continue;

        end


        nombre = ObtenerValor( ...
            bloque, 'Nombre:');

        nota = ObtenerValor( ...
            bloque, 'Nota final:');

        estado = ObtenerValor( ...
            bloque, 'Estado:');

        tarea = ObtenerValor( ...
            bloque, 'Tareas:');

        p1 = ObtenerValor( ...
            bloque, 'Parcial 1:');

        p2 = ObtenerValor( ...
            bloque, 'Parcial 2:');

        p3 = ObtenerValor( ...
            bloque, 'Parcial 3:');

        examen = ObtenerValor( ...
            bloque, 'Examen Final:');


        nombres{end + 1} = nombre;

        notas(end + 1) = str2double(nota);

        tareas(end + 1) = str2double(tarea);

        parcial1(end + 1) = str2double(p1);

        parcial2(end + 1) = str2double(p2);

        parcial3(end + 1) = str2double(p3);

        examenes(end + 1) = str2double(examen);


        if strcmp(estado, 'Aprobado')

            aprobados = aprobados + 1;

        elseif strcmp(estado, 'Reprobado')

            reprobados = reprobados + 1;

        end

    end


    if isempty(notas)

        disp( ...
            'No existen datos suficientes para generar las graficas.');

        return;

    end


    disp(' ');
    disp( ...
        'Generando Dashboard de Analitica Academica...');


    % ========================================================
    % GRAFICA 1: RENDIMIENTO INDIVIDUAL
    % ========================================================

    figure;

    bar(notas);

    title('Rendimiento Individual');

    xlabel('Estudiante');

    ylabel('Nota Final');

    set(gca, ...
        'XTick', 1:length(nombres), ...
        'XTickLabel', nombres);

    grid on;


    % ========================================================
    % GRAFICA 2: INDICE DE APROBACION
    % ========================================================

    figure;

    pie([aprobados, reprobados]);

    title('Indice de Aprobacion');

    legend( ...
        'Aprobado', ...
        'Reprobado');


    % ========================================================
    % GRAFICA 3: DESEMPEÑO POR RUBRO
    % ========================================================

    promedio_tareas = mean(tareas);

    promedio_p1 = mean(parcial1);

    promedio_p2 = mean(parcial2);

    promedio_p3 = mean(parcial3);

    promedio_examen = mean(examenes);


    promedios = [ ...
        promedio_tareas, ...
        promedio_p1, ...
        promedio_p2, ...
        promedio_p3, ...
        promedio_examen];


    figure;

    bar(promedios);

    title( ...
        'Desempeño Promedio por Rubro');

    xlabel('Evaluacion');

    ylabel('Promedio');


    set(gca, ...
        'XTick', 1:5, ...
        'XTickLabel', { ...
        'Tareas', ...
        'Parcial 1', ...
        'Parcial 2', ...
        'Parcial 3', ...
        'Examen Final'});


    grid on;

endfunction
