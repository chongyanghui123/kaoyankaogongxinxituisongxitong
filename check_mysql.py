import pymysql

try:
    # 连接MySQL数据库
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='123456789',
        database='common_db',
        charset='utf8mb4'
    )
    
    print("MySQL数据库连接成功！")
    
    try:
        with connection.cursor() as cursor:
            # 查询用户数据
            cursor.execute("SELECT id, username, email, is_admin FROM users")
            users = cursor.fetchall()
            
            print("\n用户表数据:")
            for user in users:
                print(f"ID: {user[0]}, 用户名: {user[1]}, 邮箱: {user[2]}, 管理员: {user[3]}")
            
            print(f"\n用户总数: {len(users)}")
            
            # 查询表结构
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("\n数据库中的表:")
            for table in tables:
                print(f"- {table[0]}")
                
    finally:
        connection.close()
        
except Exception as e:
    print(f"连接失败: {e}")
