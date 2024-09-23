import pygps
import cv2
import socket
import platform
import subprocess

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

def get_device_info():
    device_info = {
        'IP Address': get_ip_address(),
        'Platform': platform.platform(),
        'Machine Type': platform.machine(),
        'Processor': platform.processor(),
        'Python Version': platform.python_version(),
    }
    return device_info

def get_camera_info():
    camera_info = subprocess.check_output(['v4l2-ctl', '--list-devices']).decode('utf-8')
    return camera_info

def capture_gps_and_camera():
    # Initialize the GPS module
    gps = pygps.GPS()

    # Capture GPS location
    latitude, longitude = gps.position()

    # Capture camera access
    camera = cv2.VideoCapture(0)

    # Check if the camera is opened correctly
    if not camera.isOpened():
        raise IOError("Cannot open webcam")

    # Read a frame from the camera
    ret, frame = camera.read()

    # Save the captured frame
    cv2.imwrite('captured_image.jpg', frame)

    # Release the camera
    camera.release()

    # Store the captured information
    data = f"Latitude: {latitude}\nLongitude: {longitude}\n"
    with open('user_info.txt', 'a') as file:
        file.write(data)

    return latitude, longitude

# Example usage
latitude, longitude = capture_gps_and_camera()
device_info = get_device_info()
camera_info = get_camera_info()

# Store the captured information
data = "Device Information:\n"
for key, value in device_info.items():
    data += f"{key}: {value}\n"

data += "\nCamera Information:\n"
data += camera_info

with open('user_info.txt', 'a') as file:
    file.write(data)
