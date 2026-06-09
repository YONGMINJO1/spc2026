#!/usr/bin/env python3

import json
import sys
import subprocess
import threading
import os


LOG_FILE = "debug_proxy.log"


def log_message(msg):
    """로그를 stderr과 별도 파일에 동시 출력"""
    print(msg, file=sys.stderr)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
        f.flush()


def main():
    if len(sys.argv) < 2:
        log_message("[PROXY] 사용법: python debug_proxy.py <서버파일>")
        return

    server_file = sys.argv[1]

    # 로그 파일 초기화
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("=== MCP Proxy Debug Log ===\n")

    log_message(f"[PROXY] 서버 시작: {server_file}")

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUNBUFFERED"] = "1"

    server = subprocess.Popen(
        ["python", server_file],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
        env=env,
    )

    def log_server_stderr():
        """서버 stderr 출력 로깅"""
        while True:
            try:
                line = server.stderr.readline()
                if not line:
                    break

                log_message(f"[SERVER_OUTPUT] {line.rstrip()}")

            except Exception as e:
                log_message(f"[PROXY] stderr 읽기 오류: {e}")
                break

    stderr_thread = threading.Thread(
        target=log_server_stderr,
        daemon=True,
    )
    stderr_thread.start()

    log_message("[PROXY] 메시지 중계 시작")

    def read_from_server():
        """서버 출력을 읽어서 클라이언트로 전달"""

        while True:
            try:
                line = server.stdout.readline()

                if not line:
                    break

                line = line.strip()

                if not line:
                    continue

                try:
                    msg = json.loads(line)
                    log_message(
                        "\n[S->C] "
                        + json.dumps(
                            msg,
                            indent=2,
                            ensure_ascii=False,
                        )
                    )
                except json.JSONDecodeError:
                    log_message(f"[S->C] {line}")

                print(line, flush=True)

            except Exception as e:
                log_message(f"[PROXY] 서버 읽기 에러: {e}")
                break

    server_thread = threading.Thread(
        target=read_from_server,
        daemon=True,
    )
    server_thread.start()

    try:
        while True:
            line = sys.stdin.readline()

            if not line:
                break

            line = line.strip()

            if not line:
                continue

            try:
                msg = json.loads(line)
                log_message(
                    "\n[C->S] "
                    + json.dumps(
                        msg,
                        indent=2,
                        ensure_ascii=False,
                    )
                )
            except json.JSONDecodeError:
                log_message(f"[C->S] {line}")

            if server.stdin:
                server.stdin.write(line + "\n")
                server.stdin.flush()

    except KeyboardInterrupt:
        log_message("[PROXY] 사용자 종료")

    except Exception as e:
        log_message(f"[PROXY] 에러: {e}")

    finally:
        try:
            server.terminate()
            server.wait(timeout=5)
        except Exception:
            try:
                server.kill()
            except Exception:
                pass

        log_message("[PROXY] 종료")


if __name__ == "__main__":
    main()