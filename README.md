# Tasktracker-Dashboard Project

This project is a full-stack application with a Python FastAPI backend and a Vue.js frontend.

## Folder Structure

- `/backend`: Contains all the Python FastAPI components.
  - `/app`: Primary application code.
    - `/controllers`: Controller modules for application logic.
    - `/services`: Business logic and interaction with external services/APIs.
    - `/models`: ORM models for database interaction.
    - `/schemas`: Request and response serialization models.
    - `/tests`: Test cases for backend components.
    - `requirements.txt`: Python dependencies.
    - `Dockerfile`: Docker configuration for backend.
    - `.env`: Environment variables (not committed to version control).
- `/frontend`: Vue.js codebase.
  - `/src`: Source code with Vue components and services.
  - `/tests`: Vue unit and integration tests.
  - `package.json`: Node.js project dependencies.
  - `Dockerfile`: Docker configuration for frontend.
- `/deployment`: Docker and Kubernetes configuration files.

## Setup Instructions

To be filled with setup instructions for running the Tasktracker-Dashboard application.


# Database

This project uses Alembic for database migrations. Alembic is a database migration tool that offers version control for your database schemas by using SQLAlchemy. 

## Migrations

Migrations are like version control for your database. Alembic allows you to alter your database schema in a structured and orderly manner, reflecting your changes in code which are version controlled.

### Generating Migrations

After you modify the database schema in your SQLAlchemy models, generate a migration script with Alembic:
```SHELL
alembic -c <path_to_ini_file> revision --autogenerate -m "Your message about the migration"
```

In the command above, replace `<path_to_ini_file>` with the path to your `alembic.ini` file, and replace `"Your message about the migration"` with a brief message describing the changes the migration will make to the database.

This will create a new migration script file in your `alembic/versions` directory.

### Applying Migrations

To apply the migrations to your database, use the `upgrade` command:
```SHELL
alembic -c <path_to_ini_file> upgrade head
```

The `head` keyword refers to the most recent migration script. 

Using the `upgrade` command will apply all migration scripts that haven't been run yet.

### Rollback Migrations

If you need to undo the most recent batch of migrations, you can use the `downgrade` command:

```SHELL
alembic -c <path_to_ini_file> downgrade -1
```

This will undo the last batch of migrations applied.

### Viewing Migration History

To view a list of all the migration scripts, along with their version numbers, you can use the `history` command:
```SHELL
alembic -c <path_to_ini_file> history
```

This will list all the migrations applied to the database in chronological order.

Remember: Always back up your production data before running migrations against it. Migrations can sometimes have unintended consequences, and it's better to be safe than sorry.