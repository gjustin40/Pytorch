def detect(save_img=False):
    source, weights, view_img, save_txt, imgsz = opt.source, opt.weights, opt.view_img, opt.save_txt, opt.img_size
    webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
        ('rtsp://', 'rtmp://', 'http://')) # webcam일 때 숫자이고 나머지는 그냥 파일이름들

    # Directories
    save_dir = Path(increment_path(Path(opt.project) / opt.name, exist_ok=opt.exist_ok))  # # 파일 이름을 +1씩 하면서 생성
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # dir 만들기

    # Initialize
    set_logging() # 출력되는 warning 형식 변경
    device = select_device(opt.device) # device 사용할 인자 값 받아서 입력(01,2,3 등등)
    half = device.type != 'cpu'  # 그 딥러닝에서는 32bit 사용 안 하고 16bit만들로도 충분함. half percision이 16bit라는 뜻

    # Load Model
    model = attempt_load(weights, map_location=device)
    # assert : 오류가 생기면 그냥 assert 에러메세지 발생, 그리고 그냥 멈춤(그냥 확인용? 왜 하는거냐)
    # strip() : 문자열의 양쪽 빈 공간을 제거한다.
    # attempt_download() : github release가서 다운로드 받음. url = 'https://github.com/ultralytics/yolov3/releases/download/v1.0/' + file
    # for w in weights if isinstance(weights, list) else [weights]  : 반복열이 if문에 의해서 바뀐다.(weights -> [weights]) 즉, weights가 여러개면 그냥 weights, 1개면 [weights] 왜? 1개면 문자열 하나하나로 가니까 ㅋㅋㅋㅋ
    # .yaml 파일 : XML과 비슷한 거고 '인간이 쉽게 읽을 수 있는 데이터 직렬화 언어임'
    # torch.load('yolov5.pt')에서 pt값 뿐만 아니라 models도 불러와야 함.(models module 없다고 찡찡댐)
    # yaml 파일로 model을 만드는 부분을 잘 생각해야함. >>> 이거 아님. yaml 파일 지워도 작동 잘 함.... yolo.py 파일이 중요함


    # yolo.py 지지고 볶아보자.
    # yolo.py 지지고 볶기 전에 알아야 할 메소드들이 졸라 많음
    # Conv2d에서 group옵션의 효과 : AlexNet 처럼 group 수 만큼 나눠서 Conv을 진행한다. group=1이면 그냥 알던 conv, group=2면 AlexNet철머 위, 아래로 찢어져서 따로 Conv 진행
    # - 각 필터가 다른 양상을 학습하는 효과가 있다.

    