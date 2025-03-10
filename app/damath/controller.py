from flask import request, jsonify, session, render_template
from llmlangchain.langchainagent import LLMManager
from . import damath

# Global LLM instance
llm_manager = LLMManager()

@damath.route('/hello/')
@damath.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', person=name)

@damath.route('/init-llm', methods=['POST'])
def initialize_llm():
    try:
        data = request.get_json()
        model_name = data.get('model', 'llama3.2')

        success = llm_manager.initialize_llm(model_name)
        if not success:
            return jsonify({
                'success': False,
                'error': 'Failed to initialize LLM'
            }), 500

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
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({
                'success': False,
                'error': 'Please provide a prompt in the request body'
            }), 400

        prompt = data['prompt']
        result = llm_manager.get_response(prompt)
        response = result
        print(result)

        return jsonify({
            'success': True,
            'response': response
        })
    except ValueError as ve:
        return jsonify({
            'success': False,
            'error': str(ve)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500




@damath.route('/bstate_to_valid', methods=['POST'])
def boardstate_to_validmoves():
    try:
        data = request.get_json()
        if not data or 'board_state' not in data:
            return jsonify({
                'success': False,
                'error': 'Please provide a board_state in the request body'
            }), 400

        board_state = data['board_state']
        response = llm_manager.board_to_valid(board_state)
        print(response)
        response = response.content

        return response

        # return jsonify({
        #     'success': True,
        #     'response': response
        # })
    except ValueError as ve:
        return jsonify({
            'success': False,
            'error': str(ve)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500