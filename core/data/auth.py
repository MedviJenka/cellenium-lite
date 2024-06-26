class Authorization:

    TENANT_ID = ""
    TOKEN = ""
    HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": TOKEN
    }


a = {'id': 'chatcmpl-9eN53GrwI2Km7KslcCt11uY4C5Nlo', 'object': 'chat.completion', 'created': 1719408869, 'model': 'gpt-4o-2024-05-13', 'choices': [{'index': 0, 'message': {'role': 'assistant', 'content': 'Passed'}, 'logprobs': None, 'finish_reason': 'stop'}], 'usage': {'prompt_tokens': 894, 'completion_tokens': 1, 'total_tokens': 895}, 'system_fingerprint': 'fp_4008e3b719'}
print(a['choices'][0]['message']['content'])
