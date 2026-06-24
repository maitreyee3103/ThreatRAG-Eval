"""Ground truth Q&A pairs derived directly from CISA KEV catalog entries."""

GROUND_TRUTH = [
    {
        "question": "What is CVE-2021-44228 and what action is required?",
        "ground_truth": (
            "CVE-2021-44228 is the Apache Log4j2 Remote Code Execution Vulnerability. "
            "Apache Log4j2 contains a vulnerability where JNDI features do not protect against "
            "attacker-controlled JNDI-related endpoints, allowing for remote code execution. "
            "The required action is to apply updates for all affected software assets, or remove "
            "affected assets from agency networks. Temporary mitigations are only acceptable until "
            "updates are available, with a due date of 2021-12-24."
        ),
    },
    {
        "question": "Which Microsoft product is affected by CVE-2021-34527?",
        "ground_truth": (
            "CVE-2021-34527, also known as PrintNightmare, affects Microsoft Windows Print Spooler. "
            "The Windows Print Spooler service improperly performs privileged file operations, "
            "allowing an attacker to perform remote code execution with SYSTEM privileges. "
            "The required action is to apply updates per vendor instructions."
        ),
    },
    {
        "question": "What vulnerability does CVE-2020-1472 represent?",
        "ground_truth": (
            "CVE-2020-1472, also known as Zerologon, is a Microsoft Netlogon Privilege Escalation Vulnerability. "
            "Microsoft's Netlogon Remote Protocol (MS-NRPC) contains a privilege escalation vulnerability "
            "when an attacker establishes a vulnerable Netlogon secure channel connection to a domain controller. "
            "The required action is to apply updates per vendor instructions, with a due date of 2022-05-03."
        ),
    },
    {
        "question": "What is the required action for CVE-2019-0708 (BlueKeep)?",
        "ground_truth": (
            "CVE-2019-0708, known as BlueKeep, is a Microsoft Remote Desktop Services Remote Code Execution Vulnerability. "
            "An unauthenticated attacker can connect to the target system using RDP and send specially crafted requests "
            "to achieve remote code execution. The required action is to apply updates per vendor instructions, "
            "with a due date of 2022-05-03."
        ),
    },
    {
        "question": "What product is affected by CVE-2021-26855?",
        "ground_truth": (
            "CVE-2021-26855 affects Microsoft Exchange Server. It is a Remote Code Execution Vulnerability "
            "and is part of the ProxyLogon exploit chain. "
            "The required action is to apply updates per vendor instructions, with a due date of 2022-05-03."
        ),
    },
]
