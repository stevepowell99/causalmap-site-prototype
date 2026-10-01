# Bring the sub-processor table up to date

`content/privacy.md` and `content/ai-compliance.md` lag what the products now use, as found on 1 October 2026:

- The Google Cloud Functions row says us-central1 only. Both `start_run` and `process_chunk` now run in us-central1 and europe-west1, and EU-tier projects use the European one (causal-map-extension `CLAUDE.md`, "Deploying ai-run-executor").
- Rubicon's other model providers are missing: Scaleway (Paris), TensorX, and Anthropic. Check `rubicon/rubicon/coordinator/open_weights.py` and Ruby's deployment for what actually receives project text before listing them.
- Claude on Vertex (EU-resident Haiku 4.5, Sonnet 4.6 and Sonnet 5) is not mentioned under Vertex AI.

Verify each against the code and the provider's own terms before writing it; a push publishes.
