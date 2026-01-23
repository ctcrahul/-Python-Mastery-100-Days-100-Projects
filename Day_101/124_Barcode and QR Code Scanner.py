#pip install opencv-python
#pip install pyzbar

import cv2
from pyzbar import pyzbar

def scan_codes(frame):
    decoded_objects = pyzbar.decode(frame)

    for obj in decoded_objects:
        points = obj.polygon
        if len(points) > 4:
            hull = cv2.convexHull(
                np.array([point for point in points], dtype=np.float32)
            )
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points

        n = len(hull)
        for j in range(n):
            cv2.line(frame, hull[j], hull[(j + 1) % n], (0, 255, 0), 2)

        x, y, w, h = obj.rect
        text = f"{obj.type}: {obj.data.decode('utf-8')}"
        cv2.putText(
            frame,
            text,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        print(text)

    return frame


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot access camera")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = scan_codes(frame)
        cv2.imshow("Barcode and QR Code Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

