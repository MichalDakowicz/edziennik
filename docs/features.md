# List of Features of a School Electronic Gradebook

## Core Functions

### 1. Teaching and Grading Module

This is the heart of the system, replacing the traditional paper class register.

- **Grade Register:**  
  - **Partial grades:** Entering marks with weights, categories (test, oral answer, participation), and descriptions.  
  - **Predicted and mid-year/final grades:** These mechanisms allow teachers to assign end-of-year grades and track deadlines for entering them.  
  - **Weighted and arithmetic average:** Automatic calculation of averages (often with a simulation like “what do I need to get to have a B?”).  
- **Attendance:**  
  - Marking presence, lateness, excused/unexcused absences, and exemptions.  
  - **Online excuses:** A parent can submit an electronic excuse note, which the teacher approves with one click.  
  - Attendance counters (percentage) for each student and class.  
- **Behavior:** Register of negative notes and positive commendations/achievements, point-based behavior grading systems.

### 2. School Work Organization (Planning)

Tools used for everyday school logistics.

- **Timetable and substitutions:**  
  - Interactive timetable that takes into account group divisions (e.g. language groups, PE).  
  - **Substitution module:** When a teacher is absent, the system informs about cancelled lessons, substitutions, or free periods. This is one of the most important features for students (“do we have math tomorrow?”).  
- **Test calendar:** Teachers enter dates of quizzes and written exams. The system often blocks adding, for example, a 4th major test in one week (according to the school’s regulations).  
- **Homework:** Entering homework descriptions, due dates, and attaching files (PDFs, photos of the board).

### 3. Communication and Information

Gradebooks also act as the school’s official communication tool.

- **Internal mail:** A messaging system working like email but in a closed environment (Teacher ↔ Parent ↔ Student), with read receipts to ensure the message reached the right person.  
- **Announcements:** Notice board for the whole school or selected classes (trips, meetings, days off).  
- **Meeting scheduler:** Scheduling parent-teacher meetings and individual consultations.

### 4. Student and Parent Functions (“Client Zone”)

Often available as a mobile application.

- **“Lucky Number”:** A popular feature that draws a random roll number each day; the student with that number is exempt from being called on.  
- **Push notifications (often paid):** Instant alerts on the phone about new grades, behavior notes, or messages (in Librus this is part of the paid “Mobile Add-ons” package).  
- **Access to materials:** Downloading files shared by the teacher.  
- **Integration with videoconferencing:** Quick links to lessons on Teams/Zoom (a legacy of remote learning).

### 5. Administration and Management (For Principal and Office)

This is the **back office** invisible to students but crucial for the school.

- **Document generation:**  
  - **Printing certificates:** Automatic pulling of grades onto official certificate forms.  
  - Grade sheets.  
  - Student IDs (including support for **mobile student IDs – mLegitymacja** and electronic IDs). [en.uw.edu](https://en.uw.edu.pl/mobile-version-of-student-card-at-uw/)
- **Export to SIO:** Integration with the Education Information System (System Informacji Oświatowej – the national school information database). [pl.wikipedia](https://pl.wikipedia.org/wiki/System_informacji_o%C5%9Bwiatowej)
- **Statistics and analytics:**  
  - Comparing class averages.  
  - Attendance analysis for the whole school.  
  - Reports on individual instruction.  
- **Student registers and records:** Electronic maintenance of the school’s main student registers.

## Administrative, Management, and Specialist Functions

### 1. Secretariat and Student Records Module

This is the central school database.

- **Electronic registers:**  
  - **Student Register:** Full student file (national ID number, addresses, parents’ data, education history, GDPR consents).  
  - **Residency Register:** Records of children living in the school’s catchment area (monitoring compulsory schooling).  
- **Generation of official documents (strictly according to Ministry of Education templates):**  
  - Printing certificates (on official forms) with automatic filling (prevents spelling errors in names).  
  - Printing grade sheets (annual and multi-year).  
  - Certificates confirming student status (e.g. for social security office or social welfare center).  
  - **Electronic and mobile student IDs (e-Legitymacja and mLegitymacja):** Generating XML files/QR codes for the mObywatel app and handling printers for plastic student cards (ID-1). [gov](https://www.gov.pl/web/family/mlegitymacja-for-old-age-and-disability-pensioners)
- **Integration with SIO (Education Information System):**  
  - Exporting data about students, staff, and admissions directly to the national SIO system (crucial for calculating education subsidies). [cie.gov](https://cie.gov.pl/sio/)
  - Validating data before sending.  
- **Archiving:** Moving graduates to the archive while keeping access to their historical grades and achievements.

### 2. Principal’s Panel and Pedagogical Supervision

Tools for staff management and monitoring teaching quality.

- **Monitoring curriculum implementation:**  
  - Reports on alignment of lesson topics with the core curriculum (teacher has to tick off completed items).  
  - Alerts about delays in covering material.  
- **Register control:**  
  - The principal sees which teacher fails to enter lesson topics, mark attendance, or grade regularly.  
  - Change history (who changed which grade and when – the edit history cannot be deleted).  
- **Lesson observations:**  
  - Electronic observation forms for evaluating a teacher’s work.  
- **Management reports (BI – Business Intelligence):**  
  - Comparability of grades between classes and teachers (identifying “strict” and “lenient” teachers).  
  - Analysis of EWD (Educational Value Added) based on mock exam results. [ibe.edu](https://ibe.edu.pl/pl/edukacyjna-wartosc-dodana)

### 3. Logistics: Planning and Substitutions

One of the most algorithmically complex modules.

- **Substitution module:**  
  - Automatically suggests a teacher for substitution (e.g. one who has a free period, teaches the same subject, or is assigned to daycare).  
  - Generates printouts of the “substitution book” for signing.  
  - Settles extra paid hours and occasional unpaid or compensatory hours, which is crucial for payroll.  
- **Integration with the timetable:**  
  - Importing the timetable from external programs (e.g. Plan Lekcji Vulcan, aSc Timetables).  
  - Handling individual instruction (separate timetables for specific students).  
- **Trips and outings module:**  
  - Wizard for creating trip documentation (goal, route, supervisors).  
  - Automatic generation of participant lists with parents’ contact details.  
  - Printing consent forms and regulations.  
  - Blocking students in the class register (the teacher sees a “on a trip” icon and cannot mark an unexcused absence).

### 4. Psychological and Pedagogical Support and Specialists

Support for students with special educational needs (SEN).

- **Specialist diaries:** Separate diaries for the school counselor, psychologist, speech therapist, and special education teacher.  
- **SEN documentation:**  
  - Creating IEPs (Individual Educational and Therapeutic Programs).  
  - Creating multi-specialist assessments of the student’s functioning.  
  - Recording remedial and compensatory classes.  
- **School nurse module:** Records of visits to the nurse’s office, health checkups, and PE exemptions.

### 5. Library and Canteen

Often separate modules integrated with the central student database.

- **E-library:**  
  - Online OPAC catalogue (students can reserve books via the internet).  
  - Automatic notifications about overdue books.  
  - Electronic inventory of the book collection using barcode scanners.  
- **Canteen:**  
  - Ordering meals by parents through the system.  
  - Cancelling meals (e.g. in case of illness before 8:00 a.m.).  
  - Financial settlements and generating payment details for lunches.

### 6. HR Administration (For Teachers)

The gradebook as a staff work tool.

- **Electronic requests:** Submitting leave requests, childcare requests, and private leave.  
- **Training:** Records of completed health and safety trainings and teachers’ council meetings.  
- **Professional promotion:** Module supporting teachers in their promotion path (development plans, reports).

### 7. Advanced Reporting and Printouts

Ability to generate hundreds of different summaries.

- **Reports for the school’s governing body (municipality/city):** Aggregate reports on attendance, grade averages, and numbers of students with special needs statements.  
- **Annual statistics:** Annual classification, summaries of primary and final exam results.  
- **Bulk printouts:** Grade slips for certificates, attendance sheets for parent meetings, student ID labels.

### 8. Security and System Configuration

School System Administrator panel.

- **Permission management:** Fine-grained role assignment (who can edit grades from the previous month, who sees sensitive data, who can excuse absences).  
- **System logs:** Complete digital trail (audit) of every click – who, from which IP address, and at what time made a change in the system, which is crucial in disputes (e.g. in court or with the school superintendent).  
- **Period locking:** Closing the possibility of editing grades after the classification council meeting.