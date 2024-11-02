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
    if not data or 'notes' not in data:
        return jsonify({"error": "Invalid data. A list of 'notes' is required."}), 400

    notes = data['notes']
    combined_entries = "".join([f"Journal entry titled '{n['title']}': {n['content']}\n" for n in notes])

    prompt = f"{combined_entries}\nBased on these journal entries, provide a single emoji that best represents the overall mood."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an assistant that analyzes mood based on text."}, {"role": "user", "content": prompt}],
            max_tokens=2
        )
        emoji = response['choices'][0]['message']['content'].strip()
        return jsonify({"mood": emoji}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
