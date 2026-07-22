# brutalist

The pared-down, free-only Brutalist video toolkit: three builder skills
(`ai-explainer`, `cli-explainer`, `deep-explainer`), two personas (`nbb`,
`hai`), two Kokoro voices (Onyx `am_onyx`, Bella `af_bella`), zero API keys.

**Read [`HOW-TO.md`](HOW-TO.md)** — what Brutalist is, install, the three
skills, and the six worked examples. `CLAUDE.md` has the session rules for
agents.

```bash
./setup --install     # deps + Remotion node modules + the Kokoro model (~340MB, auto-downloaded)
./art --list          # the skills
```

Note: the Kokoro voice model is not in this repo (GitHub's 100MB file limit)
— `./setup --install` fetches it once from the kokoro-onnx releases.
