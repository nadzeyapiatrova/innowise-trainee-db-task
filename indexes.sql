
-- Composite index for joins by room and age calculations (Queries 1, 2, 3)
-- Also covers standalone lookups/joins on `room` via the leftmost prefix rule
CREATE INDEX IF NOT EXISTS idx_students_room_birthday 
ON students(room, birthday);

-- Composite index for joins by room and mixed-gender filtering (Query 4)
CREATE INDEX IF NOT EXISTS idx_students_room_sex 
ON students(room, sex);