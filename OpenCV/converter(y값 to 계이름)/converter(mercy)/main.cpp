#include <iostream>
using namespace std;

int getSound(int y, int line[], int lineSize[]);

int main()
{
	int line[5] = {10, 20, 30, 40, 50};
	int lineSize[5] = {1,1,1,1,1};
	int gap = line[1] - line[0];

	cout << getSound(12, line, lineSize);


	return 0;
}

int getSound(int y, int line[], int lineSize[])
{
	int gap = line[1] - line[0];

	if (line[0] - gap <= y && line[0] - gap + lineSize[0] >= y) //높은 라
	{
		return 0;
	}
	else if(line[0] - gap + lineSize[0] < y && line[0] > y) //높은 솔
	{
		return 1;
	}
	else if (line[0] <= y && line[0] + lineSize[0] >= y) //높은 파
	{
		return 2;
	}
	else if (line[0] + lineSize[0] < y && line[1] > y) //높은 미
	{
		return 3;
	}
	else if (line[1] <= y && line[1] + lineSize[1] >= y) //높은 레
	{
		return 4;
	}
	else if (line[1] + lineSize[1] < y && line[2] > y) //도
	{
		return 5;
	}
	else if (line[2] <= y && line[2] + lineSize[2] >= y) //시
	{
		return 6;
	}
	else if (line[2] + lineSize[2] < y && line[3] > y) //라
	{
		return 7;
	}
	else if (line[3] <= y && line[3] + lineSize[3] >= y) //솔
	{
		return 8;
	}
	else if (line[3] + lineSize[3] < y && line[4] > y) //파
	{
		return 9;
	}
	else if (line[4] <= y && line[4] + lineSize[4] >= y) //미
	{
		return 10;
	}
	else if (line[4] + lineSize[4] < y && line[4] + lineSize[4]+ gap > y) //레
	{
		return 11;
	}
	else //도
	{
		return 12;
	}
}