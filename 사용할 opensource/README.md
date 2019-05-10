# 사용할 오픈 소스 사이트 

https://github.com/cal-pratt/SheetVision

# 기본적인 사용법

1. git을 이용해서 해당 사이트의 내용을 clone합니다.(복사한다는 뜻입니다.) 
  - "git clone" 이라고 google에 치면 쉽게 찾아서 볼 수 있을 겁니다.(그냥 간단하게 zip으로 다운도 가능)
  - https://emflant.tistory.com/218
2. clone한 파일을 가상환경을 통해서 실행해볼 겁니다.
  - 방법 여러가지 있습니다. 대게 pycharm , anaconda, visual studio를 이용하시면 기본으로 해줘서 신경 안써도 됩니다.
  - visual studio 이용하는 방법 : https://mainia.tistory.com/5182
  - 굳이 cmd로 하신다면 그렇게 하셔도 됩니다.
  - "python virtual environment" 또는 "python 가상환경" 설정 검색하시면 쉽게 볼 수 있을 겁니다.
3. 가상환경에 깔아야할 라이브러리
  - 가상 환경이 만들어지면 거기서 pip install을 하시면 됩니다.
  - pip install 사용하면 되는데 opencv 랑 midiUtil 설치하면 될 겁니다.
4. arg를 통해서 인자를 넘겨주는 방식을 사용합니다.
  - python main.py 파일의 절대 경로
  - ex) python main.py C:\Users\justi\SheetVision\resources\samples\fire.jpg
5. 이렇게 하고 기다리시면 바로 실행 됩니다.
  - 여기까지 꼭 할 것!

## 설치 명령어

- anaconda(패키지 관리 프로그램) 이용하면 편하다
- anaconda 프롬프트에서 다음 명령을 실행한다.
<br>

 - `python -m pip install opencv-python`<br>
   - opencv 모듈 설치<br>
 - `python -m pip install midiutil`<br>
   - midiutil 설치<br>
 - `pip install -U numpy`<br>
   - numpy 최신 버전으로 업데이트<br>
 - `python [MIDIUtil-0.89\MIDIUtil-0.89\setup.py 경로] install`<br>
   - setup.py가 midiutil 설치하는 데 필요한 명령 모아놓은 파일인 것 같은데 그 파일에 install 파라미터 넘겨줘서 설치.<br>

## 실행법
- `python main.py [출력할 악보 이미지 파일 경로]` 입력하면 됨.
- 비주얼 스튜디오에서 실행할 때는 SheetVision-master 프로젝트 속성 - 스크립트 인수에 악보 이미지 파일 경로 입력.