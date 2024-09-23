import cv2
import face_recognition
import numpy as np
import pandas as pd
from datetime import datetime
from twilio.rest import Client
import openpyxl


account_sid = 'AC9a825271b0dce6ae8e8ebfaae417aa3b'  
auth_token = '6e76b39b8b23410cb3f50ad13bd9c501'      
twilio_phone_number = '+15864801607'  
admin_phone_number = '+919284092073'  

client = Client(account_sid, auth_token)


known_face_encodings = []
known_face_names = []


phone_numbers = {
    "Priti": "+919284092073",  
    "Salman": "+918261063570",  
    "SK": "+91750263459", 
    "Rashmi": "+918624879351",  
    "Papa": "+919373189665"
      
}


def load_known_faces():
    known_person1_image = face_recognition.load_image_file(r"C:\Users\Priti\Desktop\Python\priti.jpeg")
    known_person1_encoding = face_recognition.face_encodings(known_person1_image)
    if known_person1_encoding:
        known_face_encodings.append(known_person1_encoding[0])
        known_face_names.append("Priti")

    known_person2_image = face_recognition.load_image_file(r"C:\Users\Priti\Desktop\Python\salman.jpeg")
    known_person2_encoding = face_recognition.face_encodings(known_person2_image)
    if known_person2_encoding:
        known_face_encodings.append(known_person2_encoding[0])
        known_face_names.append("Salman")

    known_person3_image = face_recognition.load_image_file(r"C:\Users\Priti\Desktop\Python\sk.jpeg")
    known_person3_encoding = face_recognition.face_encodings(known_person3_image)
    if known_person3_encoding:
        known_face_encodings.append(known_person3_encoding[0])
        known_face_names.append("SK")

    known_person4_image = face_recognition.load_image_file(r"C:\Users\Priti\Desktop\Python\rashmi.jpg")
    known_person4_encoding = face_recognition.face_encodings(known_person4_image)
    if known_person4_encoding:
        known_face_encodings.append(known_person4_encoding[0])
        known_face_names.append("Rashmi")

    known_person5_image = face_recognition.load_image_file(r"C:\Users\Priti\Desktop\Python\Papa4.jpg")
    known_person5_encoding = face_recognition.face_encodings(known_person5_image)
    if known_person5_encoding:
        known_face_encodings.append(known_person5_encoding[0])
        known_face_names.append("Papa")

   

load_known_faces()


attendance_df = pd.DataFrame(columns=["Name", "Date", "Time"])

def mark_attendance(name, current_time):
    
    current_date = current_time.date()
    current_time_str = current_time.strftime("%H:%M:%S")

    print(f"Trying to mark attendance for: {name}")

    if not ((attendance_df['Name'] == name) & (attendance_df['Date'] == current_date)).any():
        attendance_df.loc[len(attendance_df.index)] = [name, current_date, current_time_str]
        print(f"Attendance marked for {name} at {current_time_str}")
        send_sms_notification(name)
        
        
        save_attendance_sheet()
    else:
        print(f"{name} has already been marked present today.")

def save_attendance_sheet():
   
    try:
        attendance_df.to_excel(r"C:\Users\Priti\Desktop\Python\attendance.xlsx", index=False)
        print("Attendance sheet saved successfully.")
    except Exception as e:
        print(f"Error saving attendance sheet: {str(e)}")

def send_sms_notification(name):
    
    message = f"{name} has been recognized by the face recognition system."
    recipient_number = phone_numbers.get(name, admin_phone_number)  

    try:
        client.messages.create(
            body=message,
            from_=twilio_phone_number, 
            to=recipient_number
        )
        print(f"SMS notification sent to {name}: {message}")
    except Exception as e:
        print(f"Failed to send SMS: {str(e)}")


video_capture = cv2.VideoCapture(0)
last_save_time = datetime.now()

while True:
    ret, frame = video_capture.read()
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    if not face_encodings:
        print("No face encodings found in the current frame.")
        continue

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

            current_time = datetime.now()
            mark_attendance(name, current_time)

            
            if (current_time - last_save_time).total_seconds() > 600:
                save_attendance_sheet()
                last_save_time = current_time

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

def check_attendance_sheet():
    
    wb = openpyxl.load_workbook(r"C:\Users\Priti\Desktop\Python\attendance.xlsx")
    sheet = wb.active
    for row in sheet.iter_rows(values_only=True):
        print(row)
