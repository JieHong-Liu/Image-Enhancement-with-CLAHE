# Image Enhancement with CLAHE for Dark Images and RGB images

###### tags: `Image Processing`

## Abstract

The disvantage of Global image contrast enhacement is it didn’t consider the local details of an image.

The key of this proposed algorithm is
1. local enhance on the image
2. global enhance the output.


## Introduction

CLAHE (Contrast Limited Adaptive Histogram Equalization)

[Histogram Equalization](https://www.notion.so/Global-Histogram-Equalization-GHE-fb0bc67d7d9f4df58859fba010f0ee2e) is a basic image enhancement technique to enhance the image, the goal is to improve its contrast.

where the definition of Contrast is: ![](https://i.imgur.com/UR5svZW.png)

![](https://i.imgur.com/P51xcyc.png)

The drawback of the histogram equalization is the procedure would also increase the noise. 


![](https://i.imgur.com/OvdDqXQ.png)

## Background Knowledge

### Image Enhancement Techniques

1. The image enhancement on RGB image.
    + [Image Enhancement with the Application of Local and Global Enhancement Methods for Dark Images](https://github.com/JieHong-Liu/Image-Enhancement-on-Dark-Image)

2. Linear interpolation
假設我們已知坐標 (x0, y0) 與 (x1, y1)，要得到 [x0, x1] 區間內某一位置 x 在直線上的值。根據圖中所示，我們得到 
![](https://i.imgur.com/P3yJ1OI.png)
由於 x 值已知，所以可以從公式得到 y 的值
![](https://i.imgur.com/eqlogps.png)

![](https://i.imgur.com/nU4a1WE.png)


## Proposed Algorithm (`clahe.py`)

CLAHE與AHE都是局部均衡化，也就是把整個圖像分成許多小塊Tiles (OpenCV default為8×8)，對每個小塊進行均衡化。這種方法主要對於圖像直方圖不是那麼單一的圖像(e.g. 多峰情況)比較實用。所以在每一個的區域中，直方圖會集中在某一個小的區域中。


何謂對比度限制 ：直觀來說即限制累積分佈函數(CDF)的斜率，又因累積分佈直方圖CDF是灰度直方圖積分，所以限制CDF的斜率就相當於限制Hist的幅度。Hist的積分對於每個小塊來說，如果直方圖中的bin超過對比度的上限，就把其中的像素點均勻分散到其他bins中，然後再進行直方圖均衡化。最後，為了去除每一個小塊之間”人造的”邊界，需要利用插值運算，也就是每個畫素點出的值由它周圍4個子塊的對映函式值進行雙線性插值。

![](https://i.imgur.com/3fa1Aue.png)
圖中可看出CLAHE是對直方圖進行裁剪，使其幅值低於某個上限。被修剪掉的部分不能扔掉，需要將其重新均勻的分佈到直方圖中，生成新的直方圖，以確保直方圖總面積不變。

![](https://i.imgur.com/23YfzIO.png)

插值可以在不影響結果質量的情況下顯著提高效率。圖像被分割成大小相等的矩形塊，如下圖右側部分所示。 （8列8行共64塊是常見的選擇。）。然後為每個圖塊計算直方圖、CDF 和變換函數。變換函數適用於平鋪中心像素（圖中左側的黑色方塊）。使用最多四個與中心像素最接近的圖塊的轉換函數進行轉換，並通過插值計算出所有其他像素的像素值。大部分圖像（藍色陰影）中的像素使用雙線性插值得到，靠近邊界的像素（綠色陰影）則用線性插值得到，邊角附近的像素（紅色陰影）使用角塊的變換函數進行變換。插值係數反映了像素到最近的圖塊的中心像素之間的位置，因此隨著像素接近圖塊中心，結果是連續的。

### Comparison between Proposal and origin method



### References
[1] https://zh.wikipedia.org/wiki/%E8%87%AA%E9%80%82%E5%BA%94%E7%9B%B4%E6%96%B9%E5%9B%BE%E5%9D%87%E8%A1%A1%E5%8C%96

[2] https://zhuanlan.zhihu.com/p/150381937

[3] https://medium.com/@cindylin_1410/%E6%B7%BA%E8%AB%87-opencv-%E7%9B%B4%E6%96%B9%E5%9C%96%E5%9D%87%E8%A1%A1%E5%8C%96-ahe%E5%9D%87%E8%A1%A1-clahe%E5%9D%87%E8%A1%A1-ebc9c14a8f96

[4] Pizer, S. M., Amburn, E. P., Austin, J. D., Cromartie, R., Geselowitz, A., Greer, T., ... & Zuiderveld, K. (1987). Adaptive histogram equalization and its variations. Computer vision, graphics, and image processing, 39(3), 355-368.

[5] Singh, K. B., Mahendra, T. V., Kurmvanshi, R. S., & Rao, C. R. (2017, April). Image enhancement with the application of local and global enhancement methods for dark images. In 2017 International Conference on Innovations in Electronics, Signal Processing and Communication (IESC) (pp. 199-202). IEEE.

[6] Zuiderveld, K. (1994). Contrast limited adaptive histogram equalization. Graphics gems, 474-485.
