import pymysql
import pandas as pd
db=None

try:
    db = pymysql.connect(
        host='127.0.0.1',
        user = 'root',
        passwd = 'tiger',
        db='chatbot',
        charset='utf8'
    )
    students = [
        {'name': 'kei', 'age':36, 'address':'PUSAN'},
        {'name': 'Tony', 'age': 34, 'address': 'PUSAN'},
        {'name': 'Jaeyoo', 'age': 39, 'address': 'GWANGJU'},
        {'name': 'Grace', 'age': 28, 'address': 'SEOUL'},
        {'name': 'Jenny', 'age': 27, 'address': 'SEOUL'},
    ]
    for s in students:
        with db.cursor() as cursor:
            sql='''
                insert tb_student(name, age, address) values("%s", %d, "%s")
            '''%(s['name'], s['age'], s['address'])
            cursor.execute(sql)
    db.commit()

    #30대 학생만 조회
    cond_age = 30
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        sql='''
            select*from tb_student where age> %d
            ''' % cond_age
        cursor.execute(sql)
        results = cursor.fetchall()
    print(results)

    cond_name = 'Grace'
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        sql='''
            select*from tb_student where name="%s"
            ''' % cond_name
        cursor.execute(sql)
        result= cursor.fetchone()
    print(result['name'], result['age'])

    df = pd.DataFrame(results)
    print(df)
    print("성공")

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()
