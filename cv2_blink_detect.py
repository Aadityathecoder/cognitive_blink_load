import cv2
import time

cap = cv2.VideoCapture(0)
st = str(time.time())
font = cv2.FONT_HERSHEY_SIMPLEX
blink_time_frame = []
place_holder_time = 0
cooldown = 0.5


if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

if face_cascade.empty():
    print("Error: Could not load face cascade.")
    exit()

if eye_cascade.empty():
    print("Error: Could not load eye cascade.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret or frame is None:
        print("Error: Could not read frame from camera.")
        break

    elapsed_time = f"{time.time() - float(st):.2f}" #:02d is only taken usually in f-strings, also make sure to learn whats going on in this line
    usage_elapsed_time = float(elapsed_time)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.3, minNeighbors=5)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
            cv2.putText(frame, elapsed_time, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

            if len(eyes) >= 2:
                cv2.putText(frame, "Two eyes detected", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            elif len(eyes) == 1:
                 cv2.putText(frame, "One eye detected", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                 if usage_elapsed_time > cooldown + place_holder_time:
                     blink_time_frame.append(usage_elapsed_time)
                     place_holder_time = usage_elapsed_time
            elif len(eyes) == 0:
                cv2.putText(frame, "No eyes detected", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                 # FOR THIS LINE OF CODE, MAKE YOUR EYES DETECTING ALGORITHM BETTER TO WORK
                # next checkpoint --> derive blink rate on some amount of data

    #------------------
        if len(eyes) == 0 and len(faces) == 0:
            continue
    cv2.imshow("Local Camera", frame)
    blinked = len(blink_time_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"): #q --> quit
        print(blink_time_frame)
        print(f"Blink list length: {blinked}")
        print(f"Elapsed time: {usage_elapsed_time}")
        print(f"Blink rate: {(60/usage_elapsed_time)*blinked} b/pm")
        break

cap.release()
cv2.destroyAllWindows()
