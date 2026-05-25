import os
import datetime


SCORES_DIR = os.path.dirname(os.path.abspath(__file__))


def load_scores(filepath="highscores.md"):
    path = os.path.join(SCORES_DIR, filepath)
    if not os.path.exists(path):
        return []

    scores = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("|---") or "Rank" in line:
                continue
            parts = [p.strip() for p in line.split("|")]
            parts = [p for p in parts if p]
            if len(parts) < 4:
                continue
            try:
                scores.append({
                    "name": parts[1],
                    "score": int(parts[2]),
                    "date": parts[3],
                })
            except (ValueError, IndexError):
                continue

    scores.sort(key=lambda s: s["score"], reverse=True)
    return scores


def save_scores(scores, filepath="highscores.md"):
    path = os.path.join(SCORES_DIR, filepath)
    with open(path, "w") as f:
        f.write("# High Scores\n\n")
        f.write("| Rank | Name       | Score | Date       |\n")
        f.write("|------|------------|-------|-----------|\n")
        for i, entry in enumerate(scores):
            f.write(f"| {i + 1:<4} | {entry['name']:<10} | {entry['score']:<5} | {entry['date']:<10} |\n")


def update_scores(player_name, new_score, filepath="highscores.md"):
    scores = load_scores(filepath)

    found = False
    for entry in scores:
        if entry["name"].lower() == player_name.lower():
            found = True
            if new_score > entry["score"]:
                entry["score"] = new_score
                entry["date"] = datetime.date.today().isoformat()
                entry["name"] = player_name
            break

    if not found:
        scores.append({
            "name": player_name,
            "score": new_score,
            "date": datetime.date.today().isoformat(),
        })

    scores.sort(key=lambda s: s["score"], reverse=True)
    save_scores(scores, filepath)
    return scores
