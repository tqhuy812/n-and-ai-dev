from typing import Any
import asyncio
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("deviceconfig")

# Credentials / defaults (kept for possible future use)
username = "admin"
password = "NokiaSrl1!"
port = 57400
timeout = 10  # seconds
skip_verify = True
encoding = "json_ietf"


@mcp.tool()
async def device_config(device_id: str, config: Any) -> str:
    """Apply device configuration by executing a gnmic 'set' using a pre-defined
    config file.

    This function runs the following command:
    gnmic -u admin -p NokiaSrl1! --skip-verify --encoding json_ietf -a clab-3srlinux_2clients-<device_id>:57400 set --update-path / --update-file file_name

    Args:
        device_id: The ID of the device to configure (currently unused).
        config: The configuration payload (currently unused).

    Returns:
        The stdout from the gnmic command as a string, or raises RuntimeError on failure.
    """

    cmd = [
        "gnmic",
        "-u admin -p NokiaSrl1! --skip-verify --encoding json_ietf",
        "-a clab-3srlinux_2clients-" + device_id + ":57400",
        "set",
        "--update-path",
        "/",
        "--update-file",
        config+".yaml",
    ]

    # Execute the command asynchronously and capture output
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await proc.communicate()
    stdout_text = stdout.decode().strip() if stdout else ""
    stderr_text = stderr.decode().strip() if stderr else ""

    if proc.returncode != 0:
        # Return a clear error for the caller (tooling/framework can map to error responses)
        raise RuntimeError(f"gnmic failed (rc={proc.returncode}): {stderr_text}")

    return stdout_text or "OK"


def main():
    # Initialize and run the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()