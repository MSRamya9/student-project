CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone_number TEXT,
    address TEXT,
    class_time TEXT
);

INSERT INTO students (
    student_id,
    first_name,
    last_name,
    phone_number,
    address,
    class_time
)
VALUES
    (1, 'Ramya', 'Mamillapalli', '404-555-0101', 'Atlanta, GA', '09:00 AM'),
    (2, 'John', 'Smith', '678-555-0102', 'Marietta, GA', '10:30 AM');

SELECT * FROM students;