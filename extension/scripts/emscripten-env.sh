#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXTENSION_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
EMSCRIPTEN_SHIM_DIR="$EXTENSION_ROOT/.deps/emscripten-shims"

to_bash_path() {
  local path="$1"
  if command -v cygpath >/dev/null 2>&1; then
    cygpath -u "$path" 2>/dev/null || printf '%s\n' "$path"
  else
    printf '%s\n' "$path"
  fi
}

latest_child_dir() {
  local parent="$1"
  if [[ ! -d "$parent" ]]; then
    return 1
  fi

  find "$parent" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort -Vr | head -n 1
}

write_windows_shim() {
  local tool="$1"
  local target="$2"
  local shim="$EMSCRIPTEN_SHIM_DIR/$tool"

  mkdir -p "$EMSCRIPTEN_SHIM_DIR"
  {
    echo "#!/usr/bin/env bash"
    printf 'exec %q "$@"\n' "$target"
  } >"$shim"
  chmod +x "$shim"
}

try_activate_windows_emsdk() {
  local emsdk_dir="$1"
  emsdk_dir="$(to_bash_path "$emsdk_dir")"

  local emscripten_dir="$emsdk_dir/upstream/emscripten"
  if [[ ! -f "$emscripten_dir/emcmake.bat" || ! -f "$emscripten_dir/emcc.bat" ]]; then
    return 1
  fi

  local python_dir
  local node_dir
  python_dir="$(latest_child_dir "$emsdk_dir/python" || true)"
  node_dir="$(latest_child_dir "$emsdk_dir/node" || true)"

  export EMSDK="$emsdk_dir"
  export EM_CONFIG="$emsdk_dir/.emscripten"

  if [[ -n "$node_dir" && -f "$node_dir/bin/node.exe" ]]; then
    export EMSDK_NODE="$node_dir/bin/node.exe"
    export PATH="$node_dir/bin:$PATH"
  fi

  if [[ -n "$python_dir" && -f "$python_dir/python.exe" ]]; then
    export PATH="$python_dir:$PATH"
  fi

  write_windows_shim emcmake "$emscripten_dir/emcmake.bat"
  write_windows_shim emcc "$emscripten_dir/emcc.bat"

  export PATH="$EMSCRIPTEN_SHIM_DIR:$emscripten_dir:$emsdk_dir:$PATH"
  return 0
}

add_windows_build_tool_paths() {
  local candidates=(
    "/c/mingw64/bin"
    "/c/msys64/mingw64/bin"
    "/c/msys64/usr/bin"
  )

  local path_dir
  for path_dir in "${candidates[@]}"; do
    if [[ -d "$path_dir" ]]; then
      export PATH="$path_dir:$PATH"
    fi
  done
}

ensure_emscripten_tool() {
  local tool="$1"
  local label="$2"

  local existing_tool
  existing_tool="$(command -v "$tool" 2>/dev/null || true)"
  if [[ -n "$existing_tool" && "$existing_tool" != *.bat && "$existing_tool" != *.cmd ]]; then
    return 0
  fi

  local candidates=()
  if [[ -n "${EMSDK:-}" ]]; then
    candidates+=("$EMSDK")
  fi

  candidates+=(
    "$HOME/emsdk"
    "/c/emsdk"
    "/d/emsdk"
  )

  local emsdk_dir
  for emsdk_dir in "${candidates[@]}"; do
    if try_activate_windows_emsdk "$emsdk_dir"; then
      if command -v "$tool" >/dev/null 2>&1; then
        echo "[$label] loaded Emscripten SDK from: $(to_bash_path "$emsdk_dir")"
        return 0
      fi
    fi
  done

  echo "[$label] $tool not found. Install Emscripten SDK, or set EMSDK to the emsdk directory." >&2
  echo "[$label] Windows default supported by this project: C:\\emsdk" >&2
  return 1
}
