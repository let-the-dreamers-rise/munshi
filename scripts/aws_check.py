"""Is this machine ready to run Munshi on Amazon Bedrock? Says exactly what is missing.

    python scripts/aws_check.py [--region us-east-1] [--model us.amazon.nova-pro-v1:0]
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from munshi.brain import DEFAULT_BEDROCK  # noqa: E402

OK, NO = "  ok   ", "  no   "


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--region", default=os.environ.get("AWS_REGION", "us-east-1"))
    parser.add_argument("--model", default=os.environ.get("MUNSHI_BEDROCK_MODEL", DEFAULT_BEDROCK))
    opts = parser.parse_args()
    problems = []

    try:
        import boto3
    except ImportError:
        print(NO + "boto3 is not installed.  Fix: pip install -e \".[dev]\"")
        return 1

    try:
        who = boto3.client("sts", region_name=opts.region).get_caller_identity()
        print(OK + "signed in to AWS as {0}".format(who["Arn"].split("/")[-1]))
    except Exception as error:  # noqa: BLE001 -- this script exists to explain failures
        print(NO + "no usable AWS credentials ({0}).".format(type(error).__name__))
        print("       Fix: run `aws login` (or `aws sso login`), then try again.")
        if "crt" in str(error).lower():
            print("       This one also needs: pip install \"botocore[crt]\"")
        return 1

    try:
        from strands.models import BedrockModel

        from munshi.brain import bedrock_settings
        from munshi.demo import demo_household
        from munshi.verdict import investigate

        settings = bedrock_settings()
        settings["model_id"], settings["region_name"] = opts.model, opts.region
        print(OK + "model {0} in {1}{2}".format(
            opts.model, opts.region, ", with guardrail " + settings["guardrail_id"] if settings.get("guardrail_id") else ""))
        household = demo_household()
        event = [e for e in household.events if e.kind == "scam_shaped_payment"][0]
        verdict, _, who = investigate(event, household.ledger, BedrockModel(**settings))
        if who != "model":
            problems.append("the model did not return a verdict: " + who)
            print(NO + "Bedrock answered, but not with a verdict ({0})".format(who))
        else:
            print(OK + "Bedrock wrote a verdict: " + verdict.headline)
    except Exception as error:  # noqa: BLE001
        text = str(error)
        print(NO + "Bedrock call failed: {0}: {1}".format(type(error).__name__, text[:160]))
        if "AccessDenied" in text or "not authorized" in text:
            print("       Fix: request access to this model in the Bedrock console (Model access), same region.")
        problems.append(text[:80])

    if problems:
        return 1
    print("\nReady. Run the inbox on Bedrock:  python -m munshi.run serve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
