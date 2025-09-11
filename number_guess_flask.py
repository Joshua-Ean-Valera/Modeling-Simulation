from flask import Flask, render_template_string, request
import random
import matplotlib.pyplot as plt
import io
import base64
from PIL import Image

app = Flask(__name__)

SECRET_MIN = 1
SECRET_MAX = 100_000

HTML_FORM = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Number Guess Simulation</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: #f4f6fb;
            margin: 0;
            padding: 0;
            min-height: 100vh;
        }
        .container {
            max-width: 700px;
            margin: 40px auto;
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.08);
            padding: 32px 40px 40px 40px;
        }
        h2 {
            color: #2d3a4b;
            margin-bottom: 16px;
        }
        label, .mode-label {
            font-size: 1.1em;
            color: #2d3a4b;
            margin-bottom: 8px;
            display: block;
        }
        .modes {
            margin-bottom: 18px;
        }
        input[type="radio"] {
            margin-right: 8px;
        }
        input[type="submit"] {
            background: #4f8cff;
            color: #fff;
            border: none;
            border-radius: 6px;
            padding: 10px 28px;
            font-size: 1em;
            cursor: pointer;
            transition: background 0.2s;
        }
        input[type="submit"]:hover {
            background: #2563eb;
        }
        .report-section {
            margin-top: 32px;
            background: #f7faff;
            border-radius: 8px;
            padding: 18px 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }
        pre {
            background: #eaf1fb;
            border-radius: 6px;
            padding: 14px;
            font-size: 1em;
            overflow-x: auto;
        }
        .animation-section {
            margin-top: 24px;
            text-align: center;
        }
        img {
            border-radius: 8px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            max-width: 100%;
            margin-top: 10px;
        }
        @media (max-width: 800px) {
            .container { padding: 18px 6vw; }
        }
    </style>
    <script>
        function scrollToAnimation() {
            var anim = document.getElementById('animation');
            if (anim) { anim.scrollIntoView({behavior: 'smooth'}); }
        }
        window.onload = function() {
            if (document.getElementById('animation')) scrollToAnimation();
        }
    </script>
</head>
<body>
    <div class="container">
        <h2>Number Guess Simulation</h2>
        <form method="post">
            <div class="mode-label">Choose mode:</div>
            <div class="modes">
                <input type="radio" name="mode" value="1" checked> Random Guess Mode<br>
                <input type="radio" name="mode" value="2"> Binary Search Mode
            </div>
            <input type="submit" value="Simulate">
        </form>
        {% if report %}
            <div class="report-section">
                <h3>Simulation Report</h3>
                <pre>{{ report }}</pre>
            </div>
            <div class="animation-section" id="animation">
                <h3>Simulation Animation</h3>
                <img src="data:image/gif;base64,{{ plot_url }}"/>
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

def simulate_guess(mode):
    secret = random.randint(SECRET_MIN, SECRET_MAX)
    attempts = 0
    guesses = []
    attempt_nums = []
    low = SECRET_MIN
    high = SECRET_MAX
    found = False
    report_lines = []
    frames = []
    while not found:
        if low > high:
            report_lines.append("Error: Range exhausted without finding the secret number.")
            break
        if mode == 1:
            g = random.randint(low, high)
        elif mode == 2:
            g = (low + high) // 2
        else:
            report_lines.append("Invalid mode. Use 1 for random, 2 for binary search.")
            break
        attempts += 1
        guesses.append(g)
        attempt_nums.append(attempts)
        # Create a frame for the current guess
        fig, ax = plt.subplots(figsize=(8,4))
        ax.plot(attempt_nums, guesses, marker='o', linestyle='-', color='b', label='Guesses')
        ax.axhline(secret, color='r', linestyle='--', label='Secret Number')
        ax.set_xlabel('Attempt')
        ax.set_ylabel('Guess')
        ax.set_title(f'Guessing the Secret Number (Attempt {attempts})')
        ax.legend()
        ax.grid(True)
        fig.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        frame = Image.open(buf).convert('RGB')
        frames.append(frame)
        if g == secret:
            msg = f"Guessed the secret number {secret} in {attempts} attempts!"
            report_lines.append(msg)
            found = True
        elif g < secret:
            msg = f"Attempt {attempts}: {g} is too low."
            report_lines.append(msg)
            low = g + 1
        else:
            msg = f"Attempt {attempts}: {g} is too high."
            report_lines.append(msg)
            high = g - 1
    # Create animated GIF
    gif_buf = io.BytesIO()
    frames[0].save(gif_buf, format='GIF', save_all=True, append_images=frames[1:], duration=200, loop=0)
    gif_buf.seek(0)
    plot_url = base64.b64encode(gif_buf.getvalue()).decode('utf8')
    return '\n'.join(report_lines), plot_url

@app.route('/', methods=['GET', 'POST'])
def index():
    report = None
    plot_url = None
    if request.method == 'POST':
        mode = int(request.form.get('mode', 1))
        report, plot_url = simulate_guess(mode)
    return render_template_string(HTML_FORM, report=report, plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
