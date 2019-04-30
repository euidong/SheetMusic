#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/highgui/highgui.hpp"

using namespace cv;

#include <iostream>
#include <fstream>
using namespace std;

Mat extract(Mat subimg);
int getSound(int y, int line[], int lineSize[]);

// arr�� �ش��� out_points vector�� ��� �Լ�
void SetLocalMaxPoints(const int* arr, const int arr_size, std::vector<int>& out_points);
// image x ���� ������ black �ش� �ϳ� get
int GetLocalMaxBlackPoint(const Mat& image, const int start_x, const int end_x);
// array���� �ش� �ϳ� return.
int GetLocalMaxPoint(const int * arr, const int arr_size);
int main()
{
	Mat origin;
	Mat img;
	int count2;

	//grayscale�� ��ȯ - img read
	origin = imread("simple32.jpg", IMREAD_GRAYSCALE);
	//namedWindow("grayscale", WINDOW_AUTOSIZE);
	//imshow("grayscale", origin);

	//����ȭ(threshold = 200)
	threshold(origin, img, 100, 255, THRESH_BINARY);
	//namedWindow("thresholding", WINDOW_AUTOSIZE);
	//imshow("thresholding", img);

	//----------���� ����------------
	
	int line[5] = { -1,-1,-1,-1,-1 }; // ������ y���� ���� ����. 0 = �� �� ��, 4 = �� �Ʒ� ��
	int lineSize[5] = { 0,0,0,0,0 }; // ������ ���⸦ ���� ����

	int count; // �ش� ���� ������ �ȼ��� ��
	int k; // k��° ����
	int l = 0; // l��° ����
	Mat measure[3]; // ���� 3��
	int gap; // ������ �Ÿ�
	for (int i = 0; i < img.rows; i++)
	{
		count = 0;
		for (int j = 0; j < img.cols; j++)
		{
			if (!img.at<uchar>(i, j)) // �������� ��� count++
			{
				count++;
			}
		}

		if (count / (float)img.cols > 0.6) //������ ��� ��ü ũ�⿡ 0.6�̻� ����
		{
			k = 0;
			while (k < 5)
			{
				if (line[k] == -1)
				{
					break;
				}
				k++;
			}

			if (k == 0)
			{
				line[0] = i;
				lineSize[0]++;
			}
			else if (line[k - 1] + lineSize[k - 1] == i)
			{
				lineSize[k - 1]++;
			}
			else
			{
				line[k] = i;
				lineSize[k]++;
			}
		}
		else if (line[4] != -1) //�������ٿ� ���� ä������ ������ �Ѿ���
		{
			gap = line[1] - line[0];
			Rect rect(0, line[0] - (gap * 1.5), img.cols, line[4] - line[0] + (gap * 4));
			
			measure[l] = img(rect);
			for (int p = 0; p < 5; p++)
			{
				cout << p + 1 << "��° �� ��ǥ : " << line[p] << endl << p + 1 << "��° ���� ���� : " << lineSize[p] << endl << endl;
			}
			for (int m = 0; m < 5; m++)
			{
				line[m] = -1;
				lineSize[m] = 0;
			}
			l++;
			cout << "l: " << l << endl;
		}
	}
	imwrite("measure1.jpg", measure[0]);
	imwrite("measure2.jpg", measure[1]);
	imwrite("measure3.jpg", measure[2]);


	//namedWindow("ù ����", WINDOW_AUTOSIZE);
	//imshow("ù ����", measure[0]);
	//namedWindow("��° ����", WINDOW_AUTOSIZE);
	//imshow("��° ����", measure[1]);
	//namedWindow("��° ����", WINDOW_AUTOSIZE);
	//imshow("��° ����", measure[2]);
	
	
	Mat subimg = measure[0];
	
	//Mat subimg = img;
	namedWindow("crop", WINDOW_AUTOSIZE);
	imshow("crop", subimg);
	
	for (int num = 0;num < 3; num++)
	{
		measure[num] = extract(measure[num]);
	}

	imwrite("measure1-2.jpg", measure[0]);
	imwrite("measure2-2.jpg", measure[1]);
	imwrite("measure3-2.jpg", measure[2]);





	Mat music_image;
	int* num_black_x;    // x�࿡�� ���� �ȼ��� �� ���� �迭
	std::vector<int> points_x;	// x�࿡�� ��ǥ �ִ� ��ǥ(�߾� ����)
	std::vector<Point2d> note_points;    // ���� ��ǥ ��ǥ(�߾� ����)

	music_image = imread("measure3-2.jpg", IMREAD_REDUCED_GRAYSCALE_2);
	// 2bit ��� �̹��� �о����

	num_black_x = new int[music_image.cols];

	// ���� pixel count
	int line_sum = 0;
	std::cout << "x�� ����" << std::endl;
	line_sum = 0;
	for (int i = 0; i < music_image.cols; i++) {
		for (int j = 0; j < music_image.rows; j++) {
			if (music_image.at<uchar>(j, i) < 125) {
				line_sum += 1;
			}
		}
		/*if (line_sum != 0) {
			std::cout << i << " " << line_sum << std::endl;
		}*/
		num_black_x[i] = line_sum;
		line_sum = 0;
	}


	std::cout << "------------------------------" << std::endl;

	std::cout << "x�� ���� �ִ� ��ǥ" << std::endl;
	SetLocalMaxPoints(num_black_x, music_image.cols, points_x);
	std::cout << "count: " << points_x.size() << std::endl;

	// ���� ��ǥ ��ǥ ���ϱ�
	int y;
	int x;
	for (int i = 0; i < points_x.size(); i++) {
		x = points_x[i];
		// x�� �����ϴ� y��ǥ x +- 1�� crop�ؼ� �ش����� ���ϱ�
		y = GetLocalMaxBlackPoint(music_image, x - 1, x + 1);
		note_points.push_back(Point(x, y));
	}

	for (int i = 0; i < note_points.size(); i++) {
		std::cout << note_points[i].x << ", " << note_points[i].y << std::endl;
	}
	std::cout << "count: " << note_points.size() << std::endl;


	delete[] num_black_x;

	Mat lineGeter = imread("measure3.jpg", IMREAD_REDUCED_GRAYSCALE_2);
	threshold(lineGeter, lineGeter, 200, 255, THRESH_BINARY);
	namedWindow("2", WINDOW_AUTOSIZE);
	imshow("2", lineGeter);

	for (int i = 0; i < lineGeter.rows; i++)
	{
		count = 0;
		for (int j = 0; j < lineGeter.cols; j++)
		{
			if (!lineGeter.at<uchar>(i, j)) // �������� ��� count++
			{
				count++;
			}
		}

		if (count / (float)lineGeter.cols > 0.8) //������ ��� ��ü ũ�⿡ 0.6�̻� ����
		{
			k = 0;
			while (k < 5)
			{
				if (line[k] == -1)
				{
					break;
				}
				k++;
			}

			if (k == 0)
			{
				line[0] = i;
				lineSize[0]++;
			}
			else if (line[k - 1] + lineSize[k - 1] == i)
			{
				lineSize[k - 1]++;
			}
			else
			{
				line[k] = i;
				lineSize[k]++;
			}
		}
	}

	ofstream outfile("Sounds.txt");
	

	for (int i = 0; i < note_points.size(); i++)
	{
		outfile << getSound(note_points[i].y, line, lineSize) << "  ";
	}

	outfile.close();
	while (waitKey(0) < 0);
	return 0;
}

int getSound(int y, int line[], int lineSize[])
{
	int gap = line[1] - line[0];
	int range = gap / 4;
	if (line[0] - gap - range <= y && line[0] - gap + lineSize[0] + range >= y) //���� ��
	{
		return 0;
	}
	else if (line[0] - range > y) //���� ��
	{
		return 1;
	}
	else if (line[0] + lineSize[0] + range >= y) //���� ��
	{
		return 2;
	}
	else if (line[1] - range > y) //���� ��
	{
		return 3;
	}
	else if (line[1] + lineSize[1] + range >= y) //���� ��
	{
		return 4;
	}
	else if (line[2] - range > y) //���� ��
	{
		return 5;
	}
	else if (line[2] + lineSize[2] + range >= y) //��
	{
		return 6;
	}
	else if (line[3] - range > y) //��
	{
		return 7;
	}
	else if (line[3] + lineSize[3] + range >= y) //��
	{
		return 8;
	}
	else if (line[4] - range > y) //��
	{
		return 9;
	}
	else if (line[4] + lineSize[4] + range >= y) //��
	{
		return 10;
	}
	else if (line[4] + lineSize[4] + gap - range > y) //��
	{
		return 11;
	}
	else //��
	{
		return 12;
	}
}


void SetLocalMaxPoints(const int * arr, const int arr_size, std::vector<int>& out_points)
{
	bool is_rising = false;
	bool is_same = false;
	int same_start = 0;
	int local_max;
	for (int i = 0; i < arr_size - 1; i++) {
		// �ö󰡴� �������� �ش�
		if (arr[i] > arr[i + 1] && is_rising) {
			if (is_same) {
				local_max = int((same_start + i) / 2);
			}
			else {
				local_max = i;
			}
			out_points.push_back(local_max);

			is_rising = false;
			is_same = false;
		}
		else if (arr[i] < arr[i + 1]) {
			is_rising = true;
			is_same = false;
		}
		else if (arr[i] == arr[i + 1] && !is_same) {
			is_same = true;
			same_start = i;
		}

	}
}

int GetLocalMaxBlackPoint(const Mat & image, const int start_x, const int end_x)
{
	int* num_black;    // y�࿡�� ���� �ȼ��� �� ���� �迭
	int crop_size;

	crop_size = end_x - start_x + 1;
	num_black = new int[image.rows];

	// ���� pixel count
	int line_sum = 0;
	for (int i = 0; i < image.rows; i++) {
		for (int j = start_x; j <= end_x; j++) {
			if (image.at<uchar>(i, j) < 125) {
				line_sum += 1;
			}
		}
		num_black[i] = line_sum;
		line_sum = 0;
	}

	int local_max = GetLocalMaxPoint(num_black, image.rows);

	delete[] num_black;

	return local_max;
}

int GetLocalMaxPoint(const int * arr, const int arr_size)
{
	bool is_rising = false;
	bool is_same = false;
	int same_start = 0;
	int local_max;
	for (int i = 0; i < arr_size; i++) {
		// �ö󰡴� �������� �ش�
		if (arr[i] > arr[i + 1] && is_rising) {
			if (is_same) {
				local_max = int((same_start + i) / 2);
			}
			else {
				local_max = i;
			}
			return local_max;

			is_rising = false;
			is_same = false;
		}
		else if (arr[i] < arr[i + 1]) {
			is_rising = true;
			is_same = false;
		}
		else if (arr[i] == arr[i + 1] && !is_same) {
			is_same = true;
			same_start = i;
		}
	}
	return -1;
}


//��ǥ ���� �Լ�
Mat extract(Mat subimg) 
{
	int count2;

	//---------����(���μ�) ����--------
	for (int i = 0; i < subimg.rows; i++)
	{
		count2 = 0;
		for (int j = 0; j < subimg.cols; j++)
		{
			//�������̸� count����
			if (!subimg.at<uchar>(i, j))
			{
				count2++;
			}
		}
		//80%�Ѿ�� ������ �Ǵ�
		if (count2 / (float)subimg.cols > 0.8)
		{
			//�ش� line������� ��ȯ
			for (int p = 0; p < subimg.cols; p++)
			{
				subimg.at<uchar>(i, p) = (uchar)255;
			}
		}

	}
	//���μ� ���� ��� print
	//namedWindow("delete", WINDOW_AUTOSIZE);
	//imshow("delete", subimg);

	//---------���μ� ����--------
	for (int i = 0; i < subimg.cols; i++)
	{
		count2 = 0;
		for (int j = 0; j < subimg.rows; j++)
		{
			//�������̸� count����
			if (!subimg.at<uchar>(j, i))
			{
				count2++;
			}
		}
		//20%�� �Ѿ�� ������ �Ǵ�
		if (count2 / (float)subimg.rows > 0.2)
		{
			for (int p = 0; p < subimg.rows; p++)
			{
				subimg.at<uchar>(p, i) = (uchar)255;
			}
		}
	}
	//���μ� ���� ��� print
	//namedWindow("delete2", WINDOW_AUTOSIZE);
	//imshow("delete2", subimg);


	//-------�������� ������ ���� ��ǥ ����---------
	Mat enroded, dilated;
	dilate(subimg, enroded, Mat());//ħ��
	erode(enroded, dilated, Mat());//��â
	erode(dilated, enroded, Mat());//��â
	erode(enroded, dilated, Mat());//��â
	dilate(dilated, enroded, Mat());//ħ��
	dilate(enroded, dilated, Mat());//ħ��
	//��ǥ ���� ��� print
	//namedWindow("mo0", WINDOW_AUTOSIZE);
	//imshow("mo0", dilated);

	//-----median filter�� ���� noise����-----
	Mat medianFilteredImg;
	medianBlur(dilated, medianFilteredImg, 5);
	//median filter ���� ��� print
	//namedWindow("medianFilteredImg", WINDOW_AUTOSIZE);
	//imshow("medianFilteredImg", dilated);

	return dilated;
}