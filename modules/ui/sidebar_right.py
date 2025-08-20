import gradio as gr

from modules.core import constants
from modules.ui import setting_components


class Element:
    def __init__(self) -> None:
        with gr.Sidebar(position="right"):
            gr.HTML(f"""
            <h1 style="text-align: right;">
                Version {constants.VERSION}
            </h1>
            """)
            with gr.Accordion("Samplers"):
                self.temperature_slider: setting_components.Slider = setting_components.Slider(
                    key="language_model/temperature",
                    default_value=constants.DEFAULT_SETTINGS["language_model"]["temperature"],
                    minimum=0.0,
                    maximum=2.0,
                    step=0.01,
                    label="Temperature",
                    interactive=True,
                )
                self.top_k_slider: setting_components.Slider = setting_components.Slider(
                    key="language_model/top_k",
                    default_value=constants.DEFAULT_SETTINGS["language_model"]["top_k"],
                    minimum=0.0,
                    maximum=100.0,
                    step=1.0,
                    precision=0,
                    label="Top-K",
                    interactive=True,
                )
                self.top_p_slider: setting_components.Slider = setting_components.Slider(
                    key="language_model/top_p",
                    default_value=constants.DEFAULT_SETTINGS["language_model"]["top_p"],
                    minimum=0.0,
                    maximum=1.0,
                    step=0.01,
                    label="Top-P",
                    interactive=True,
                )
                self.min_p_slider: setting_components.Slider = setting_components.Slider(
                    key="language_model/min_p",
                    default_value=constants.DEFAULT_SETTINGS["language_model"]["min_p"],
                    minimum=0.0,
                    maximum=1.0,
                    step=0.01,
                    label="Min-P",
                    interactive=True,
                )
                self.typical_p_slider: setting_components.Slider = setting_components.Slider(
                    key="language_model/typical_p",
                    default_value=constants.DEFAULT_SETTINGS["language_model"]["typical_p"],
                    minimum=0.0,
                    maximum=1.0,
                    step=0.01,
                    label="Typical-P",
                    interactive=True,
                )
                self.repetition_penalty_slider: setting_components.Slider = setting_components.Slider(
                    key="language_model/repetition_penalty",
                    default_value=constants.DEFAULT_SETTINGS["language_model"]["repetition_penalty"],
                    minimum=1.0,
                    maximum=2.0,
                    step=0.01,
                    label="Repetition Penalty",
                    interactive=True,
                )
                self.repetition_penalty_range_slider: setting_components.Slider = setting_components.Slider(
                    key="language_model/repetition_penalty_range",
                    default_value=constants.DEFAULT_SETTINGS["language_model"]["repetition_penalty_range"],
                    minimum=-1.0,
                    maximum=256.0,
                    step=1.0,
                    precision=0,
                    label="Rep. Penalty Range",
                    info="`-1` = context size",
                    interactive=True,
                )
                self.presence_penalty_slider: setting_components.Slider = setting_components.Slider(
                    key="language_model/presence_penalty",
                    default_value=constants.DEFAULT_SETTINGS["language_model"]["presence_penalty"],
                    minimum=-2.0,
                    maximum=2.0,
                    step=0.01,
                    label="Presence Penalty",
                    interactive=True,
                )
                self.frequency_penalty_slider: setting_components.Slider = setting_components.Slider(
                    key="language_model/frequency_penalty",
                    default_value=constants.DEFAULT_SETTINGS["language_model"]["frequency_penalty"],
                    minimum=-2.0,
                    maximum=2.0,
                    step=0.01,
                    label="Frequency Penalty",
                    interactive=True,
                )
            with gr.Accordion("Mirostat"):
                self.mirostat_mode_dropdown: setting_components.Dropdown = setting_components.Dropdown(
                    key="language_model/mirostat_mode",
                    default_value=constants.DEFAULT_SETTINGS["language_model"]["mirostat_mode"],
                    choices=(
                        "Off",
                        "Version 1.0",
                        "Version 2.0",
                    ),
                    label="Mode",
                    interactive=True,
                )
                self.mirostat_tau_slider: setting_components.Slider = setting_components.Slider(
                    key="language_model/mirostat_tau",
                    default_value=constants.DEFAULT_SETTINGS["language_model"]["mirostat_tau"],
                    minimum=0.0,
                    maximum=30.0,
                    step=0.01,
                    label="Tau",
                    interactive=True,
                    visible=False,
                )
                self.mirostat_eta_slider: setting_components.Slider = setting_components.Slider(
                    key="language_model/mirostat_eta",
                    default_value=constants.DEFAULT_SETTINGS["language_model"]["mirostat_eta"],
                    minimum=0.0,
                    maximum=10.0,
                    step=0.01,
                    label="Eta",
                    interactive=True,
                    visible=False,
                )
            with gr.Accordion("Don't Repeat Yourself (DRY)"):
                self.dry_base_slider: setting_components.Slider = setting_components.Slider(
                    key="language_model/dry_base",
                    default_value=constants.DEFAULT_SETTINGS["language_model"]["dry_base"],
                    minimum=0.0,
                    maximum=8.0,
                    step=0.01,
                    label="Base",
                    interactive=True,
                )
                self.dry_multiplier_slider: setting_components.Slider = setting_components.Slider(
                    key="language_model/dry_multiplier",
                    default_value=constants.DEFAULT_SETTINGS["language_model"]["dry_multiplier"],
                    minimum=0.0,
                    maximum=100.0,
                    step=0.01,
                    label="Multiplier",
                    interactive=True,
                )
                self.dry_allowed_length_slider: setting_components.Slider = setting_components.Slider(
                    key="language_model/dry_allowed_length",
                    default_value=constants.DEFAULT_SETTINGS["language_model"]["dry_allowed_length"],
                    minimum=0.0,
                    maximum=100.0,
                    step=1.0,
                    precision=0,
                    label="Allowed Length",
                    interactive=True,
                )
                self.dry_penalty_range_slider: setting_components.Slider = setting_components.Slider(
                    key="language_model/dry_penalty_range",
                    default_value=constants.DEFAULT_SETTINGS["language_model"]["dry_penalty_range"],
                    minimum=-1.0,
                    maximum=256.0,
                    step=1.0,
                    precision=0,
                    label="Penalty Range",
                    info="`-1` = context size",
                    interactive=True,
                )
            with gr.Accordion("Exclude Top Choices (XTC)"):
                self.xtc_threshold_slider: setting_components.Slider = setting_components.Slider(
                    key="language_model/xtc_threshold",
                    default_value=constants.DEFAULT_SETTINGS["language_model"]["xtc_threshold"],
                    minimum=0.0,
                    maximum=1.0,
                    step=0.01,
                    label="Threshold",
                    interactive=True,
                )
                self.xtc_probability_slider: setting_components.Slider = setting_components.Slider(
                    key="language_model/xtc_probability",
                    value=constants.DEFAULT_SETTINGS["language_model"]["xtc_probability"],
                    minimum=0.0,
                    maximum=1.0,
                    step=0.01,
                    label="Probability",
                    interactive=True,
                )
            self.reset_button: gr.Button = gr.Button(
                value="Reset to Defaults",
                variant="stop",
                interactive=True,
            )

            self.mirostat_mode_dropdown.event.then(
                fn=lambda value: (gr.update(visible=value != "Off"), gr.update(visible=value != "Off")),  # type: ignore
                inputs=self.mirostat_mode_dropdown.instance,
                outputs=(
                    self.mirostat_tau_slider.instance,
                    self.mirostat_eta_slider.instance,
                ),
                show_progress="hidden",
            )
            self.reset_button.click(
                fn=lambda: (
                    constants.DEFAULT_SETTINGS["language_model"]["temperature"],
                    constants.DEFAULT_SETTINGS["language_model"]["top_k"],
                    constants.DEFAULT_SETTINGS["language_model"]["top_p"],
                    constants.DEFAULT_SETTINGS["language_model"]["min_p"],
                    constants.DEFAULT_SETTINGS["language_model"]["typical_p"],
                    constants.DEFAULT_SETTINGS["language_model"]["repetition_penalty"],
                    constants.DEFAULT_SETTINGS["language_model"]["repetition_penalty_range"],
                    constants.DEFAULT_SETTINGS["language_model"]["presence_penalty"],
                    constants.DEFAULT_SETTINGS["language_model"]["frequency_penalty"],
                    constants.DEFAULT_SETTINGS["language_model"]["mirostat_mode"],
                    constants.DEFAULT_SETTINGS["language_model"]["mirostat_tau"],
                    constants.DEFAULT_SETTINGS["language_model"]["mirostat_eta"],
                    constants.DEFAULT_SETTINGS["language_model"]["dry_base"],
                    constants.DEFAULT_SETTINGS["language_model"]["dry_multiplier"],
                    constants.DEFAULT_SETTINGS["language_model"]["dry_allowed_length"],
                    constants.DEFAULT_SETTINGS["language_model"]["dry_penalty_range"],
                    constants.DEFAULT_SETTINGS["language_model"]["xtc_threshold"],
                    constants.DEFAULT_SETTINGS["language_model"]["xtc_probability"],
                ),
                outputs=(  # type: ignore
                    self.temperature_slider.instance,
                    self.top_k_slider.instance,
                    self.top_p_slider.instance,
                    self.min_p_slider.instance,
                    self.typical_p_slider.instance,
                    self.repetition_penalty_slider.instance,
                    self.repetition_penalty_range_slider.instance,
                    self.presence_penalty_slider.instance,
                    self.frequency_penalty_slider.instance,
                    self.mirostat_mode_dropdown.instance,
                    self.mirostat_tau_slider.instance,
                    self.mirostat_eta_slider.instance,
                    self.dry_base_slider.instance,
                    self.dry_multiplier_slider.instance,
                    self.dry_allowed_length_slider.instance,
                    self.dry_penalty_range_slider.instance,
                    self.xtc_threshold_slider.instance,
                    self.xtc_probability_slider.instance,
                ),
                show_progress="hidden",
            )
