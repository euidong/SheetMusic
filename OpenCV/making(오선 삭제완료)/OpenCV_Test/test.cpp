
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/highgui/highgui.hpp"

using namespace cv;

#include <iostream>

int main()
{
	Mat img;
	img = imread("school.jpg", IMREAD_GRAYSCALE);

	imwrite("gray_piano.jpg", img);
	Mat blackorWhite;

	threshold(img, blackorWhite, 127, 255, THRESH_BINARY);


	imwrite("1bit_piano.jpg", blackorWhite);
	int count;
	for (int i = 0; i < blackorWhite.rows; i++)
	{
		count = 0;
		for (int j = 0; j < blackorWhite.cols; j++)
		{
			if (!blackorWhite.at<uchar>(i,j))
			{
				count++;
			}
		}
		if (count / (float)blackorWhite.cols > 0.8)
		{
			for (int p = 0; p < blackorWhite.cols; p++)
			{
				blackorWhite.at<uchar>(i,p) = (uchar)255;
			}
		}

	}
	namedWindow("delete", WINDOW_AUTOSIZE);
	imshow("delete", blackorWhite);

	imwrite("delete_line.jpg", blackorWhite);
	while (waitKey(0) < 0);

}