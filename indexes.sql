-- 1. Index for accelerating table joins (JOIN students ON room = r.id)
CREATE INDEX IF NOT EXISTS idx_students_room 
ON students(room);

-- 2. Composite index for calculating average age and age difference (Queries 2 and 3)
CREATE INDEX IF NOT EXISTS idx_students_room_birthday 
ON students(room, birthday);

-- 3. Composite index for searching for mixed-gender rooms (Query 4)
CREATE INDEX IF NOT EXISTS idx_students_room_sex 
ON students(room, sex);