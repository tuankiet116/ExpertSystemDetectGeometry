## Hệ thống chuyên gia dựa trên quy tắc - phát hiện đồ họa
### Lời tựa
Dự án này là một dự án khóa học về ** Trí tuệ nhân tạo **. Yêu cầu cụ thể là nhận ra * hệ thống chuyên gia dựa trên quy tắc * để phát hiện hình dạng của các hình hình học tuyến tính đơn giản.
Trọng tâm của việc triển khai dự án là ** biểu diễn các quy tắc **, ** xây dựng công cụ suy luận **, ** xây dựng cơ sở kiến ​​thức **, ** tiền xử lý hình ảnh ** và ** giao diện người dùng **.
Ngôn ngữ thực hiện dự án là Python, OpenCV được sử dụng để tiền xử lý hình ảnh và wxPython được sử dụng cho giao diện người dùng.
Thiết kế của hệ thống chuyên gia đề cập đến Chương 2 của ["Hướng dẫn Hệ thống Thông minh-Trí tuệ Nhân tạo" (Sách gốc lần 3)] (https://book.douban.com/subject/11606478/).
Nếu bạn có bất kỳ đề xuất nào để cải thiện dự án, chúng tôi hoan nghênh các ý kiến ​​đóng góp. : ~)

### nội dung
1. [Tổng quan] (# chung)
2. [Cấu trúc của Hệ thống Chuyên gia Kiểm tra Đồ họa] (# cấu trúc)
3. [Xây dựng và trình bày quy tắc] (# quy tắc)
4. [Trình bày Cơ sở Kiến thức] (# kiến ​​thức)
5. [Xử lý trước hình ảnh] (# pic_handle)
6. [Biểu diễn của cơ sở dữ liệu] (# fact)
7. [Xây dựng Công cụ lý luận: Công nghệ lập luận liên kết ngược] (# trở lại)
8. [Giao diện người dùng] (# GUI)
9. [Test Case] ​​(# test)
10. [Kết luận] (# kết luận)
11. [Phụ lục] (# bổ sung)

### <a name='general'> </a> Tổng quan
Quy trình hoạt động của hệ thống chuyên gia kiểm tra đồ họa là:

* Có được một tập hợp các dữ kiện cơ bản thông qua xử lý trước hình ảnh (tức là tọa độ của các điểm cuối của mỗi đoạn thẳng trong biểu đồ)
* Xử lý tập hợp các dữ kiện cơ bản này và tạo cơ sở dữ liệu của hệ thống chuyên gia
* Công cụ lập luận đọc các tài liệu quy tắc bên ngoài và tạo ra cơ sở kiến ​​thức
* Công cụ suy luận đọc vào cơ sở dữ liệu
* Sử dụng công nghệ lập luận liên kết ngược để lập luận
* Ghi lại các quy tắc được kích hoạt và các dữ kiện tuân thủ các quy tắc trong quá trình suy luận
* Vẽ vị trí của hình mà người dùng muốn phát hiện
* Hiển thị trong giao diện người dùng

Hệ thống chuyên gia kiểm tra đồ họa cũng cung cấp các chức năng bổ sung, bao gồm:

* Cung cấp trình chỉnh sửa quy tắc để thêm các quy tắc mới
* Hiển thị cơ sở quy tắc hiện tại
* Hiển thị thư viện dữ kiện của các hình ảnh được phát hiện hiện tại

Đồ họa hiện được hỗ trợ bởi hệ thống chuyên gia phát hiện đồ họa bao gồm:

* Tam giác
    * Tam giác nhọn
    * Hình tam giác vuông
    * Hình tam giác
    * Tam giác cân
        * Tam giác cân vuông góc
        * Hình tam giác cân
        * Tam giác cân Obtuse
    * Tam giác đều
* Tứ giác
    * Hình bình hành
        * Hình chữ nhật
            * Quảng trường
        * Hình thoi
    * Hình thang
        * Hình thang cân
        * Hình thang góc vuông
* Hình năm góc
    * Hình ngũ giác đều
* Hình lục giác
    * Hình lục giác


Hệ thống chuyên gia phát hiện đồ họa hỗ trợ phát hiện đồ họa ở các vị trí khác nhau, nhiều hình dạng và kích thước khác nhau và hỗ trợ phát hiện nhiều đồ họa trong một ảnh.

### <a name=' architecture'> </a> Cấu trúc của hệ thống chuyên gia kiểm tra đồ họa
Cấu trúc của hệ thống chuyên gia phát hiện đồ họa bắt chước cấu trúc cơ bản của hệ thống chuyên gia dựa trên quy tắc được hiển thị trong sách càng nhiều càng tốt.
Cấu trúc cụ thể như sau:
! [cấu trúc] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/osystem.png)
Hệ thống chuyên gia phát hiện đồ họa cũng bao gồm 5 phần: 
	- [Cơ sở kiến ​​thức] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/rules/rules.txt), 
	- [Cơ sở dữ liệu] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/fact/fact.txt), 
	- [Công cụ suy luận] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/engine/inference_engine.py), 
	- [Phương tiện giải thích, Giao diện người dùng] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/GUI/main_frame.py).
Các thư mục dự án tương ứng là quy tắc, dữ kiện, công cụ, GUI.
Ngoài ra, do đặc thù của đồ họa, tệp dự án còn chứa [Bộ xử lý hình ảnh] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/Picture_handler/cv_handler2.py).

### <a name='rule'> </a> Xây dựng và trình bày quy tắc
Bởi vì hệ thống chuyên gia cần hỗ trợ tải động cơ sở tri thức, các quy tắc phát hiện không thể được mã hóa cứng trong chương trình mà cần được lưu trữ trong một tệp bên ngoài 
trong một thời gian dài và được tải trong công cụ suy luận.
Dựa trên những lý do trên, một lớp Rule đầu tiên được xây dựng để đại diện cho một quy tắc nhất định. Lớp Rule bao gồm id (số quy tắc), antecedent (mục trước quy tắc), 
hậu quả (mục tiếp theo quy tắc), mô tả (mô tả quy tắc) bốn thành viên lớp này.
Trong số đó, có tính đến các đặc điểm của quy tắc phát hiện đồ họa, các mục trước của quy tắc được kết nối một cách hợp lý với *** và ***.
Một quy tắc điển hình như sau:
> {
IF: ['hình dạng là tam giác', 'các đường thẳng đều bằng nhau']
THÌ: 'hình dạng là tam giác đều'
MÔ TẢ: 'tam giác đều'
}

Các quy tắc trên được sử dụng để xác định rằng một hình là tam giác đều.
Các quy tắc khác cũng tương tự.
Trong phần giao diện người dùng, chức năng của trình chỉnh sửa quy tắc được cung cấp, có thể thêm các quy tắc mới trên cơ sở các tệp cơ sở kiến ​​thức hiện có.

### <a name='knowledge'> </a> Trình bày cơ sở tri thức
Cơ sở kiến ​​thức là bộ quy tắc của hệ thống chuyên gia kiểm tra đồ họa này. Cơ sở tri thức được lưu trữ ở định dạng txt và chứa tất cả các quy tắc cần thiết để xác định đồ họa.
Khi chương trình đang chạy, công cụ suy luận đọc tất cả các quy tắc từ tệp cơ sở tri thức và xây dựng các thể hiện Quy tắc của tất cả các quy tắc tương ứng.

### <a name='pic_handle'> </a> Xử lý trước ảnh
Đầu vào trực tiếp của hệ thống chuyên gia phát hiện đồ họa này là hình ảnh được phát hiện. Để có được một cơ sở dữ liệu về ảnh, trước tiên cần phải có một mức độ xử lý trước đối với ảnh.
Thư viện xử lý hình ảnh được sử dụng là OpenCV và hai phương pháp lấy dữ liệu đã được thử:

* Biến đổi Hough: `cv2.HoughLines2 ()`
* Phát hiện đường viền: `cv2.findContours ()`

1. Biến đổi Hough:
    Biến đổi Hough cơ bản hơn và có thể lấy tọa độ điểm cuối của tất cả các đoạn thẳng trong hình.
    Nhưng biến đổi Hough có một số vấn đề rõ ràng:
    * Khó điều chỉnh các thông số: Trong nỗ lực ban đầu để phát hiện các đoạn thẳng bằng phép biến đổi Hough, các thông số khác nhau sẽ dẫn đến các bộ sưu tập đoạn thẳng khác nhau và chất 
lượng của các bộ sưu tập đoạn thẳng được phát hiện dưới cùng một thông số cho các ảnh khác nhau cũng không đồng đều và rất khó để tìm một tham số biến đổi Hough phù hợp
    * Việc điều chỉnh kết quả của phép biến đổi Hough rất rắc rối: do các điểm cuối của đoạn thẳng thu được không chính xác lắm, nên cần phải phán đoán một cách giả tạo mối quan hệ giữa các điểm cuối này.
    Nếu được đánh giá là liệu hai điểm cuối có đủ gần để được coi là cùng một điểm cuối hay không, thì ngưỡng gần nhau cần phải được đặt một cách giả tạo. Tuy nhiên, ngưỡng gần có kết quả phán đoán 
khác nhau đối với các bức tranh khác nhau. Đôi khi ngưỡng quá lớn để đánh giá sai các điểm cuối không giống nhau với cùng một điểm cuối và đôi khi ngưỡng quá nhỏ để đánh giá tất cả các điểm cuối liền kề.
    Vấn đề này rất quan trọng trong quá trình tiền xử lý hình ảnh, đặc biệt là khi đánh giá góc giữa hai đường thẳng.
    * Khi có nhiều đồ họa trong hình, quá trình xử lý gặp phải tắc nghẽn: vì phép biến đổi Hough thu được tất cả các đoạn thẳng trong hình và không thể phân biệt được đoạn 
thẳng thuộc về đồ họa nào, do đó cần phải xác định theo cách thủ công tập hợp các phân đoạn dòng Các vấn đề về phân bổ đồ họa. Điều này mang lại rất nhiều công việc.

    Dựa trên các vấn đề trên và kết quả phát hiện không đạt yêu cầu trong các lần thử thực tế, nó đã được quyết định từ bỏ việc sử dụng biến đổi Hough như một phương tiện xử lý trước hình ảnh.

2. Phát hiện đường viền:
     Phát hiện đường viền cũng tương đối cơ bản và tương đối đơn giản hơn so với biến đổi Hough. Phát hiện đường bao cũng thu được tọa độ điểm cuối của đoạn thẳng. 
Nhưng không giống như biến đổi Hough, kết quả trả về bởi phát hiện đường bao là đỉnh đường bao của đồ thị (nó cần phải trải qua bước gần đúng `cv2.approxPolyDP ()`).
     Nói cách khác, mỗi hình trong hình đều có các đỉnh riêng của nó. Hơn nữa, tất cả các cạnh của đồ thị và mối quan hệ giữa các cạnh và các cạnh (kích thước của góc bao gồm, 
liệu chúng có song song không, v.v.) có thể thu được từ các đỉnh. Thông qua các bước tiền xử lý này, bạn có thể thu được các thông tin cơ bản về các bức tranh, có thể được sử dụng để tạo thành cơ sở dữ liệu sau.
     Vì giá trị trả về của phát hiện đường viền không còn vấn đề hợp nhất các điểm cuối liền kề và vấn đề phân bổ đồ họa của các tập hợp đoạn thẳng **, nên công nghệ tiền xử lý hình ảnh cuối cùng dựa trên phát hiện đường viền.

Nhiều đường vòng đã được thực hiện trong bước xử lý trước của bức tranh, nhưng cuối cùng vẫn thu được kết quả xử lý ưng ý.

### <a name='fact'> </a> Biểu diễn cơ sở dữ liệu
Cơ sở dữ liệu sử dụng các đường bao như một đơn vị và chứa mối quan hệ giữa tất cả các cạnh và các góc trong mỗi đường bao.
Nói một cách trừu tượng, cơ sở dữ liệu chứa các dữ kiện cơ bản của mỗi đồ thị.
Một cơ sở dữ liệu điển hình như sau:
> Đường viền # 0
{
--Giới thiệu về dòng-- 4 dòng
<
2 dòng bằng nhau
(84, 156) -> (365, 155): Chiều dài: 281,00, Góc: -0,20
(366, 252) -> (85, 253): Chiều dài: 281,00, Góc: -0,20
\>
<
4 dòng đóng cửa
(84, 156) -> (365, 155): Chiều dài: 281,00, Góc: -0,20
(365, 155) -> (366, 252): Chiều dài: 97.01, Góc: 89.41
(366, 252) -> (85, 253): Chiều dài: 281,00, Góc: -0,20
(85, 253) -> (84, 156): Chiều dài: 97,01, Góc: 89,41
\>
--Về góc độ--
<
1 góc là góc vuông
(84, 156) -> (365, 155): Chiều dài: 281,00, Góc: -0,20
(365, 155) -> (366, 252): Chiều dài: 97.01, Góc: 89.41
\>
<
2 cặp đường thẳng song song
(84, 156) -> (365, 155): Chiều dài: 281,00, Góc: -0,20
(366, 252) -> (85, 253): Chiều dài: 281,00, Góc: -0,20
(365, 155) -> (366, 252): Chiều dài: 97.01, Góc: 89.41
(85, 253) -> (84, 156): Chiều dài: 97,01, Góc: 89,41
\>
}
Đường viền # 1
{
--Giới thiệu về dòng-- 3 dòng
một số sự kiện dòng ở đây
--Về góc độ--
một số sự kiện góc ở đây
}

Cơ sở dữ liệu trên là một phần của cơ sở dữ liệu do test case tạo ra.
Một mặt, cơ sở dữ liệu dùng để kiểm tra độ chính xác của quá trình tiền xử lý hình ảnh, mặt khác, nó cũng được dùng để hiển thị cho người dùng xem.

### <a name='back'> </a> Xây dựng công cụ suy luận: Công nghệ suy luận liên kết ngược
1. Sự lựa chọn giữa liên kết chuyển tiếp và liên kết ngược:
    Như gợi ý trong cuốn sách, trước tiên hãy phân tích cách chúng ta giải quyết vấn đề khi xác định hình dạng của hình.
    Nếu chúng ta muốn xác định một hình, ví dụ, một hình vuông, trước tiên chúng ta sẽ xác minh xem nó có phải là hình chữ nhật hay không, sau đó xem bốn cạnh có chiều dài bằng nhau hay không. Loại phương pháp lập luận này là bắt đầu từ một giả thuyết và tìm bằng chứng, đây là một kỹ thuật lập luận liên kết ngược.
    Mặt khác, từ quan điểm của mục tiêu dự án, người dùng được yêu cầu chọn đồ họa được phát hiện, và sau đó công cụ suy luận tìm các dữ kiện liên quan để hỗ trợ các giả thuyết được phát hiện. Vì vậy, điều này cũng đòi hỏi hệ thống chuyên gia phát hiện đồ họa sử dụng công cụ suy luận của công nghệ liên kết ngược.
    Liên kết ngược là một kỹ thuật lập luận theo hướng mục tiêu. Về độ phức tạp, liên kết ngược hiệu quả hơn liên kết thuận, vì vậy liên kết ngược cũng sẽ là lựa chọn hàng đầu cho công nghệ lập luận.
2. Việc thực hiện liên kết ngược:
    Ví dụ về công nghệ suy luận liên kết ngược được đưa ra trong sách tham khảo, việc thực hiện suy luận liên kết ngược yêu cầu cấu trúc ngăn xếp ***.
    Trong việc triển khai công cụ suy luận, cấu trúc dữ liệu kiểu danh sách Python được sử dụng để mô phỏng hoạt động của ngăn xếp và nó cung cấp * điều kiện nhấn vào ngăn xếp suy luận *, * bật điều kiện trên cùng của ngăn xếp suy luận *, * lấy điều kiện cao nhất của ngăn xếp suy luận *, * Xác định xem ngăn xếp suy luận có trống không * Bốn phép toán ngăn xếp.
3. Cơ chế suy luận của động cơ suy luận:
    * Trước hết, công cụ suy luận sẽ tải cơ sở quy tắc và cơ sở dữ liệu khi nó được khởi động. Miễn là hình ảnh được phát hiện không thay đổi, cơ sở quy tắc và cơ sở dữ liệu đã tải sẽ không được tải lại.
    * Sau đó, theo hình dạng mà người dùng muốn phát hiện, đặt mục tiêu suy luận của công cụ suy luận làm điều kiện đầu tiên để đẩy nó vào ngăn xếp suy luận.
    * Sau đó, khởi động công cụ suy luận.
        * Bước 1: Lấy điều kiện cao nhất của ngăn xếp suy luận và khớp nó với mục bài đăng quy tắc trong thư viện quy tắc. Nếu kết hợp thành công, tất cả các mục trước đó của quy tắc đã so khớp sẽ nhận được. Nếu trận đấu không thành công, điều đó có nghĩa là tất cả các quy tắc không được áp dụng và vòng suy luận liên kết ngược trực tiếp thoát ra.
        * Bước 2: Ghép tất cả các mục trước với các dữ kiện trong cơ sở dữ liệu từng cái một. Nếu nó khớp có nghĩa là tiền tập đã được đáp ứng trong cơ sở dữ liệu, nếu không khớp có nghĩa là tiền tập thể cũng là một trong những điều kiện để suy luận và nó được đẩy lên ngăn xếp suy luận. Thực hiện thao tác này trên tất cả các mục trước của quy tắc đã so khớp.
        * Bước 3: Lặp lại các thao tác Bước 1 và Bước 2 ở trên cho đến khi gặp hai tình huống sau:
            * Nếu ngăn xếp lý luận trống, có nghĩa là tất cả lý luận đã được thực hiện triệt để, mục tiêu lý luận có thể đạt được và lý luận liên kết ngược của mục tiêu đã thành công.
            * Nếu không có quy tắc phù hợp, có nghĩa là không có đủ dữ kiện để hỗ trợ mục tiêu lý luận, mục tiêu lý luận không thể đạt được và lý luận liên kết ngược của mục tiêu không thành công.


### <a name='GUI'> </a> Giao diện người dùng
Giao diện người dùng bao gồm các phần sau:

* Nguồn ảnh
* Hiển thị hình ảnh kết quả kiểm tra
* Báo cáo kết quả thử nghiệm thành công hay thất bại
* Thực tế đã được khớp trong quá trình phát hiện
* Các quy tắc được kích hoạt trong quá trình phát hiện
* Danh sách dạng cây gồm các biểu đồ có thể được phát hiện
* Chọn nút của hình ảnh gốc
* Nút để mở trình chỉnh sửa quy tắc
* Nút để hiển thị tất cả các quy tắc
* Một nút hiển thị tất cả các dữ kiện về hình ảnh nguồn

Giao diện người dùng chính được hiển thị trong hình bên dưới:
! [main] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/main.png)
Giao diện chỉnh sửa quy tắc được hiển thị trong hình bên dưới:
! [biên tập viên] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/editor.png)
Giao diện hiển thị tất cả các quy tắc và tất cả các dữ kiện được hiển thị bên dưới:
! [rule_fact] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/rule_fact.png)

### <a name='test'> </a> Trường hợp thử nghiệm
#### A. Kiểm tra đồ thị đơn:
1. Hình tam giác:
    ! [tam giác] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/triangle.png)
    * Tam giác nhọn:  
        ! [sharp_triangle] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/acute_triangle.png)
    * Hình tam giác vuông:
        ! [right_triangle] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/right_triangle.png)
    * Hình tam giác:
        ! [tù_triangle] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/obtuse_triangle.png)
    * Tam giác cân:
        ! [isosceles_triangle] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/isosceles_triangle.png)
        * Tam giác vuông cân:
            ! [tam giác cân vuông] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/right_and_isosceles_triangle.png)
        * Tam giác nhọn Isosceles:
            ! [tam giác nhọn và cân] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/acute_and_isosceles_triangle.png)
        * Tam giác tù cân:
            ! [tam giác tù và cân] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/obtuse_and_isosceles_triangle.png)
    * Tam giác đều:  
        ! [Hình tam giác đều] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/equilateral_triangle.png)
2. Hình tứ giác:
    ! [tứ giác] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/quadrirical.png)
    * Hình bình hành:
        ! [hình bình hành] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/parallelogram.png)
        * Hình chữ nhật:
            ! [hình chữ nhật] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/rectangle.png)
            * Quảng trường:  
                ! [square] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/square.png)
        * Kim cương:
            ! [hình thoi] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/rhombus.png)
    * Hình thang:
        ! [hình thang] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/trapezoid.png)
        * Hình thang cân:
            ! [isosceles_trapezoid] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/isosceles_trapezoid.png)
        * Hình thang vuông:
            ! [right_trapezoid] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/right_trapezoid.png)
3. Lầu Năm Góc:
    ! [ngũ giác] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/pentagon.png)
    * Hình ngũ giác đều:
    ! [regular_pentagon] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/regular_pentagon.png)
4. Hình lục giác:
    ! [hexagon] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/hexagon.png)
    * Hình lục giác:   
    ! [regular_hexagon] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/regular_hexagon.png)
    
#### B. Kiểm tra đồ họa hỗn hợp:
*! [mix10] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/mix10.png)
  ! [mix11] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/mix11.png)
*! [mix20] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/mix20.png)
  ! [mix21] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/mix21.png)
*! [mix30] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/mix30.png)
   ! [mix31] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/mix31.png)
   ! [mix32] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/mix32.png)
*! [mix40] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/mix40.png)
   ! [mix41.png] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/mix41.png)

### <a name='conclusion'> </a> Tóm tắt
Hộp văn bản * Dữ kiện phù hợp * và hộp văn bản * Quy tắc truy cập * trong giao diện đồ họa có thể được sử dụng làm thiết bị giải thích của hệ thống chuyên gia kiểm tra đồ họa này.
Trên đây là toàn bộ nội dung của hệ thống chuyên gia giám định đồ họa.
Một chút cải tiến của công cụ lập luận có thể được sử dụng như một khung hệ thống lý luận chuyên gia liên kết ngược nói chung.

### <a name='addition'> </a> Phụ lục
Cơ sở kiến ​​thức của hệ thống chuyên gia kiểm tra đồ họa này: [Cơ sở kiến ​​thức] (https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/rules/rules.txt)






















