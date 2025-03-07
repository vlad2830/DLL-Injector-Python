from pymem import Pymem
from pymem.process import inject_dll_from_path
import base64
import ctypes
import time
import psutil

def encrypt_path(path):
    return base64.b64encode(path.encode()).decode()

dll_path = input("Enter the DLL PATH: ")
encrypted_dll_path = encrypt_path(dll_path)
process_name = input("Enter the process name: ")

open_process = Pymem(process_name)

actual_dll_path = base64.b64decode(encrypted_dll_path).decode()

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

def suspend_thread(thread_handle):
    kernel32.SuspendThread(thread_handle)

def resume_thread(thread_handle):
    kernel32.ResumeThread(thread_handle)

def suspend_process(process):
    process_psutil = psutil.Process(process.process_id)
    for thread in process_psutil.threads():
        thread_handle = kernel32.OpenThread(0x0002, False, thread.id)
        suspend_thread(thread_handle)
        kernel32.CloseHandle(thread_handle)

def resume_process(process):
    process_psutil = psutil.Process(process.process_id)
    for thread in process_psutil.threads():
        thread_handle = kernel32.OpenThread(0x0002, False, thread.id)
        resume_thread(thread_handle)
        kernel32.CloseHandle(thread_handle)

suspend_process(open_process)

time.sleep(0.100)

inject_dll_from_path(open_process.process_handle, actual_dll_path)

resume_process(open_process)

print("DLL injected successfully")