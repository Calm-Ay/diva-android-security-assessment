#!/usr/bin/env bash
set -euo pipefail

project_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
tools_dir="$project_root/.tools"
venv_dir="$project_root/.venv-frida16"
version="16.6.6"
archive="$tools_dir/frida-server-${version}-android-x86_64.xz"
server="$tools_dir/frida-server-${version}-android-x86_64"
url="https://github.com/frida/frida/releases/download/${version}/frida-server-${version}-android-x86_64.xz"

mkdir -p "$tools_dir"
python3 -m venv "$venv_dir"
"$venv_dir/bin/pip" install "frida==${version}"
curl -fL --retry 3 "$url" -o "$archive"
xz -d -f "$archive"
chmod 700 "$server"
adb -s 127.0.0.1:6555 push "$server" /data/local/tmp/frida-server-16

printf 'Installed Frida %s and pushed the matching x86_64 server.\n' "$version"

