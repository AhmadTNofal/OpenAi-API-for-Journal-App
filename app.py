import openai
from flask import Flask, request, jsonify

app = Flask(__name__)
openai.api_key = 'sk-tbtbdjXN0PNeKVX8x6oXJFABUkwYsEeOj9TinWn3jOT3BlbkFJuGto6skfATpazIFkDBnEr1JtKDe0ykgJkavseRQP0A'  

@app.route('/api/give-advice', methods=['POST'])
def give_advice():
    data = request.get_json()
    if not data or 'notes' not in data:
        return jsonify({"error": "Invalid data. A list of 'notes' is required."}), 400

    notes = data['notes']
    combined_entries = "".join([f"Journal entry titled '{n['title']}': {n['content']}\n" for n in notes])

    prompt = f"{combined_entries}\nCan you provide one sentence of advice based on these journal entries?"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
            max_tokens=50
        )
        advice = response['choices'][0]['message']['content'].strip()
        return jsonify({"advice": advice}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/track-mood', methods=['POST'])
def track_mood():
    data = request.get_json()

    # Validate the request data
    if not data or 'notes' not in data or not isinstance(data['notes'], list) or len(data['notes']) != 1:
        return jsonify({"error": "Invalid data. A single note with 'title' and 'content' is required."}), 400

    note = data['notes'][0]
    if 'title' not in note or 'content' not in note:
        return jsonify({"error": "Invalid data. 'title' and 'content' are required in the note."}), 400

    title = note['title']
    content = note['content']

    prompt = f"Journal entry titled '{title}': {content}\nProvide a single emoji that best represents the mood of this journal entry."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an assistant that analyzes mood based on text."}, {"role": "user", "content": prompt}],
            max_tokens=2,
            n=1,  # Ensure only one response
            stop=None,  # Avoid using stop sequences
            temperature=0.7  # Adjust temperature for better emoji results
        )
        emoji = response['choices'][0]['message']['content'].strip()
        
        # Ensure the emoji is valid and does not contain additional text
        if not emoji or len(emoji) > 2:  # Most emojis are one character, but some are two
            emoji = "❓"  # Default emoji if the response is invalid
        
        return jsonify({"mood": emoji}), 200
    except Exception as e:
        return jsonify({"error": "Failed to analyze mood. Please try again later."}), 500

if __name__ == '__main__':
    app.run(debug=True)