import sqlite3

def create_database():
    conn = sqlite3.connect('api.db')
    c = conn.cursor()

    # Create dictionary table
    c.execute('''CREATE TABLE IF NOT EXISTS dictionary
                 (id INTEGER PRIMARY KEY, word TEXT UNIQUE)''')

    # Create youtube_channels table
    c.execute('''CREATE TABLE IF NOT EXISTS youtube_channels
                 (id INTEGER PRIMARY KEY, channel_name TEXT UNIQUE)''')

    # Create video_details table
    c.execute('''CREATE TABLE IF NOT EXISTS video_details
                 (id INTEGER PRIMARY KEY, channel_id INTEGER, video_id TEXT UNIQUE)''')

    # Create word_counts table
    c.execute('''CREATE TABLE IF NOT EXISTS word_counts
                 (id INTEGER PRIMARY KEY, video_id INTEGER, word_id INTEGER, count INTEGER)''')

    conn.commit()
    conn.close()

def get_or_create_word(word):
    conn = sqlite3.connect('api.db')
    c = conn.cursor()

    # Check if the word exists in the dictionary
    c.execute("SELECT id FROM dictionary WHERE word = ?", (word,))
    result = c.fetchone()

    if result:
        word_id = result[0]
    else:
        # If the word doesn't exist, insert it into the dictionary
        c.execute("INSERT INTO dictionary (word) VALUES (?)", (word,))
        word_id = c.lastrowid

    conn.commit()
    conn.close()
    return word_id

def get_or_create_channel(channel_name):
    conn = sqlite3.connect('api.db')
    c = conn.cursor()

    # Check if the channel exists in the youtube_channels table
    c.execute("SELECT id FROM youtube_channels WHERE channel_name = ?", (channel_name,))
    result = c.fetchone()

    if result:
        channel_id = result[0]
    else:
        # If the channel doesn't exist, insert it into the youtube_channels table
        c.execute("INSERT INTO youtube_channels (channel_name) VALUES (?)", (channel_name,))
        channel_id = c.lastrowid

    conn.commit()
    conn.close()
    return channel_id

def insert_video(channel_id, video_id, word_counts):
    conn = sqlite3.connect('api.db')
    c = conn.cursor()

    # Insert video details
    c.execute("INSERT INTO video_details (channel_id, video_id) VALUES (?, ?)", (channel_id, video_id))
    video_row_id = c.lastrowid  # Get the ID of the inserted video row

    # Insert word counts
    for word_id, count in word_counts.items():
        c.execute("INSERT INTO word_counts (video_id, word_id, count) VALUES (?, ?, ?)", 
                  (video_row_id, word_id, count))

    conn.commit()
    conn.close()

def get_common_words(channel_id):
    conn = sqlite3.connect('api.db')
    c = conn.cursor()

    c.execute('''
        SELECT d.word, SUM(wc.count) AS total_count
        FROM dictionary d
        JOIN word_counts wc ON d.id = wc.word_id
        JOIN video_details vd ON wc.video_id = vd.id AND vd.channel_id = ?
        GROUP BY d.word
        ORDER BY total_count DESC
        LIMIT 10;
    ''', (channel_id,))

    common_words = [{'word': row[0], 'count': row[1]} for row in c.fetchall()]
    conn.close()
    return common_words

def get_top_videos(channel_id):
    conn = sqlite3.connect('api.db')
    c = conn.cursor()

    c.execute('''
        SELECT vd.video_id, SUM(wc.count) AS total_words
        FROM word_counts wc
        JOIN video_details vd ON wc.video_id = vd.id AND vd.channel_id = ?
        GROUP BY vd.video_id
        ORDER BY total_words DESC
        LIMIT 10;
    ''', (channel_id,))

    top_videos = [{'video_id': row[0], 'total_words': row[1]} for row in c.fetchall()]
    conn.close()
    return top_videos