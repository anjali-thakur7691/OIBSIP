"""
===========================================
        AI Voice Assistant
        System Information Module
===========================================
Author : Anjali Thakur
Project : AI Voice Assistant
Internship : OASIS INFOBYTE
===========================================
"""

import os
import platform
import socket
import getpass
import psutil


# =========================================
# Get System Information
# =========================================

def get_system_info():

    try:

        username = getpass.getuser()

        computer_name = socket.gethostname()

        operating_system = (
            f"{platform.system()} "
            f"{platform.release()}"
        )

        processor = platform.processor()

        architecture = platform.architecture()[0]

        ram = round(
            psutil.virtual_memory().total /
            (1024 ** 3),
            2
        )

        cpu_usage = psutil.cpu_percent(interval=1)

        disk = psutil.disk_usage("/")

        disk_total = round(
            disk.total / (1024 ** 3),
            2
        )

        disk_used = round(
            disk.used / (1024 ** 3),
            2
        )

        disk_free = round(
            disk.free / (1024 ** 3),
            2
        )

        report = f"""
System Information

User Name : {username}

Computer Name : {computer_name}

Operating System : {operating_system}

Processor : {processor}

Architecture : {architecture}

RAM : {ram} GB

CPU Usage : {cpu_usage} %

Disk Total : {disk_total} GB

Disk Used : {disk_used} GB

Disk Free : {disk_free} GB
"""

        # ==========================
        # Battery Information
        # ==========================

        battery = psutil.sensors_battery()

        if battery:

            battery_percent = battery.percent

            charging = battery.power_plugged

            if charging:

                battery_status = "Charging"

            else:

                battery_status = "Not Charging"

        else:

            battery_percent = "Not Available"

            battery_status = "Unknown"

        # ==========================
        # IP Address
        # ==========================

        try:

            ip_address = socket.gethostbyname(socket.gethostname())

        except Exception:

            ip_address = "Not Available"

        # ==========================
        # RAM Usage
        # ==========================

        memory = psutil.virtual_memory()

        ram_used = round(
            memory.used / (1024 ** 3),
            2
        )

        ram_available = round(
            memory.available / (1024 ** 3),
            2
        )

        ram_percent = memory.percent

        report += f"""

Battery Percentage : {battery_percent}

Battery Status : {battery_status}

RAM Used : {ram_used} GB

RAM Available : {ram_available} GB

RAM Usage : {ram_percent} %

IP Address : {ip_address}

"""

        return report

    except Exception as e:

        return (
            "Unable to fetch system information.\n"
            f"Error: {str(e)}"
        )
    