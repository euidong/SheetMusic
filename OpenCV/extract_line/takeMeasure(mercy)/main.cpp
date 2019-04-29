#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/highgui/highgui.hpp"

using namespace cv;

#include <iostream>

using namespace std;

int main()
{
	Mat origin;
	Mat img;
	origin = imread("threeBear.jpg", IMREAD_GRAYSCALE);
	threshold(origin, img, 127, 255, THRESH_BINARY);

	namedWindow("delete", WINDOW_AUTOSIZE);
	imshow("delete", img);
	namedWindow("origin", WINDOW_AUTOSIZE);
	imshow("origin", origin);
	int count;
	int firstline = 0;
	int secondline;
	for (int i = 0; i < img.rows; i++)
	{
		count = 0;
		for (int j = 0; j < img.cols; j++)
		{
			if (!img.at<uchar>(i, j))
			{
				count++;
			}
		}
		if (count / (float)img.cols > 0.8)
		{
			if (firstline == i - 1)
			{
				firstline = i;
			}
			else if (firstline == 0)
			{
				firstline = i;
			}
			else
			{
				secondline = i;
				break;
			}
		}
	}

	cout << firstline << endl << secondline << endl;

	int gap = secondline - firstline;

	Rect rect(0, firstline - gap, img.cols, gap * 9 );
	Mat subimg = img(rect);

	imwrite("measure.jpg", subimg);

	while (waitKey(0) < 0);
	return 0;
}