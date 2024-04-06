from openai import OpenAI
import time

client = OpenAI(api_key="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")

assistant = client.beta.assistants.create(
    name = "Academic Ally",
    instructions = "You are a math tutor",
    tools = [{"type": "code_interpreter"}],
    model = "gpt-3.5-turbo",
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role = "user",
    content = input("User: "),
)

run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id = assistant.id,
    instructions="Address the user as Sam",
)

while run.status in ['queued', 'in_progress', 'cancelling']:
    time.sleep(1) # Wait for 1 second
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread.id)
        print(messages)
    else:
        print(run.status)

#testtt5