import cv2
from pyzbar.pyzbar import decode
from openpyxl import Workbook
from datetime import datetime

def detect_barcodes(frame):
    barcodes = decode(frame)
    results = []
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type
        results.append((barcode_data, barcode_type))
    return results

def log_to_excel(data):
    filename = "barcode_log.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Scanned Barcodes"
    ws.append(["Barcode", "Type", "Timestamp"])

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for barcode_data, barcode_type in data:
        ws.append([barcode_data, barcode_type, timestamp])
    wb.save(filename)

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        barcodes = detect_barcodes(frame)
        if barcodes:
            log_to_excel(barcodes)

        cv2.imshow("Camera Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()