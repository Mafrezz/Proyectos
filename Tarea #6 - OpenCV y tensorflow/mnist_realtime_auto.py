"""
mnist_realtime_auto.py
Reconocimiento MNIST en tiempo real, detecta si el modelo es MLP (784) o CNN (28,28,1)
Uso:
  python mnist_realtime_auto.py --model mnist_cnn.keras
"""

import cv2
import numpy as np
import tensorflow as tf
import argparse
import time
import traceback

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--model", "-m", default="mnist_cnn.keras", help="Ruta al modelo .keras/.h5")
    p.add_argument("--min_area", type=int, default=2000, help="Área mínima de contorno para considerar (reduce ruido)")
    p.add_argument("--show_debug", action="store_true", help="Muestra ventanas extra para debugging")
    return p.parse_args()

def detect_model_type(model):
    # model.input_shape devuelve tupla tipo (None, 28, 28, 1) o (None, 784)
    shape = model.input_shape
    # Convertir a lista si es TensorShape
    try:
        if hasattr(shape, "as_list"):
            shape = shape.as_list()
    except Exception:
        pass
    # Normalizar a tuplas
    if isinstance(shape, (list, tuple)):
        # Ej: [None, 28,28,1]  o (None, 784)
        dims = [d for d in shape if d is not None]
        if len(dims) == 1 and dims[0] == 784:
            return "mlp", shape
        if len(dims) == 3 and (dims[0] == 28 and dims[1] == 28):
            # puede ser (28,28,1) ó (28,28)
            if len(dims) == 3 and dims[2] == 1:
                return "cnn", shape
            return "cnn", shape
    # Fallback: si el modelo acepta vectores 2D -> mlp
    if len(shape) == 2:
        return "mlp", shape
    # Si no lo sabemos, intentamos inferir por número total
    raise ValueError(f"Imposible inferir tipo de entrada desde model.input_shape={shape}")

def preprocess_roi_for_model(roi_binary, model_type):
    """
    roi_binary: imagen binaria (digit foreground ~255, background ~0) o gris.
    Devuelve: input listo para model.predict, y preview_uint8_28x28
    """
    # Asegurarnos de que es gris 2D
    if roi_binary.ndim == 3:
        roi_gray = cv2.cvtColor(roi_binary, cv2.COLOR_BGR2GRAY)
    else:
        roi_gray = roi_binary

    # Redimensionar a 28x28 con interpolación adecuada
    roi28 = cv2.resize(roi_gray, (28,28), interpolation=cv2.INTER_AREA)

    # Normalizar: queremos que el dígito tenga valores 1.0 y fondo 0.0
    # Si fondo es claro y dígito oscuro, invertimos
    if np.mean(roi28) > 127:
        roi28 = 255 - roi28

    x = roi28.astype("float32") / 255.0

    if model_type == "mlp":
        inp = x.reshape(1, 28*28).astype("float32")
    else:  # cnn
        inp = x.reshape(1, 28, 28, 1).astype("float32")

    return inp, roi28.astype("uint8")

def safe_find_contours(binary_img):
    res = cv2.findContours(binary_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # compatibilidad OpenCV 3/4: res puede ser (contours, hierarchy) o (image, contours, hierarchy)
    if len(res) == 2:
        contours = res[0]
    else:
        contours = res[1]
    return contours

def main():
    args = parse_args()

    try:
        print("Cargando modelo:", args.model)
        model = tf.keras.models.load_model(args.model)
    except Exception as e:
        print("ERROR cargando el modelo:", e)
        traceback.print_exc()
        return

    # Detectamos qué tipo de entrada espera el modelo
    try:
        model_type, shape = detect_model_type(model)
    except Exception as e:
        print("No pude inferir el tipo de entrada del modelo:", e)
        print("model.input_shape:", model.input_shape)
        return

    print(f"Modelo cargado. Tipo detectado: {model_type}. input_shape: {model.input_shape}")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No pude abrir la cámara. Revisa que esté conectada.")
        return

    last_time = time.time()
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Frame no recibido, saliendo...")
                break

            # ---- Preprocesado básico ----
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5,5), 0)
            # Umbral automático con Otsu + invertimos para tener dígito blanco(255) sobre negro(0)
            _, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            # Encontrar contornos
            contours = safe_find_contours(th)
            # Ordenar por área (más grandes primero)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)

            # Procesar contornos relevantes
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area < args.min_area:
                    continue

                x, y, w, h = cv2.boundingRect(cnt)
                # Hacemos padding para captar todo el trazo
                pad = int(max(w, h) * 0.25)
                x0 = max(0, x - pad); y0 = max(0, y - pad)
                x1 = min(frame.shape[1], x + w + pad); y1 = min(frame.shape[0], y + h + pad)

                roi = th[y0:y1, x0:x1]  # imagen binaria ya
                try:
                    inp, preview28 = preprocess_roi_for_model(roi, model_type)
                    preds = model.predict(inp, verbose=0)
                    pred_class = int(np.argmax(preds, axis=1)[0])
                    conf = float(np.max(preds))

                    # Dibujar en frame
                    cv2.rectangle(frame, (x0,y0), (x1,y1), (0,255,0), 2)
                    cv2.putText(frame, f"{pred_class} {conf*100:.1f}%", (x0, max(10, y0-10)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 2)

                    # Mostrar preview 28x28 (ampliado)
                    preview_big = cv2.resize(preview28, (140,140), interpolation=cv2.INTER_NEAREST)
                    # colocar preview en la esquina superior derecha
                    hpb, wpb = preview_big.shape
                    frame[0:hpb, frame.shape[1]-wpb:frame.shape[1]] = cv2.cvtColor(preview_big, cv2.COLOR_GRAY2BGR)

                except Exception as e:
                    # Si hay error en predict, no cerramos la app, solo lo reportamos
                    print("Error durante predict/preprocess:", e)
                    traceback.print_exc()

            # FPS (opcional)
            now = time.time()
            fps = 1.0 / (now - last_time) if now != last_time else 0.0
            last_time = now
            cv2.putText(frame, f"FPS: {fps:.1f}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

            # Mostrar ventanas
            cv2.imshow("MNIST Live", frame)
            if args.show_debug:
                cv2.imshow("Threshold (binary)", th)

            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord('q'):  # ESC o q para salir
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
