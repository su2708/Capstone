import subprocess

def main():
    source = "0"
    img_size = 160
    #weights = "best.pt" --weights {weights}

    # detect.py를 실행하는 명령어를 만듭니다.
    cmd = f"python detect.py --source {source} --img-size {img_size} "

    # subprocess를 사용하여 명령어를 실행합니다.
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
