import subprocess
import time

# Sleep for a short duration to allow PyInstaller to extract the bundled scripts
time.sleep(2)

# Run get_temp script
get_temp_process = subprocess.Popen(["python", "get_temp.py"])

# Wait for get_temp to finish
get_temp_process.wait()

# Sleep for a while to make sure get_temp script has completed and written the file
time.sleep(2)

# Run read_temp script
subprocess.call(["python", "read_temp.py"])

