version = "1.0"

import os
os.system("auto-py-to-exe -c config.json")
os.system("mkdir \"output/images\"")
os.system("xcopy \"images\" \"output/images\" /E/H/C/I")
os.system("mkdir \"output/data\"")
os.system("xcopy \"data\" \"output/data\" /E/H/C/I")
os.system(f"zip -r \"Minicraft {version}.zip\" \"output\"")
os.system("mkdir \"output/zip\"")
os.system(f"copy \"Minicraft {version}.zip\" \"output/zip\"")
os.system(f"del \"Minicraft {version}.zip\"")