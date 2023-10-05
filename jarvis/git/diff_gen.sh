#!/bin/bash

cd $JARVIS_WORKSPACE/JARVIS/workspace/$COPIED_WORKSPACE/$TARGET_REPO_NAME
echo $COPIED_WORKSPACE

mkdir patches

git diff -- ':(exclude)*/.staticdata/*' > fix_vioation.patch
