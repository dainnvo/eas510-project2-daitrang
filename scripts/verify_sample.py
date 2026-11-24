"""Run sample with network calls denied; compare against existing metric evidence."""
import ctypes
import json
from pathlib import Path
import platform
import runpy
import socket
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
expected = json.loads((ROOT / "results/sample/metrics.json").read_text(encoding="utf-8"))


def deny_network(*args, **kwargs):
    raise RuntimeError("Network is disabled for sample verification")


socket.create_connection = deny_network
socket.socket.connect = deny_network
socket.socket.connect_ex = deny_network
sys.argv = [str(ROOT / "main.py")]
start = time.perf_counter()
runpy.run_path(str(ROOT / "main.py"), run_name="__main__")
elapsed = time.perf_counter() - start
actual = json.loads((ROOT / "results/sample/metrics.json").read_text(encoding="utf-8"))
for name, metrics in expected["models"].items():
    for key in ("accuracy", "macro_f1", "weighted_f1"):
        assert abs(metrics[key] - actual["models"][name][key]) <= 1e-5
if sys.platform == "win32":
    from ctypes import wintypes
    class Counters(ctypes.Structure):
        _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD)] + [
            (name, ctypes.c_size_t) for name in ("PeakWorkingSetSize", "WorkingSetSize",
                "QuotaPeakPagedPoolUsage", "QuotaPagedPoolUsage", "QuotaPeakNonPagedPoolUsage",
                "QuotaNonPagedPoolUsage", "PagefileUsage", "PeakPagefileUsage")]
    counters = Counters()
    counters.cb = ctypes.sizeof(counters)
    if not ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.c_void_p(-1), ctypes.byref(counters), counters.cb):
        raise ctypes.WinError()
    peak_mib = counters.PeakWorkingSetSize / (1024 ** 2)
else:
    import resource
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_mib = peak / (1024 ** 2 if sys.platform == "darwin" else 1024)
result = {"python": platform.python_version(), "platform": platform.platform(),
          "sample_network_calls_denied": True, "sample_matches_saved_metrics": True,
          "metric_tolerance": 1e-5, "sample_wall_seconds_including_imports": elapsed,
          "peak_process_memory_mib": peak_mib,
          "full_raw_dataset_present": (ROOT / "data/raw/ESConv.json").exists()}
from src.data import save_json
save_json(ROOT / "results/verification.json", result)
print(json.dumps(result, indent=2))
