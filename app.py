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
    title = note.get('title', '').strip()
    content = note.get('content', '').strip()

    if not title or not content:
        return jsonify({"error": "Invalid data. 'title' and 'content' are required and cannot be empty."}), 400

    # Refined prompt to encourage more accurate and creative emoji responses
    prompt = (
        f"Journal entry titled '{title}': {content}\n"
        "Based on this journal entry, provide a single emoji that best reflects its mood. "
        "Be creative and pick the emoji that feels most emotionally appropriate."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that analyzes mood based on text."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=5,  # Restrict response length to a single emoji
            n=1,
            stop=None,
            temperature=0.8  # Slightly higher temperature for creativity
        )
        emoji = response['choices'][0]['message']['content'].strip()
        
        # Validate the emoji response
        if not emoji or len(emoji) > 2:  # Most emojis are 1-2 characters
            emoji = "🤔"  # Default fallback emoji for invalid responses
        
        return jsonify({"mood": emoji}), 200
    except Exception as e:
        return jsonify({"error": "Failed to analyze mood. Please try again later."}), 500


if __name__ == '__main__':
    app.run(debug=True)