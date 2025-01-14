from flask import Flask, render_template, request, session
import google.generativeai as genai

# Initialize the Generative AI model
genai.configure(api_key="AIzaSyDqzISVvI0fHukFDpx_UUkJ7Pj9XDynygA")
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for session management



# Define the homepage route
@app.route("/", methods=["GET", "POST"])
def chatbot():
    if "history" not in session:
        session["history"] = []

    history = session["history"]

    if request.method == "POST":
        if "clear_chat" in request.form:
            # Clear the chat history when "Clear Chat" is clicked
            session["history"] = []
            return render_template("chatbot.html", history=history)
        
        user_input = request.form.get("user_input")
        if user_input:
            # Format the input as per the rules
            rules = "i will give you the address text you have to give me the size of property the full postcode the location the phone number and the cost in a proper formatted way in each line and nothing else,the size of the room can also be ensuite, sharing with one person, maintain proper line breaks, here is the address text: "
            prompt = rules + user_input

            # Generate the response from the model
            try:
                response = model.generate_content(prompt)
                bot_reply = response.text
                bot_reply = bot_reply.replace("\n", "<br>")
            except Exception as e:
                bot_reply = f"Error: {e}"

            # Add the interaction to history
            history.append({"user": user_input, "bot": bot_reply})
            session["history"] = history

    return render_template("chatbot.html", history=history)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)