from typing import Any
import os
import json
import base64

import gradio as gr
import asyncio
import httpx

from modules.core import constants
from modules.core import shared
from modules import lm_backend


def set_chatbot():
    rendered_history: list[gr.MessageDict] = []
    for message in shared.chat_history:
        rendered_history.append({
            "role": message.role,
            "content": message.content,  # type: ignore
            "metadata": message.metadata,
            "options": message.options,
        })
    return rendered_history


def on_chatbot_retry():
    shared.chat_history.pop()
    return shared.chat_history


def on_chatbot_undo(undo_data: gr.UndoData):
    __delete_last_exchange()
    return (
        shared.chat_history,
        undo_data.value,
    )


def on_chatbot_example_select(select_data: gr.SelectData):
    return select_data.value


def on_chatbot_clear(is_assistant_busy: bool):
    if not is_assistant_busy:
        shared.chat_history.clear()
    return shared.chat_history


def create_user_message(prompt: dict[str, Any], system_prompt: str, is_assistant_busy: bool):
    if is_assistant_busy:
        raise gr.Error(visible=False, print_exception=False)

    if prompt["text"].rstrip() == "" and len(prompt["files"]) == 0:
        raise gr.Error("Your message cannot be empty.", print_exception=False)

    if len(prompt["files"]) > 3:
        raise gr.Error("You cannot send more than 3 files.", print_exception=False)

    if len(shared.chat_history) == 0:
        shared.chat_history.append(gr.ChatMessage(system_prompt, "system"))
    else:
        shared.chat_history[0].content = system_prompt

    for file_path in prompt["files"]:
        shared.chat_history.append(gr.ChatMessage(gr.FileData(path=file_path, orig_name=os.path.basename(file_path)), "user"))
    shared.chat_history.append(gr.ChatMessage(prompt["text"], "user"))

    return (
        shared.chat_history,
        "",
        True,
    )


async def create_assistant_message(port: int, stream_responses: bool, temperature: float, top_k: int, top_p: float, min_p: float, typical_p: float, repetition_penalty: float, repetition_penalty_range: int, presence_penalty: float, frequency_penalty: float, mirostat_mode: str, mirostat_tau: float, mirostat_eta: float, dry_base: float, dry_multiplier: float, dry_allowed_length: int, dry_penalty_range: int, xtc_threshold: float, xtc_probability: float):
    shared.chat_history.append(gr.ChatMessage("", "assistant"))
    yield shared.chat_history

    if not await lm_backend.check_server_health(port):
        __delete_last_exchange()
        yield shared.chat_history
        return

    messages: list[dict[str, Any]] = []
    for message in shared.chat_history:
        if isinstance(message.content, str):  # type: ignore
            if message.role == "system" and message.content.rstrip() == "":
                continue

            messages.append({
                "role": message.role,
                "content": message.content,
            })
        elif isinstance(message.content, gr.FileData):  # type: ignore
            file_extension: str = os.path.splitext(message.content.path)[1]
            if file_extension in constants.GENERIC_FILE_EXTENSIONS:
                with open(message.content.path, "rt", encoding="utf-8") as file:
                    messages.append({
                        "role": message.role,
                        "content": f"`{os.path.basename(message.content.path)}`:\n\n```\n{file.read()}\n```"
                    })
            elif file_extension in constants.IMAGE_FILE_EXTENSIONS:
                with open(message.content.path, "rb") as file:
                    messages.append({
                        "role": message.role,
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/{file_extension[1:]};base64,{base64.b64encode(file.read()).decode()}"
                                },
                            },
                        ],
                    })
            elif file_extension in constants.AUDIO_FILE_EXTENSIONS:
                with open(message.content.path, "rb") as file:
                    messages.append({
                        "role": message.role,
                        "content": [
                            {
                                "type": "input_audio",
                                "input_audio": {
                                    "data": base64.b64encode(file.read()).decode(),
                                    "format": file_extension[1:],
                                }
                            },
                        ],
                    })

    payload: dict[str, Any] = {
        "messages": messages,
    }
    payload = lm_backend.create_payload(payload, stream_responses, temperature, top_k, top_p, min_p, typical_p, repetition_penalty, repetition_penalty_range, presence_penalty, frequency_penalty, mirostat_mode, mirostat_tau, mirostat_eta, dry_base, dry_multiplier, dry_allowed_length, dry_penalty_range, xtc_threshold, xtc_probability)

    async with httpx.AsyncClient() as client:
        # Since this is the face of our app, we want server-specific error messages
        # (e.g., no Context Shift, invalid image or audio file, etc).
        try:
            if not payload["stream"]:
                shared.assistant_task = asyncio.create_task(client.request("POST", f"http://localhost:{port}/v1/chat/completions", json=payload, timeout=None))
                response: httpx.Response = await shared.assistant_task
                response_data: dict[str, Any] = response.json()
                if "error" not in response_data:
                    chunk: dict[str, Any] = response_data["choices"][0]

                    shared.chat_history[-1].content = chunk["message"]["content"]
                    if chunk["finish_reason"] == "length":
                        gr.Warning(constants.WARNING_NO_CONTEXT_SHIFT_CUTOFF)
                else:
                    __delete_last_exchange()
                    match response_data["error"]["message"]:
                        case constants.SERVER_ERROR_NO_CONTEXT_SHIFT:
                            gr.Warning(constants.WARNING_NO_CONTEXT_SHIFT)
                        case constants.SERVER_ERROR_INVALID_IMAGE_OR_AUDIO:
                            gr.Warning(constants.WARNING_INVALID_IMAGE_OR_AUDIO)
                        case constants.SERVER_ERROR_IMAGE_INPUT_UNSUPPORTED:
                            gr.Warning(constants.WARNING_IMAGE_INPUT_UNSUPPORTED)
                        case constants.SERVER_ERROR_AUDIO_INPUT_UNSUPPORTED:
                            gr.Warning(constants.WARNING_AUDIO_INPUT_UNSUPPORTED)
                        case _:
                            gr.Warning(constants.WARNING_GENERIC)
            else:
                shared.assistant_task = 0
                async with client.stream("POST", f"http://localhost:{port}/v1/chat/completions", json=payload, timeout=None) as response:
                    async for line in response.aiter_lines():
                        if shared.assistant_task is None:  # type: ignore
                            break

                        if line.startswith("data: ") and not line.endswith("[DONE]"):
                            chunk: dict[str, Any] = json.loads(line[6:])["choices"][0]
                            chunk_text: str | None = chunk["delta"].get("content", "")

                            if chunk_text is not None:
                                shared.chat_history[-1].content += chunk_text  # type: ignore
                                yield shared.chat_history

                            if chunk["finish_reason"] == "length":
                                gr.Warning(constants.WARNING_NO_CONTEXT_SHIFT_CUTOFF)
                        elif line.startswith("error: ") and constants.SERVER_ERROR_NO_CONTEXT_SHIFT in line:
                            __delete_last_exchange()
                            gr.Warning(constants.WARNING_NO_CONTEXT_SHIFT)
                        elif line.startswith("{\"error\":"):
                            __delete_last_exchange()
                            match json.loads(line)["error"]["message"]:
                                case constants.SERVER_ERROR_INVALID_IMAGE_OR_AUDIO:
                                    gr.Warning(constants.WARNING_INVALID_IMAGE_OR_AUDIO)
                                case constants.SERVER_ERROR_IMAGE_INPUT_UNSUPPORTED:
                                    gr.Warning(constants.WARNING_IMAGE_INPUT_UNSUPPORTED)
                                case constants.SERVER_ERROR_AUDIO_INPUT_UNSUPPORTED:
                                    gr.Warning(constants.WARNING_AUDIO_INPUT_UNSUPPORTED)
                                case _:
                                    gr.Warning(constants.WARNING_GENERIC)
        except httpx.ConnectError:
            __delete_last_exchange()
            lm_backend.issue_connection_warning(port)
        except asyncio.CancelledError:
            pass
        except:
            __delete_last_exchange()
            gr.Warning(constants.WARNING_GENERIC)
    yield shared.chat_history


def __delete_last_exchange() -> None:
    if len(shared.chat_history) > 0:
        shared.chat_history.pop()
        while True:
            if len(shared.chat_history) == 0 or shared.chat_history[-1].role == "assistant":
                break
            shared.chat_history.pop()
