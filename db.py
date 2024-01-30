import psycopg2
import config


def add_user(user):

    if get_user(user['id']):
        return False

    sql = "INSERT INTO users (tg_id, tg_name, username) VALUES (%s, %s, %s)"
    userdata = (user['id'], user['first_name'], user['username'])
    conn = psycopg2.connect(dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS, host=config.DB_HOST)
    with conn.cursor() as cursor:
        cursor.execute(sql, userdata)
        conn.commit()
    conn.close()

    return True


def get_user(user_id):
    sql = "SELECT * FROM users WHERE tg_id=%s"
    conn = psycopg2.connect(dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS, host=config.DB_HOST)
    with conn.cursor() as cursor:
        cursor.execute(sql, (user_id,))
        result_user = cursor.fetchone()
        conn.commit()
    conn.close()

    if not result_user:
        return None

    return {
        'id': result_user[0],
        'tg_id': result_user[1],
        'name': result_user[2],
        'username': result_user[3],
    }


def delete_user(user_id):
    sql = "DELETE FROM users WHERE tg_id=%s"
    conn = psycopg2.connect(dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS, host=config.DB_HOST)
    with conn.cursor() as cursor:
        cursor.execute(sql, (user_id,))
        conn.commit()
    conn.close()


def update_group(user_id, group):

    if not get_user(user_id):
        return False

    sql = "UPDATE users SET \"group\"=%s WHERE tg_id=%s"
    conn = psycopg2.connect(dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS, host=config.DB_HOST)
    data = (group, user_id)
    with conn.cursor() as cursor:
        cursor.execute(sql, data)
        conn.commit()
    conn.close()

    return True

print(get_user(1))