import subprocess


def run_claude(prompt: str, timeout: int = 45) -> str:
    """
    Calls `claude -p "<prompt>"` as a subprocess.
    Returns stdout string on success.
    Raises RuntimeError on failure or timeout.
    """
    result = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True,
        text=True,
        timeout=timeout
    )
    if result.returncode != 0:
        raise RuntimeError(f"claude exited with code {result.returncode}: {result.stderr.strip()}")
    output = result.stdout.strip()
    if not output:
        raise RuntimeError("claude returned empty output")
    return output
