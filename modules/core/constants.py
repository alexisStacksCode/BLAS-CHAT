from typing import Any


VERSION: str = "1.0.0"
DEFAULT_SETTINGS: dict[str, Any] = {
    "language_model": {
        "port": 8080,
        "stream_responses": True,
        "temperature": 0.8,
        "top_k": 40,
        "top_p": 0.95,
        "min_p": 0.05,
        "typical_p": 1.0,
        "repetition_penalty": 1.1,
        "repetition_penalty_range": 64,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.0,
        "mirostat_mode": "Off",
        "mirostat_tau": 5.0,
        "mirostat_eta": 0.1,
        "dry_base": 1.75,
        "dry_multiplier": 0.0,
        "dry_allowed_length": 2,
        "dry_penalty_range": -1,
        "xtc_threshold": 0.1,
        "xtc_probability": 0.0,
    },
    "chat": {
        "system_prompt": "",
    },
    "writer": {
        "max_tokens": 128,
    },
}
DATA_DIR_PATH: str = "data/"
SETTINGS_FILENAME: str = "settings.json"
GENERIC_FILE_EXTENSIONS: list[str] = [
    # Text File
    ".text",
    ".txt",

    # Markdown
    ".md",
    ".markdown",

    # reStructuredText
    ".rst",

    # TeX
    ".tex",

    # AsciiDoc
    ".adoc",
    ".asciidoc",

    # Comma-Separated Values
    ".csv",

    # Tab-Separated Values
    ".tsv",

    # JavaScript Object Notation
    ".json",
    ".jsonc",

    # Tom's Obvious, Minimal Language
    ".toml",

    # Extensible Markup Language
    ".xml",

    # YAML Ain't Markup Language
    ".yaml",
    ".yml",

    # Configuration File
    ".cnf",
    ".conf",
    ".cfg",
    ".cf",
    ".ini",

    # Shell Script
    ".sh",

    # Batch File
    ".bat",
    ".cmd",
    ".btm",

    # PowerShell
    ".ps1",
    ".psd1",
    ".psm1",
    ".ps1xml",
    ".psc1",
    ".pssc",
    ".psrc",

    # Assembly
    ".asm",
    ".s",
    ".inc",
    ".wla",
    ".SRC",

    # Fortran
    ".f90",
    ".f",
    ".for",

    # Pascal
    ".p",
    ".pp",
    ".pas",

    # Haskell
    ".hs",
    ".lhs",

    # Julia
    ".jl",

    # C (also identifiable as C++)
    ".c",
    ".h",  # Also identifiable as Objective-C.

    # C++
    ".cc",
    ".cpp",
    ".cxx",
    ".c++",
    ".hh",
    ".hpp",
    ".hxx",
    ".h++",
    ".cppm",
    ".ixx",

    # C#
    ".cs",
    ".csx",

    # Objective-C & Objective-C++
    ".m",
    ".mm",

    # D
    ".d",
    ".dd",
    ".di",

    # Rust
    ".rs",

    # Python
    ".py",
    ".pyw",
    ".pyi",

    # Lua & Luau
    ".lua",
    ".luau",

    # Ruby
    ".rb",
    ".ru",

    # Go
    ".go",

    # Java
    ".java",

    # Swift
    ".swift",

    # HTML
    ".html",
    ".htm",

    # XHTML
    ".xhtml",
    ".xht",

    # CSS & Sass & SCSS & Stylus & Less
    ".css",
    ".sass",
    ".scss",
    ".styl",
    ".less",

    # PHP
    ".php",
    ".php3",
    ".php4",
    ".php5",
    ".phtml",
    ".pht",
    ".phps",

    # ActionScript
    ".as",

    # Haxe
    ".hx",
    ".hxml",

    # JavaScript & JS++
    ".js",
    ".mjs",
    ".cjs",
    ".jspp",
    ".js++",
    ".jpp",
    ".jsx",

    # TypeScript & Ark TypeScript
    ".ts",  # Also identifiable as ArkTS.
    ".tsx",
    ".mts",
    ".cts",
    ".ets",

    # Jupyter Notebook
    ".ipynb",

    # CoffeeScript
    ".coffee",

    # Dart
    ".dart",

    # Structured Query Language
    ".sql",

    # OpenGL Shading Language
    ".glsl",
    ".vert",
    ".tesc",
    ".tese",
    ".geom",
    ".frag",
    ".comp",

    # High-Level Shader Language
    ".hlsl",

    # Godot
    ".tscn",
    ".tres",
    ".gd",  # GDScript
    ".shader",
    ".gdshader",
    ".gdextension",

    # Jinja2
    ".j2",
]
IMAGE_FILE_EXTENSIONS: list[str] = [
    ".png",
    ".jpg",
    ".jpeg",
    ".jpe",
    ".jif",
    ".jfif",
    ".jfi",
    ".webp",
]
AUDIO_FILE_EXTENSIONS: list[str] = [
    ".wav",
    ".mp3",
]
SERVER_ERROR_NO_CONTEXT_SHIFT: str = "the request exceeds the available context size. try increasing the context size or enable context shift"
SERVER_ERROR_INVALID_IMAGE_OR_AUDIO: str = "Failed to load image or audio file"
SERVER_ERROR_IMAGE_INPUT_UNSUPPORTED: str = "image input is not supported - hint: if this is unexpected, you may need to provide the mmproj"
SERVER_ERROR_AUDIO_INPUT_UNSUPPORTED: str = "audio input is not supported - hint: if this is unexpected, you may need to provide the mmproj"
WARNING_NO_CONTEXT_SHIFT_CUTOFF: str = "The model's message was cut off because Context Shift is disabled."
WARNING_NO_CONTEXT_SHIFT: str = "Your message could not be sent because Context Shift is disabled."
WARNING_INVALID_IMAGE_OR_AUDIO: str = "The image or audio file(s) you sent are unviewable."
WARNING_IMAGE_INPUT_UNSUPPORTED: str = "The currently running model cannot see images. You may need to refresh the model info or reload llama.cpp with the multimodal projector."
WARNING_AUDIO_INPUT_UNSUPPORTED: str = "The currently running model cannot hear audio. You may need to refresh the model info or reload llama.cpp with the multimodal projector."
WARNING_GENERIC: str = "An error occurred."
