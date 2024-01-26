#!/bin/bash

cd $JARVIS_WORKSPACE/JARVIS/workspace/home/workspace/$TARGET_REPO_NAME
echo $JARVIS_WORKSPACE/JARVIS/workspace/home/workspace/$TARGET_REPO_NAME 

mkdir patches

# 현재 변경 사항이 있는 파일 목록 가져옴.
files=$(git diff --name-only)
​git config --global core.autocrlf true
# 각 파일별로 diff를 생성합니다.
for file in $files; do
    # 경로에서 슬래시를 대시로 대체하여 파일명을 생성
    # diff_file="$(echo $file | sed 's/\//_/g').diff"
    echo "MKDIR $JARVIS_WORKSPACE/JARVIS/workspace/outputs/$file.diff"
    mkdir -p "$JARVIS_WORKSPACE/JARVIS/workspace/outputs/$file.diff"
    rm -rf "$JARVIS_WORKSPACE/JARVIS/workspace/outputs/$file.diff"
    # git diff 결과를 파일에 저장
    git diff -- --ignore-space-at-eol "$file" > "$JARVIS_WORKSPACE/JARVIS/workspace/outputs/$file.diff"
    echo "Saved diff for $file to $JARVIS_WORKSPACE/JARVIS/workspace/outputs/$file.diff"
done

