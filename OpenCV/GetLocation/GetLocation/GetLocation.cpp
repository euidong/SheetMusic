#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>
#include <vector>

#define MAX_PIXEL 255

using namespace cv;

// arr의 극댓값을 out_points vector에 담는 함수
void SetLocalMaxPoints(const int* arr, const int arr_size, std::vector<int>& out_points);

int main() {
	Mat music_image;
	int* num_black_x;    // x축에서 검은 픽셀의 수 동적 배열
	int* num_black_y;    // y축에서 검은 픽셀의 수 동적 배열
	std::vector<int> points_x;	// x축에서 음표 있는 좌표(중앙 지점)
	std::vector<int> points_y;	// y축에서 음표 있는 좌표(중앙 지점)
	std::vector<Point2d> note_points;    // 최종 음표 좌표(중앙 지점)

	music_image = imread("dot_image_big.jpg", IMREAD_REDUCED_GRAYSCALE_2);
	// 2bit 흑백 이미지 읽어오기
	
	num_black_x = new int[music_image.cols];
	num_black_y = new int[music_image.rows];

	// 검은 pixel count
	std::cout << "y축 분포" << std::endl;
	int line_sum = 0;
	for (int i = 0; i < music_image.rows; i++) {
		for (int j = 0; j < music_image.cols; j++) {
			if (music_image.at<uchar>(i, j) < 125) {
				line_sum += 1;
			}
		}
		/*if (line_sum != 0) {
			std::cout << i << " " << line_sum << std::endl;
		}*/
		num_black_y[i] = line_sum;
		line_sum = 0;
	}
	
	std::cout << "x축 분포" << std::endl;
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

	std::cout << "y축 국소 최대 좌표" << std::endl;
	SetLocalMaxPoints(num_black_y, music_image.rows, points_y);
	std::cout << "count: " << points_y.size() << std::endl;

	std::cout << "x축 국소 최대 좌표" << std::endl;
	SetLocalMaxPoints(num_black_x, music_image.cols, points_x);
	std::cout << "count: " << points_x.size() << std::endl;

	// 최종 음표 좌표 구하기
	for (int i = 0; i < points_x.size(); i++) {
		for (int j = 0; j < points_y.size(); j++) {
			if (music_image.at<uchar>(points_y[j], points_x[i]) < 125) {
				note_points.push_back(Point(points_x[i], points_y[j]));
				std::cout << points_x[i] << ", " << points_y[j] << std::endl;
			}
		}
	}

	delete[] num_black_x;
	delete[] num_black_y;

	/*
	//이름 짓기해주고
	namedWindow("MusicDot", WINDOW_AUTOSIZE);
	//그 이름으로 화면창에 띄운다. 
	imshow("MusicDot", music_image);


	music_image.at<uchar>();
	*/

	while (waitKey(0) > 0) {
	}

	return 0;
}

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
