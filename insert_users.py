import sqlite3
conn = sqlite3.connect('/Users/huichongyang/Desktop/考研考公双赛道情报监控系统/backend/data/common_db.db')
cursor = conn.cursor()

# 插入用户43
try:
    cursor.execute('''
        INSERT INTO users (id, username, email, phone, password, real_name, is_active, is_admin, is_vip, vip_start_time, vip_end_time, vip_type, trial_status, created_at, updated_at)
        VALUES (43, '惠yang', 'chongyanghui123@gmail.com', '18109271097', '123456a', '惠重阳', 1, 0, 0, NULL, NULL, 0, 1, '2026-04-12 19:11:56', '2026-04-12 22:19:38')
    ''')
    print('用户43插入成功')
except sqlite3.Error as e:
    print(f'用户43插入失败: {e}')

# 插入用户44
try:
    cursor.execute('''
        INSERT INTO users (id, username, email, phone, password, real_name, is_active, is_admin, is_vip, vip_start_time, vip_end_time, vip_type, trial_status, created_at, updated_at)
        VALUES (44, '惠重阳', 'chongyanghui12@gmail.com', '18109271096', '123456a', '惠重阳', 1, 0, 0, NULL, NULL, 0, 1, '2026-04-12 21:35:54', '2026-04-12 21:35:54')
    ''')
    print('用户44插入成功')
except sqlite3.Error as e:
    print(f'用户44插入失败: {e}')

conn.commit()
conn.close()
print('用户数据插入完成')
