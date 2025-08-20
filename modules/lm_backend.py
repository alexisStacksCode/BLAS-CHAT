from typing import Any

import gradio as gr
import httpx

from modules.core import shared


def mark_assistant_as_idle():
    return (
        gr.update(interactive=True),
        gr.update(interactive=True),
        gr.update(stop_btn=False),
        gr.update(value="Generate", variant="primary"),
        False,
    )


def mark_assistant_as_busy():
    return (
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(stop_btn=True),
        gr.update(value="Stop", variant="stop"),
        True,
    )


def stop_assistant_task(is_assistant_busy: bool):
    if is_assistant_busy and shared.assistant_task is not None:
        if not isinstance(shared.assistant_task, int):
            shared.assistant_task.cancel()
        shared.assistant_task = None
        return False
    return is_assistant_busy


def create_payload(payload: dict[str, Any], stream_responses: bool, temperature: float, top_k: int, top_p: float, min_p: float, typical_p: float, repetition_penalty: float, repetition_penalty_range: int, presence_penalty: float, frequency_penalty: float, mirostat_mode: str, mirostat_tau: float, mirostat_eta: float, dry_base: float, dry_multiplier: float, dry_allowed_length: int, dry_penalty_range: int, xtc_threshold: float, xtc_probability: float) -> dict[str, Any]:
    def mirostat_mode_to_int(mirostat_mode: str) -> int:
        match mirostat_mode:
            case "Off":
                return 0
            case "Version 1.0":
                return 1
            case "Version 2.0":
                return 2
            case _:
                raise ValueError

    payload.update({
        "stream": stream_responses,
        "temperature": temperature,
        "top_k": top_k,
        "top_p": top_p,
        "min_p": min_p,
        "typical_p": typical_p,
        "repeat_penalty": repetition_penalty,
        "repeat_last_n": repetition_penalty_range,
        "presence_penalty": presence_penalty,
        "frequency_penalty": frequency_penalty,
        "mirostat": mirostat_mode_to_int(mirostat_mode),
        "mirostat_tau": mirostat_tau,
        "mirostat_eta": mirostat_eta,
        "dry_base": dry_base,
        "dry_multiplier": dry_multiplier,
        "dry_allowed_length": dry_allowed_length,
        "dry_penalty_last_n": dry_penalty_range,
        "xtc_threshold": xtc_threshold,
        "xtc_probability": xtc_probability,
    })
    return payload


async def check_server_health(port: int) -> bool:
    async with httpx.AsyncClient() as client:
        try:
            response: httpx.Response = await client.request("GET", f"http://localhost:{port}/health")
            if response.status_code != 200:
                issue_connection_warning(port)
                return False
        except httpx.ConnectError:
            issue_connection_warning(port)
            return False
    return True


def issue_connection_warning(port: int) -> None:
    gr.Warning(f"Could not connect to language model server at port {port}.")
