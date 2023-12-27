# SEWeb
**Software Engineering Website project** was created to encourage education and teamwork in the software engineering industry. Meeting rooms, room availability management, user authentication, homework submission, and user customization are just a few of the features that this platform will provide to meet the needs of both teachers and students. This web application uses a web socket to communicate throughout the meeting. Fast API server on python to fetch user authentication data. Uses ZODB database to store website data and user information.

## SEE ON WEBSITE
[Software Engineering ALL-IN-ONE Website](https://seweb.kasitphoom.com/)
### How to use
1. Click on user avatar
2. Click on login
    - For teacher: Username - 9001 ; Password - 1234
    - For student: Username - 1100, 1101, 1102 ; Password - 1234
3. Browse through features as you want
> :warning: **ANY CHANGES OR UPLOADS WILL PERMANENTLY AFFECTED AND UPLOADED**: Be very careful here! _**Do not upload any vulnerable informations**_

## HOW TO RUN LOCALLY
### Install dependencies
1. You must have **Python** installed
2. You must have **uvicorn** dependency installed
  - Install uvicorn by run `pip install uvicorn` in your terminal
3. You must have **zodb** dependency installed
  - Install ZODB by run `pip install zodb` in your terminal
4. You must have **FastAPI** dependency installed
  - Install ZODB by run `pip install fastapi` in your terminal
5. Clone this repository
``` cmd
git clone https://www.github.com/Kasitphoom/SEWeb.git
```
### Run FastAPI server
1. go to `FastAPI` directory
``` cmd
cd FastAPI
```
3. Run command `uvicorn main:app --reload`
4. Enter `http://localhost:8000` in to your browser

## Collaborator
- **Kasitphoom Thowongs**
- **Phupa Denphatcharangkul**
- **Pitiphong Kitrueangphatchara**

## Features
**Meeting Rooms**
- Create and manage virtual meeting rooms.
- Real-time video conferencing.
- Owner can customize room name, description.
- personal real-time canvas.

**Room Availability**
- Check room availability in real-time.
- Join their preferred room in real-time.

**Basic Online meeting controls**
- Microphone + Camera + Hand raise

**Audio Video Devices selection**
- Allow users to manage their input and output devices. User Authentication
- Secure login for students and teachers.
- User profiles with role-based access.

**Homework Submissions**
- Upload and submit homework assignments + File management for students and teachers.
- Grading mechanisms.

**User Customization**
- Customize user profiles with personal information.

**Security and Privacy**
- End-to-end encryption for private meetings.
- Reporting and moderation features for maintaining a safe environment.
