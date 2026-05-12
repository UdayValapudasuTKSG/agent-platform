import vertexai.preview.reasoning_engines as re
try:
    import vertexai.preview.reasoning_engines.templates as templates
    print("Templates available:", dir(templates))
except ImportError:
    print("Templates not found in this version of the SDK.")
