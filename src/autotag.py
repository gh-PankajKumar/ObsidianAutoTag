from pathlib import Path
import logging
from functools import lru_cache

from .model_loader import ModelLoader
from .prompt import get_prompt
from .vault import Vault


class ObsidianAutoTag:
    def __init__(self, vault_path: str):
        self.logger = logging.getLogger(__name__)
        self.vault = Vault(vault_path)
        self.llm = ModelLoader().load_model()

    @lru_cache(maxsize=100)
    def _get_prompts(self) -> dict:
        """Cache and return prompts to avoid redundant processing."""
        return get_prompt(self.vault.existing_tags)

    def process_note(self, note_path: Path) -> str:
        """Process a single note and return suggested tags."""
        try:
            note_content = note_path.read_text(encoding="utf-8")
            prompts = self._get_prompts(self.vault.existing_tags)
            messages = [
                {"role": "system", "content": prompts["system_prompt"]},
                {"role": "user", "content": f"{prompts['prompt']} \n {note_content}"},
            ]
            result = self.llm.create_chat_completion(temperature=0.3, messages=messages)
            return self._extract_tags(
                result.get("choices", [{}])[0].get("message", {}).get("content", "")
            )
        except Exception as e:
            self.logger.error(f"Failed to process note {note_path}: {e}")
            return ""

    def process_untagged_notes(self) -> None:
        """Process all notes without tags in the vault."""
        for note_name in self.vault.notes_without_tags:
            note_path = self.vault.notes_dir / note_name
            if tags := self.process_note(note_path):
                self.vault.write_tags_to_note(tags, note_path)
                self.logger.info(f"Added tags to {note_name}: {tags}")
            else:
                self.logger.warning(f"No tags generated for {note_name}")

    def process_tagged_notes(self) -> None:
        """Process all notes with tags in the vault."""
        for note_name in self.vault.notes_with_tags:
            note_path = self.vault.notes_dir / note_name
            if tags := self.process_note(note_path):
                self.vault.write_tags_to_note(tags, note_path)
                self.logger.info(f"Added tags to {note_name}: {tags}")
            else:
                self.logger.warning(f"No tags generated for {note_name}")

    def process_all_notes(self) -> None:
        """Process all notes in the vault."""
        for note_name in self.vault.notes:
            note_path = self.vault.notes_dir / note_name
            if tags := self.process_note(note_path):
                self.vault.write_tags_to_note(tags, note_path)
                self.logger.info(f"Added tags to {note_name}: {tags}")
            else:
                self.logger.warning(f"No tags generated for {note_name}")

    def _extract_tags(self, llm_response: str) -> str:
        """Extract tags from LLM response ensuring correct format."""
        if "Suggested Tags:" not in llm_response:
            return ""
        tags_part = llm_response.split("Suggested Tags:", 1)[1].strip()
        tags = [tag.strip() for tag in tags_part.split(",")]
        return (
            f"Tags: {', '.join(tags)}"
            if all(tag.startswith("[[") and tag.endswith("]]") for tag in tags)
            else ""
        )
