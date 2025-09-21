from flask import Flask, render_template, send_from_directory

app = Flask(__name__, static_folder="static", template_folder="templates")

# Serve files from existing Next.js public/ folder for convenience (images, placeholders)
@app.route('/public/<path:filename>')
def public_files(filename):
    return send_from_directory('public', filename)

# Maintain Next.js-style image path: /images/... maps to public/images
@app.route('/images/<path:filename>')
def public_images(filename):
    return send_from_directory('public/images', filename)


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/groups')
def groups():
    return render_template('groups.html')


@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/quiz')
def quiz():
    return render_template('quiz.html')


if __name__ == '__main__':
    # Run with: py app.py
    app.run(host='0.0.0.0', port=5000, debug=True)
