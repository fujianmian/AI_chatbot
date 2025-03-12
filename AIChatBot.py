import json
from difflib import get_close_matches
import tkinter as tk
from tkinter import scrolledtext

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.5)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None


def chat_bot(event, entry, response, knowledge_base):
    user_input = entry.get().strip()
    entry.delete(0, tk.END)

    if user_input.lower() == 'quit':
        root.destroy()
        return

    best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    if best_match:
        answer: str | None = get_answer_for_question(best_match, knowledge_base)
        if answer:
            response.config(state=tk.NORMAL)
            response.insert(tk.END, f'You: {user_input}\nHelloChat: {answer}\n\n')
            response.config(state=tk.DISABLED)
        else:
            response.config(state=tk.NORMAL)
            response.insert(tk.END, f'You: {user_input}\nHelloChat: I don\'t know the answer.\n\n')
            response.config(state=tk.DISABLED)
    else:
        response.config(state=tk.NORMAL)
        response.insert(tk.END, f'You: {user_input}\nHelloChat: I don\'t know the answer.\n\n')
        response.config(state=tk.DISABLED)

    response.see(tk.END)


if __name__ == "__main__":
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    root = tk.Tk()
    root.title("HelloChat")
    root.geometry("600x500")

    background_image = tk.PhotoImage(file="testbk.png")

    canvas = tk.Canvas(root, width=600, height=500)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

    hello_chat_label = tk.Label(root, text="HelloChat", font=("Arial", 20))
    hello_chat_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    response = scrolledtext.ScrolledText(root, width=60, height=15)
    response.place(relx=0.5, rely=0.35, anchor=tk.CENTER, width=580)

    entry = tk.Entry(root, width=40)
    entry.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
    entry.bind("<Return>", lambda event: chat_bot(event, entry, response, knowledge_base))

    ask_label = tk.Label(root, text="Ask me a question:", font=("Arial", 12), bg="white")
    ask_label.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

    button = tk.Button(root, text="Send", command=lambda: chat_bot(None, entry, response, knowledge_base), width=10, height=2)
    button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    root.mainloop()
