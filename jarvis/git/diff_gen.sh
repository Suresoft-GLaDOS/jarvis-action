#!/bin/bash

cd $JARVIS_WORKSPACE/JARVIS/workspace/home/workspace/$TARGET_REPO_NAME
echo $JARVIS_WORKSPACE/JARVIS/workspace/home/workspace/$TARGET_REPO_NAME 

mkdir patches

git diff -- ':(exclude)*/.staticdata/*' > fix_vioation.patch
mv fix_violation.patch $JARVIS_WORKSPACE/JARVIS/workspace/outputs
