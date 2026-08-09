import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import welch

FS = 44100
NBITS = 16
CHAN = 1
AUDIO_FILE = 'audio.wav'

def grabar():
    try:
        dur = float(input('Duración de la grabación en segundos (e.g., 10): '))
        if dur <= 0:
            print('Duración no válida.')
            return
        print('Comenzando la grabación... ¡Habla ahora!')
        rec = sd.rec(int(dur * FS), samplerate=FS, channels=CHAN, dtype='float32')
        sd.wait()
        sf.write(AUDIO_FILE, rec, FS)
        print(f'Archivo guardado: {AUDIO_FILE}')
    except Exception as e:
        print('Error al grabar:', e)


def reproducir():
    try:
        data, fs = sf.read(AUDIO_FILE, always_2d=False)
        sd.play(data, fs)
        sd.wait()
    except Exception as e:
        print('Error al reproducir:', e)


def graficar_tiempo():
    try:
        data, fs = sf.read(AUDIO_FILE)
        if data.ndim > 1:
            data = data[:, 0]
        t = np.arange(len(data)) / fs
        plt.figure()
        plt.plot(t, data)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Amplitud')
        plt.title('Señal de audio en el tiempo')
        plt.grid(True)
        plt.show()
    except Exception as e:
        print('Error al graficar (tiempo):', e)


def graficar_densidad():
    try:
        x, fs = sf.read(AUDIO_FILE)
        if x.ndim > 1:
            x = x[:, 0]
        nperseg = max(128, int(0.05 * fs))  # ventana ~50 ms
        f, Pxx = welch(x, fs=fs, nperseg=nperseg)
        import numpy as np
        plt.figure()
        plt.plot(f, 10 * np.log10(Pxx))
        plt.xlim([0, fs / 2])
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Densidad espectral de potencia (dB/Hz)')
        plt.title('Espectro (método de Welch)')
        plt.grid(True)
        plt.show()
    except Exception as e:
        print('Error al graficar densidad:', e)


def menu():
    while True:
        print('\nSeleccione una opción:')
        print('1. Grabar')
        print('2. Reproducir')
        print('3. Graficar')
        print('4. Graficar densidad')
        print('5. Salir')
        try:
            op = int(input('Ingrese su elección: '))
        except Exception:
            print('Opción no válida.')
            continue

        if op == 1:
            grabar()
        elif op == 2:
            reproducir()
        elif op == 3:
            graficar_tiempo()
        elif op == 4:
            graficar_densidad()
        elif op == 5:
            print('Saliendo...')
            break
        else:
            print('Opción no válida.')


if __name__ == '__main__':
    menu()
    