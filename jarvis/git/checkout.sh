# vulcan/github_cli/checkout.sh
#!/bin/bash

# shellcheck disable=SC2164
cd "$JARVIS_TARGET"

DESTINATION_BRANCH="$GITHUB_REF_NAME"

echo ==========Switching to $DESTINATION_BRANCH==========
git checkout $DESTINATION_BRANCH
git clean -f > /dev/null
echo ==================================
