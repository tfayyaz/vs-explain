# vs explain

## Design Principles

### No quizzes
Explanations must never be in quiz form (no "classify this", "pick the right answer", score tracking, right/wrong feedback). The user should learn through direct interaction with the concept, not by being tested on it.

### One strong interactive idea per page
Each explanation should have one central interactive mechanism that teaches the comparison through doing. The interaction itself should make the difference click — not text, not questions.

### Teach through interaction, not testing
As the user interacts, the app should reveal the concept. The interface should respond in a way that builds understanding naturally. Think: "play with this and you'll get it" — not "answer this and we'll tell you if you're right."

### Keep it simple
- Pure HTML + JavaScript, no frameworks
- Serif typography (Georgia), minimal design
- Mobile and touch friendly
- Each page is a single self-contained HTML file

## GitHub Pages Setup & Management (gh CLI)

The site is hosted on GitHub Pages at: https://tfayyaz.github.io/vs-explain/

### Configuration
- **Build type**: `legacy` (direct file serving from branch, no Actions workflow)
- **Source**: `main` branch, `/` root directory
- **Deploys automatically** on every push to `main`

### Useful gh CLI commands

```bash
# Check Pages status (building, built, errored)
gh api repos/tfayyaz/vs-explain/pages

# Check most recent deployment
gh api repos/tfayyaz/vs-explain/pages/builds/latest

# List all Pages builds
gh api repos/tfayyaz/vs-explain/pages/builds

# Enable Pages on a repo (first time setup)
gh api repos/tfayyaz/vs-explain/pages -X POST -f build_type=workflow

# Switch to deploy from branch (legacy mode, no Actions needed)
gh api repos/tfayyaz/vs-explain/pages -X PUT --input - <<< '{"build_type":"legacy","source":{"branch":"main","path":"/"}}'

# Delete Pages site
gh api repos/tfayyaz/vs-explain/pages -X DELETE

# Set custom domain
gh api repos/tfayyaz/vs-explain/pages -X PUT --input - <<< '{"cname":"versus-explainable.tahirfayyaz.dev"}'
```

### Important notes
- Always switch to `tfayyaz` gh account before Pages operations: `gh auth switch --user tfayyaz`
- Switch back to work account after: `gh auth switch --user tahir-fayyaz_data`
- Repo must be public for free Pages hosting
- Legacy mode serves static files directly — no build step, instant deploys
