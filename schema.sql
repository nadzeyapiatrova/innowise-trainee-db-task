CREATE TABLE IF NOT EXISTS rooms (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS students (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthday DATE NOT NULL,
    sex CHAR(1) NOT NULL,
    room INT REFERENCES rooms(id)
);

-- Composite index for joins by room and age calculations (Queries 1, 2, 3)
-- Also covers standalone lookups/joins on `room` via the leftmost prefix rule
CREATE INDEX IF NOT EXISTS idx_students_room_birthday 
ON students(room, birthday);

-- Composite index for joins by room and mixed-gender filtering (Query 4)
CREATE INDEX IF NOT EXISTS idx_students_room_sex 
ON students(room, sex);