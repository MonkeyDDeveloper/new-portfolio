"""
Database initialization script
Executes the schema.sql file to create all tables and insert sample data
"""

import pymysql
from decouple import config
import os


def get_connection():
    """Create a database connection"""
    return pymysql.connect(
        host=config("HOST"),
        port=int(config("DB_PORT")),
        user=config("USERNAME"),
        password=config("PASSWORD"),
        database=config("DATABASE"),
        cursorclass=pymysql.cursors.DictCursor
    )


def execute_sql_file(filepath: str):
    """Execute SQL statements from a file"""
    # Read the SQL file
    with open(filepath, 'r', encoding='utf-8') as file:
        sql_content = file.read()

    # Split by semicolon to get individual statements
    statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            print(f"🚀 Executing {len(statements)} SQL statements from {filepath}...\n")

            for i, statement in enumerate(statements, 1):
                # Skip comments and empty statements
                if statement.startswith('--') or not statement:
                    continue

                try:
                    cursor.execute(statement)

                    # Print info about what was executed
                    if 'CREATE TABLE' in statement.upper():
                        table_name = statement.split('CREATE TABLE')[1].split('(')[0].strip()
                        print(f"  ✅ [{i}/{len(statements)}] Created table: {table_name}")
                    elif 'INSERT INTO' in statement.upper():
                        table_name = statement.split('INSERT INTO')[1].split('(')[0].strip()
                        print(f"  ✅ [{i}/{len(statements)}] Inserted data into: {table_name}")
                    elif 'DROP TABLE' in statement.upper():
                        table_name = statement.split('DROP TABLE IF EXISTS')[1].strip()
                        print(f"  ⚠️  [{i}/{len(statements)}] Dropped table: {table_name}")
                    else:
                        print(f"  ✅ [{i}/{len(statements)}] Executed statement")

                except Exception as e:
                    print(f"  ❌ Error executing statement {i}: {str(e)}")
                    print(f"     Statement: {statement[:100]}...")
                    raise

            connection.commit()
            print("\n✅ Database initialized successfully!")

    except Exception as e:
        connection.rollback()
        print(f"\n❌ Error initializing database: {str(e)}")
        raise
    finally:
        connection.close()


def main():
    """Main function to initialize the database"""
    print("=" * 60)
    print("Portfolio Database Initialization")
    print("=" * 60)
    print()

    # Get the path to schema.sql
    current_dir = os.path.dirname(os.path.abspath(__file__))
    schema_file = os.path.join(current_dir, 'schema.sql')

    if not os.path.exists(schema_file):
        print(f"❌ Error: schema.sql not found at {schema_file}")
        return

    print(f"📄 Schema file: {schema_file}")
    print(f"🗄️  Database: {config('DATABASE')}")
    print(f"🖥️  Host: {config('HOST')}:{config('DB_PORT')}")
    print()

    # Ask for confirmation
    response = input("⚠️  This will DROP all existing tables and recreate them. Continue? (yes/no): ")

    if response.lower() not in ['yes', 'y']:
        print("❌ Operation cancelled.")
        return

    print()

    try:
        execute_sql_file(schema_file)
        print()
        print("=" * 60)
        print("🎉 Database setup complete!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("  1. Start the API: python start.py")
        print("  2. Visit the docs: http://localhost:8000/docs")
        print("  3. Login with: username='admin', password='Juan123!'")
        print()

    except Exception as e:
        print()
        print("=" * 60)
        print("❌ Database setup failed!")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()


if __name__ == "__main__":
    main()
