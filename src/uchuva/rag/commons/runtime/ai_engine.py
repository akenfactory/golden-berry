import openai

def generate_text(log, api_key, engine, prompt, commands = ""):
    try:
        """Genera texto con OpenAI."""
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model = engine,
            messages=[
                {"role": "system", "content": f"Tu eres un asistente virtual. {commands}"},
                {"role": "user", "content": prompt},
            ]
        )
        if response['choices'][0]['finish_reason'] == 'completed' or response['choices'][0]['finish_reason'] == 'stop':
            return (response['choices'][0]['message']['content'], response['usage'])
        else:
            log.error("Error en la respuesta de OpenAI: " + response['choices'][0]['finish_reason'])
            return (None, None)
    except Exception as e:
        log.error("Error en la respuesta de OpenAI: " + str(e))
        return (None, None)