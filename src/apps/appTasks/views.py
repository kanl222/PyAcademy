from django.shortcuts import render
import subprocess

import subprocess
import psutil

def run_python_code(code, input_data, timeout_seconds, memory_limit_mb):
    try:
        # Запуск процесса для выполнения кода
        process = subprocess.Popen(['python', '-c', code],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)

        # Установка ограничений по времени и памяти
        process_pid = process.pid
        process_resource = psutil.Process(process_pid)
        process_resource.cpu_limit(timeout_seconds)  # Ограничение времени выполнения
        process_resource.memory_limit(memory_limit_mb * 1024 * 1024)  # Ограничение памяти в байтах

        # Передача вводных данных в процесс
        stdout, stderr = process.communicate(input=input_data)
        if process.returncode == 0:
            return stdout.strip()  # Возвращаем вывод кода
        else:
            return stderr.strip()  # Возвращаем ошибку выполнения кода
    except Exception as e:
        return str(e)


def code_execution_view(request):
    if request.method == 'POST':
        code = request.POST.get('code', '')
        input_data = request.POST.get('input_data', '')  # Получаем вводные данные из POST-запроса
        result = run_python_code(code, input_data)
        context = {'result': result}
        return render(request, 'result.html', context)
    else:
        return render(request, 'code_input.html')
