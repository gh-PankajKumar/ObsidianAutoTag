from pathlib import Path
import re
import logging


class Vault:
    def __init__(self, vault_dir: str, notes_dir: str, tag_dir: str) -> None:
        self.vault_dir = Path(vault_dir)
        self.notes_dir = Path(notes_dir)
        self.tag_dir = Path(tag_dir)

        if not self.vault_dir.is_dir():
            raise FileNotFoundError(f"Vault directory not found: {vault_dir}")

        if not self.notes_dir.is_dir():
            raise FileNotFoundError(f"Notes directory not found in vault: {vault_dir}")

        if not self.tag_dir.is_dir():
            raise FileNotFoundError(f"MOCs directory not found in vault: {vault_dir}")

        self._mocs_tag_pattern = re.compile(
            r"[Tt]ags:?\s*(?:\[\[([^\]]+)\]\]|([^\n\r]+))"
        )

        self.logger = logging.getLogger(__name__)

    @property
    def existing_tags(self):
        return [file.stem for file in self.tag_dir.glob("*.md")]

    @property
    def notes_with_tags(self):
        """Get list of notes that have tags."""
        return [
            note_path.name
            for note_path in self.notes_dir.glob("*.md")
            if (note_text := note_path.read_text()) and self._has_tags(note_text)
        ]

    @property
    def notes_without_tags(self):
        """Get list of notes that have no tags."""
        return [
            note_path.name
            for note_path in self.notes_dir.glob("*.md")
            if (note_text := note_path.read_text()) and not self._has_tags(note_text)
        ]

    # TODO: Is this needed? if Path.read_text() is used
    def _read_note(self, note_path):
        if note_path.suffix == ".md":
            with open(note_path, "r") as f:
                return f.read()
        else:
            self.logger.error(
                "Invalid file type. Check the note path to ensure it is a markdown file."
            )
            return None

    def _has_tags(self, note_text):
        return bool(self._mocs_tag_pattern.search(note_text))

    def write_tags_to_note(self, tags, note_path):
        try:
            note_path = Path(note_path)

            # Validate file
            if not note_path.exists():
                self.logger.error(f"Note not found: {note_path}")
                return False

            if note_path.suffix != ".md":
                self.logger.error(f"Invalid file type: {note_path}")
                return False

            # Read existing content
            content = note_path.read_text(encoding="utf-8")
            note_path.write_text(f"{tags}\n{content}", encoding="utf-8")

            self.logger.info(f"Successfully added tags to {note_path}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to write tags to {note_path}: {str(e)}")
            return False

    # TODO: Implement formatting tags to ensure they are of the form: "Suggested Tags: [[tag1]], [[tag2]]"
    # maybe it is better to use Guidance AI to ensure the LLM output is formatted correctly
    def _format_tags(self, tags):
        pass
