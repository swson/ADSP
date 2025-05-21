import os
import re

for root, _, files in os.walk("./src"):
    for file in files:
        if file.endswith(".cpp"):
            path = os.path.join(root, file)
            with open(path, "r") as f:
                content = f.read()
            # .values → .values.data(), but ignore .values.size()
            content = re.sub(r'\.values(?!\s*\.\s*size)', '.values.data()', content)
            with open(path, "w") as f:
                f.write(content)
