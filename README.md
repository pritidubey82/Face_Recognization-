# Face Recognition Attendance System

This project implements a face recognition-based attendance system that captures and logs attendance using a webcam. It also sends SMS notifications to designated contacts via Twilio when a recognized individual is detected.

## Key Components

### Libraries Used:
- **OpenCV**: For video capture and image processing.
- **face_recognition**: For recognizing faces in images.
- **numpy**: For numerical operations.
- **pandas**: For managing attendance data.
- **datetime**: For handling date and time operations.
- **twilio**: For sending SMS notifications.
- **openpyxl**: For working with Excel files.

### Twilio Configuration:
The code initializes the Twilio client with account SID and authentication token to enable SMS notifications. You'll need your own Twilio credentials for this.

### Known Faces:
The program loads images of known individuals from specified file paths and encodes their faces for recognition. This is done in the `load_known_faces` function, which populates two lists: `known_face_encodings` and `known_face_names`.

### Attendance Management:
Attendance is logged into a Pandas DataFrame, which includes columns for Name, Date, and Time. The function `mark_attendance` checks if the individual is already marked present for the day; if not, it records the attendance and sends an SMS notification.

### Saving Attendance:
The attendance data is saved to an Excel file using the `save_attendance_sheet` function. The attendance sheet is updated automatically at regular intervals or when a new entry is made.

### Video Capture and Recognition:
The main loop captures video frames from the webcam, detects faces, and compares them to the known faces. If a match is found, it marks the attendance for the individual and displays their name on the video feed.

### User Interface:
The recognized individuals are highlighted with rectangles in the video feed, and their names are displayed above their faces. Pressing 'q' will exit the video capture.

### Attendance Check:
The function `check_attendance_sheet` can be used to print the attendance records from the saved Excel sheet.

## Requirements
To run this project, ensure you have the following installed:
- Python 3.x
- Required libraries (install via pip):

```bash
pip install opencv-python face_recognition numpy pandas twilio openpyxl

![image](https://github.com/user-attachments/assets/30990d81-8720-4830-a9f0-4cf727c1379d)

