"""
bgremover web interface, running locally.

Usage (with the virtual environment activated):
    python app.py

Your browser opens on http://127.0.0.1:7860.
Everything runs on your computer: no image is sent over the internet.
"""

import gradio as gr

# Reuse the engine from remove_bg.py: the interface contains no
# background removal logic, it only calls the engine.
from remove_bg import DEFAULT_MODEL, MODELS, remove_background


def process(image, model_name, single_subject):
    """Called by Gradio every time the button is clicked."""
    if image is None:
        # gr.Warning shows a small alert in the page.
        gr.Warning("Please add an image first.")
        return None
    return remove_background(image, model_name, single_subject)


# gr.Blocks lets us place the components wherever we want on the page.
with gr.Blocks(title="bgremover") as app:
    gr.Markdown(
        "# bgremover\n"
        "Remove the background from any image. Everything runs on your computer."
    )

    # Row = side-by-side components: original on the left, result on the right.
    with gr.Row():
        # type="pil": Gradio hands us a Pillow image,
        # which is exactly what remove_background() expects.
        input_image = gr.Image(label="Original image", type="pil")
        # format="png" keeps the transparency when downloading.
        output_image = gr.Image(label="Result", type="pil", format="png")

    with gr.Row():
        model = gr.Dropdown(
            choices=list(MODELS.keys()),
            value=DEFAULT_MODEL,
            label="Model",
            info="The first use of a model downloads it (may take a few minutes).",
        )
        single_subject = gr.Checkbox(
            label="Single subject",
            info="Keep only the largest object (removes stray text, logos...).",
        )

    button = gr.Button("Remove background", variant="primary")

    # Wire everything together: on click, call process() with the 3 inputs
    # and display what it returns in output_image.
    button.click(process, inputs=[input_image, model, single_subject], outputs=output_image)


if __name__ == "__main__":
    # launch() starts a small web server on your computer
    # and opens the page in your browser.
    app.launch(inbrowser=True)
