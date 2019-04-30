#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/highgui/highgui.hpp"

using namespace cv;

#include <iostream>
#include <fstream>
#include <vector>

using namespace std;
//음표, 오선 추출
Mat Extract(Mat subimg);

//좌표를 계이름으로 변환 
int GetSound(int y, int line[], int lineSize[]);

//소절을 분리합니다.
void CutMeasures(Mat img, Mat* measure, int size);

// 라인의 y좌표를 받아옵니다.
void GetLineY(Mat lineGetter, int* line, int* lineSize);
// 음표의 중앙 좌표 생성
void GenerateNotePoints(const Mat& dot_image, vector<Point2d>& out_note_points);
// arr의 극댓값을 out_points vector에 담는 함수
void SetLocalMaxPoints(const int* arr, const int arr_size, std::vector<int>& out_points);
// image x 범위 내에서 black 극댓값 하나 get
int GetLocalMaxBlackPoint(const Mat& image, const int start_x, const int end_x);
// array에서 극댓값 하나 return.
int GetLocalMaxPoint(const int * arr, const int arr_size);

int main()
{
	Mat origin;
	Mat img;
	int count2;

	//grayscale로 변환 - img read
	origin = imread("simple0.jpg", IMREAD_GRAYSCALE);

	//이진화(threshold = 200)
	threshold(origin, img, 100, 255, THRESH_BINARY);
	namedWindow("thresholding", WINDOW_AUTOSIZE);
	imshow("thresholding", img);



	//----------소절 분할 ------------
	Mat measure[3]; // 소절 3개

	CutMeasures(img, measure, 3);

	imwrite("measure1.jpg", measure[0]);
	imwrite("measure2.jpg", measure[1]);
	imwrite("measure3.jpg", measure[2]);



	/* line 좌표값 받기 */
	Mat lineGetter = imread("measure3.jpg", IMREAD_REDUCED_GRAYSCALE_2);
	namedWindow("2", WINDOW_AUTOSIZE);
	imshow("2", lineGetter);
	int line[5]; // 오선의 y값을 받을 변수. 0 = 맨 윗 줄, 4 = 맨 아래 줄
	int lineSize[5]; // 오선의 굵기를 받을 변수

	GetLineY(lineGetter, line, lineSize);

	// 음표 외에 모든 데이터 제거
	for (int num = 0; num < 3; num++)
	{
		measure[num] = Extract(measure[num]);
	}

	imwrite("measure1-2.jpg", measure[0]);
	imwrite("measure2-2.jpg", measure[1]);
	imwrite("measure3-2.jpg", measure[2]);

	vector<Point2d> note_points;    // 최종 음표 좌표값 배열

	// 음표 좌표 값 note_points에 저장
	GenerateNotePoints(measure[2], note_points);
	// 찾은 좌표 콘솔 출력
	for (int i = 0; i < note_points.size(); i++) {
		std::cout << note_points[i].x << ", " << note_points[i].y << std::endl;
	}
	std::cout << "count: " << note_points.size() << std::endl;


	// 계이름 파일로 반환
	ofstream outfile("Sounds.txt");


	for (int i = 0; i < note_points.size(); i++)
	{
		outfile << GetSound(note_points[i].y, line, lineSize) << "  ";
	}

	outfile.close();

	while (waitKey(0) < 0);
	return 0;
}
// 음표 좌표로 계이름
int GetSound(int y, int line[], int lineSize[])
{
	int gap = line[1] - line[0];
	int range = gap / 4;
	if (line[0] - gap - range <= y && line[0] - gap + lineSize[0] + range >= y) //높은 라
	{
		return 0;
	}
	else if (line[0] - range > y) //높은 솔
	{
		return 1;
	}
	else if (line[0] + lineSize[0] + range >= y) //높은 파
	{
		return 2;
	}
	else if (line[1] - range > y) //높은 미
	{
		return 3;
	}
	else if (line[1] + lineSize[1] + range >= y) //높은 레
	{
		return 4;
	}
	else if (line[2] - range > y) //높은 도
	{
		return 5;
	}
	else if (line[2] + lineSize[2] + range >= y) //시
	{
		return 6;
	}
	else if (line[3] - range > y) //라
	{
		return 7;
	}
	else if (line[3] + lineSize[3] + range >= y) //솔
	{
		return 8;
	}
	else if (line[4] - range > y) //파
	{
		return 9;
	}
	else if (line[4] + lineSize[4] + range >= y) //미
	{
		return 10;
	}
	else if (line[4] + lineSize[4] + gap - range > y) //레
	{
		return 11;
	}
	else //도
	{
		return 12;
	}
}


// 음표의 중앙 좌표 값을 out_note_points 레퍼런스에 저장
void GenerateNotePoints(const Mat & dot_image, vector<Point2d>& out_note_points)
{
	int* num_black_x;    // x축에서 검은 픽셀의 수 동적 배열
	vector<int> points_x;	// x축에서 음표 있는 좌표(중앙 지점)

	num_black_x = new int[dot_image.cols];

	// 검은 pixel count
	int line_sum = 0;
	cout << "x축 분포" << endl;
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

	// 검은색 분포 중 극댓값(주변 비해 많이 분포하는 값) 가지는 x를 배열에 저장
	SetLocalMaxPoints(num_black_x, dot_image.cols, points_x);
	cout << "count: " << points_x.size() << endl;

	// 최종 음표 좌표 구하기
	int y;
	int x;
	for (int i = 0; i < points_x.size(); i++) {
		x = points_x[i];
		// x에 대응하는 y좌표 구하기
		// 찾은 x 주변 위치(+-1) 에서만 극댓값 찾음
		y = GetLocalMaxBlackPoint(dot_image, x - 1, x + 1);
		out_note_points.push_back(Point(x, y));
	}

	delete[] num_black_x;
}

// 배열에서 극댓값 가지게 하는 변수를 out_points에 저장
void SetLocalMaxPoints(const int * arr, const int arr_size, std::vector<int>& out_points)
{
	bool is_rising = false;
	bool is_same = false;
	int same_start = 0;
	int local_max;
	for (int i = 0; i < arr_size - 1; i++) {
		// 올라가다 떨어지면 극댓값
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

// start, end x 범위 내에서 y값당 검은 픽셀 개수 세기
// 검은 픽셀 수가 극댓값 갖게 하는 y 반환.
int GetLocalMaxBlackPoint(const Mat & image, const int start_x, const int end_x)
{
	int* num_black;    // y축에서 검은 픽셀의 수 동적 배열
	int crop_size;

	crop_size = end_x - start_x + 1;
	num_black = new int[image.rows];

	// 검은 pixel count
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
		// 올라가다 떨어지면 극댓값
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


//소절을 분리합니다.
void CutMeasures(Mat img, Mat* measure, int size)
{
	threshold(img, img, 200, 255, THRESH_BINARY);
	int line[5] = { -1,-1,-1,-1,-1 }; // 오선의 y값을 받을 변수. 0 = 맨 윗 줄, 4 = 맨 아래 줄
	int lineSize[5] = { 0,0,0,0,0 }; // 오선의 굵기를 받을 변수

	int count; // 해당 행의 검은색 픽셀의 수
	int k; // k번째 라인
	int l = 0; // l번째 소절
	
	int gap; // 오선간 거리

	for (int i = 0; i < img.rows; i++)
	{
		count = 0;
		for (int j = 0; j < img.cols; j++)
		{
			if (!img.at<uchar>(i, j)) // 검은색인 경우 count++
			{
				count++;
			}
		}

		if (count / (float)img.cols > 0.6) //오선인 경우 전체 크기에 0.6이상 차지
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
		else if (line[4] != -1) //마지막줄에 값이 채워졌고 오선을 넘어선경우
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

// 라인의 Y좌표를 받아옵니다.
void GetLineY(Mat lineGetter, int* line, int* lineSize)
{
	threshold(lineGetter, lineGetter, 200, 255, THRESH_BINARY);
	for (int i = 0; i < 5; i++)
	{
		line[i] = -1;
		lineSize[i] = 0;
	}

	int count; // 해당 행의 검은색 픽셀의 수
	int k; // k번째 라인

	int gap; // 오선간 거리
	for (int i = 0; i < lineGetter.rows; i++)
	{
		count = 0;
		for (int j = 0; j < lineGetter.cols; j++)
		{
			if (!lineGetter.at<uchar>(i, j)) // 검은색인 경우 count++
			{
				count++;
			}
		}

		if (count / (float)lineGetter.cols > 0.8) //오선인 경우 전체 크기에 0.6이상 차지
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

//음표, 오선 추출 함수
Mat Extract(Mat subimg)
{
	int count2;

	//---------오선(가로선) 제거--------
	for (int i = 0; i < subimg.rows; i++)
	{
		count2 = 0;
		for (int j = 0; j < subimg.cols; j++)
		{
			//검은색이면 count증가
			if (!subimg.at<uchar>(i, j))
			{
				count2++;
			}
		}
		//80%넘어가면 선으로 판단
		if (count2 / (float)subimg.cols > 0.8)
		{
			//해당 line흰색으로 변환
			for (int p = 0; p < subimg.cols; p++)
			{
				subimg.at<uchar>(i, p) = (uchar)255;
			}
		}

	}
	//가로선 제거 결과 print
	namedWindow("delete", WINDOW_AUTOSIZE);
	imshow("delete", subimg);

	//---------세로선 제거--------
	for (int i = 0; i < subimg.cols; i++)
	{
		count2 = 0;
		for (int j = 0; j < subimg.rows; j++)
		{
			//검은색이면 count증가
			if (!subimg.at<uchar>(j, i))
			{
				count2++;
			}
		}
		//20%가 넘어가면 선으로 판단
		if (count2 / (float)subimg.rows > 0.2)
		{
			for (int p = 0; p < subimg.rows; p++)
			{
				subimg.at<uchar>(p, i) = (uchar)255;
			}
		}
	}
	//세로선 제거 결과 print
	namedWindow("delete2", WINDOW_AUTOSIZE);
	imshow("delete2", subimg);


	//-------모폴로지 연산을 통한 음표 추출---------
	Mat enroded, dilated;

	dilate(subimg, enroded, Mat());//침식
	erode(enroded, dilated, Mat());//팽창
	erode(dilated, enroded, Mat());//팽창
	erode(enroded, dilated, Mat());//팽창
	
	dilate(dilated, enroded, Mat());//침식
	dilate(enroded, dilated, Mat());//침식

	dilate(dilated, enroded, Mat());//침식
	dilate(enroded, dilated, Mat());//침식
	dilate(dilated, enroded, Mat());//침식
	dilate(enroded, dilated, Mat());//침식
	dilate(dilated, enroded, Mat());//침식
	dilate(enroded, dilated, Mat());//침식

	erode(enroded, dilated, Mat());//팽창
	erode(dilated, enroded, Mat());//팽창
	erode(enroded, dilated, Mat());//팽창
	erode(dilated, enroded, Mat());//팽창
	erode(enroded, dilated, Mat());//팽창
	erode(dilated, enroded, Mat());//팽창



	//음표 추출 결과 print
	namedWindow("mo0", WINDOW_AUTOSIZE);
	imshow("mo0", dilated);

	//-----median filter를 통한 noise제거-----
	Mat medianFilteredImg;
	medianBlur(dilated, medianFilteredImg, 5);
	//median filter 적용 결과 print
	namedWindow("medianFilteredImg", WINDOW_AUTOSIZE);
	imshow("medianFilteredImg", dilated);

	return dilated;
}