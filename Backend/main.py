import openai
from config_loader import load_api_key, save_api_key
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


openai.api_key = load_api_key()
if not openai.api_key:
    print('No OpenAI API key found. POST to /set_api_key to configure.')

app = FastAPI(title='AI Code Assistant')

class CodeRequest(BaseModel):
    language: str
    code: str

class APIKeyRequest(BaseModel):
    api_key: str


@app.post('/explain_code')
def explain_code(request: CodeRequest):
    if not request.code:
        raise HTTPException(status_code=400, detail='Code snippet required')
    if not openai.api_key:
        raise HTTPException(status_code=500, detail='OpenAI API key not set')

    prompt = f'Explain this {request.language} code in simple terms:\n```{request.language}\n{request.code}\n```'
    try:
        response = openai.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': 'You are a helpful AI that explains code'},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.3
        )
        explanation = response.choices[0].message.content
        return {'explanation': explanation}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



@app.post('/set_api_key')
def set_api_key(request: APIKeyRequest):
    save_api_key(request.api_key)
    openai.api_key = request.api_key
    return {'message': 'API key saved successfully'}

@app.post('/get_api_key')
def get_api_key():
    key = load_api_key()
    return {'api_key': key}