#!/usr/bin/env bash
set -euo pipefail

: "${WORKDIR:=$PWD}"
: "${PID_FILE:=pipeline.pid}"
: "${CONSOLE_LOG:=pipeline_console.log}"
: "${PREFIX:=md}"
: "${LOG_DIR:=logs}"
: "${TAIL_LINES:=40}"

cd "${WORKDIR}"

echo "Working directory: $(pwd)"

if [[ -f "${PID_FILE}" ]]; then
  pid="$(cat "${PID_FILE}")"
  echo "PID: ${pid}"
  if ps -p "${pid}" >/dev/null 2>&1; then
    echo "Status: running"
    ps -fp "${pid}" || true
  else
    echo "Status: not running"
  fi
else
  echo "PID: unavailable (${PID_FILE} not found)"
fi

echo
echo "Latest pipeline console lines:"
if [[ -f "${CONSOLE_LOG}" ]]; then
  tail -n "${TAIL_LINES}" "${CONSOLE_LOG}"
else
  echo "${CONSOLE_LOG} not found"
fi

echo
echo "Existing output files:"
for path in \
  processed.gro boxed.gro solv.gro ions.tpr solv_ions.gro \
  em.tpr em.gro nvt.tpr nvt.gro nvt.cpt npt.tpr npt.gro npt.cpt \
  "${PREFIX}.tpr" "${PREFIX}.gro" "${PREFIX}.cpt" "${PREFIX}.xtc" "${PREFIX}.log" \
  "${PREFIX}_centered.xtc" "${PREFIX}_centered_nopbc.xtc"; do
  if [[ -e "${path}" ]]; then
    ls -lh "${path}"
  fi
done

echo
echo "Step logs:"
if [[ -d "${LOG_DIR}" ]]; then
  ls -lh "${LOG_DIR}"/*.log 2>/dev/null || echo "No step logs found"
else
  echo "${LOG_DIR} not found"
fi

echo
echo "Production progress:"
if [[ -f "${PREFIX}.log" ]]; then
  awk '
    /^           Step/ {
      if (getline > 0) {
        step=$1
        time_ps=$2
      }
    }
    END {
      if (step != "") {
        printf "latest_step=%s time_ps=%s\n", step, time_ps
      } else {
        print "No production step records found yet"
      }
    }
  ' "${PREFIX}.log"
else
  echo "${PREFIX}.log not found"
fi

if [[ -f FAILED_STEP.txt ]]; then
  echo
  echo "Failed step: $(cat FAILED_STEP.txt)"
fi
