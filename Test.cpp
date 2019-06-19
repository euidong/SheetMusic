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

//midiOutShortMsg��� �Լ��� �Ķ���͸� ������־� ȣ���ϱ� ���� ����
static void midi(/*HMIDIOUT device, */int status, int channel, int low, int high)
{
	DWORD dwMsg = (status | channel | (high << 16) | (low << 8));
	midiOutShortMsg(mDevHandle, dwMsg);
}

//���� ���� �����Ű�� ���� ���̸�ŭ sleep�� ��, ���� �����ϴ� thread�Լ�
void Play(/*HMIDIOUT& device,*/ int delay, int channel, int tune, int volume)
{
	midi( 0x90, channel, tune, volume); //���� �Ѵ� �Լ�
	Sleep(delay);
	midi( 0x80, channel, tune, 0); //���� ����(���� �Լ�)
}
int main()
{
	//���� ���� ǥ���� �Ǻ� ������ �޾ƿ��� ����
	//ifstream inFile("TestData.txt");

	/* ���� ������� ������ (���籸����)
	int num; //�Է°��� ù���� ǥ���� ���� ������ ����ִ�.
	inFile >> num;
	int** data = new int*[num];
	for (int i = 0; i < num; i++)
	{
		data[i] = new int[3]; //�� ���� (���α׷��� ����� �ķ� ���� ó�� ����Ǵ� ����, ����, ���� ����) 3��Ҹ� ���Ϸκ��� �޾ƿ´�.
		inFile >> data[i][0] >> data[i][1] >> data[i][2];
	}

	//���� ������ midi�� ����ϱ� ���� �������� midiOutOpen�� ���� ���� ������ �ִ��� Ȯ���Ѵ�.
	mDevHandle=NULL;
	MMRESULT uiMidiOpen = 0;
	uiMidiOpen = midiOutOpen(&mDevHandle, MIDIMAPPER, 0, NULL, CALLBACK_FUNCTION);
	if (uiMidiOpen != MMSYSERR_NOERROR)
	{
		cout << "MIDI output error" << endl;
		return NULL;
	}


	//���� ������ ���� ���� ��� ��Ű�� ����
	int cnt = 0; //cnt�� ���� ���° ���� �ٷ���� ��Ÿ����.
	int cur_interval = data[0][0]; //cur_interval�� ���� �ٷ�� ���� �������� ó�� ����Ǵ� ������ ���̷�
									
	Sleep(cur_interval);//�������� �߻��� �� �����Ŀ� �������� �߻���ų���� �ٷ������ �ʿ��ϴ�.
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
	//���� �����Ҵ�� �Ǻ� ������ delete����
	for (int i = 0; i < num; i++)
	{
		delete data[i];
	}
	delete data;
	*/


	//���� ���������� �׽�Ʈ����
	ifstream inFile("TestData.txt");

	int table[13] = { 81,79,77,76,74,72,71,69,67,65,64,62,60 };  //�� �ε�����(i)�� �ش��ϴ� midi�������� ���̸��� mapping�س��� table
	//���� midi�� ����� ���� device�� open�Ͽ� ������ �ִ��� �����ϴ� ����. ���������� �� �߿伺 ����
	mDevHandle = NULL;
	MMRESULT uiMidiOpen = 0;
	uiMidiOpen = midiOutOpen(&mDevHandle, MIDIMAPPER, 0, NULL, CALLBACK_FUNCTION);
	if (uiMidiOpen != MMSYSERR_NOERROR)
	{
		cout << "MIDI output error" << endl;
		return NULL;
	}

	//temp�� inFile�� �鿩�� int�� �Ѱ� �������ִ� �뵵, cnt�� � �޾Ƶ鿴���� ���� �뵵
	int temp,cnt=0;
	//�޾Ƶ鿩�� ��� int���� vector�� ����
	vector<int> v;

	//�����Է��� ���� ������ ���Ϳ� TestData.txt�� ��� ���� �޾ƿͼ� ����
	while (!inFile.eof())
	{
		inFile >> temp;
		v.push_back(temp);
		cnt++;
	}

	//1�� �������� ���� ���
	for (int i = 0; i < cnt; i++)
	{
		midi(0x90, 0, table[v.at(i)], 127); //status�Ķ���ͷ�  0x90�� �ְԵǸ� �ش����� �Ѱڴٴ� �ǹ��̴�. (127�� �����ִ밪�� �ǹ� 0~127)
		Sleep(1000); //���� �������¿��� 1�ʰ� ����϶�� �ǹ��̴�.  ######���⼭ ���� ���� ��������#####
		midi(0x80, 0, table[v.at(i)]   , 0); //status�Ķ���ͷ� 0x80�� �ְԵǸ� �ش����� ���ڴٴ� �ǹ��̴�.
	}

	midiOutReset(mDevHandle);
	midiOutClose(mDevHandle);

	system("pause");
	inFile.close();
}