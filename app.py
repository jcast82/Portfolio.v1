from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# Projects route
@app.route("/projects")
def projects():
    return render_template("projects.html")

# About route
@app.route("/about")
def about():
    return render_template("about.html")

# Contact route with GET and POST handling
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # Extract and sanitize form data
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        errors = []

        # Basic validation
        if not name:
            errors.append("Name is required.")
        if not email or "@" not in email:
            errors.append("Valid email is required.")
        if not message:
            errors.append("Message cannot be empty.")

        if errors:
            return render_template("contact.html", errors=errors)

        # Prepare payload for Lambda
        payload = {
            "name": name,
            "email": email,
            "message": message
        }

        try:
            # Replace with your actual Lambda endpoint
            lambda_url = "https://cy32pm6vda.execute-api.us-east-2.amazonaws.com/contact"
            response = requests.post(lambda_url, json=payload)
            response.raise_for_status()
            return render_template("contact.html", success=True)
        except requests.RequestException as e:
            errors.append("Failed to send message. Please try again later.")
            return render_template("contact.html", errors=errors)

    # Default GET request
    return render_template("contact.html")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)