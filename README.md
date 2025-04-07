<<<<<<< HEAD
# flask_tasklist_backend
=======
# for psql part
Server [localhost]:
Database [postgres]:
Port [5432]:
Username [postgres]: postgres
Password for user postgres:
psql (17.4)
WARNING: Console code page (437) differs from Windows code page (1252)
         8-bit characters might not work correctly. See psql reference
         page "Notes for Windows users" for details.
Type "help" for help.

postgres=# -- Step 1: Create your database
postgres=# CREATE DATABASE flask_task_db;
CREATE DATABASE
postgres=#
postgres=# -- Step 2: (Optional) Create a new user
postgres=# CREATE USER flask_user WITH PASSWORD 'yourpassword';
CREATE ROLE
postgres=#
postgres=# -- Step 3: Give user access to the database
postgres=# GRANT ALL PRIVILEGES ON DATABASE flask_task_db TO flask_user;
GRANT
postgres=#
postgres=# -- Step 4: Connect to the new database
postgres=# \c flask_task_db
You are now connected to database "flask_task_db" as user "postgres".
flask_task_db=#
flask_task_db=# -- Step 5: Create the table
flask_task_db=# CREATE TABLE tasks (
flask_task_db(#     id SERIAL PRIMARY KEY,
flask_task_db(#     title VARCHAR(255) NOT NULL,
flask_task_db(#     description TEXT,
flask_task_db(#     status VARCHAR(50) DEFAULT 'pending',
flask_task_db(#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
flask_task_db(#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
flask_task_db(# );
CREATE TABLE
flask_task_db=#
flask_task_db=# -- Step 6: Insert 10 sample tasks
flask_task_db=# INSERT INTO tasks (title, description, status) VALUES
flask_task_db-# ('Buy groceries', 'Milk, Eggs, Bread', 'pending'),
flask_task_db-# ('Complete assignment', 'Finish Flask backend assignment', 'in_progress'),
flask_task_db-# ('Call mom', 'Check in with family', 'done'),
flask_task_db-# ('Fix bug #123', 'Null pointer exception in task module', 'in_progress'),
flask_task_db-# ('Read a book', 'Start reading Clean Code', 'pending'),
flask_task_db-# ('Workout', '30-minute cardio session', 'pending'),
flask_task_db-# ('Plan weekend trip', 'Look for places near the lake', 'pending'),
flask_task_db-# ('Pay electricity bill', 'Due next Monday', 'done'),
flask_task_db-# ('Update resume', 'Add latest internship experience', 'in_progress'),
flask_task_db-# ('Schedule dentist appointment', 'Anytime next week', 'pending');
INSERT 0 10
flask_task_db=#
flask_task_db=# CREATE TABLE tasks (
flask_task_db(#     id SERIAL PRIMARY KEY,
flask_task_db(#     title VARCHAR(255) NOT NULL,
flask_task_db(#     description TEXT,
flask_task_db(#     status VARCHAR(50) DEFAULT 'pending',
flask_task_db(#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
flask_task_db(#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
flask_task_db(# );
ERROR:  relation "tasks" already exists
flask_task_db=# SELECT * FROM tasks;
 id |            title             |              description              |   status    |         created_at         |         updated_at
----+------------------------------+---------------------------------------+-------------+----------------------------+----------------------------
  1 | Buy groceries                | Milk, Eggs, Bread                     | pending     | 2025-04-06 16:49:54.466271 | 2025-04-06 16:49:54.466271
  2 | Complete assignment          | Finish Flask backend assignment       | in_progress | 2025-04-06 16:49:54.466271 | 2025-04-06 16:49:54.466271
  3 | Call mom                     | Check in with family                  | done        | 2025-04-06 16:49:54.466271 | 2025-04-06 16:49:54.466271
  4 | Fix bug #123                 | Null pointer exception in task module | in_progress | 2025-04-06 16:49:54.466271 | 2025-04-06 16:49:54.466271
  5 | Read a book                  | Start reading Clean Code              | pending     | 2025-04-06 16:49:54.466271 | 2025-04-06 16:49:54.466271
  6 | Workout                      | 30-minute cardio session              | pending     | 2025-04-06 16:49:54.466271 | 2025-04-06 16:49:54.466271
  7 | Plan weekend trip            | Look for places near the lake         | pending     | 2025-04-06 16:49:54.466271 | 2025-04-06 16:49:54.466271
  8 | Pay electricity bill         | Due next Monday                       | done        | 2025-04-06 16:49:54.466271 | 2025-04-06 16:49:54.466271
  9 | Update resume                | Add latest internship experience      | in_progress | 2025-04-06 16:49:54.466271 | 2025-04-06 16:49:54.466271
 10 | Schedule dentist appointment | Anytime next week                     | pending     | 2025-04-06 16:49:54.466271 | 2025-04-06 16:49:54.466271
(10 rows)
>>>>>>> 54a6fb3 (Initial commit)
