

#include "opencv2/imgcodecs.hpp"

#include "opencv2/highgui/highgui.hpp"


using namespace cv;

int main()

{

	//이미지 파일을 불러와 그레이 이미지로 변환한다.  

	Mat input_gray_image = imread("school.jpg", IMREAD_GRAYSCALE);



	namedWindow("origin", WINDOW_AUTOSIZE);

	namedWindow("gray image", WINDOW_AUTOSIZE);



	Mat result_binary_image;

	//threshold값을 127로 해서 이진화 한다.

	//입력 이미지의 특정 필셀값이 threshold값보다 크면 결과 

	//이미지상의 같은 위치의 픽셀값을 255로 한다.

	//thshold값보다 작을 경우에는 0이 된다.

	threshold(input_gray_image, result_binary_image, 127, 255, THRESH_BINARY);



	imshow("black or white", result_binary_image);

	imshow("gray image", input_gray_image);



	//아무키나 누를 때 까지 대기한다.

	while (waitKey(0) < 0);
}