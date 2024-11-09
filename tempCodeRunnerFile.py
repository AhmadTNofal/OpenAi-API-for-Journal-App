@app.route('/api/track-mood', methods=['POST'])
def track_mood():
    data = request.get_json()

    # Validate the request data to ensure 'notes' contains at least one entry
    if not data or 'notes' not in data or not isinstance(data['notes'], list) or len(data['notes']) != 1:
        return jsonify({"error": "Invalid data. A single note with 'title' and 'content' is required."}), 400

    # Extract the single note entry from the list
    note = data['notes'][0]
    
    # Check if 'title' and 'content' are in the note
    if 'title' not in note or 'content' not in note:
        return jsonify({"error": "Invalid data. 'title' and 'content' are required in the note."}), 400

    title = note['title']
    content = note['content']
    
    # Create the prompt for mood analysis
    prompt = f"Journal entry titled '{title}': {content}\nProvide a single emoji that best represents the mood of this journal entry."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an assistant that analyzes mood based on text."}, {"role": "user", "content": prompt}],
            max_tokens=2
        )
        
        # Extract the emoji response
        emoji = response['choices'][0]['message']['content'].strip()
        return jsonify({"mood": emoji}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
