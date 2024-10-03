import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, find_peaks
from collections import deque
import time

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut=0.7, highcut=2.5, fs=30, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

buffer_size = 300
r_values = deque(maxlen=buffer_size)
g_values = deque(maxlen=buffer_size)
b_values = deque(maxlen=buffer_size)
times = deque(maxlen=buffer_size)
SpO2_values = deque(maxlen=buffer_size)
BPM_values = deque(maxlen=buffer_size)

start_time = time.time()

plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1)
line1, = ax1.plot([], [], label="BPM", color='r')
line2, = ax2.plot([], [], label="SpO2", color='b')
ax1.set_ylim(0, 220)
ax2.set_ylim(0, 100)
ax1.set_title('Heart Rate (BPM)')
ax2.set_title('SpO2 Levels')

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        face_region = frame[y:y+h, x:x+w]

        avg_color_per_row = np.mean(face_region, axis=0)
        avg_color = np.mean(avg_color_per_row, axis=0)
        b_value = avg_color[0]
        g_value = avg_color[1]
        r_value = avg_color[2]
        r_values.append(r_value)
        g_values.append(g_value)
        b_values.append(b_value)
        times.append(time.time() - start_time)

        if len(r_values) == buffer_size:
            r_array = np.array(r_values)
            g_array = np.array(g_values)
            b_array = np.array(b_values)
            t_array = np.array(times)
            r_detrended = r_array - np.mean(r_array)
            g_detrended = g_array - np.mean(g_array)
            fs = buffer_size / (t_array[-1] - t_array[0])
            filtered_r = bandpass_filter(r_detrended, fs=fs)
            filtered_g = bandpass_filter(g_detrended, fs=fs)
            red_ac = np.std(filtered_r)
            red_dc = np.mean(r_array)
            green_ac = np.std(filtered_g)
            green_dc = np.mean(g_array)

            if green_ac != 0 and green_dc != 0:
                R = (red_ac / red_dc) / (green_ac / green_dc)
                SpO2 = 100 - 5 * R
                SpO2 = np.clip(SpO2, 0, 100)
                print(f"Estimated SpO2: {SpO2:.2f}%")
                SpO2_values.append(SpO2)
            else:
                SpO2 = None
                print("Calculating...")

            peaks, _ = find_peaks(filtered_g, distance=int(fs * 0.5))
            num_beats = len(peaks)

            if num_beats > 1:
                peak_times = t_array[peaks]
                rr_intervals = np.diff(peak_times)
                avg_rr_interval = np.mean(rr_intervals)
                bpm = 60 / avg_rr_interval
                bpm = np.clip(bpm, 0, 220)
                print(f"Estimated BPM: {bpm:.2f}")
                BPM_values.append(bpm)
            else:
                bpm = None
                print("Calculating BPM...")

            if SpO2 is not None:
                cv2.putText(frame, f"SpO2: {SpO2:.2f}%", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            if bpm is not None:
                cv2.putText(frame, f"BPM: {bpm:.2f}", (x, y - 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            if len(BPM_values) > 1 and len(SpO2_values) > 1:
                line1.set_xdata(np.arange(len(BPM_values)))
                line1.set_ydata(BPM_values)
                ax1.relim()
                ax1.autoscale_view()

                line2.set_xdata(np.arange(len(SpO2_values)))
                line2.set_ydata(SpO2_values)
                ax2.relim()
                ax2.autoscale_view()

                plt.draw()
                plt.pause(0.001)

        spectrum = np.zeros_like(face_region)
        spectrum[:, :, 0] = np.full_like(face_region[:, :, 0], b_value)
        spectrum[:, :, 1] = np.full_like(face_region[:, :, 1], g_value)
        spectrum[:, :, 2] = np.full_like(face_region[:, :, 2], r_value)
        cv2.imshow('Full-Face Light Spectrum', spectrum)

    else:
        cv2.putText(frame, "No face detected", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Webcam Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
plt.ioff()
