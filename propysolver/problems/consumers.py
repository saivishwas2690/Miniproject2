from channels.generic.websocket import WebsocketConsumer
from channels.consumer import SyncConsumer, AsyncConsumer
from anthropic import Anthropic
from .prompts import category_template, template1, template2, template3
import json, time, re, os
from .models import *
from asgiref.sync import sync_to_async
from django.conf import settings

class ChatConsumer(AsyncConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = []
        self.code_number = 0

    async def llm_response(self, user_input):
        client = Anthropic(api_key="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")
        MODEL_NAME = "claude-3-sonnet-20240229"

        conversation = ""
        for x in self.messages:
            conversation += x['role'] + ": "
            conversation += x['content']

        response = client.messages.create(
            model="claude-instant-1.2",
            max_tokens=1,
            temperature=0.0,
            messages=[
                {
                    "role": "user",
                    "content": category_template + conversation
                }
            ]
        ).content[0].text
        category = response

        time.sleep(2)
        print("mode: ", category)
        if category == "1":
            self.messages.append({'role': 'user', 'content': template1 + user_input})
        elif category == "2":
            self.messages.append({'role': 'user', 'content': template2 + user_input})
        elif category == "3":
            self.messages.append({'role': 'user', 'content': template3 + user_input})
        else:
            self.messages.append({'role': 'user', 'content': template2 + user_input})

        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=1024,
            temperature=1,
            messages=self.messages
        ).content[0].text

        self.messages.append({'role': 'assistant', 'content': response})
        return response

    async def extract_text_and_code(self, response):
        pattern = r"```(.*?)```"
        segments = re.split(pattern, response, flags=re.DOTALL)
        cleaned_segments = [segment.strip() for segment in segments]
        result = []
        is_code = ""
        for segment in cleaned_segments:
            if segment.startswith('python'):
                is_code = 'python'
            elif segment.startswith('javascript'):
                is_code = 'javascript'
            elif segment.startswith('java'):
                is_code = 'java'
            elif segment.startswith('cpp'):
                is_code = 'cpp'
            elif segment.startswith('c'):
                is_code = 'c'
            else :
                is_code = ""
            if is_code != "":
                self.code_number += 1
            result.append([segment.strip(is_code).strip(), is_code,self.code_number])
        return result

    async def websocket_connect(self, event):
        print("websocket connected...")
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_disconnect(self, event):
        print("websocket disconnected...")

    async def websocket_receive(self, event):
        data = json.loads(event['text'])
        print("message received from client...", data)
        print(data["type"])
        if(data["type"] == "query"):
            message = data["prompt"]
            response = await self.llm_response(message)
        elif(data["type"] == "hint"):
            problmeid = data["problmeid"]
            code = data["code"]
            problem = await sync_to_async(Problem.objects.get)(pk=problmeid)
            problem_statment = problem.problem_statement
            input_format = problem.input_format
            output_format = problem.output_format
            hint = problem.hint
            prompt = "this is the question i am trying to solve: " + problem_statment 
            prompt += " this is the input format: " + input_format
            prompt += " this is the output format: " + output_format
            prompt += " this is the hint from the database: " + hint
            if code != "":
                prompt += " this is the code i have written: \n ```" + code + "\n ```"

            prompt += "do not solve the problem, but give hints to the user on how to solve the problem. If you write any program, wrap programs with ```  ```"
            response = await self.llm_response(prompt)

        extracted_response = await self.extract_text_and_code(response)
        data = {}
        for i, block in enumerate(extracted_response):
            data[f'block{i + 1}'] = {
                'text': block[0],
                'is_code': block[1],
                'code_number': block[2]
            }
        await self.send({
            'type': 'websocket.send',
            'text': json.dumps(data)
        })





