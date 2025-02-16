import tkinter as tk
import serial
import math

ser = serial.Serial('COM13', 115200, timeout=1)  # Ganti 'COM5' dan 115200 dengan konfigurasi esp32

# Fungsi Proyeksi 3D ke 2D
def project_3d(x, y, z, scale=250, distance=4):
    factor = scale / (z + distance)
    x_2d = x * factor + 200
    y_2d = -y * factor + 200
    return x_2d, y_2d

# Fungsi Rotasi
def rotate_x(point, angle):
    x, y, z = point
    rad = math.radians(angle)
    cos_theta, sin_theta = math.cos(rad), math.sin(rad)
    y_new = y * cos_theta - z * sin_theta
    z_new = y * sin_theta + z * cos_theta
    return x, y_new, z_new

def rotate_y(point, angle):
    x, y, z = point
    rad = math.radians(angle)
    cos_theta, sin_theta = math.cos(rad), math.sin(rad)
    x_new = x * cos_theta + z * sin_theta
    z_new = -x * sin_theta + z * cos_theta
    return x_new, y, z_new

vertices = [
    (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
    (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

root = tk.Tk()
root.title("main")
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()

# Fungsi untuk Update Kubus
def update_cube():
    global vertices

    try:
        data = ser.readline().decode().strip()
        if data:
            angle_y, angle_x = map(int, data.split(','))
            canvas.delete("all")

            rotated_vertices = [rotate_x(rotate_y(v, -angle_y), angle_x) for v in vertices]
            projected_points = [project_3d(*v) for v in rotated_vertices]

            for edge in edges:
                p1, p2 = edge
                x1, y1 = projected_points[p1]
                x2, y2 = projected_points[p2]
                canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
            
    except Exception as e:
        print("Error:", e)

    root.after(10, update_cube)

update_cube()
root.mainloop()
