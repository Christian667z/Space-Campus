"""Bridge minimal pour appeler un LLM local via CLI.

Ce module exécute une commande configurable (core.config.LOCAL_LLM_CMD)
en passant le prompt sur stdin et en lisant stdout. Il est volontairement
léger et générique pour supporter plusieurs frontends (gpt4all, llama.cpp, ...).

Usage:
  from core.local_llm import generate
  text = generate(prompt, max_tokens=512, timeout=30)
"""
import shlex
import subprocess
import logging
from typing import Optional

from core import config

logger = logging.getLogger(__name__)


def _build_cmd(prompt: str, max_tokens: int) -> list[str]:
    # La commande configurée peut contenir des placeholders : {max_tokens}
    # L'prompt est envoyé via stdin pour la plupart des CLIs modernes.
    cmd_template = config.LOCAL_LLM_CMD
    if not cmd_template:
        raise RuntimeError("LOCAL_LLM_CMD non configuré dans core.config")
    cmd = cmd_template.format(max_tokens=max_tokens)
    return shlex.split(cmd)


def generate(prompt: str, max_tokens: int = 512, timeout: int = 30) -> Optional[str]:
    """Génère une réponse en appelant le binaire LLM local.

    Retourne la sortie stdout (str) ou None en cas d'erreur / timeout.
    """
    try:
        cmd = _build_cmd(prompt, max_tokens)
        logger.debug("Exécution LLM local : %s", " ".join(cmd))
        proc = subprocess.run(
            cmd,
            input=prompt.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
        if proc.returncode != 0:
            logger.error("LLM local non zero exit (%d): %s", proc.returncode, proc.stderr.decode('utf-8', errors='ignore'))
            return None
        out = proc.stdout.decode('utf-8', errors='ignore').strip()
        return out
    except subprocess.TimeoutExpired:
        logger.warning("LLM local timeout après %ds", timeout)
        return None
    except Exception as e:
        logger.exception("Erreur lors de l'appel LLM local: %s", e)
        return None
