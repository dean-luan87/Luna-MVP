# OCR mapping

The existing Registry distinguishes `text_recognition` and `precise_ocr`.
They are separate capability identities even when `ocr_v1` is a shared model
dependency. OCR Manager assets are implementations/supporting boundaries;
they do not become additional Registry owners. No OCR provider is invoked by
this package.
