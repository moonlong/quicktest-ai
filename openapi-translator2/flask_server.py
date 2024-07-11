import sys
import os
from translator import PDFTranslator, TranslationConfig
from utils import ArgumentParser, LOG

from flask import Flask, request, send_file, jsonify

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

TEMP_FILE_DIR = "flask_temp/"


@app.route('/translate', methods=['POST'])
def translate():
    try:
        input_file = request.files['input_file']
        source_language = request.form.get('source_language', 'English')
        target_language = request.form.get('target_language', 'Chinese')

        LOG.debug(f"[input_file]\n{input_file}")
        LOG.debug(f"[input_file.filename]\n{input_file.filename}")

        if input_file and input_file.filename:
            # 创建文件，存储在临时目录中
            input_file_path = TEMP_FILE_DIR + input_file.filename
            LOG.debug(f"[input_file_path]\n{input_file_path}")
            input_file.save(input_file_path)

            output_file_path = Translator.translate_pdf(input_file_path,
                                                        source_language=source_language,
                                                        target_language=target_language)

            output_file_path = os.getcwd() + "/" + output_file_path
            LOG.debug(output_file_path)

            return send_file(output_file_path, as_attachment=True)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


def initialize_translator():
    args = ArgumentParser().parse_arguments()
    config = TranslationConfig()
    config.initialize(args)

    global Translator
    Translator = PDFTranslator(config.model_name)


if __name__ == '__main__':
    initialize_translator()
    app.run(host='0.0.0.0', port=5000, debug=True)
