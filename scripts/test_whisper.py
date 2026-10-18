import sys
try:
    import faster_whisper
    print("faster_whisper is available!")
except ImportError as e:
    print("faster_whisper not installed:", e)

try:
    import transformers
    print("transformers is available:", transformers.__version__)
except ImportError as e:
    print("transformers not installed:", e)
