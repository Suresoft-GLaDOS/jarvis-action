#!/bin/bash

cd $JARVIS_WORKSPACE/JARVIS/workspace/home/workspace/JARVIS_demo
echo $JARVIS_WORKSPACE/JARVIS/workspace/home/workspace/$TARGET_REPO_NAME 

mkdir patches

git diff -- ':(exclude)*/.staticdata/*' > $JARVIS_WORKSPACE/JARVIS/workspace/outputs/fix_violation.patch
# mv $JARVIS_WORKSPACE/JARVIS/workspace/outputs/fix_violation.patch $JARVIS_WORKSPACE/JARVIS/workspace/outputs
