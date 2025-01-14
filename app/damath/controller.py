from flask import request, jsonify, session, render_template
from langchain_ollama.llms import OllamaLLM
from . import damath

# Global LLM instance
global_llm = None

@damath.route('/hello/')
@damath.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', person=name)

@damath.route('/init-llm', methods=['POST'])
def initialize_llm():
    try:
        global global_llm
        data = request.get_json()
        model_name = data.get('model', 'llama3.2')

        global_llm = OllamaLLM(model=model_name)

        return jsonify({
            'success': True,
            'message': f'LLM initialized with model: {model_name}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@damath.route('/ask', methods=['POST'])
def ask_llm():
    try:
        global global_llm
        if global_llm is None:
            return jsonify({
                'success': False,
                'error': 'LLM not initialized. Please call /init-llm first'
            }), 400

        # Get the prompt from request JSON
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({
                'success': False,
                'error': 'Please provide a prompt in the request body'
            }), 400

        prompt = data['prompt']
        response = global_llm.invoke(prompt)

        return jsonify({
            'success': True,
            'response': response
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
