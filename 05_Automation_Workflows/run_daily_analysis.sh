#!/bin/bash

# ==========================================
# SPREP ClimSA Automation Pipeline
# Lecture 27: Scheduling Implementation using Cron
# Lecture 28: Logging & Error Handling
# ==========================================

# 1. 환경 설정 (Configuration)
# ------------------------------------------
# 현재 스크립트가 있는 경로를 프로젝트 루트로 설정
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
LOG_FILE="$PROJECT_DIR/daily_automation.log"
DATE=$(date "+%Y-%m-%d %H:%M:%S")

# 로그 시작 기록
echo "===================================================" >> $LOG_FILE
echo "[$DATE] 🚀 Starting Daily Climate Analysis Pipeline" >> $LOG_FILE
echo "===================================================" >> $LOG_FILE

# 2. [Step 1] 데이터 품질 관리 (Python QC)
# ------------------------------------------
echo "[$DATE] 1️⃣  Running Data QC (Python)..." >> $LOG_FILE

# 다른 폴더(02_Quality_Control)에 있는 Python 스크립트 실행
# 실제 환경에서는 가상환경 activate 명령어가 필요할 수 있음
# 예: source activate climsa_env
python3 "$PROJECT_DIR/../02_Quality_Control/qc_outlier_check.py" >> $LOG_FILE 2>&1

# 실행 결과 확인 (Exit Code: 0이면 성공, 아니면 실패)
if [ $? -eq 0 ]; then
    echo "[$DATE]    ✅ Python QC Script Completed Successfully." >> $LOG_FILE
else
    echo "[$DATE]    ❌ CRITICAL ERROR: Python QC Script Failed." >> $LOG_FILE
    # 파이썬이 실패하면 여기서 멈춤 (보고서 생성 안 함)
    exit 1
fi

# 3. [Step 2] 기후 보고서 생성 (R Markdown)
# ------------------------------------------
DATE=$(date "+%Y-%m-%d %H:%M:%S")
echo "[$DATE] 2️⃣  Generating Monthly Report (R)..." >> $LOG_FILE

# 같은 폴더에 있는 R 스크립트 실행
Rscript "$PROJECT_DIR/generate_report.R" >> $LOG_FILE 2>&1

if [ $? -eq 0 ]; then
    echo "[$DATE]    ✅ R Report Generated Successfully." >> $LOG_FILE
else
    echo "[$DATE]    ❌ ERROR: R Reporting Failed." >> $LOG_FILE
    exit 1
fi

# 4. 종료 (Completion)
# ------------------------------------------
END_DATE=$(date "+%Y-%m-%d %H:%M:%S")
echo "[$END_DATE] 🎉 All Tasks Finished Successfully." >> $LOG_FILE
echo "===================================================" >> $LOG_FILE
echo "" >> $LOG_FILE
