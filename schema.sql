-- Users
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

-- Courses
CREATE TABLE courses (
    course_id TEXT PRIMARY KEY,
    course_name TEXT NOT NULL,
    description TEXT,
    credits INTEGER
);

-- Prerequisites
CREATE TABLE prerequisites (
    course_id TEXT,
    prereq_id TEXT,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (prereq_id) REFERENCES courses(course_id)
);

-- Tags
CREATE TABLE tags (
    tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_name TEXT UNIQUE
);

-- Course-Tags
CREATE TABLE course_tags (
    course_id TEXT,
    tag_id INTEGER,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);

