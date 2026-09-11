"""AgentCore Runtime entrypoint: `agentcore configure --entrypoint agentcore_app.py`."""

from munshi.app import app

if __name__ == "__main__":
    app.run()
