import cv2
import sys
import qrcode
import zxing
from PIL import Image
import requests

def scan_qr_code():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        decoder = zxing.QrCodeDecoder()
        result = decoder.decode(frame)

        if result:
            qr_code_data = result.data.decode('utf-8')
            print("QR Code Data:", qr_code_data)
            cap.release()
            cv2.destroyAllWindows()
            save_qr_code_image(qr_code_data)
            break

        cv2.imshow('QR Code Scanner', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def save_qr_code_image(qr_code_data):
    url = input("Enter the URL to save the QR code image: ")

    # Generate a QR code image
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_code_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qr_code.png")

    # Send the image to the PHP server
    files = {'file': open('qr_code.png', 'rb')}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        print("QR code image saved successfully.")
    else:
        print("Failed to save QR code image. Server responded with status code:", response.status_code)

def main():
    scan_qr_code()

if __name__ == "__main__":
    main()
