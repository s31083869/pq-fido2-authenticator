import { existsSync } from "node:fs";

const [, , script, ...args] = process.argv;

if (!script) {
  console.error("[run-bash] missing script path");
  process.exit(1);
}

function resolveBash(): string {
  if (process.env.GIT_BASH && existsSync(process.env.GIT_BASH)) {
    return process.env.GIT_BASH;
  }

  if (process.platform === "win32") {
    const candidates = [
      "C:\\Program Files\\Git\\bin\\bash.exe",
      "C:\\Program Files\\Git\\usr\\bin\\bash.exe",
      "C:\\Program Files (x86)\\Git\\bin\\bash.exe",
      "C:\\Program Files (x86)\\Git\\usr\\bin\\bash.exe",
    ];

    const gitBash = candidates.find((candidate) => existsSync(candidate));
    if (gitBash) {
      return gitBash;
    }

    console.error("[run-bash] Git for Windows bash.exe not found.");
    console.error("[run-bash] Install Git for Windows or set GIT_BASH to bash.exe.");
    process.exit(1);
  }

  return "bash";
}

const bash = resolveBash();
const child = Bun.spawnSync([bash, script, ...args], {
  cwd: process.cwd(),
  env: process.env,
  stdin: "inherit",
  stdout: "inherit",
  stderr: "inherit",
});

process.exit(child.exitCode ?? 1);
