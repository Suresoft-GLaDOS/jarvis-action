#!/bin/bash

echo JARVIS_WORKSPACE=$JARVIS_WORKSPACE
JARVIS_OUTPUT_DIR=$JARVIS_WORKSPACE/JARVIS/workspace/outputs

git config --global --add safe.directory "$JARVIS_TARGET"
git config --global user.email "jarvis@action"
git config --global user.name "jarvis-action"

echo ==========gh auth login==========
gh auth login --with-token < $JARVIS_WORKSPACE/token.txt
gh auth status

echo ==================================

echo ==========issue create==========
_create_issue() {
	cd $JARVIS_TARGET
	echo [DEBUG] create issue
	JARVIS_ISSUE_CREATE_RESULT=$(\
		gh issue create \
		-t "$(cat $JARVIS_OUTPUT_DIR/issue_title)" \
		-a "$GITHUB_ACTORY" \
		-b "$(cat $JARVIS_OUTPUT_DIR/issue_body)" \
	)
	printf "$JARVIS_ISSUE_CREATE_RESULT\n" > $JARVIS_OUTPUT_DIR/issue_link
}

# echo "DIFFGEN"
# export TARGET_REPO_NAME=$TARGET_REPO_NAME; sh $JARVIS_WORKSPACE/scripts/git/diff_gen.sh
python3 $JARVIS_WORKSPACE/scripts/git/issue_title_generator.py
python3 $JARVIS_WORKSPACE/scripts/git/issue_body_generator.py

_create_issue 
python3 $JARVIS_WORKSPACE/scripts/git/create-pull-request.py
rm $JARVIS_WORKSPACE/token.txt