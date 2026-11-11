import sqlite3
import json
import os
from google import genai
from google.genai import types

conn = sqlite3.connect('data.db')
client = genai.Client(api_key="AQ.Ab8RN6LiWTPwc1aRxG1BhSI5sbBp_cNM18DANzfMjz9P3KrYzw")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS customer_reviews (
    id integer primary key AUTOINCREMENT,
    customer_name TEXT,
    review_text TEXT NOT NULL,
    sentiment TEXT DEFAULT NULL,   
    departament TEXT DEFAULT NULL      
)
""")
cursor.execute("SELECT COUNT(*) FROM customer_reviews")


if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO customer_reviews (customer_name, review_text) VALUES (?, ?)
    """, [
        ('Alex Smith', 'The laptop screen is fantastic, but delivery took almost three weeks!'),
        ('Maria Garcia', 'Customer support answered in 2 minutes and fixed my account. Super happy!'),
        ('John Doe', 'Overpriced junk. The keyboard broke on the second day.'),
        ('Anna Novak', 'Package arrived damaged and the mouse was broken inside.')
    ])
    conn.commit()

cursor.execute("SELECT id, customer_name, review_text FROM customer_reviews WHERE sentiment IS NULL")
unprocessed_reviews = cursor.fetchall()
# print (unprocessed_reviews)
conn.commit()

def check_reviews(text):
    prompt_for_gem = f""" Analyze this customer review: "{text}"
    Return ONLY a JSON object with keys:
    - "sentiment": ("Positive", "Negative", or "Neutral")
    - "departament": ("Product", "Support", "Pricing", or "Shipping")"""

    response = client.models.generate_content(
        model="models/gemini-3.5-flash-lite",  
        contents=prompt_for_gem,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    return json.loads(response.text)

for row in unprocessed_reviews:
    id, name, text = row
    # print (id, name, text)

    data = check_reviews(text)
    # print (data)

    cursor.execute("""
        UPDATE customer_reviews
        SET sentiment = ?, departament = ?
        WHERE id = ?
    """, (data['sentiment'], data['departament'], id))

    # print(f"  -> VYSLEDOK: Sentiment={data['sentiment']}, Departament={data['departament']}")  

    cursor.execute("SELECT id, customer_name, sentiment, departament FROM customer_reviews")

for row in cursor.fetchall():
    print(row) 

    conn.close()
# print("\nОтвет от Gemini:")
# print(response.text)