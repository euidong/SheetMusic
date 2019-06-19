#include <iostream>
#include <fstream>
//#include <thread>
#include <windows.h>
#include <mmsystem.h>
//#include <process.h>
#include <vector>
#pragma comment(lib, "winmm.lib")
using namespace std;
HMIDIOUT mDevHandle;

//midiOutShortMsg라는 함수의 파라미터를 만들어주어 호출하기 위한 구문
static void midi(/*HMIDIOUT device, */int status, int channel, int low, int high)
{
	DWORD dwMsg = (status | channel | (high << 16) | (low << 8));
	midiOutShortMsg(mDevHandle, dwMsg);
}

//이하 음을 재생시키고 음의 길이만큼 sleep한 뒤, 음을 종료하는 thread함수
void Play(/*HMIDIOUT& device,*/ int delay, int channel, int tune, int volume)
{
	midi( 0x90, channel, tune, volume); //음을 켜는 함수
	Sleep(delay);
	midi( 0x80, channel, tune, 0); //음을 종료(끄는 함수)
}
int main()
{
	//이하 수로 표현된 악보 데이터 받아오는 구문
	//ifstream inFile("TestData.txt");

	/* 이하 쓰레드로 구현시 (현재구현중)
	int num; //입력값의 첫줄은 표현된 음의 개수가 들어있다.
	inFile >> num;
	int** data = new int*[num];
	for (int i = 0; i < num; i++)
	{
		data[i] = new int[3]; //각 음당 (프로그램이 실행된 후로 음이 처음 재생되는 시점, 음정, 음의 길이) 3요소를 파일로부터 받아온다.
		inFile >> data[i][0] >> data[i][1] >> data[i][2];
	}

	//이하 구문은 midi를 사용하기 위한 구문으로 midiOutOpen을 통해 열고 에러가 있는지 확인한다.
	mDevHandle=NULL;
	MMRESULT uiMidiOpen = 0;
	uiMidiOpen = midiOutOpen(&mDevHandle, MIDIMAPPER, 0, NULL, CALLBACK_FUNCTION);
	if (uiMidiOpen != MMSYSERR_NOERROR)
	{
		cout << "MIDI output error" << endl;
		return NULL;
	}


	//이하 구문은 실제 음을 재생 시키는 구문
	int cnt = 0; //cnt는 현재 몇번째 음을 다루는지 나타낸다.
	int cur_interval = data[0][0]; //cur_interval은 현재 다루는 음과 이전음의 처음 재생되는 시점의 차이로
									
	Sleep(cur_interval);//이전음이 발생된 후 몇초후에 현재음을 발생시킬지를 다루기위해 필요하다.
	_beginthread()
	thread t1(Play, data[cnt][2], 0, data[cnt][1], 127);
	/*while (num-1 > cnt)
	{
		cnt++;
		cur_interval = data[cnt][0] - data[cnt - 1][0];

		Sleep(cur_interval);
		thread t1(Play, data[cnt][2], 0, data[cnt][1], 127);

	}
	Sleep(2000);
	thread(Play, data[1][2], 0, data[1][1], 127);
	thread t3(Play, data[2][2], 0, data[2][1], 127);
	
	Sleep(1000);
	thread t4(Play, data[3][2], 0, data[3][1], 127);
	thread t5(Play, data[4][2], 0, data[4][1], 127);
	Sleep(5000);

	midiOutReset(mDevHandle);
	midiOutClose(mDevHandle);
	//이하 동적할당된 악보 데이터 delete구문
	for (int i = 0; i < num; i++)
	{
		delete data[i];
	}
	delete data;
	*/


	//이하 쓰레드제거 테스트버전
	ifstream inFile("TestData.txt");

	int table[13] = { 81,79,77,76,74,72,71,69,67,65,64,62,60 };  //각 인덱스값(i)에 해당하는 midi내에서의 계이름을 mapping해놓은 table
	//이하 midi의 출력을 위한 device를 open하여 에러가 있는지 점검하는 구문. 세부적으로 알 중요성 없음
	mDevHandle = NULL;
	MMRESULT uiMidiOpen = 0;
	uiMidiOpen = midiOutOpen(&mDevHandle, MIDIMAPPER, 0, NULL, CALLBACK_FUNCTION);
	if (uiMidiOpen != MMSYSERR_NOERROR)
	{
		cout << "MIDI output error" << endl;
		return NULL;
	}

	//temp는 inFile로 들여온 int값 한개 저장해주는 용도, cnt는 몇개 받아들였는지 세는 용도
	int temp,cnt=0;
	//받아들여온 모든 int값을 vector에 저장
	vector<int> v;

	//파일입력이 끝날 때까지 벡터에 TestData.txt의 모든 값을 받아와서 저장
	while (!inFile.eof())
	{
		inFile >> temp;
		v.push_back(temp);
		cnt++;
	}

	//1초 간격으로 음을 출력
	for (int i = 0; i < cnt; i++)
	{
		midi(0x90, 0, table[v.at(i)], 127); //status파라미터로  0x90을 주게되면 해당음을 켜겠다는 의미이다. (127은 볼륨최대값을 의미 0~127)
		Sleep(1000); //음이 켜진상태에서 1초간 대기하라는 의미이다.  ######여기서 음의 길이 조절가능#####
		midi(0x80, 0, table[v.at(i)]   , 0); //status파라미터로 0x80을 주게되면 해당음을 끄겠다는 의미이다.
	}

	midiOutReset(mDevHandle);
	midiOutClose(mDevHandle);

	system("pause");
	inFile.close();
}