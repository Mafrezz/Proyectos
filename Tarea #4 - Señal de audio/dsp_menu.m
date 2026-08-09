function dsp_menu()
  % ===== Detección de Octave/MATLAB y carga de paquete signal =====
  if exist('OCTAVE_VERSION', 'builtin') ~= 0
    % Estamos en Octave
    try
      pkg load signal;   % Necesario para pwelch / ventanas
    catch
      warning(['No se pudo cargar el paquete "signal". ', ...
               'Instálalo con: pkg install -forge signal']);
    end
  end

  % ===== Parámetros generales =====
  fs = 44100;                  % Frecuencia de muestreo
  nbits = 16;                  % Resolución
  nchan = 1;                   % Mono
  audio_file = 'audio.wav';

  % ===== Menú =====
  opcion = 0;
  while opcion ~= 5
    fprintf('\nSeleccione una opción:\n');
    fprintf('1. Grabar\n');
    fprintf('2. Reproducir\n');
    fprintf('3. Graficar (tiempo)\n');
    fprintf('4. Graficar densidad (Welch)\n');
    fprintf('5. Salir\n');

    opcion = input('Ingrese su elección: ');
    switch opcion
      case 1
        % ===== Grabación =====
        try
          duracion = input('Duración de la grabación en segundos (ej. 10): ');
          if isempty(duracion) || ~isscalar(duracion) || duracion <= 0
            error('Duración no válida.');
          end

          % Si tienes múltiples dispositivos y falla la grabación, usa:
          % devID = audiodevinfo(1); % (en Octave recientes) o consulta audiodevinfo
          % recObj = audiorecorder(fs, nbits, nchan, devID);
          recObj = audiorecorder(fs, nbits, nchan);

          disp('Comenzando la grabación... ¡Habla ahora!');
          recordblocking(recObj, duracion);
          disp('Grabación finalizada.');

          data = getaudiodata(recObj);
          audiowrite(audio_file, data, fs);
          fprintf('Archivo guardado: %s\n', audio_file);
        catch err
          fprintf(2, 'Error al grabar el audio: %s\n', err.message);
          sugerencias_dispositivo();
        end

      case 2
        % ===== Reproducción =====
        try
          [data, fs2] = audioread(audio_file);
          sound(data, fs2);
        catch err
          fprintf(2, 'Error al reproducir el audio: %s\n', err.message);
          fprintf('¿Existe el archivo %s? Graba primero con la opción 1.\n', audio_file);
        end

      case 3
        % ===== Gráfica en el tiempo =====
        try
          [data, fs2] = audioread(audio_file);
          t = (0:length(data)-1) / fs2;
          figure; plot(t, data);
          xlabel('Tiempo (s)'); ylabel('Amplitud'); grid on;
          title('Señal de audio en el tiempo');
        catch err
          fprintf(2, 'Error al graficar (tiempo): %s\n', err.message);
        end

      case 4
        try
    disp('Graficando espectro de frecuencia');
    [audio, Fs] = audioread('audio.wav');
    N = length(audio);

    % Ventana de Hann
    ventana = hann(N);

    % Solapamiento como porcentaje (50%)
    overlap = 0.5;

    % FFT con N puntos
    [Sxx, f] = pwelch(audio, ventana, overlap, N, Fs);

    plot(f, 10*log10(Sxx));
    xlabel('Frecuencia (Hz)');
    ylabel('Densidad espectral de potencia (dB/Hz)');
    title('Espectro de frecuencia de la señal grabada');
catch err
    fprintf(2, 'Error al graficar densidad: %s\n', err.message);
end

      case 5
        disp('Saliendo del programa...');

      otherwise
        disp('Opción no válida. Intenta de nuevo.');
    end
  end
end
