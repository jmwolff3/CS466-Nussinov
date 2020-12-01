from flask import Flask, render_template, request, jsonify
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config.from_object('config.DevConfig')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    from nussinov.nussinov import checkSequence, classicalNussinov, backtrace, structure_output
    sequence = request.values.get('sequence', None)
    if sequence is None:
        return jsonify({'success': False, 'response': 'Please enter a sequence.'})
    sequence = sequence.upper()
    if not checkSequence(sequence):
        return jsonify({'success': False, 'response': 'Your sequence contains invalid characters.'}) # return error that sequence is invalid
    solution_matrix = classicalNussinov(sequence)
    solution = []
    backtrace(sequence, solution_matrix, solution, 0, len(sequence)-1)
    optimal_structure = structure_output(sequence, solution)
    return jsonify({'success': True, 'matrix': solution_matrix.tolist(), 'sequence': sequence, 'solution': solution, 'optimal_structure': optimal_structure})

if __name__ == "__main__":
    app.run()