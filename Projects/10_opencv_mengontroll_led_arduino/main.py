import serial
import time
import cv2
import mediapipe as mp
import math

global led_delay
led_delay = [0.5, 0.5, 0.5]

def send_command(ser, led_index, brightness):
    command = f"{led_index}_{brightness}\n"
    ser.write(command.encode())


def calculate_brightness(hand_landmarks, w, h):
    index_finger_tip = hand_landmarks.landmark[8]
    thumb_tip = hand_landmarks.landmark[4]
    
    x1, y1 = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
    x2, y2 = int(thumb_tip.x * w), int(thumb_tip.y * h)
    
    distance = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
    # print(int(distance), brightness)
    if distance <= 0:
        distance = 0
    if distance >= 255:
        distance = 0
    
    cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
    cv2.putText(frame, f"Brightness: {distance}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    return distance

if __name__ == "__main__":
    ser = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)
    
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils
    
    cap = cv2.VideoCapture(0)
    
    led_states = [0, 0, 0]
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue
        
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                x, y = int(hand_landmarks.landmark[8].x * w), int(hand_landmarks.landmark[8].y * h)
                cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)

                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                brightness = calculate_brightness(hand_landmarks, w, h)
                send_command(ser, 0, brightness)
        
        cv2.imshow("Hand Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    ser.close()
