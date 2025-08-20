from typing import Any
import json

import gradio as gr
import asyncio
import httpx

from modules.core import constants
from modules.core import shared
from modules import lm_backend


async def generate_text(prompt: str, port: int, stream_responses: bool, temperature: float, top_k: int, top_p: float, min_p: float, typical_p: float, repetition_penalty: float, repetition_penalty_range: int, presence_penalty: float, frequency_penalty: float, mirostat_mode: str, mirostat_tau: float, mirostat_eta: float, dry_base: float, dry_multiplier: float, dry_allowed_length: int, dry_penalty_range: int, xtc_threshold: float, xtc_probability: float, max_tokens: int):
    if not await lm_backend.check_server_health(port):
        return

    payload: dict[str, Any] = {
        "prompt": prompt,
        "n_predict": max_tokens,
    }
    payload = lm_backend.create_payload(payload, stream_responses, temperature, top_k, top_p, min_p, typical_p, repetition_penalty, repetition_penalty_range, presence_penalty, frequency_penalty, mirostat_mode, mirostat_tau, mirostat_eta, dry_base, dry_multiplier, dry_allowed_length, dry_penalty_range, xtc_threshold, xtc_probability)

    shared.writer_text = prompt
    async with httpx.AsyncClient() as client:
        # Server-specific error messages aren't really needed here as this is intended
        # to enable users to write stories or mess around.
        try:
            if not payload["stream"]:
                shared.assistant_task = asyncio.create_task(client.request("POST", f"http://localhost:{port}/completion", json=payload, timeout=None))
                response: httpx.Response = await shared.assistant_task
                response_data: dict[str, Any] = response.json()
                if "error" not in response_data:
                    shared.writer_text += response_data["content"]
            else:
                shared.assistant_task = 0
                async with client.stream("POST", f"http://localhost:{port}/completion", json=payload, timeout=None) as response:
                    async for line in response.aiter_lines():
                        if shared.assistant_task is None:  # type: ignore
                            break

                        if line.startswith("data: "):
                            chunk_text: str = json.loads(line[6:])["content"]
                            shared.writer_text += chunk_text
                            yield shared.writer_text
        except httpx.ConnectError:
            lm_backend.issue_connection_warning(port)
        except asyncio.CancelledError:
            pass
        except:
            gr.Warning(constants.WARNING_GENERIC)
    yield shared.writer_text


def on_generate_button_click(is_assistant_busy: bool):
    if is_assistant_busy:
        raise gr.Error(visible=False, print_exception=False)


def on_clear_button_click(is_assistant_busy: bool):
    if not is_assistant_busy:
        shared.writer_text = ""
    return shared.writer_text
