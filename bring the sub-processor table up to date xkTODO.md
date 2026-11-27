# Bring the sub-processor table up to date

`content/privacy.md`'s sub-processor table, for Rubicon only. The Causal Map app's rows (Cloud Functions in two regions, Claude on Vertex) were corrected from the code on 27 November 2026.

- Rubicon's other model providers are not listed: Scaleway (Paris) and TensorX (Dublin, Helsinki, Paris), beside Lyceum. `rubicon/rubicon/coordinator/open_weights.py` reads their keys from the local `rubicon/.env`; whether hosted Ruby, now parked, ever sends them project text is not settled from the code. List them only once something real goes through them.

Verify each against the code and the provider's own terms before writing it; a push publishes.
