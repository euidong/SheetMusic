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
