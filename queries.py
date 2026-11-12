QUERIES = {
    "1_students_per_room": """
        SELECT 
            r.name,
            COUNT(s.id) AS students_count
        FROM rooms r 
        LEFT JOIN students s ON s.room = r.id 
        GROUP BY r.id, r.name
        ORDER BY r.id;
    """,

    "2_top5_youngest_rooms": """
        SELECT 
            r.name,
            ROUND(AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday)))::numeric, 1) AS students_avg_age
        FROM rooms r 
        JOIN students s ON s.room = r.id 
        GROUP BY r.name
        ORDER BY students_avg_age
        LIMIT 5;
    """,

    "3_top5_biggest_age_diff": """
        SELECT 
            r.name,
            EXTRACT(YEAR FROM AGE(MAX(s.birthday), MIN(s.birthday))) AS students_diff_age
        FROM rooms r 
        JOIN students s ON s.room = r.id 
        GROUP BY r.name
        ORDER BY students_diff_age DESC
        LIMIT 5;
    """,

    "4_mixed_gender_rooms": """
        SELECT 
            r.name
        FROM rooms r 
        JOIN students s ON s.room = r.id 
        GROUP BY r.name
        HAVING COUNT(DISTINCT s.sex) > 1;
    """
}
