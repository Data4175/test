import sqlite3
db_name = 'quiz.sqlite'
conn = None
cursor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    global conn, cursor
    cursor.close()
    conn.close()

def do(query):
    global conn, cursor
    cursor.execute(query)
    conn.commit()

def clear_db():
    ''' удаляет все таблицы '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()

def check_answers(quest_id, answer):
    query = ''' 
    SELECT question.answer 
    FROM question, quiz_content 
    WHERE question.id = (?) AND quiz_content.question_id = question.id '''
    open()
    cursor.execute(query, str(quest_id))
    data = cursor.fetchone()
    close()
    print(data)
    if data is None:
        return False
    else:
        if data[0] == answer:
            return True
        else:
            return False
    
def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')

    do(''' CREATE TABLE IF NOT EXISTS quiz_content (
        id INTEGER PRIMARY KEY,
        quiz_id INTEGER,
        question_id INTEGER,
        FOREIGN KEY (quiz_id) REFERENCES quiz (id),
        FOREIGN KEY (question_id) REFERENCES question (id)
    ) ''')

    do(''' CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY,
        name VARCHAR
    ) ''')

    do(''' CREATE TABLE IF NOT EXISTS question (
        id INTEGER PRIMARY KEY,
        question VARCHAR,
        answer VARCHAR,
        wrong1 VARCHAR,
        wrong2 VARCHAR,
        wrong3 VARCHAR
    ) ''')

    close()

def add_question():
    questions = [
        ('Сколько месяцев в году имеют 28 дней?', 'Все', 'Один', 'Ни одного', 'Два'),
        ('Каким станет зелёный утёс, если упадёт в Красное море?', 'Мокрым', 'Красным', 'Не изменится', 'Фиолетовым'),
        ('Какой рукой лучше размешивать чай?', 'Ложкой', 'Правой', 'Левой', 'Любой'),
        ('Что не имеет длины, глубины, ширины, высоты, а можно измерить?', 'Время', 'Глупость', 'Море', 'Воздух')]
    open()
    cursor.executemany(''' INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (?, ?, ?, ?, ?) ''', questions)
    conn.commit()
    close()

def add_quiz():
    open()
    names = [
        ('Своя игра', ),
        ('Кто хочет стать миллионером?', ),
        ('Самый умный', )
            ]
    cursor.executemany(''' INSERT INTO quiz (name) VALUES (?)''', names)
    conn.commit()
    close()

def add_content():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')

    answer = input('Хотите добавить связь? (y/n)')
    while answer != 'n':
        quiz_id = int(input('ID викторины'))
        question_id = int(input('ID вопроса'))

        cursor.execute(''' INSERT INTO quiz_content (quiz_id, question_id) VALUES (?, ?)''', [quiz_id, question_id])
        conn.commit()
        answer = input('Хотите добавить связь? (y/n)')
    close()
        
def get_question_after(question_id=0, quiz_id=1):
    ''' возвращает следующий вопрос после вопроса с переданным id
    для первого вопроса передаётся значение по умолчанию '''
    open()
    query = '''
    SELECT question.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
    FROM question, quiz_content
    WHERE quiz_content.question_id == question.id
    AND quiz_content.quiz_id == ? AND question.id > ?
    ORDER BY question.id'''
    cursor.execute(query, [quiz_id, question_id])
    result = cursor.fetchone()
    close()
    return result

def get_quiz():
    open()
    cursor.execute(''' SELECT * FROM quiz ORDER BY id ''')
    result = cursor.fetchall()
    close()
    return result

def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

def main():
    clear_db()
    create()
    add_question()
    add_quiz()
    add_content()
    show_tables()
    print(get_question_after(1, 1))

if __name__ == "__main__":
    main()
