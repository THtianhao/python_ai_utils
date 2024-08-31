def get_message_by_history(system, history, first_is_me, is_history_format=False):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    if is_history_format:
        for i in history:
            messages.append({"role":i.role, "content": i.content})
        return messages
    for index, i in enumerate(history):
        is_me = index % 2 == 0 if first_is_me else index % 2 == 1
        if is_me:
            messages.append({"role": "user", "content": i})
        else:
            messages.append({"role": "assistant", "content": i})
    return messages
