from __future__ import annotations

import json
import re
import time
from typing import Any

from app.integrations.openclaw import OpenClawClient


def _slug(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "agent"


def desired_agent_id(*, employee_id: int, name: str) -> str:
    return f"employee-{employee_id}-{_slug(name)}"


def ensure_full_agent_profile(
    *,
    client: OpenClawClient,
    employee_id: int,
    employee_name: str,
) -> dict[str, str]:
    """Ensure an OpenClaw agent profile exists for this employee.

    Returns {"agent_id": ..., "workspace": ...}.

    Implementation strategy:
    - Create per-agent workspace + agent dir on the gateway host.
    - Add/ensure entry in openclaw.json agents.list.

    NOTE: This uses OpenClaw gateway tools via /tools/invoke (gateway + exec).
    """

    agent_id = desired_agent_id(employee_id=employee_id, name=employee_name)

    workspace = f"/home/asaharan/.openclaw/workspaces/{agent_id}"
    agent_dir = f"/home/asaharan/.openclaw/agents/{agent_id}/agent"

    # 1) Create dirs
    client.tools_invoke(
        "exec",
        {
            "command": f"mkdir -p {workspace} {agent_dir}",
        },
        timeout_s=20.0,
    )

    # 2) Write minimal identity files in the per-agent workspace
    identity_md = (
        "# IDENTITY.md\n\n"
        "- **Name:** " + employee_name + "\n"
        "- **Creature:** AI agent employee (Mission Control)\n"
        "- **Vibe:** Direct, action-oriented, leaves audit trails\n"
    )
    user_md = (
        "# USER.md\n\n"
        "You work for Abhimanyu.\n"
        "You must execute Mission Control tasks via the API and keep state synced.\n"
    )

    # Use cat heredocs to avoid dependency on extra tooling.
    client.tools_invoke(
        "exec",
        {
            "command": "bash -lc "
            + json.dumps(
                """
cat > {ws}/IDENTITY.md <<'EOF'
{identity}
EOF
cat > {ws}/USER.md <<'EOF'
{user}
EOF
""".format(ws=workspace, identity=identity_md, user=user_md)
            ),
        },
        timeout_s=20.0,
    )

    # 3) Update openclaw.json agents.list (idempotent)
    cfg_resp = client.tools_invoke("gateway", {"action": "config.get"}, timeout_s=20.0)
    raw = (
        (((cfg_resp or {}).get("result") or {}).get("content") or [{}])[0].get("text")
        if isinstance((((cfg_resp or {}).get("result") or {}).get("content") or [{}]), list)
        else None
    )

    if not raw:
        # fallback: tool may return {ok:true,result:{raw:...}}
        raw = ((cfg_resp.get("result") or {}).get("raw")) if isinstance(cfg_resp, dict) else None

    if not raw:
        raise RuntimeError("Unable to read gateway config via tools")

    cfg = json.loads(raw)

    agents = cfg.get("agents") or {}
    agents_list = agents.get("list") or []
    if not isinstance(agents_list, list):
        agents_list = []

    exists = any(isinstance(a, dict) and a.get("id") == agent_id for a in agents_list)
    if not exists:
        agents_list.append(
            {
                "id": agent_id,
                "name": employee_name,
                "workspace": workspace,
                "agentDir": agent_dir,
                "identity": {"name": employee_name, "emoji": "🜁"},
            }
        )
        agents["list"] = agents_list
        cfg["agents"] = agents

        client.tools_invoke(
            "gateway",
            {"action": "config.apply", "raw": json.dumps(cfg)},
            timeout_s=30.0,
        )
        # give the gateway a moment to reload the agent registry
        time.sleep(2.5)

    return {"agent_id": agent_id, "workspace": workspace}
