#!/usr/bin/env bash
set -euo pipefail

# Pipeline mode: full_background_pipeline_mode.
# Launch from the working directory with:
#   nohup bash run_explicit_water_pipeline.sh > pipeline_console.log 2>&1 & echo $! > pipeline.pid

# -----------------------------
# User-configurable variables
# -----------------------------
: "${INPUT_PDB:=input.pdb}"
: "${WORKDIR:=$PWD}"
: "${PREFIX:=md}"
: "${GMX_BIN:=gmx}"
: "${MDP_DIR:=mdp}"
: "${FORCE_FIELD_SELECTION:=amber99sb-ildn}"
: "${WATER_SELECTION:=tip3p}"
: "${BOX_DISTANCE:=1.2}"
: "${BOX_TYPE:=triclinic}"
: "${POSITIVE_ION:=NA}"
: "${NEGATIVE_ION:=CL}"
: "${SALT_CONC:=0.15}"
: "${GPU_ID:=0}"
: "${NTOMP:=32}"
: "${RUN_PRODUCTION:=yes}"
: "${RUN_PBC_POSTPROCESS:=no}"
: "${CENTER_GROUP:=}"
: "${OUTPUT_GROUP:=}"
: "${FIT_GROUP:=}"

LOG_DIR="logs"
FAILED_STEP_FILE="FAILED_STEP.txt"
ENV_LOG="${LOG_DIR}/00_environment.log"

step_name="initialization"
step_log=""

fail() {
  local message="$1"
  printf 'ERROR [%s]: %s\n' "${step_name}" "${message}" >&2
  if [[ -n "${step_log}" ]]; then
    printf 'Inspect log: %s\n' "${step_log}" >&2
  fi
  printf '%s\n' "${step_name}" > "${FAILED_STEP_FILE}"
  exit 1
}

on_error() {
  local exit_code=$?
  printf 'FAILED step: %s\n' "${step_name}" >&2
  if [[ -n "${step_log}" ]]; then
    printf 'Inspect log: %s\n' "${step_log}" >&2
  fi
  printf '%s\n' "${step_name}" > "${FAILED_STEP_FILE}"
  exit "${exit_code}"
}
trap on_error ERR

require_file() {
  local path="$1"
  [[ -f "${path}" ]] || fail "Required file not found: ${path}"
}

require_dir() {
  local path="$1"
  [[ -d "${path}" ]] || fail "Required directory not found: ${path}"
}

require_output() {
  local path="$1"
  [[ -s "${path}" ]] || fail "Expected output file missing or empty: ${path}"
}

run_logged() {
  step_name="$1"
  step_log="$2"
  shift 2
  printf '\n[%s] %s\n' "$(date '+%F %T')" "${step_name}"
  "$@" 2>&1 | tee "${step_log}"
}

run_logged_stdin() {
  step_name="$1"
  step_log="$2"
  local stdin_text="$3"
  shift 3
  printf '\n[%s] %s\n' "$(date '+%F %T')" "${step_name}"
  printf '%b' "${stdin_text}" | "$@" 2>&1 | tee "${step_log}"
}

run_logged_stdin_append() {
  step_name="$1"
  step_log="$2"
  local stdin_text="$3"
  shift 3
  printf '\n[%s] %s\n' "$(date '+%F %T')" "${step_name}"
  printf '%b' "${stdin_text}" | "$@" 2>&1 | tee -a "${step_log}"
}

mkdir -p "${WORKDIR}"
cd "${WORKDIR}"
mkdir -p "${LOG_DIR}"
rm -f "${FAILED_STEP_FILE}"

step_name="input validation"
step_log="${ENV_LOG}"
{
  printf 'Pipeline mode: full_background_pipeline_mode\n'
  printf 'Started: %s\n' "$(date '+%F %T')"
  printf 'Host: %s\n' "$(hostname)"
  printf 'Working directory: %s\n' "$(pwd)"
  printf 'INPUT_PDB=%s\n' "${INPUT_PDB}"
  printf 'PREFIX=%s\n' "${PREFIX}"
  printf 'GMX_BIN=%s\n' "${GMX_BIN}"
  printf 'MDP_DIR=%s\n' "${MDP_DIR}"
  printf 'FORCE_FIELD_SELECTION=%s\n' "${FORCE_FIELD_SELECTION}"
  printf 'WATER_SELECTION=%s\n' "${WATER_SELECTION}"
  printf 'BOX_DISTANCE=%s\n' "${BOX_DISTANCE}"
  printf 'BOX_TYPE=%s\n' "${BOX_TYPE}"
  printf 'POSITIVE_ION=%s\n' "${POSITIVE_ION}"
  printf 'NEGATIVE_ION=%s\n' "${NEGATIVE_ION}"
  printf 'SALT_CONC=%s\n' "${SALT_CONC}"
  printf 'GPU_ID=%s\n' "${GPU_ID}"
  printf 'NTOMP=%s\n' "${NTOMP}"
  printf 'RUN_PRODUCTION=%s\n' "${RUN_PRODUCTION}"
  printf 'RUN_PBC_POSTPROCESS=%s\n' "${RUN_PBC_POSTPROCESS}"
  printf 'CENTER_GROUP=%s\n' "${CENTER_GROUP}"
  printf 'OUTPUT_GROUP=%s\n' "${OUTPUT_GROUP}"
  printf 'FIT_GROUP=%s\n' "${FIT_GROUP}"
  printf '\nGROMACS version:\n'
  "${GMX_BIN}" --version
} 2>&1 | tee "${ENV_LOG}"

cat <<'STATUS_COMMANDS'

Background launch command:
  nohup bash run_explicit_water_pipeline.sh > pipeline_console.log 2>&1 & echo $! > pipeline.pid

Status helper commands:
  tail -f pipeline_console.log
  cat pipeline.pid
  ps -fp $(cat pipeline.pid)

STATUS_COMMANDS

require_file "${INPUT_PDB}"
require_dir "${MDP_DIR}"
require_file "${MDP_DIR}/ions.mdp"
require_file "${MDP_DIR}/em.mdp"
require_file "${MDP_DIR}/nvt.mdp"
require_file "${MDP_DIR}/npt.mdp"
require_file "${MDP_DIR}/md.mdp"

step_name="01_pdb2gmx"
step_log="${LOG_DIR}/01_pdb2gmx.log"
require_file "${INPUT_PDB}"
run_logged "${step_name}" "${step_log}" \
  "${GMX_BIN}" pdb2gmx \
  -f "${INPUT_PDB}" \
  -o processed.gro \
  -p topol.top \
  -i posre.itp \
  -ff "${FORCE_FIELD_SELECTION}" \
  -water "${WATER_SELECTION}" \
  -ignh
require_output processed.gro
require_output topol.top

step_name="02_editconf"
step_log="${LOG_DIR}/02_editconf.log"
require_file processed.gro
run_logged "${step_name}" "${step_log}" \
  "${GMX_BIN}" editconf \
  -f processed.gro \
  -o boxed.gro \
  -c \
  -d "${BOX_DISTANCE}" \
  -bt "${BOX_TYPE}"
require_output boxed.gro

step_name="03_solvate"
step_log="${LOG_DIR}/03_solvate.log"
require_file boxed.gro
require_file topol.top
run_logged "${step_name}" "${step_log}" \
  "${GMX_BIN}" solvate \
  -cp boxed.gro \
  -cs spc216.gro \
  -o solv.gro \
  -p topol.top
require_output solv.gro
require_output topol.top

step_name="04_grompp_ions"
step_log="${LOG_DIR}/04_grompp_ions.log"
require_file "${MDP_DIR}/ions.mdp"
require_file solv.gro
require_file topol.top
run_logged "${step_name}" "${step_log}" \
  "${GMX_BIN}" grompp \
  -f "${MDP_DIR}/ions.mdp" \
  -c solv.gro \
  -p topol.top \
  -o ions.tpr
require_output ions.tpr

step_name="05_genion"
step_log="${LOG_DIR}/05_genion.log"
require_file ions.tpr
require_file topol.top
run_logged_stdin "${step_name}" "${step_log}" "SOL\n" \
  "${GMX_BIN}" genion \
  -s ions.tpr \
  -o solv_ions.gro \
  -p topol.top \
  -pname "${POSITIVE_ION}" \
  -nname "${NEGATIVE_ION}" \
  -conc "${SALT_CONC}" \
  -neutral
require_output solv_ions.gro
require_output topol.top

step_name="06_grompp_em"
step_log="${LOG_DIR}/06_grompp_em.log"
require_file "${MDP_DIR}/em.mdp"
require_file solv_ions.gro
require_file topol.top
run_logged "${step_name}" "${step_log}" \
  "${GMX_BIN}" grompp \
  -f "${MDP_DIR}/em.mdp" \
  -c solv_ions.gro \
  -p topol.top \
  -o em.tpr
require_output em.tpr

step_name="07_mdrun_em"
step_log="${LOG_DIR}/07_mdrun_em.log"
require_file em.tpr
run_logged "${step_name}" "${step_log}" \
  "${GMX_BIN}" mdrun \
  -deffnm em \
  -ntmpi 1 \
  -ntomp "${NTOMP}"
require_output em.gro

step_name="08_grompp_nvt"
step_log="${LOG_DIR}/08_grompp_nvt.log"
require_file "${MDP_DIR}/nvt.mdp"
require_file em.gro
require_file topol.top
run_logged "${step_name}" "${step_log}" \
  "${GMX_BIN}" grompp \
  -f "${MDP_DIR}/nvt.mdp" \
  -c em.gro \
  -r em.gro \
  -p topol.top \
  -o nvt.tpr
require_output nvt.tpr

step_name="09_mdrun_nvt"
step_log="${LOG_DIR}/09_mdrun_nvt.log"
require_file nvt.tpr
run_logged "${step_name}" "${step_log}" \
  "${GMX_BIN}" mdrun \
  -deffnm nvt \
  -ntmpi 1 \
  -ntomp "${NTOMP}" \
  -gpu_id "${GPU_ID}"
require_output nvt.gro
require_output nvt.cpt

step_name="10_grompp_npt"
step_log="${LOG_DIR}/10_grompp_npt.log"
require_file "${MDP_DIR}/npt.mdp"
require_file nvt.gro
require_file nvt.cpt
require_file topol.top
run_logged "${step_name}" "${step_log}" \
  "${GMX_BIN}" grompp \
  -f "${MDP_DIR}/npt.mdp" \
  -c nvt.gro \
  -r nvt.gro \
  -t nvt.cpt \
  -p topol.top \
  -o npt.tpr
require_output npt.tpr

step_name="11_mdrun_npt"
step_log="${LOG_DIR}/11_mdrun_npt.log"
require_file npt.tpr
run_logged "${step_name}" "${step_log}" \
  "${GMX_BIN}" mdrun \
  -deffnm npt \
  -ntmpi 1 \
  -ntomp "${NTOMP}" \
  -gpu_id "${GPU_ID}"
require_output npt.gro
require_output npt.cpt

step_name="12_grompp_md"
step_log="${LOG_DIR}/12_grompp_md.log"
require_file "${MDP_DIR}/md.mdp"
require_file npt.gro
require_file npt.cpt
require_file topol.top
run_logged "${step_name}" "${step_log}" \
  "${GMX_BIN}" grompp \
  -f "${MDP_DIR}/md.mdp" \
  -c npt.gro \
  -t npt.cpt \
  -p topol.top \
  -o "${PREFIX}.tpr"
require_output "${PREFIX}.tpr"

if [[ "${RUN_PRODUCTION}" == "yes" || "${RUN_PRODUCTION}" == "true" || "${RUN_PRODUCTION}" == "1" ]]; then
  step_name="13_mdrun_md"
  step_log="${LOG_DIR}/13_mdrun_md.log"
  require_file "${PREFIX}.tpr"
  run_logged "${step_name}" "${step_log}" \
    "${GMX_BIN}" mdrun \
    -deffnm "${PREFIX}" \
    -ntmpi 1 \
    -ntomp "${NTOMP}" \
    -gpu_id "${GPU_ID}" \
    -pin on
  require_output "${PREFIX}.gro"
  require_output "${PREFIX}.cpt"
  require_output "${PREFIX}.log"
else
  printf '\n[%s] 13_mdrun_md skipped because RUN_PRODUCTION=%s\n' "$(date '+%F %T')" "${RUN_PRODUCTION}" | tee "${LOG_DIR}/13_mdrun_md.log"
fi

step_name="14_pbc_postprocess"
step_log="${LOG_DIR}/14_pbc_postprocess.log"
if [[ "${RUN_PBC_POSTPROCESS}" == "yes" || "${RUN_PBC_POSTPROCESS}" == "true" || "${RUN_PBC_POSTPROCESS}" == "1" ]]; then
  if [[ -z "${CENTER_GROUP}" || -z "${OUTPUT_GROUP}" || -z "${FIT_GROUP}" ]]; then
    {
      printf 'PBC postprocess skipped: CENTER_GROUP, OUTPUT_GROUP, and FIT_GROUP must all be configured.\n'
      printf 'Manual example:\n'
      printf '  printf "Protein\\nSystem\\n" | %s trjconv -s %s.tpr -f %s.xtc -o %s_centered.xtc -pbc mol -center\n' "${GMX_BIN}" "${PREFIX}" "${PREFIX}" "${PREFIX}"
      printf '  printf "Backbone\\nSystem\\n" | %s trjconv -s %s.tpr -f %s_centered.xtc -o %s_centered_nopbc.xtc -fit rot+trans\n' "${GMX_BIN}" "${PREFIX}" "${PREFIX}" "${PREFIX}"
    } | tee "${step_log}"
  else
    require_file "${PREFIX}.tpr"
    require_file "${PREFIX}.xtc"
    run_logged_stdin "${step_name}_center" "${step_log}" "${CENTER_GROUP}\n${OUTPUT_GROUP}\n" \
      "${GMX_BIN}" trjconv \
      -s "${PREFIX}.tpr" \
      -f "${PREFIX}.xtc" \
      -o "${PREFIX}_centered.xtc" \
      -pbc mol \
      -center
    require_output "${PREFIX}_centered.xtc"
    run_logged_stdin_append "${step_name}_fit" "${step_log}" "${FIT_GROUP}\n${OUTPUT_GROUP}\n" \
      "${GMX_BIN}" trjconv \
      -s "${PREFIX}.tpr" \
      -f "${PREFIX}_centered.xtc" \
      -o "${PREFIX}_centered_nopbc.xtc" \
      -fit rot+trans
    require_output "${PREFIX}_centered_nopbc.xtc"
  fi
else
  printf '\n[%s] 14_pbc_postprocess skipped because RUN_PBC_POSTPROCESS=%s\n' "$(date '+%F %T')" "${RUN_PBC_POSTPROCESS}" | tee "${step_log}"
fi

printf '\nPipeline completed successfully at %s\n' "$(date '+%F %T')"
