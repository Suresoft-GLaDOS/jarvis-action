# vulcan/github_cli/auth.sh
#!/bin/bash

git config --global --add safe.directory $TARGET_DIR
git config --global user.email "jarvis@action"
git config --global user.name "jarvis-action"