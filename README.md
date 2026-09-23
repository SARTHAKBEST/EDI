# Adaptive Memory Evolution Framework for Long-Term AI Agents

Four-person project. Each member owns one folder; a shared contract in
`shared/interfaces.py` is how the folders talk to each other without
needing to know each other's internals.

## Folder structure

```
adaptive-memory-agent/
├── shared/interfaces.py            # contracts everyone codes against
├── member1_conversation/           # Member 1: chatbot + LLM + response generation
├── member2_memory_storage/         # Member 2: storing/retrieving memories
├── member3_memory_evolution/       # Member 3: decay, forgetting, importance updates
├── member4_evaluation_ui/          # Member 4: frontend + evaluation scripts
├── app/main.py                     # wires all four modules into one backend
├── requirements.txt
├── .env.example
└── .gitignore
```

If your team split responsibilities differently than assumed here,
rename the folders to match and adjust `shared/interfaces.py` — the
overall layout still works.

## Setup

```bash
git clone <your-repo-url>
cd adaptive-memory-agent
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then fill in your real API key
```

## Run the whole system

```bash
uvicorn app.main:app --reload
```

Then open `member4_evaluation_ui/chat_ui.html` directly in a browser,
or test with curl:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "u1", "message": "My favorite language is Python"}'
```

Always run Python commands from the project root (not from inside a
member's subfolder) — the imports assume the root is on the path.

## Testing your own module before others are ready

Each module implements an abstract interface from `shared/interfaces.py`.
That means you can write a 5-line fake/mock implementation of a
teammate's interface to unblock your own testing, then swap in their
real class later without touching your code — that's the whole point
of coding against the interface instead of a concrete class.

## Team git workflow — adding everyone's files

1. **Create the repo.** One person creates a GitHub repository and pushes
   this starter project as the first commit on `main`.
2. **Add collaborators.** On GitHub: Settings → Collaborators and teams →
   Add people → enter each teammate's GitHub username or email. They'll
   get an email invite to accept.
3. **Everyone clones it.** Each member runs `git clone <repo-url>` locally.
4. **One branch per member.** Each person creates a branch named after
   their module, e.g. `git checkout -b member2-memory-storage`. Working
   in separate branches (and separate folders) means your changes won't
   collide with a teammate's while you're both mid-task.
5. **Work only inside your own folder.** Member 2 edits files under
   `member2_memory_storage/` (and, if the team agrees, proposes changes
   to `shared/interfaces.py` in their own small commit that everyone
   reviews). Commit regularly: `git add member2_memory_storage/ && git commit -m "..."`.
6. **Push and open a pull request.** `git push origin member2-memory-storage`,
   then open a PR into `main` on GitHub.
7. **Get a review before merging.** Have at least one other teammate look
   at the PR — this is when integration problems (a function signature
   that doesn't quite match `shared/interfaces.py`) get caught early.
8. **Merge, then everyone pulls.** After merging to `main`, everyone runs
   `git pull origin main` to stay in sync — do this before you start a
   new work session.
9. **Integrate often.** Don't wait until the deadline to run `app/main.py`
   with all four real modules plugged in. Do it weekly so integration
   bugs surface while there's still time to fix them.
10. **Track tasks.** Use GitHub Issues (or a simple shared doc) with one
    checklist per member, so it's visible who's blocked on whose interface.

## Module ownership

| Folder | Owner | Implements |
|---|---|---|
| `member1_conversation/` | Member 1 | Chat backend, LLM connection, prompt building, response generation |
| `member2_memory_storage/` | Member 2 | `MemoryStoreInterface` — store and retrieve memories |
| `member3_memory_evolution/` | Member 3 | `MemoryEvolutionInterface` — decay, forgetting, importance updates |
| `member4_evaluation_ui/` | Member 4 | Chat frontend, evaluation scripts |
