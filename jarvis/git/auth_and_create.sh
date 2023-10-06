# vulcan/github_cli/auth.sh
#!/bin/bash

echo ==========gh auth login==========
gh auth login --with-token < $JARVIS_WORKSPACE/token.txt
gh auth status
rm $JARVIS_WORKSPACE/token.txt
echo ==================================

echo ==========issue create==========
_create_issue() {
	echo [DEBUG] create issue
	JARVIS_ISSUE_CREATE_RESULT=$(\
		gh issue create \
		-t "$(cat $JARVIS_OUTPUT_DIR/issue_title)" \
		-a "$GITHUB_ACTORY" \
		-b "$(cat $JARVIS_OUTPUT_DIR/issue_body)" \
	)
	printf "$JARVIS_ISSUE_CREATE_RESULT\n" > $JARVIS_OUTPUT_DIR/issue_link
}

python3 $GITHUB_ACTION_PATH/jarvis/git/issue_title_generator.py
python3 $GITHUB_ACTION_PATH/jarvis/git/issue_body_generator.py
_create_issue

