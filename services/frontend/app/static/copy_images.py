import shutil
import os

source_dir = r"C:\Users\Lenovo\.gemini\antigravity-ide\brain\9d40dae4-5bcc-4503-8413-69c6ec2cb93e"
dest_dir = r"c:\Users\Lenovo\Desktop\Languages\Traffic Management System\services\frontend\app\static\img"

files_to_copy = {
    "triple_riding_1782061646138.png": "triple_riding_violation.png",
    "stop_line_1782061659112.png": "stop_line_violation.png",
    "wrong_side_1782061669041.png": "wrong_side_driving.png",
    "illegal_parking_1782061682488.png": "illegal_parking.png"
}

for src_name, dest_name in files_to_copy.items():
    src_path = os.path.join(source_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    shutil.copy2(src_path, dest_path)
    print(f"Copied {src_name} -> {dest_name}")

print("All images copied successfully.")
