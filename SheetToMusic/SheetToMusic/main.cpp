#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/highgui/highgui.hpp"

using namespace cv;

#include <iostream>
#include <fstream>
#include <vector>

using namespace std;
//��ǥ, ���� ����
Mat Extract(Mat subimg);

//��ǥ�� ���̸����� ��ȯ 
int GetSound(int y, int line[], int lineSize[]);

//������ �и��մϴ�.
void CutMeasures(Mat img, Mat* measure, int size);

// ������ y��ǥ�� �޾ƿɴϴ�.
void GetLineY(Mat lineGetter, int* line, int* lineSize);
// ��ǥ�� �߾� ��ǥ ����
void GenerateNotePoints(const Mat& dot_image, vector<Point2d>& out_note_points);
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
	origin = imread("simple0.jpg", IMREAD_GRAYSCALE);

	//����ȭ(threshold = 200)
	threshold(origin, img, 100, 255, THRESH_BINARY);
	namedWindow("thresholding", WINDOW_AUTOSIZE);
	imshow("thresholding", img);



	//----------���� ���� ------------
	Mat measure[3]; // ���� 3��

	CutMeasures(img, measure, 3);

	imwrite("measure1.jpg", measure[0]);
	imwrite("measure2.jpg", measure[1]);
	imwrite("measure3.jpg", measure[2]);



	/* line ��ǥ�� �ޱ� */
	Mat lineGetter = imread("measure3.jpg", IMREAD_REDUCED_GRAYSCALE_2);
	namedWindow("2", WINDOW_AUTOSIZE);
	imshow("2", lineGetter);
	int line[5]; // ������ y���� ���� ����. 0 = �� �� ��, 4 = �� �Ʒ� ��
	int lineSize[5]; // ������ ���⸦ ���� ����

	GetLineY(lineGetter, line, lineSize);

	// ��ǥ �ܿ� ��� ������ ����
	for (int num = 0; num < 3; num++)
	{
		measure[num] = Extract(measure[num]);
	}

	imwrite("measure1-2.jpg", measure[0]);
	imwrite("measure2-2.jpg", measure[1]);
	imwrite("measure3-2.jpg", measure[2]);

	vector<Point2d> note_points;    // ���� ��ǥ ��ǥ�� �迭

	// ��ǥ ��ǥ �� note_points�� ����
	GenerateNotePoints(measure[2], note_points);
	// ã�� ��ǥ �ܼ� ���
	for (int i = 0; i < note_points.size(); i++) {
		std::cout << note_points[i].x << ", " << note_points[i].y << std::endl;
	}
	std::cout << "count: " << note_points.size() << std::endl;


	// ���̸� ���Ϸ� ��ȯ
	ofstream outfile("Sounds.txt");


	for (int i = 0; i < note_points.size(); i++)
	{
		outfile << GetSound(note_points[i].y, line, lineSize) << "  ";
	}

	outfile.close();

	while (waitKey(0) < 0);
	return 0;
}
// ��ǥ ��ǥ�� ���̸�
int GetSound(int y, int line[], int lineSize[])
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


// ��ǥ�� �߾� ��ǥ ���� out_note_points ���۷����� ����
void GenerateNotePoints(const Mat & dot_image, vector<Point2d>& out_note_points)
{
	int* num_black_x;    // x�࿡�� ���� �ȼ��� �� ���� �迭
	vector<int> points_x;	// x�࿡�� ��ǥ �ִ� ��ǥ(�߾� ����)

	num_black_x = new int[dot_image.cols];

	// ���� pixel count
	int line_sum = 0;
	cout << "x�� ����" << endl;
	line_sum = 0;
	for (int i = 0; i < dot_image.cols; i++) {
		for (int j = 0; j < dot_image.rows; j++) {
			if (dot_image.at<uchar>(j, i) < 125) {
				line_sum += 1;
			}
		}
		num_black_x[i] = line_sum;
		line_sum = 0;
	}

	// ������ ���� �� �ش�(�ֺ� ���� ���� �����ϴ� ��) ������ x�� �迭�� ����
	SetLocalMaxPoints(num_black_x, dot_image.cols, points_x);
	cout << "count: " << points_x.size() << endl;

	// ���� ��ǥ ��ǥ ���ϱ�
	int y;
	int x;
	for (int i = 0; i < points_x.size(); i++) {
		x = points_x[i];
		// x�� �����ϴ� y��ǥ ���ϱ�
		// ã�� x �ֺ� ��ġ(+-1) ������ �ش� ã��
		y = GetLocalMaxBlackPoint(dot_image, x - 1, x + 1);
		out_note_points.push_back(Point(x, y));
	}

	delete[] num_black_x;
}

// �迭���� �ش� ������ �ϴ� ������ out_points�� ����
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

// start, end x ���� ������ y���� ���� �ȼ� ���� ����
// ���� �ȼ� ���� �ش� ���� �ϴ� y ��ȯ.
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


//������ �и��մϴ�.
void CutMeasures(Mat img, Mat* measure, int size)
{
	threshold(img, img, 200, 255, THRESH_BINARY);
	int line[5] = { -1,-1,-1,-1,-1 }; // ������ y���� ���� ����. 0 = �� �� ��, 4 = �� �Ʒ� ��
	int lineSize[5] = { 0,0,0,0,0 }; // ������ ���⸦ ���� ����

	int count; // �ش� ���� ������ �ȼ��� ��
	int k; // k��° ����
	int l = 0; // l��° ����
	
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

			for (int m = 0; m < 5; m++)
			{
				line[m] = -1;
				lineSize[m] = 0;
			}
			l++;
		}
	}
}

// ������ Y��ǥ�� �޾ƿɴϴ�.
void GetLineY(Mat lineGetter, int* line, int* lineSize)
{
	threshold(lineGetter, lineGetter, 200, 255, THRESH_BINARY);
	for (int i = 0; i < 5; i++)
	{
		line[i] = -1;
		lineSize[i] = 0;
	}

	int count; // �ش� ���� ������ �ȼ��� ��
	int k; // k��° ����

	int gap; // ������ �Ÿ�
	for (int i = 0; i < lineGetter.rows; i++)
	{
		count = 0;
		for (int j = 0; j < lineGetter.cols; j++)
		{
			if (!lineGetter.at<uchar>(i, j)) // �������� ��� count++
			{
				count++;
			}
		}

		if (count / (float)lineGetter.cols > 0.8) //������ ��� ��ü ũ�⿡ 0.6�̻� ����
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
}

//��ǥ, ���� ���� �Լ�
Mat Extract(Mat subimg)
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
	namedWindow("delete", WINDOW_AUTOSIZE);
	imshow("delete", subimg);

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
	namedWindow("delete2", WINDOW_AUTOSIZE);
	imshow("delete2", subimg);


	//-------�������� ������ ���� ��ǥ ����---------
	Mat enroded, dilated;

	dilate(subimg, enroded, Mat());//ħ��
	erode(enroded, dilated, Mat());//��â
	erode(dilated, enroded, Mat());//��â
	erode(enroded, dilated, Mat());//��â
	
	dilate(dilated, enroded, Mat());//ħ��
	dilate(enroded, dilated, Mat());//ħ��

	dilate(dilated, enroded, Mat());//ħ��
	dilate(enroded, dilated, Mat());//ħ��
	dilate(dilated, enroded, Mat());//ħ��
	dilate(enroded, dilated, Mat());//ħ��
	dilate(dilated, enroded, Mat());//ħ��
	dilate(enroded, dilated, Mat());//ħ��

	erode(enroded, dilated, Mat());//��â
	erode(dilated, enroded, Mat());//��â
	erode(enroded, dilated, Mat());//��â
	erode(dilated, enroded, Mat());//��â
	erode(enroded, dilated, Mat());//��â
	erode(dilated, enroded, Mat());//��â



	//��ǥ ���� ��� print
	namedWindow("mo0", WINDOW_AUTOSIZE);
	imshow("mo0", dilated);

	//-----median filter�� ���� noise����-----
	Mat medianFilteredImg;
	medianBlur(dilated, medianFilteredImg, 5);
	//median filter ���� ��� print
	namedWindow("medianFilteredImg", WINDOW_AUTOSIZE);
	imshow("medianFilteredImg", dilated);

	return dilated;
}