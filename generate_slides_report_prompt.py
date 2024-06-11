def generate_slides_report_prompt(image_urls):
    prompt = f"""
    You will receive images. They are part of a presentation. Your role is to give feedback
    based on criteria I will define.

    I am giving the base64 of each image and also a JSON that includes the URL of the image.
    ```
    {image_urls}
    ```

    Remember this, you will need to merge the image_url with the generated report later.
    You don't need to download images as I am giving you the base64 string directly.

    The slides are sorted in order; do not change the order of the slides as they are being presented.

    For each image, analyze:

    1. Category to which the slide belongs. Let's remember the parts of a presentation:
        1. Opening: Responsible for securing audience attention
        2. Body: Responsible for elaborating the whole topic
        3. Closing: Where you wrap up everything

    2. Title: It defines a short phrase of what the slide is about. Should be short and concise, like: Introduction, About Me, Closing, etc.

    3. Summary: Longer summary of what the slide is about. 50 words or less.

    4. To improve: 
    Actionable points about the slide.
    The feedback can be positive or negative, categorize it accordingly.
    Here are some good rules about presentations (by section):
    General rules:
    - If there is too much text (> 50 words), say: there are too many words and consider writing less.
    - Slides should have a max of 3 key ideas per slide. More than that, people won't remember.
    
    Opening:
    - Start with WHY:
        - What is this presentation about?
        - Why should people listen?
        - What will be the outcomes?

    Closing:
        - How is the body connected with the outcomes?

    5. For the output of this prompt, I want a JSON in the following format:

    [
      {{
        "title": "Introduction", 
        "image_url": "/0.jpg",
        "slideDetails": {{
          "description": "This slide introduces the presentation.",
          "feedback": [
            {{"id": 1, "content": "Feedback point 1 for Introduction", type:'positive'}},
            {{"id": 1, "content": "Feedback point 1 for Introduction", type:'negative'}},
          ],
          "category": "OPENING" // or BODY or CLOSING
        }}
      }}
    ]

    I want the output to be an array of objects as described and only that. No extra characters.
    """

    return prompt
