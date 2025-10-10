import os
import glob
import pandas as pd

# 결과를 저장할 리스트
data = []

# raw 폴더 내의 abft_*.txt 파일 모두 탐색
for filename in glob.glob("raw/grid-8/abft_*.txt"):
    try:
        base = os.path.splitext(os.path.basename(filename))[0]
        _, err_rate, inj_rate, run_id, k = base.split("_")
        err_rate = float(err_rate)
        inj_rate = float(inj_rate)
        run_id = int(run_id)
        k = int(k)
    except ValueError:
        print(f"Skipping malformed filename: {filename}")
        continue

    # 파일 내용 읽기
    values = {"err_rate": err_rate, "inj_rate": inj_rate, "run_id": run_id, "k": k}
    with open(filename, "r") as f:
        for line in f:
            if "=" in line:
                key, val = line.strip().split("=")
                if key in ["error", "detected", "abft_error"]:
                    values[key] = val.lower() == "true" or val == "1"
                else:
                    try:
                        values[key] = float(val)
                    except ValueError:
                        values[key] = val

    data.append(values)

# DataFrame 생성 및 CSV 저장
df = pd.DataFrame(data)
df.to_csv("abft_results_grid-8_v2.csv", index=False)
print("Saved to abft_results.csv")
