from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
import mediapipe as mp
from keras.models import load_model

app = Flask(__name__)

# Load the pre-trained ASL recognition models
beginner_model = load_model('your_model.h5')
intermediate_model = load_model('wordrecognition_model.h5')

# Initialize MediaPipe hands solution
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Label map for intermediate model predictions
label_map = {0: 'aunt', 1: 'hi', 2: 'thankyou',3:'please',4:'eat',5:'father',6:'i_love_you',7:'look',8:'mother',9:'water'} 

# Route for the index (landing) page
@app.route('/')
def index():
    return render_template('load.html')

# Route for the beginner page@app.route('/beginner')
# Route for the beginner page
@app.route('/beginner')
def beginner():
    return render_template('beginner.html')


# Route for the intermediate page
@app.route('/intermediate')
def intermediate():
    return render_template('intermediate.html')

@app.route('/advanced')
def advanced():
    print("Advanced route accessed")
    return render_template('advanced.html')


@app.route('/test')
def test():
    return "This is a test route."

@app.route('/talk_to_expert')
def talk_to_expert():
    return render_template('video.html')
# Video streaming generator for the beginner page (your_model.h5)
@app.route('/video_feed_beginner')
def video_feed_beginner():
    return Response(gen_frames_beginner(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Video streaming generator for the intermediate page (asl_word_model.h5)
@app.route('/video_feed_intermediate')
def video_feed_intermediate():
    
    return Response(gen_frames_intermediate(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Function to capture webcam frames and predict ASL hand gestures for beginner model (your_model.h5)
def gen_frames_beginner():
    cap = cv2.VideoCapture(0)


    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(frame_rgb)
            
            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                    # Collect landmarks for prediction (input: (None, 63))
                    landmarks = []
                    for lm in hand_landmarks.landmark:
                        landmarks.append([lm.x, lm.y, lm.z])
                    landmarks = np.array(landmarks).flatten().reshape(1, -1)  # (None, 63)

                    # Make prediction using beginner model
                    prediction = beginner_model.predict(landmarks)
                    predicted_class = np.argmax(prediction)
                    predicted_letter = chr(predicted_class + 65) if predicted_class != 26 else 'TAB'

                    cv2.putText(frame, f"Predicted: {predicted_letter}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

# Function to capture webcam frames and predict ASL hand gestures for intermediate model (asl_word_model.h5)
def gen_frames_intermediate():
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            frame = cv2.flip(frame, 1)  # Flip the frame horizontally for a mirror view
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            result = hands.process(frame_rgb)  # Process hand landmarks

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Collect landmarks for prediction (input shape: (None, 63))
                    landmarks = []
                    for lm in hand_landmarks.landmark:
                        landmarks.append([lm.x, lm.y, lm.z])
                    landmarks = np.array(landmarks).flatten().reshape(1, -1)  # Reshape to (1, 63)

                    # Make prediction using the intermediate model
                    prediction = intermediate_model.predict(landmarks)  
                    predicted_word = label_map[np.argmax(prediction)]  # Map the predicted index to the corresponding word

                    # Display the predicted word on the video feed
                    cv2.putText(frame, f"Predicted: {predicted_word}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            # Encode the frame for web streaming
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()




if __name__ == '__main__':
    app.run(debug=True)
