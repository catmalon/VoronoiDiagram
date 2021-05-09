# Voronoi Diagram 演算法
中山大學 資訊工程學系 碩士班一年級 M093040067 歐陽安媛

## 軟體規格書
### - 輸入與輸出資料規格
#### 輸入
1. 以滑鼠在600*600的畫布上隨機點擊
x軸由左到右漸增
y軸由上到下漸增
四角座標如下所示：
```
(0, 0)          (600, 0)

(600, 0)        (600, 600)
```
2. 點擊![](https://i.imgur.com/2sPUhtI.gif)，讀入「輸入文字檔」：
```
# 請以UTF-8編碼
# 前面加入"#"，即可自由添加備註
3 // 共三點
100 100 // 第1點座標(x, y) = (100, 100)
200 100 // 第2點座標(x, y) = (200, 100)
300 200 // 第3點座標(x, y) = (300, 200)
#中間也可加入備註
0 // 檔案結尾
```
3. 點擊![](https://i.imgur.com/2sPUhtI.gif)，讀入「輸出文字檔」，格式同輸出檔，將點與線段直接繪於畫布
#### 輸出
1. 點擊![](https://i.imgur.com/5Bdrz3r.gif)，輸出「output.txt」
2. 輸出格式：
分為「原輸入點」和「分割線段」：
點座標(x, y)
線段為兩個端點A(x, y),B(x, y)的座標

```
P 100 100 // 點 (100, 100)
P 200 100 // 點 (200, 100)
P 300 200 // 點 (300, 200)
E 0 550 150 250 // 線段 A(  0, 550); B(150, 250)
E 150 0 150 250 // 線段 A(150,   0); B(150, 250)
E 150 250 400 0 // 線段 A(150, 250); B(400,   0)
```
3. 點與線段之排列
3.1 座標點排列在前半段，線段排列在後半段
3.2 座標點以 lexical order順序排列（即先排序第一維座標，若相同，則再排序第二維座標；線段亦以 lexical order順序排列。
3.3 線段的 lexical order (字典序)：
線段E x1 y1 x2 y2，座標須滿足x1≦x2 或 x1=x2, y1≦y2。
不同線段之間，依照x1, y1, x2, y2的順序進行排序(字典序)。以上述輸出文字檔案為例，比較x1時，因為0<193，x1為0的2條線段放前面，並繼續比較y1；後3條線段亦同理。

### - 功能規格與介面規格
#### 介面
1. 上方一排為互動按鈕
2. 中間為視窗畫布，大小為600*600，左上原點為(0,0)。
滑鼠在畫布上任意點擊，均可顯示，並作為輸入資料。
Convex hull<font color="#f00">(紅色虛線)</font>和Voronoi Diagram(黑色實線)結果亦會顯示於其上。
3. 右側為在畫布上直接點擊之點座標。
 
![](https://i.imgur.com/dTt5Z3j.png)
#### 功能
![](https://i.imgur.com/rEF7IjD.gif)：開啟檔案(Open)，用以輸入資料，詳細格式如上一段落所述。
![](https://i.imgur.com/8Oq4NSO.gif)：逐步執行(Step by Step)，將於下一段落說明。
![](https://i.imgur.com/1BQ8e5w.gif)：執行(Run)，直接顯示輸入資料之Voronoi Diagram
![](https://i.imgur.com/XCXl3NR.gif)：存檔(Save)，用以輸出資料，詳細格式如上一段落所述。
![](https://i.imgur.com/MiyoV2C.gif)：清除(Clean)，清除畫布及輸入資料、輸出資料。

### - 軟體測試規劃書
可用滑鼠直接點擊畫布，或以輸入按鈕讀取，以獲得輸入資料；
並以逐步執行或執行按鈕，檢視Voronoi Diagram是否正確繪於畫布，以進行軟體測試。
* 1~3點，直接顯示
* 4~6點，一次Divide及一次merge
* 7點以上，多次Divide及多次merge

## 軟體說明
需安裝Python 3.9 + tkinter(tk)模組
自main.py開始執行

### - 使用說明
#### 輸入資料
可以以下兩種方式輸入欲產生Voronoi Diagram之資料：
* 直接點擊畫布產生點資料，可用旁邊座標顯示確認實際位置
![](https://i.imgur.com/rwZmHHl.png)
* 點擊![](https://i.imgur.com/rEF7IjD.gif)開啟檔案Open按鈕，以讀取點資料。
input檔案範例：
![](https://i.imgur.com/spg4752.png)


#### 執行程式與結果顯示
可以以下兩種方式執行並產生結果：
* 點擊![](https://i.imgur.com/1BQ8e5w.gif)執行Run按鈕，可直接顯示點(黑色點)、Voronoi Diagram(黑色實線)及Convex hull<font color="#f00">(紅色虛線)</font>
![](https://i.imgur.com/eVOcDnR.png)

* 點擊![](https://i.imgur.com/8Oq4NSO.gif)逐步執行Step by step，顯示過程與結果：
(1) 每次 merge 前暫停，並以<font color="#FFA500">橘色(點與線)</font>與<font color="#6495ED">藍色(點與線)</font>區分出左右兩個Voronoi Diagram
(2) 以**黑色粗線段**繪出 Hyper Plane
(3) 擦去多餘線段
![](https://i.imgur.com/2St2xcw.png)

#### 輸出資料與清除畫布

* 點擊![](https://i.imgur.com/XCXl3NR.gif)存檔Save，輸出資料存為「output.txt」，格式如上「輸出規格」所述
![](https://i.imgur.com/JMCdoeO.png)

* 點擊![](https://i.imgur.com/MiyoV2C.gif)清除Clean，清除畫布及輸入資料、輸出資料。
![](https://i.imgur.com/JZBqnX1.png)

## 程式設計
### 資料結構
* **Point:** 儲存點座標(x,y)及處理相關運算。
* **Vector:** 處理向量相關運算，如：內積、外積、順時針或逆時針旋轉。
* **Triangle:** 處理三角形相關運算，如：三點外心、三角形面積(判斷是否共線、共點)。
* **Divider:** 儲存Voronoi Diagram之分割線(線段起點, 線段終點, 被分割點A, 被分割點B)，如：找交點、消線。
* **ConvexHull:** 儲存Voronoi Diagram之ConvexHull(點的清單, 最上面的分割線, 最下面的分割線)及相關運算，如：合併。
ConvexHull合併為使用左右兩點連線的旋轉，時間複雜度為O(n)。
(0) 紀錄左邊最右的點p，與右邊最左的點q
![](https://i.imgur.com/ke2OJ06.png)
(1) 先旋轉一組連線到最上方，將其儲存為「最上面的分割線」
![](https://i.imgur.com/o0ug8pn.png)
(2) 再旋轉另一組連線到最下方，將其儲存為「最下面的分割線」
![](https://i.imgur.com/xEdxdR2.png)
(3) 最後刪除中間虛線的點

*參考出處：https://algorithmtutor.com/Computational-Geometry/An-efficient-way-of-merging-two-convex-hull/*

* **VoronoiDiagram:** 儲存Voronoi Diagram及相關運算，如：產生1~3點圖形及多個合併
Voronoi Diagram之Hyper plane產生方法為：
從merge完的ConvexHull取得最上面之分割線，依序檢查左右兩邊Voronoi Diagram的所有分割線是否與其有交點。找到最上面的交點(y值最小)後，兩端點依序往下更換，直到碰到ConvexHull之最下面分割線。時間複雜度為O(n)。
![](https://i.imgur.com/4toojfn.png)
  
*參考出處：http://web.ntnu.edu.tw/~algo/Neighbor.html*


## 軟體測試與實驗結果
### 測試環境
#### -電腦硬體系統
* CPU型號： intel® Xeon® 處理器 E3-1230 v2 3.30 GHz
* 記憶體容量：16 GB
* 作業系統： Window 10 專業版
* 語言及編譯器名稱(版本)：Python 3.9
#### -測試極限
輸入點約在22左右以上，可能會有多餘的線段未被削去。猜測可能是Hyper plane完後的消線功能尚有bug存在。

## 結論與心得
本課堂之Term Project，算是我第一次寫python，第一次做視覺化的程式，且是第一次遇到要設計和使用偏向物件導向的資料結構。（因為大學時非本系生）

本次所使用的演算法，單純用想像的就不是很簡單，實際上要寫成程式的時候，更會遇到很多例外狀況，大概知道是哪部分有問題，要確實發現bug並做修改卻非常困難。深刻的體會演算法的概念與實際的實做之間巨大的鴻溝。因此也找了很多相關較容易實做出來的方法，以及可處理所有例外狀況的演算法實例。

但第一次寫出可以視覺化的程式，還是覺得非常有成就感！雖然其中投入了很多時間，有時候為了找出一個function的bug更是曠日廢時。但最後看到從無到有的多個py檔，並且匯集成一個執行檔，可以依照自己希望的樣子，確實的讓所有按鈕做出反應，產生出期待中的Voronoi Diagram圖形，就覺得前面時間和精力的投入都沒有白費！