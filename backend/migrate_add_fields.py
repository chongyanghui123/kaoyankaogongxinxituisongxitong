import os
import sys
from sqlalchemy import create_engine, text, inspect

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import settings


def get_db_url():
    if settings.DATABASE_HOST and settings.DATABASE_USER:
        return (
            f"mysql+pymysql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@"
            f"{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.COMMON_DB}?charset=utf8mb4"
        )
    else:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", f"{settings.COMMON_DB}.db")
        return f"sqlite:///{db_path}"


def column_exists(inspector, table_name, column_name):
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns


def migrate():
    db_url = get_db_url()
    engine = create_engine(db_url)
    inspector = inspect(engine)

    with engine.connect() as conn:
        if 'users' in inspector.get_table_names():
            new_columns = [
                ('user_type', 'INTEGER DEFAULT 1'),
                ('wx_openid', 'VARCHAR(100)'),
                ('wx_unionid', 'VARCHAR(100)'),
                ('phone_bound', 'BOOLEAN DEFAULT 0'),
            ]

            for col_name, col_type in new_columns:
                if not column_exists(inspector, 'users', col_name):
                    print(f"Adding column '{col_name}' to 'users' table...")
                    conn.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}"))
                    conn.commit()
                    print(f"  Column '{col_name}' added successfully.")
                else:
                    print(f"  Column '{col_name}' already exists in 'users', skipping.")

            if column_exists(inspector, 'users', 'phone'):
                result = conn.execute(text(
                    "SELECT COUNT(*) FROM information_schema.COLUMNS "
                    "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'users' "
                    "AND COLUMN_NAME = 'phone' AND IS_NULLABLE = 'NO'"
                ))
                if result.fetchone()[0] > 0:
                    print(f"Making 'phone' column nullable in 'users' table...")
                    try:
                        conn.execute(text("ALTER TABLE users MODIFY COLUMN phone VARCHAR(20) NULL"))
                        conn.commit()
                        print(f"  Column 'phone' is now nullable.")
                    except Exception as e:
                        print(f"  Could not modify 'phone' column: {e}")
                else:
                    print(f"  Column 'phone' is already nullable, skipping.")

        if 'learning_materials' in inspector.get_table_names():
            if not column_exists(inspector, 'learning_materials', 'is_vip'):
                print(f"Adding column 'is_vip' to 'learning_materials' table...")
                conn.execute(text("ALTER TABLE learning_materials ADD COLUMN is_vip BOOLEAN DEFAULT 0"))
                conn.commit()
                print(f"  Column 'is_vip' added successfully.")
            else:
                print(f"  Column 'is_vip' already exists in 'learning_materials', skipping.")

    print("\nMigration completed!")


if __name__ == "__main__":
    migrate()
