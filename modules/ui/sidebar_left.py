from typing import Any

import gradio as gr
import asyncio
import httpx

from modules.core import constants
from modules.core import shared
from modules import lm_backend
from modules.ui import setting_components


class Element:
    def __init__(self) -> None:
        with gr.Sidebar(position="left"):
            gr.HTML("""
            <h1 style="text-align: left;">
                BLAS-CHAT
            </h1>
            """)
            with gr.Accordion("Server"):
                self.port_number: setting_components.Number = setting_components.Number(
                    key="language_model/port",
                    default_value=constants.DEFAULT_SETTINGS["language_model"]["port"],
                    label="Port",
                    placeholder="8080",
                    interactive=True,
                    precision=0,
                    minimum=0.0,
                    maximum=65535.0,
                )
                gr.Markdown("---")
                self.vision_status: gr.Markdown = gr.Markdown("**Vision:** False")
                self.audio_status: gr.Markdown = gr.Markdown("**Audio:** False")
                self.refresh_model_info_button: gr.Button = gr.Button(
                    value="Refresh Model Info",
                    variant="primary",
                    interactive=True,
                )
            with gr.Accordion("Responses"):
                self.stream_responses_checkbox: setting_components.Checkbox = setting_components.Checkbox(
                    key="language_model/stream_responses",
                    default_value=constants.DEFAULT_SETTINGS["language_model"]["stream_responses"],
                    label="Streaming",
                    interactive=True,
                )

    async def on_refresh_model_info_button_click(self, port: int):
        left_buttons: list[str] = [
            "upload",
        ]
        file_extensions: list[str] = constants.GENERIC_FILE_EXTENSIONS.copy()

        yield (
            gr.update(),
            gr.update(),
            gr.update(value="Refreshing...", interactive=False),
            gr.update(),
        )
        async with httpx.AsyncClient() as client:
            try:
                task = asyncio.create_task(client.request("GET", f"http://localhost:{port}/props"))
                response: httpx.Response = await task
                response_data: dict[str, Any] = response.json()

                shared.model_modalities["vision"] = response_data["modalities"]["vision"]
                shared.model_modalities["audio"] = response_data["modalities"]["audio"]

                if shared.model_modalities["vision"]:
                    file_extensions += constants.IMAGE_FILE_EXTENSIONS.copy()
                if shared.model_modalities["audio"]:
                    left_buttons.append("microphone")
                    file_extensions += constants.AUDIO_FILE_EXTENSIONS.copy()
            except httpx.ConnectError:
                lm_backend.issue_connection_warning(port)
        yield (
            f"**Vision:** {shared.model_modalities["vision"]}",
            f"**Audio:** {shared.model_modalities["audio"]}",
            gr.update(value="Refresh Model Info", interactive=True),
            gr.update(sources=left_buttons, file_types=file_extensions),
        )
