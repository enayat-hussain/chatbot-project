import gradio as gr
from chatbot import chat_with_groq
import time


def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)


def respond(history):
    # Convert history to messages format for chat_with_groq
    messages = []
    for msg in history:
        if isinstance(msg, dict):
            messages.append({"role": msg["role"], "content": msg["content"]})

    # Build prompt
    prompt = "\n".join(
        f"{msg['role'].capitalize()}: {msg['content']}"
        for msg in messages
    )

    # Get bot response
    bot_reply = chat_with_groq(prompt)

    # Stream the response
    history.append({"role": "assistant", "content": ""})
    for character in bot_reply:
        history[-1]["content"] += character
        time.sleep(0.02)
        yield history


def add_message(history, message):
    if message.strip():
        history.append({"role": "user", "content": message})
    return history, ""


def clear_chat():
    return [], ""


# Create the interface
with gr.Blocks() as demo:
    gr.Markdown("# Welcome to Mini Chatbot 🤖")
    gr.Markdown("Chat with an AI assistant powered by GroqAI")

    chatbot = gr.Chatbot(
        elem_id="chatbot",
        type="messages",
        height=500
    )

    with gr.Row():
        chat_input = gr.Textbox(
            placeholder="Type your message here...",
            show_label=False,
            container=False,
            scale=8
        )
        submit_btn = gr.Button("Send", variant="primary", scale=1)
        clear_btn = gr.Button("Clear", variant="secondary", scale=1)

    # Submit on Enter
    chat_msg = chat_input.submit(
        add_message,
        [chatbot, chat_input],
        [chatbot, chat_input],
        queue=False
    ).then(
        respond,
        chatbot,
        chatbot,
        api_name="bot_response"
    )

    # Submit on button click
    submit_btn.click(
        add_message,
        [chatbot, chat_input],
        [chatbot, chat_input],
        queue=False
    ).then(
        respond,
        chatbot,
        chatbot
    )

    # Clear chat
    clear_btn.click(
        clear_chat,
        inputs=None,
        outputs=[chatbot, chat_input]
    )

    # Like/dislike functionality
    chatbot.like(print_like_dislike, None, None)

if __name__ == "__main__":
    demo.launch()