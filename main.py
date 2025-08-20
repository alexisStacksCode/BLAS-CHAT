from typing import Any

import gradio as gr
import gradio.themes

from modules.core import constants
from modules.core import shared
from modules import settings
from modules import lm_backend
from modules.ui import setting_components
from modules.ui import sidebar_left
from modules.ui import sidebar_right
from modules.ui import tab_chat
from modules.ui import tab_writer


if __name__ == "__main__":
    def on_demo_load_1():
        outputs: list[Any] = []
        for setting_component_value in shared.setting_component_values.values():
            outputs.append(setting_component_value)
        if len(outputs) == 1:
            return outputs[0]
        return outputs

    def on_demo_load_2(mirostat_mode: str):
        is_mirostat_enabled: bool = mirostat_mode != "Off"
        textbox_left_buttons: list[str] = [
            "upload",
        ]
        textbox_file_extensions: list[str] = constants.GENERIC_FILE_EXTENSIONS.copy()

        if shared.model_modalities["vision"]:
            textbox_file_extensions += constants.IMAGE_FILE_EXTENSIONS.copy()
        if shared.model_modalities["audio"]:
            textbox_left_buttons.append("microphone")
            textbox_file_extensions += constants.AUDIO_FILE_EXTENSIONS.copy()

        return (
            f"**Vision:** {shared.model_modalities["vision"]}",
            f"**Audio:** {shared.model_modalities["audio"]}",
            gr.update(visible=is_mirostat_enabled),
            gr.update(visible=is_mirostat_enabled),
            gr.update(sources=textbox_left_buttons, file_types=textbox_file_extensions)
        )

    settings.load()
    settings.save()

    with gr.Blocks(theme=gradio.themes.Origin(), analytics_enabled=False, title="BLAS-CHAT", css_paths="main.css") as demo:
        is_assistant_busy: gr.State = gr.State(False)

        sidebar_l: sidebar_left.Element = sidebar_left.Element()
        sidebar_r: sidebar_right.Element = sidebar_right.Element()

        with gr.Tabs():
            with gr.Tab("💬 Chat") as tab_1:
                chat_chatbot: gr.Chatbot = gr.Chatbot(
                    value=tab_chat.set_chatbot,
                    type="messages",
                    show_label=False,
                    editable="all",
                    sanitize_html=False,
                    examples=[
                        {"text": "Explain quantum computing in simple terms."},
                        {"text": "Got any creative ideas for a 10-year-old's birthday?"},
                        {"text": "How do I make a HTTP request in JavaScript?"},
                    ],
                    allow_tags=True,
                )
                chat_textbox: gr.MultimodalTextbox = gr.MultimodalTextbox(
                    sources="upload",
                    file_types=constants.GENERIC_FILE_EXTENSIONS,
                    file_count="multiple",
                    placeholder="Type a message...",
                    show_label=False,
                    interactive=True,
                )
                gr.Markdown("---")
                chat_system_prompt_text_area: setting_components.TextArea = setting_components.TextArea(
                    key="chat/system_prompt",
                    max_lines=7,
                    placeholder="You are a helpful assistant.",
                    label="System Prompt",
                    interactive=True,
                )
            with gr.Tab("📝 Writer") as tab_2:
                writer_text_area: gr.TextArea = gr.TextArea(
                    value=lambda: shared.writer_text,
                    lines=20,
                    label="Your Text Document",
                    interactive=True,
                )
                with gr.Row():
                    writer_generate_button: gr.Button = gr.Button(
                        value="Generate",
                        variant="primary",
                        interactive=True,
                    )
                    writer_clear_button: gr.Button = gr.Button(
                        value="Clear",
                        variant="secondary",
                        interactive=True,
                    )
                gr.Markdown("---")
                writer_max_tokens_slider: setting_components.Slider = setting_components.Slider(
                    key="writer/max_tokens",
                    default_value=128,
                    minimum=16.0,
                    maximum=512.0,
                    step=1.0,
                    label="Maximum Tokens Per Generation",
                    interactive=True,
                )

        sidebar_l.refresh_model_info_button.click(
            fn=sidebar_l.on_refresh_model_info_button_click,
            inputs=sidebar_l.port_number.instance,
            outputs=(
                sidebar_l.vision_status,
                sidebar_l.audio_status,
                sidebar_l.refresh_model_info_button,
                chat_textbox,
            ),
            show_progress="hidden",
        )

        chat_chatbot.retry(
            fn=tab_chat.on_chatbot_retry,
            outputs=chat_chatbot,
            show_progress="hidden",
        ).then(
            fn=lm_backend.mark_assistant_as_busy,
            outputs=(
                tab_1,
                tab_2,
                chat_textbox,
                writer_generate_button,
                is_assistant_busy,
            ),
            show_progress="hidden",
        ).then(
            fn=tab_chat.create_assistant_message,
            inputs=(  # type: ignore
                sidebar_l.port_number.instance,
                sidebar_l.stream_responses_checkbox.instance,
                sidebar_r.temperature_slider.instance,
                sidebar_r.top_k_slider.instance,
                sidebar_r.top_p_slider.instance,
                sidebar_r.min_p_slider.instance,
                sidebar_r.typical_p_slider.instance,
                sidebar_r.repetition_penalty_slider.instance,
                sidebar_r.repetition_penalty_range_slider.instance,
                sidebar_r.presence_penalty_slider.instance,
                sidebar_r.frequency_penalty_slider.instance,
                sidebar_r.mirostat_mode_dropdown.instance,
                sidebar_r.mirostat_tau_slider.instance,
                sidebar_r.mirostat_eta_slider.instance,
                sidebar_r.dry_base_slider.instance,
                sidebar_r.dry_multiplier_slider.instance,
                sidebar_r.dry_allowed_length_slider.instance,
                sidebar_r.dry_penalty_range_slider.instance,
                sidebar_r.xtc_threshold_slider.instance,
                sidebar_r.xtc_probability_slider.instance,
            ),
            outputs=chat_chatbot,
            show_progress="hidden",
        ).then(
            fn=lm_backend.mark_assistant_as_idle,
            outputs=(
                tab_1,
                tab_2,
                chat_textbox,
                writer_generate_button,
                is_assistant_busy,
            ),
            show_progress="hidden",
        )
        chat_chatbot.undo(
            fn=tab_chat.on_chatbot_undo,
            outputs=(
                chat_chatbot,
                chat_textbox,
            ),
            show_progress="hidden",
        )
        chat_chatbot.example_select(
            fn=tab_chat.on_chatbot_example_select,
            outputs=chat_textbox,
            show_progress="hidden",
        )
        chat_chatbot.clear(
            fn=tab_chat.on_chatbot_clear,
            inputs=is_assistant_busy,
            outputs=chat_chatbot,
            show_progress="hidden",
        )
        chat_textbox.submit(
            fn=tab_chat.create_user_message,
            inputs=(
                chat_textbox,
                chat_system_prompt_text_area.instance,  # type: ignore
                is_assistant_busy,
            ),
            outputs=(
                chat_chatbot,
                chat_textbox,
                is_assistant_busy,
            ),
            show_progress="hidden",
        ).success(
            fn=lm_backend.mark_assistant_as_busy,
            outputs=(
                tab_1,
                tab_2,
                chat_textbox,
                writer_generate_button,
                is_assistant_busy,
            ),
            show_progress="hidden",
        ).then(
            fn=tab_chat.create_assistant_message,
            inputs=(  # type: ignore
                sidebar_l.port_number.instance,
                sidebar_l.stream_responses_checkbox.instance,
                sidebar_r.temperature_slider.instance,
                sidebar_r.top_k_slider.instance,
                sidebar_r.top_p_slider.instance,
                sidebar_r.min_p_slider.instance,
                sidebar_r.typical_p_slider.instance,
                sidebar_r.repetition_penalty_slider.instance,
                sidebar_r.repetition_penalty_range_slider.instance,
                sidebar_r.presence_penalty_slider.instance,
                sidebar_r.frequency_penalty_slider.instance,
                sidebar_r.mirostat_mode_dropdown.instance,
                sidebar_r.mirostat_tau_slider.instance,
                sidebar_r.mirostat_eta_slider.instance,
                sidebar_r.dry_base_slider.instance,
                sidebar_r.dry_multiplier_slider.instance,
                sidebar_r.dry_allowed_length_slider.instance,
                sidebar_r.dry_penalty_range_slider.instance,
                sidebar_r.xtc_threshold_slider.instance,
                sidebar_r.xtc_probability_slider.instance,
            ),
            outputs=chat_chatbot,
            show_progress="hidden",
        ).then(
            fn=lm_backend.mark_assistant_as_idle,
            outputs=(
                tab_1,
                tab_2,
                chat_textbox,
                writer_generate_button,
                is_assistant_busy,
            ),
            show_progress="hidden",
        )
        chat_textbox.stop(
            fn=lm_backend.stop_assistant_task,
            inputs=is_assistant_busy,
            outputs=is_assistant_busy,
        )

        writer_generate_event = writer_generate_button.click(
            fn=tab_writer.on_generate_button_click,
            inputs=is_assistant_busy,
        )
        writer_generate_event.success(
            fn=lm_backend.mark_assistant_as_busy,
            outputs=(
                tab_1,
                tab_2,
                chat_textbox,
                writer_generate_button,
                is_assistant_busy,
            ),
            show_progress="hidden",
        ).then(
            fn=lambda: gr.update(interactive=False),
            outputs=writer_text_area,
            show_progress="hidden",
        ).then(
            fn=tab_writer.generate_text,
            inputs=(  # type: ignore
                writer_text_area,
                sidebar_l.port_number.instance,
                sidebar_l.stream_responses_checkbox.instance,
                sidebar_r.temperature_slider.instance,
                sidebar_r.top_k_slider.instance,
                sidebar_r.top_p_slider.instance,
                sidebar_r.min_p_slider.instance,
                sidebar_r.typical_p_slider.instance,
                sidebar_r.repetition_penalty_slider.instance,
                sidebar_r.repetition_penalty_range_slider.instance,
                sidebar_r.presence_penalty_slider.instance,
                sidebar_r.frequency_penalty_slider.instance,
                sidebar_r.mirostat_mode_dropdown.instance,
                sidebar_r.mirostat_tau_slider.instance,
                sidebar_r.mirostat_eta_slider.instance,
                sidebar_r.dry_base_slider.instance,
                sidebar_r.dry_multiplier_slider.instance,
                sidebar_r.dry_allowed_length_slider.instance,
                sidebar_r.dry_penalty_range_slider.instance,
                sidebar_r.xtc_threshold_slider.instance,
                sidebar_r.xtc_probability_slider.instance,
                writer_max_tokens_slider.instance,
            ),
            outputs=writer_text_area,
            show_progress="hidden",
        ).then(
            fn=lambda: gr.update(interactive=True),
            outputs=writer_text_area,
            show_progress="hidden",
        ).then(
            fn=lm_backend.mark_assistant_as_idle,
            outputs=(
                tab_1,
                tab_2,
                chat_textbox,
                writer_generate_button,
                is_assistant_busy,
            ),
            show_progress="hidden",
        )
        writer_generate_event.failure(
            fn=lm_backend.stop_assistant_task,
            inputs=is_assistant_busy,
            outputs=is_assistant_busy,
        )
        writer_clear_button.click(
            fn=tab_writer.on_clear_button_click,
            inputs=is_assistant_busy,
            outputs=writer_text_area,
            show_progress="hidden",
        )

        demo.load(
            fn=on_demo_load_1,
            outputs=shared.setting_components,
            show_progress="hidden",
        ).then(
            fn=on_demo_load_2,
            inputs=sidebar_r.mirostat_mode_dropdown.instance,
            outputs=(  # type: ignore
                sidebar_l.vision_status,
                sidebar_l.audio_status,
                sidebar_r.mirostat_tau_slider.instance,
                sidebar_r.mirostat_eta_slider.instance,
                chat_textbox,
            ),
            show_progress="hidden",
        )

    demo.launch(inbrowser=True, server_port=6969)
