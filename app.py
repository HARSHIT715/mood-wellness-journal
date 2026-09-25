import os
from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)

ENTRIES = []
NEXT_ID = 1
MOOD_LABELS = {1: '😞', 2: '🙁', 3: '😐', 4: '🙂', 5: '😄'}


def average_mood():
    if not ENTRIES:
        return None
    return round(sum(entry['mood'] for entry in ENTRIES) / len(ENTRIES), 1)


def most_common_mood():
    if not ENTRIES:
        return '—'

    mood_counts = {}
    for entry in ENTRIES:
        mood = entry['mood']
        mood_counts[mood] = mood_counts.get(mood, 0) + 1

    most_common = max(mood_counts, key=mood_counts.get)
    return f'{most_common}/5 {MOOD_LABELS[most_common]}'


def validate_entry(form):
    name = form.get('name', '').strip()
    entry_date = form.get('entry_date', '').strip()
    note = form.get('note', '').strip()
    mood_raw = form.get('mood', '').strip()

    if not name or not entry_date or not note or not mood_raw:
        return None, 'All fields are required.'
    try:
        mood = int(mood_raw)
    except ValueError:
        return None, 'Mood must be a number from 1 to 5.'
    if mood not in MOOD_LABELS:
        return None, 'Mood must be a number from 1 to 5.'
    try:
        datetime.strptime(entry_date, '%Y-%m-%d')
    except ValueError:
        return None, 'Please enter a valid date.'
    return {'name': name, 'date': entry_date, 'note': note, 'mood': mood}, None


@app.route('/')
def home():
    return render_template(
        'index.html',
        entries=ENTRIES,
        average=average_mood(),
        most_common_mood=most_common_mood(),
        commit_id=(
            os.getenv('RENDER_GIT_COMMIT')
            or os.getenv('GIT_SHA')
            or 'local-development'
        ),
        mood_labels=MOOD_LABELS,
    )


@app.post('/add')
def add_entry():
    global NEXT_ID
    entry, error = validate_entry(request.form)
    if error:
        return render_template(
            'index.html',
            entries=ENTRIES,
            average=average_mood(),
            most_common_mood=most_common_mood(),
            commit_id=(
                os.getenv('RENDER_GIT_COMMIT')
                or os.getenv('GIT_SHA')
                or 'local-development'
            ),
            mood_labels=MOOD_LABELS,
            error=error,
            form=request.form,
        ), 400
    entry['id'] = NEXT_ID
    NEXT_ID += 1
    entry['emoji'] = MOOD_LABELS[entry['mood']]
    ENTRIES.insert(0, entry)
    return redirect(url_for('home'))


@app.get('/api/entries')
def api_entries():
    return jsonify({'entries': ENTRIES, 'average_mood': average_mood()})


@app.get('/health')
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)

