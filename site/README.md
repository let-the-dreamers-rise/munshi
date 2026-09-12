# The hosted demo

The product at [munshi.vercel.app](https://munshi.vercel.app): a landing page, Meera's afternoon, and a box where
anyone can paste their own bank SMS and get the real paperwork back.

It is stateless. `api/munshi.py` runs the same Strands agent as everything else, packs the whole run (inbox,
audit log, the paused session) into one string, and hands it to the browser; the browser sends it back with the
family's answer, so the agent resumes from the exact tool call that asked. Nothing is written on the server, and
pasted message text is read once in memory and never stored.

The hosted model is the offline playbook by default (no AWS account needed); set `MUNSHI_MODEL=bedrock` with
credentials to run it on Amazon Bedrock.

```bash
python scripts/build_site.py   # copies the shared page assets into site/public
cd site && vercel deploy --prod
```
