from typing import Any

import gradio as gr


setting_components: list[gr.Component] = []
setting_component_values: dict[int, Any] = {}
model_modalities: dict[str, bool] = {
    "vision": False,
    "audio": False,
}
chat_history: list[gr.ChatMessage] = []
writer_text: str = ""
assistant_task: Any = None
