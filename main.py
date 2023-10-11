import gradio as gr
from dynaconf import Dynaconf
from utils import DatasetCreator

settings = Dynaconf(
    settings_file="settings.yaml",
)

dcreator = DatasetCreator(
        settings.get('input_dir_path'),
        settings.get('output_dir_path'),
        settings.get('class_dict').to_dict()
    )

with gr.Blocks(title="Pose Annotator") as annot_window:
    class_dict = settings.get('class_dict').to_dict()
    disp_image = gr.Image(value=dcreator.iter_images_in_dir(), type="filepath", height=600)
    label_picker = gr.Radio(choices=list(class_dict.keys()), label="Image Label")

    # On Selecting Label
    label_picker.input(dcreator.label_and_save, inputs=[disp_image, label_picker], outputs=[disp_image, label_picker])

    # Change Image
    disp_image.change(dcreator.iter_images_in_dir, outputs=[disp_image])


if __name__ == "__main__":
    annot_window.launch()