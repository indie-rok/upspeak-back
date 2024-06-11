import os
import base64
from flask import request, jsonify
from openai import OpenAI
from app import app, logger, download_from_s3
from generate_slides_report_prompt import generate_slides_report_prompt

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_chat_completion(client, model_name, image_messages, selected_topic, slides):
    messages = [
        {"role": "system", "content": "You are a world-class speaker giving feedback on presentation slides"},
        {"role": "user", "content": generate_slides_report_prompt(slides)},
        {"role": "user", "content": image_messages}
    ]
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.0,
        )
        return response
    except Exception as e:
        logger.error("Error creating chat completion: %s", e)
        raise

@app.route('/slides_report', methods=['POST'])
def slides_report():
    try:
        data = request.get_json()

        selected_topic = data.get('selected_topic')
        slides = data.get('slides')

        if not selected_topic or not slides:
            logger.error("Validation error: 'selected_topic' or 'slides' missing")
            return jsonify({"error": "'selected_topic' and 'slides' are required"}), 400

        image_messages = []

        logger.info("Converting images to base64")

        for image in slides:
            try:
                image_temp_path = download_from_s3(image["url"])
                with open(image_temp_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                    image_messages.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    })
            except Exception as e:
                logger.error("Error processing image %s: %s", image["url"], e)
                return jsonify({"error": "Image processing error"}), 500

        logger.info("Sending images to OpenAI")

        try:
            response = create_chat_completion(client, 'gpt-4o', image_messages, selected_topic, slides)
            logger.info("Tokens used: %s", response.usage.total_tokens)
            return jsonify(response.choices[0].message.content)
        except Exception as e:
            logger.error("Error in OpenAI response: %s", e)
            return jsonify({"error": "OpenAI API error"}), 500

    except Exception as e:
        logger.error("Server error: %s", e)
        return jsonify({"error": "Server Error"}), 500

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"working": True})
