# app/config/management/commands/sync_config.py
import os, json, logging, tempfile
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from utils.client import (
    ConfigClient
)
logger = logging.getLogger(__name__)

# If your ConfigClient lives elsewhere, fix the import
CLIENT_INTERNAL_URL = "https://brtgw.britam.com/config/kafka/api/v1/config/internal/"

CONFIG_JSON_PATH = "config.json"

def atomic_write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", delete=False, dir=path.parent, encoding="utf-8") as tmp:
        json.dump(payload, tmp, indent=4)
        tmp.flush()
        os.fsync(tmp.fileno())
        tmp_name = tmp.name
    os.replace(tmp_name, path)  # atomic on POSIX

class Command(BaseCommand):
    help = "Fetch remote config and write to local JSON (atomic)."
    def add_arguments(self, parser):
        parser.add_argument("--url", required=False,
            default=CLIENT_INTERNAL_URL)
        parser.add_argument("--out", required=False,
            default=CONFIG_JSON_PATH)
        parser.add_argument("--timeout", type=float, default=float(os.getenv("CONFIG_TIMEOUT", "10")))

    def handle(self, *args, **opts):
        url = opts["url"]
        out = opts["out"]
        if not out:
            # keep in sync with settings.py default
            from django.conf import settings
            out = str(settings.CONFIG_JSON_PATH)
        target = Path(out)

        self.stdout.write(f"Fetching config from {url}")
        try:
            app = ConfigClient(CLIENT_INTERNAL_URL)
            message = app.get_all()
            logger.info(message)
            if not isinstance(message, dict):
                raise CommandError(f"Remote config did not return a dict: type={type(message).__name__}")
        except Exception as e:
            raise CommandError(f"Failed to fetch config: {e}") from e

        try:
            atomic_write_json(target, message)
        except Exception as e:
            raise CommandError(f"Failed to write {target}: {e}") from e

        self.stdout.write(self.style.SUCCESS(f"Wrote config to {target}"))