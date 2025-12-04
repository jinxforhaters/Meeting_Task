import re
from typing import List, Optional

from .models import Task, TeamMember

TASK_VERBS = [
    "fix",
    "update",
    "design",
    "optimize",
    "write",
    "implement",
    "deploy",
    "review",
    "create",
    "test",
    "add",
    "improve",
    "refactor",
]

TASK_MARKERS = [
    "need to",
    "should",
    "must",
    "have to",
    "let's",
    "we need someone to",
    "we need to",
    "can you",
    "could you",
    "please",
]


def is_task_sentence(sent: str) -> bool:
    """Return True if the sentence looks like a task."""
    lower = sent.lower().strip()
    if not lower:
        return False

    if any(marker in lower for marker in TASK_MARKERS):
        return True

    if any(lower.startswith(verb + " ") for verb in TASK_VERBS):
        return True

    if "someone" in lower and any(v in lower for v in TASK_VERBS):
        return True

    return False


def find_assigned_member(sent: str, team_members: List[TeamMember]) -> Optional[str]:
    """Return the name of the member mentioned in the sentence, if any."""
    lower = sent.lower()
    for member in team_members:
        if member.name.lower() in lower:
            return member.name
    return None


def clean_description(sent: str, assigned_to: Optional[str]) -> str:
    """Strip names and polite phrases, keep the core task text."""
    desc = sent.strip()

    if assigned_to:
        for pattern in (assigned_to + ",", assigned_to + ":", assigned_to):
            if desc.startswith(pattern):
                desc = desc[len(pattern):].lstrip()
                break

    leading_phrases = [
        "we need someone to",
        "we need to",
        "we should",
        "can you",
        "could you",
        "please",
        "let's",
        "let us",
        "i want you to",
        "i want someone to",
    ]

    lower = desc.lower().lstrip()
    for phrase in leading_phrases:
        if lower.startswith(phrase):
            desc = desc[len(phrase):].lstrip()
            break

    return desc


def get_priority_from_sentence(sent: str) -> str:
    """Determine priority based on simple keyword rules."""
    lower = sent.lower()

    if "critical" in lower or "blocking users" in lower or "blocker" in lower:
        return "Critical"

    if "high priority" in lower or "top priority" in lower or "urgent" in lower or "asap" in lower:
        return "High"

    if "low priority" in lower or "can wait" in lower or "nice to have" in lower:
        return "Low"

    return "Medium"


def get_deadline_from_sentence(sent: str) -> Optional[str]:
    """Extract a simple deadline phrase from the sentence, if any."""
    lower = sent.lower()

    direct_keywords = [
        "by tomorrow",
        "by today",
        "by tonight",
        "by friday",
        "by monday",
        "by tuesday",
        "by wednesday",
        "by thursday",
        "by saturday",
        "by sunday",
        "tomorrow",
        "today",
        "tonight",
        "this week",
        "next week",
        "this month",
        "next month",
        "end of this week",
        "end of the week",
        "before the release",
    ]

    for phrase in direct_keywords:
        if phrase in lower:
            start = lower.index(phrase)
            end = start + len(phrase)
            return sent[start:end].strip()

    match = re.search(r"\bby ([a-zA-Z ]{3,30})", lower)
    if match:
        start, end = match.span()
        return sent[start:end].strip()

    match = re.search(r"\bbefore ([a-zA-Z ]{3,30})", lower)
    if match:
        start, end = match.span()
        return sent[start:end].strip()

    return None


def get_dependencies_for_sentence(
    sent: str,
    existing_tasks: List[Task],
    team_members: List[TeamMember],
) -> List[int]:
    """Infer simple dependencies on existing tasks."""
    lower = sent.lower()
    dep_ids: List[int] = []

    # "depends on <phrase>"
    if "depends on" in lower:
        after = lower.split("depends on", 1)[1]
        for sep in (",", "."):
            if sep in after:
                after = after.split(sep, 1)[0]
        phrase = after.strip()
        for task in existing_tasks:
            if phrase and phrase in task.description.lower():
                dep_ids.append(task.id)

    # "once <member> is done ..."
    if "once" in lower and "done" in lower:
        try:
            start = lower.index("once") + len("once")
            end = lower.index("done", start)
            middle = lower[start:end].strip(" ,.")
        except ValueError:
            middle = ""

        for member in team_members:
            if member.name.lower() in middle:
                for task in reversed(existing_tasks):
                    if task.assigned_to == member.name:
                        dep_ids.append(task.id)
                        break
                break

    # "after <phrase>"
    if "after" in lower:
        after = lower.split("after", 1)[1]
        for sep in (",", "."):
            if sep in after:
                after = after.split(sep, 1)[0]
        phrase = after.strip()
        for task in existing_tasks:
            if phrase and phrase in task.description.lower():
                dep_ids.append(task.id)

    # Deduplicate
    return list(dict.fromkeys(dep_ids))


def get_reason_for_task(
    sent: str,
    assigned_to: Optional[str],
    priority: str,
    dependencies: List[int],
    team_members: List[TeamMember],
) -> Optional[str]:
    """Build a short explanation string for the task."""
    lower = sent.lower()

    # Explicit reasons, if present
    if "because" in lower:
        part = sent.lower().split("because", 1)[1]
        return "because " + part.strip(" ,.")

    if "since" in lower:
        part = sent.lower().split("since", 1)[1]
        return "since " + part.strip(" ,.")

    if " as " in lower:
        part = sent.lower().split(" as ", 1)[1]
        return "as " + part.strip(" ,.")

    if "so that" in lower:
        part = sent.lower().split("so that", 1)[1]
        return "so that " + part.strip(" ,.")

    reasons: List[str] = []

    if assigned_to:
        member = next((m for m in team_members if m.name == assigned_to), None)
        if member and member.skills:
            reasons.append(
                f"Assigned to {assigned_to} because their skills ({', '.join(member.skills)}) match the task."
            )
        else:
            reasons.append(f"Assigned to {assigned_to} because they were mentioned in the meeting.")
    else:
        reasons.append("No specific assignee mentioned in the transcript.")

    if priority == "Critical":
        reasons.append("Marked critical based on urgency/impact keywords in the sentence.")
    elif priority == "High":
        reasons.append("Marked high priority based on priority-related keywords.")
    elif priority == "Low":
        reasons.append("Marked low priority because the language suggests it can wait.")

    if dependencies:
        dep_str = ", ".join(str(d) for d in dependencies)
        reasons.append(f"This task depends on tasks: {dep_str}.")

    return " ".join(reasons) if reasons else None


def extract_tasks_from_transcript(
    sentences: List[str],
    team_members: List[TeamMember],
) -> List[Task]:
    """Extract Task objects from a list of sentences."""
    tasks: List[Task] = []
    task_id = 1

    for sent in sentences:
        if not is_task_sentence(sent):
            continue

        assigned_to = find_assigned_member(sent, team_members)
        description = clean_description(sent, assigned_to)
        priority = get_priority_from_sentence(sent)
        deadline = get_deadline_from_sentence(sent)
        dependencies = get_dependencies_for_sentence(sent, tasks, team_members)
        reason = get_reason_for_task(sent, assigned_to, priority, dependencies, team_members)

        task = Task(
            id=task_id,
            description=description,
            assigned_to=assigned_to,
            priority=priority,
            deadline=deadline,
            dependencies=dependencies,
            reason=reason,
        )
        tasks.append(task)
        task_id += 1

    return tasks
