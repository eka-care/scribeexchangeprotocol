# Examples

Valid payloads, one or more per schema. File name: `NN-<object>[.variant].json`, matching `../schemas/NN-<object>.schema.json`: `06-source.audio.recording.json`, `04-discovery.no-auth.json`.

Every file here validates against its schema; `python3 ../validate.py` checks them all and CI fails otherwise. An example shown in a spec chapter also lives here as a file.
