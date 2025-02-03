from flask import Flask, render_template_string, request
import time as t
import requests

app = Flask(__name__)

# HTML & CSS Combined in the same script for rendering
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Comment Bot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        .form-container {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 300px;
            text-align: center;
        }

        h1 {
            font-size: 24px;
            margin-bottom: 20px;
        }

        textarea {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }

        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }

        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <h1>Post a Comment on Facebook</h1>
        <form method="POST" action="/comment">
            <label for="comment">Enter your comment:</label>
            <textarea name="comment" id="comment" rows="4" required></textarea>
            <button type="submit">Post Comment</button>
        </form>
    </div>
</body>
</html>
"""

# Read configuration from text files
def read_config():
    config = {}
    
    # Reading from hatters_name.txt file to get name and post URL
    with open("hatters_name.txt", "r") as f:
        lines = f.readlines()
        config['name'] = lines[0].strip()  # First line: User's name
        config['post_url'] = lines[1].strip()  # Second line: Facebook post URL
    
    # Reading token and time from other files
    with open("token.txt", "r") as f:
        config['token'] = f.read().strip()
    with open("time.txt", "r") as f:
        config['time'] = int(f.read().strip())
    
    return config

@app.route('/')
def index():
    return render_template_string(html_code)

@app.route('/comment', methods=['POST'])
def comment():
    config = read_config()

    # Get data from the form
    comment_text = request.form.get('comment')

    # Retrieve the Facebook API token and post URL from the config files
    token = config['token']
    post_url = config['post_url']
    comment_time = config['time']
    user_name = config['name']

    # Append the user's name to the comment
    full_comment = f"Comment by {user_name}: {comment_text}"

    # Perform the commenting after the specified time
    t.sleep(comment_time)
    comment_on_facebook(post_url, full_comment, token)

    return f"Comment scheduled successfully. It will post after {comment_time} seconds."

def comment_on_facebook(url, comment_text, token):
    api_url = f"https://graph.facebook.com/{url}/comments"
    params = {
        'message': comment_text,
        'access_token': token
    }
    response = requests.post(api_url, params=params)
    if response.status_code == 200:
        print("Comment posted successfully!")
    else:
        print(f"Failed to post comment. Error: {response.text}")

if __name__ == '__main__':
    app.run(debug=True)
