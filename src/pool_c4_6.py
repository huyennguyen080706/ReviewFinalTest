"""Ngân hàng câu hỏi Chương 4–6, bám các hộp "Hay ra thi" trong GiangGiai_Chuong4-6.pdf.

Các câu tính toán đều được tính lại bằng code ngay trong file này (assert) để chắc
đáp án và phương án nhiễu khớp với số liệu đề cho.
"""
import math
from fractions import Fraction as Fr
from de_common import Q, num, table


def H(*c):
    n = sum(c)
    return -sum(x / n * math.log2(x / n) for x in c if x)


# ---------------------------------------------------------------- kiểm tra số liệu Chương 4
assert abs((78 - 50) / 8 - 3.5) < 1e-12
_iqr = [12, 14, 15, 15, 16, 17, 18, 19, 40]
_q1, _q3 = (14 + 15) / 2, (17 + 18) / 2          # trung vị nửa dưới / nửa trên (bỏ trung vị 16)
assert (_q1, _q3, _q3 + 1.5 * (_q3 - _q1)) == (14.5, 17.5, 22.0)
_A1, _B1 = {"Python", "SQL", "Excel", "Tableau", "R"}, {"SQL", "R", "Power BI", "Python"}
assert (len(_A1 & _B1), len(_A1 | _B1)) == (3, 6)
_A2, _B2 = set("abcde"), set("cdefgh")
assert (len(_A2 & _B2), len(_A2 | _B2)) == (3, 8)
_p = [50, 54, 52, 58, 61, 57]
assert sum(_p[2:5]) / 3 == 57 and abs(sum(_p[1:5]) / 4 - 56.25) < 1e-12
_bw = [5, 8, 9, 11, 14, 16, 20, 45, 65]
assert [sum(1 for v in _bw if lo <= v < hi) for lo, hi in ((5, 25), (25, 45), (45, 66))] == [7, 0, 2]
assert (60 - 20) / (180 - 20) == 0.25 and (22 - 40) / 12 == -1.5
assert abs(H(6, 2) - 0.8113) < 1e-4 and abs(1 - 0.6 * H(1, 5) - 0.61) < 1e-3

CH4 = [
    # --- Chiều chất lượng dữ liệu (4)
    Q("NB", "Chất lượng dữ liệu (C4)", "Hồ sơ khách hàng ghi năm sinh <b>1890</b>. Đây là vi phạm chiều chất lượng nào?",
      ["Accuracy", "Completeness", "Consistency", "Timeliness"],
      ["Completeness là thiếu giá trị (Null); ở đây có giá trị nhưng sai.", "Consistency là lệch đơn vị/định dạng giữa các nguồn.", "Timeliness là dữ liệu đến muộn."],
      "Accuracy: mức dữ liệu mô tả đúng thực thể. Năm sinh 1890 có giá trị nhưng sai thực tế.",
      "Chọn Completeness vì nghĩ dữ liệu “hỏng” là thiếu.", "Thiếu → Completeness · Sai → Accuracy · Lệch nguồn → Consistency · Muộn → Timeliness."),
    Q("TH", "Chất lượng dữ liệu (C4)", "Hệ thống Thẻ lưu số tiền theo <b>VNĐ</b>, hệ thống Khoản vay lưu theo <b>nghìn VNĐ</b>; gộp lại cho mô hình chấm điểm. Vi phạm chiều nào?",
      ["Consistency", "Accuracy", "Completeness", "Timeliness"],
      ["Mỗi hệ đều đúng theo đơn vị của mình; vấn đề là lệch giữa các nguồn.", "Không thiếu giá trị.", "Không liên quan độ trễ."],
      "Consistency: đồng bộ logic và định dạng giữa các nguồn, tránh xung đột đơn vị (VNĐ – nghìn VNĐ, dd/mm/yyyy – yyyy-mm-dd).",
      "Chọn Accuracy vì số tiền “sai”.", "Lệch đơn vị/định dạng giữa nguồn → Consistency."),
    Q("TH", "Chất lượng dữ liệu (C4)", "Quy tắc kiểm tra <code>ngay_tat_toan &gt;= ngay_giai_ngan</code> trên mỗi khoản vay được gọi là gì?",
      ["Cross-field validation", "Kiểm tra schema bằng metadata", "Entity resolution", "Kiểm tra Completeness"],
      ["Kiểm tra schema xác thực kiểu dữ liệu đồng nhất (cột phải là DATE).", "Entity resolution xác định bản ghi nhiều nguồn cùng là một thực thể.", "Completeness đo tỷ lệ ô không bị khuyết."],
      "Cross-field validation: quy tắc logic liên thuộc tính, kiểm tra quan hệ giữa hai cột trở lên (ngày tất toán ≥ ngày giải ngân; tuổi khớp năm sinh).",
      "Lẫn kiểm tra kiểu dữ liệu với kiểm tra quan hệ giữa các cột.", "Quan hệ nhiều cột → cross-field validation."),
    Q("VD", "Chất lượng dữ liệu (C4)", "Bảng có <b>200 dòng × 5 cột</b>, trong đó có <b>80 ô bị Null</b>. Độ đầy đủ (Completeness) đo theo số ô là:",
      ["92%", "8%", "60%", "84%"],
      ["8% là tỷ lệ ô bị thiếu, không phải độ đầy đủ.", "Coi nhầm 80 ô thiếu là 80 dòng thiếu: (200 − 80)/200.", "Chia nhầm cho 500 ô."],
      "Completeness = số ô có giá trị / tổng số ô = (1.000 − 80)/1.000 = 92%.",
      "Lấy tỷ lệ thiếu thay cho tỷ lệ đầy đủ.", "Completeness = ô có giá trị / tổng số ô."),
    # --- Noise và outlier (4)
    Q("VD", "Z-score (C4)", "Chi tiêu thẻ có µ = 50 triệu, σ = 8 triệu. Một giao dịch <b>78 triệu</b> có Z-score bao nhiêu và có bị gắn cờ outlier không?",
      ["Z = 3,5 → là outlier tiềm năng", "Z = 3,5 → không phải outlier vì ngưỡng là |Z| > 4", "Z ≈ 0,44 → không phải outlier", "Z = 0,56 → không phải outlier"],
      ["Ngưỡng theo slide là |Z| > 3, không phải 4.", "Chia nhầm cho phương sai 64 thay vì σ = 8.", "Chia hiệu số cho µ = 50 thay vì σ."],
      "Z = (78 − 50)/8 = 3,5 > 3 → outlier tiềm năng (với phân phối chuẩn, 99,7% giá trị nằm trong µ ± 3σ).",
      "Chia cho phương sai thay vì độ lệch chuẩn.", "Z = (x − µ)/σ; outlier khi |Z| > 3."),
    Q("VDC", "IQR (C4)", "Dữ liệu đã sắp xếp: 12, 14, 15, 15, 16, 17, 18, 19, 40. Q1, Q3 lấy bằng trung vị nửa dưới và nửa trên (không tính trung vị chung). <b>Ngưỡng trên</b> của phương pháp IQR là:",
      ["22", "22,5", "26,5", "20,5"],
      ["Tính cả trung vị 16 vào hai nửa: Q1 = 15, Q3 = 18 → 18 + 4,5.", "Dùng hệ số 3 (ngưỡng ngoại lai cực đoan) thay vì 1,5.", "Cộng 1,5 × IQR vào trung vị (16) thay vì Q3."],
      "Nửa dưới 12, 14, 15, 15 → Q1 = 14,5; nửa trên 17, 18, 19, 40 → Q3 = 17,5; IQR = 3. Ngưỡng trên = 17,5 + 1,5 × 3 = 22 → giá trị 40 là outlier.",
      "Cộng vào trung vị thay vì Q3, hoặc nhớ sai hệ số 1,5.", "Outlier nếu ngoài [Q1 − 1,5·IQR, Q3 + 1,5·IQR]."),
    Q("TH", "IQR và Z-score (C4)", "Trong ví dụ chi tiêu 4, 5, 5, 6, 6, 7, 7, 8, 30, Z-score không gắn cờ giá trị 30 nhưng IQR thì có. Lý do:",
      ["Chính giá trị 30 làm µ và σ phình to; Q1, Q3 hầu như không đổi", "Z-score chỉ dùng được với dữ liệu có giá trị âm", "IQR dùng ngưỡng 3σ nên chặt hơn so với Z-score", "Z-score luôn cho kết quả sai với mọi mẫu có dưới 10 phần tử dữ liệu"],
      ["Z-score không có giới hạn về dấu.", "IQR dùng hệ số 1,5 × IQR, không dùng σ.", "Không phải lý do; vấn đề là outlier tự “che” mình."],
      "Z(30) = (30 − 8,67)/7,63 ≈ 2,80 < 3 vì outlier làm méo µ và σ. IQR dựa trên phân vị nên ít bị chính outlier làm sai lệch.",
      "Nghĩ hai phương pháp luôn cho cùng kết luận.", "IQR bền với outlier hơn Z-score."),
    Q("NB", "Noise và outlier (C4)", "Ghép đúng cách xử lý theo slide:",
      ["Noise: làm mượt (binning, moving average); outlier: Z-score, IQR", "Noise: phát hiện bằng Z-score, IQR; outlier: làm mượt bằng binning", "Noise và outlier đều xử lý bằng cách xoá bản ghi", "Noise: chuẩn hoá Min-Max; outlier: giảm chiều bằng PCA"],
      ["Đảo ngược cách xử lý hai loại.", "Outlier có thể cần giữ lại để điều tra (ví dụ gian lận).", "Min-Max và PCA không phải kỹ thuật làm sạch noise/outlier."],
      "Noise là sai số ngẫu nhiên nhỏ phủ lên mọi giá trị → làm mượt. Outlier là vài điểm rất xa phần còn lại → phát hiện rồi quyết định bỏ, sửa hay giữ.",
      "Đảo cách xử lý noise và outlier.", "Noise → làm mượt · Outlier → phát hiện."),
    # --- Jaccard, dedup (4)
    Q("VD", "Jaccard (C4)", "Ứng viên A có kỹ năng {Python, SQL, Excel, Tableau, R}; ứng viên B có {SQL, R, Power BI, Python}. Hệ số <b>Jaccard J(A, B)</b> bằng:",
      ["0,5", "0,6", "0,75", "≈ 0,333"],
      ["Chia cho kích thước tập A (3/5).", "Chia cho kích thước tập B (3/4).", "Chia cho tổng kích thước hai tập (3/9)."],
      "A ∩ B = {Python, SQL, R} → 3; A ∪ B có 5 + 4 − 3 = 6 phần tử → J = 3/6 = 0,5.",
      "Chia cho một tập hoặc cho tổng hai tập.", "J = |A ∩ B| / |A ∪ B|."),
    Q("VD", "Jaccard (C4)", "Hai hồ sơ có tập thuộc tính A = {a, b, c, d, e} và B = {c, d, e, f, g, h}. J(A, B) bằng:",
      ["0,375", "0,6", "0,5", "≈ 0,273"],
      ["Chia cho |A| = 5.", "Chia cho |B| = 6.", "Chia cho tổng 5 + 6 = 11."],
      "Giao {c, d, e} = 3; hợp = 5 + 6 − 3 = 8 → J = 3/8 = 0,375.",
      "Quên trừ phần giao khi tính hợp.", "|A ∪ B| = |A| + |B| − |A ∩ B|."),
    Q("TH", "Deduplication (C4)", "<b>Golden Record</b> là kết quả trực tiếp của bước nào?",
      ["Deduplication (khử trùng lặp)", "Metadata Resolution (đối chiếu tên cột)", "Equal-frequency binning", "Stratified sampling"],
      ["Metadata Resolution đối chiếu thuộc tính khác tên cùng nghĩa (cust_id – customer_number).", "Binning là rời rạc hoá.", "Lấy mẫu phân tầng là numerosity reduction."],
      "Deduplication loại bản ghi trùng sau tích hợp và tạo một Golden Record duy nhất cho mỗi thực thể, tổng hợp từ mọi nguồn.",
      "Lẫn đối chiếu tên cột với khử trùng bản ghi.", "Dedup → Golden Record."),
    Q("TH", "Xung đột dữ liệu (C4)", "Hai nguồn ghi số điện thoại khác nhau cho cùng một khách; hệ thống chọn số được <b>cập nhật gần nhất</b>. Đây là quy tắc nào?",
      ["Latest timestamp", "Source Authority", "Jaccard similarity", "Metadata Resolution"],
      ["Source Authority chọn theo nguồn được tin hơn (ví dụ eKYC thắng form tự khai).", "Jaccard đo độ giống giữa hai tập, không chọn giá trị.", "Metadata Resolution xử lý tên cột, không chọn giá trị."],
      "Hai quy tắc giải xung đột: Source Authority (trọng số tin cậy của nguồn) và Latest timestamp (giá trị mới nhất thắng).",
      "Lẫn hai quy tắc giải xung đột.", "Nguồn tin cậy hơn → Source Authority · Mới hơn → Latest timestamp."),
    # --- SMA, roll-up (4)
    Q("VD", "Moving Average (C4)", "Giá 6 ngày: 50, 54, 52, 58, 61, 57. Với cửa sổ k = 3, <b>SMA tại ngày 5</b> bằng:",
      ["57", "56,25", "55", "≈ 58,67"],
      ["Lấy 4 giá trị (ngày 2–5) thay vì 3.", "Lấy trung bình cả 5 ngày đầu.", "Đó là SMA ngày 6 (58, 61, 57)."],
      "Ngày 5 lấy 3 giá trị gần nhất tính đến ngày 5: 52, 58, 61 → 171/3 = 57.",
      "Lấy sai số điểm hoặc sai vị trí cửa sổ.", "SMA_n = trung bình k giá trị từ n − k + 1 đến n."),
    Q("VD", "Moving Average (C4)", "Chuỗi có <b>10</b> điểm, tính SMA với cửa sổ <b>k = 4</b>. Có bao nhiêu giá trị SMA và giá trị đầu tiên ở điểm thứ mấy?",
      ["7 giá trị, bắt đầu từ điểm thứ 4", "10 giá trị, bắt đầu từ điểm thứ 1", "6 giá trị, bắt đầu từ điểm thứ 5", "7 giá trị, bắt đầu từ điểm thứ 1"],
      ["Ba điểm đầu chưa đủ 4 giá trị nên chưa tính được.", "Tính nhầm n − k = 6.", "Số giá trị đúng nhưng điểm đầu phải là điểm thứ k."],
      "Có n − k + 1 = 10 − 4 + 1 = 7 giá trị SMA; điểm đầu tiên có SMA là điểm thứ k = 4.",
      "Quên rằng k − 1 điểm đầu không có SMA.", "Số SMA = n − k + 1; bắt đầu tại điểm k."),
    Q("NB", "Roll-up / Drill-down (C4)", "Trong OLAP, thao tác <b>roll-up</b> là:",
      ["Đi lên mức tổng quát hơn, ví dụ ngày → tháng", "Đi xuống mức chi tiết hơn, ví dụ tháng → ngày", "Xoay trục báo cáo để đổi chiều phân tích", "Lọc dữ liệu theo một giá trị của một chiều"],
      ["Đó là drill-down.", "Đó là pivot, không thuộc nội dung slide này.", "Đó là slice."],
      "Data cube cho phép roll-up (tổng quát hoá) và drill-down (chi tiết hoá). Granularity là chọn mức tập hợp cân bằng hiệu suất và độ chi tiết.",
      "Đảo roll-up và drill-down.", "Roll-up lên · Drill-down xuống."),
    Q("TH", "Moving Average (C4)", "Trong phân tích kỹ thuật ở slide, <b>Golden Cross</b> là gì?",
      ["Đường MA50 cắt lên trên đường MA200, tín hiệu xu hướng tăng", "Đường MA200 cắt lên trên đường MA50, tín hiệu xu hướng giảm", "Giá đóng cửa vượt giá mở cửa trong một cây nến 1 giờ", "Z-score của giá vượt ngưỡng 3"],
      ["Đảo hai đường trung bình.", "Đó chỉ là một nến tăng, không phải Golden Cross.", "Z-score dùng phát hiện outlier."],
      "MA50, MA200 là trung bình 50 và 200 phiên gần nhất (làm mượt). Gộp lệnh khớp thành nến 1 giờ là tập hợp (aggregation).",
      "Đảo vai trò MA ngắn hạn và dài hạn.", "MA ngắn cắt lên MA dài → Golden Cross."),
    # --- PCA, numerosity (3)
    Q("TH", "PCA (C4)", "Điểm khác cơ bản giữa <b>PCA</b> và <b>feature selection</b>:",
      ["PCA tạo cột mới từ tổ hợp cột cũ; selection giữ một số cột gốc", "PCA giữ một số cột gốc; selection tạo cột mới từ tổ hợp cột cũ", "PCA tăng số chiều; feature selection giảm số chiều", "PCA chỉ dùng cho dữ liệu phân loại, không cho dữ liệu số"],
      ["Đảo ngược hai kỹ thuật.", "Cả hai đều nhằm giảm số chiều.", "PCA làm việc với dữ liệu số."],
      "PCA (PC1 = 0,6x1 + 0,5x2 + …) giữ tối đa phương sai. Feature selection (ví dụ theo Information Gain) chỉ bỏ cột kém.",
      "Đảo bản chất hai kỹ thuật.", "PCA = cột mới · Selection = giữ cột gốc."),
    Q("NB", "PCA (C4)", "Trong PCA, các <b>thành phần chính</b> là:",
      ["Vector riêng có trị riêng lớn nhất của ma trận hiệp phương sai", "Các cột gốc có phương sai nhỏ nhất của dữ liệu", "Các tâm cụm thu được sau khi chạy KMeans", "Các cột gốc có Information Gain lớn nhất so với nhãn của biến mục tiêu"],
      ["PCA giữ hướng có phương sai lớn, không phải nhỏ.", "Thay nhóm điểm bằng centroid là numerosity reduction bằng clustering.", "Đó là feature selection."],
      "Vector riêng là hướng mới; trị riêng cho biết lượng phương sai theo hướng đó; giữ vài hướng có trị riêng lớn nhất.",
      "Nghĩ PCA chọn cột gốc tốt nhất.", "Thành phần chính = vector riêng của ma trận hiệp phương sai."),
    Q("TH", "Numerosity reduction (C4)", "Kỹ thuật nào <b>KHÔNG</b> thuộc nhóm numerosity reduction theo slide?",
      ["PCA", "Regression models", "Stratified sampling", "Histograms"],
      ["Thay dữ liệu bằng tham số mô hình là numerosity reduction.", "Lấy mẫu phân tầng là numerosity reduction.", "Lưu phân phối tần suất là numerosity reduction."],
      "Numerosity: regression, sampling, histogram, clustering (bớt dòng). PCA thuộc dimensionality reduction (bớt cột).",
      "Gộp mọi kỹ thuật “giảm” vào một nhóm.", "Bớt cột → PCA · Bớt dòng → regression, sampling, histogram, clustering."),
    # --- Binning (3)
    Q("VD", "Equal-width binning (C4)", "Hạn mức thẻ từ min = 15 đến max = 95 triệu, chia <b>N = 4</b> nhóm equal-width theo quy ước [a, b). Độ rộng nhóm và vị trí của giá trị <b>55</b>:",
      ["Độ rộng 20; 55 thuộc nhóm 3 [55; 75)", "Độ rộng 20; 55 thuộc nhóm 2 [35; 55]", "Độ rộng 23,75; 55 thuộc nhóm 2", "Độ rộng 26,67; 55 thuộc nhóm 2"],
      ["Theo [a, b), giá trị đúng biên thuộc nhóm phía trên.", "Lấy nhầm max/N = 95/4.", "Chia nhầm cho N − 1 = 3."],
      "Width = (95 − 15)/4 = 20: [15; 35), [35; 55), [55; 75), [75; 95]. Giá trị 55 đúng biên nên thuộc nhóm 3.",
      "Quên trừ min hoặc xếp sai giá trị đúng biên.", "Width = (max − min)/N."),
    Q("TH", "Discretization (C4)", "Thu nhập khách hàng lệch nặng (đa số thấp, vài người rất cao). Muốn mỗi nhóm có <b>số khách bằng nhau</b>, nên dùng:",
      ["Equal-frequency binning", "Equal-width binning", "Decimal scaling", "Min-Max normalization"],
      ["Equal-width làm các nhóm phía giá trị cao gần như rỗng.", "Decimal scaling là chuẩn hoá thang đo, không rời rạc hoá.", "Min-Max là chuẩn hoá thang đo."],
      "Equal-frequency chia đều số bản ghi, hợp với dữ liệu lệch; equal-width chia đều khoảng giá trị.",
      "Lẫn rời rạc hoá với chuẩn hoá.", "Dữ liệu lệch → equal-frequency."),
    Q("VDC", "Equal-width binning (C4)", "Dữ liệu: 5, 8, 9, 11, 14, 16, 20, 45, 65. Chia <b>3</b> nhóm equal-width theo quy ước [a, b), giá trị max xếp vào nhóm cuối. Số phần tử mỗi nhóm lần lượt là:",
      ["7 – 0 – 2", "3 – 3 – 3", "7 – 1 – 1", "7 – 2 – 0"],
      ["Đó là kết quả của equal-frequency.", "Xếp 45 vào nhóm 2, trong khi 45 đúng biên nên thuộc nhóm 3.", "Đẩy cả 45 và 65 vào nhóm 2."],
      "Width = (65 − 5)/3 = 20: [5; 25) có 7 phần tử; [25; 45) không có phần tử nào; [45; 65] có 45 và 65. Equal-width có thể sinh nhóm rỗng khi dữ liệu lệch.",
      "Xếp sai giá trị đúng biên.", "Đúng biên [a, b) → nhóm phía trên; max → nhóm cuối."),
    # --- Normalization (4)
    Q("VD", "Min-Max (C4)", "Thu nhập có min = 20, max = 180 triệu. Chuẩn hoá Min-Max về [0, 1], thu nhập <b>60 triệu</b> thành:",
      ["0,25", "≈ 0,333", "0,375", "0,75"],
      ["Chia 60 cho max 180, quên trừ min.", "Quên trừ min ở tử số: 60/160.", "Lấy 1 − 0,25."],
      "v′ = (60 − 20)/(180 − 20) = 40/160 = 0,25. Min-Max cho 0 tại min và 1 tại max.",
      "Quên trừ min ở tử hoặc mẫu.", "v′ = (v − min)/(max − min)."),
    Q("VD", "Z-score normalization (C4)", "Tuổi khách hàng có µ = 40, σ = 12. Khách <b>22 tuổi</b> sau chuẩn hoá Z-score bằng:",
      ["−1,5", "1,5", "−0,45", "−0,125"],
      ["Đảo dấu: khách thấp hơn trung bình phải có giá trị âm.", "Chia hiệu số cho µ thay vì σ.", "Chia cho phương sai 144."],
      "v′ = (22 − 40)/12 = −1,5: thấp hơn trung bình 1,5 độ lệch chuẩn. Sau chuẩn hoá cột có trung bình 0, độ lệch chuẩn 1.",
      "Chia cho µ hoặc phương sai.", "v′ = (v − µ)/σ."),
    Q("VD", "Decimal scaling (C4)", "Số dư tài khoản nằm trong khoảng <b>−48.700 đến 12.300</b>. Chuẩn hoá decimal scaling, giá trị −48.700 thành:",
      ["j = 5; −0,487", "j = 4; −4,87", "j = 6; −0,0487", "j = 5; −4,87"],
      ["Với j = 4, |v′| = 4,87 ≥ 1, vi phạm điều kiện |v′| < 1.", "j = 6 không phải số nhỏ nhất thoả điều kiện.", "Chia 48.700 cho 10⁵ được 0,487, không phải 4,87."],
      "max |v| = 48.700 (5 chữ số phần nguyên) → j = 5 nhỏ nhất để 10⁵ > 48.700 → v′ = −48.700/10⁵ = −0,487.",
      "Lấy max theo giá trị dương thay vì giá trị tuyệt đối.", "j = số chữ số phần nguyên của max |v|."),
    Q("VDC", "Decimal scaling (C4)", "Dữ liệu có giá trị tuyệt đối lớn nhất đúng bằng <b>1.000.000</b>. Theo điều kiện mọi |v′| &lt; 1, chọn j và giá trị chuẩn hoá của 1.000.000 là:",
      ["j = 7; 0,1", "j = 6; 1", "j = 6; 0,1", "j = 7; 1"],
      ["Với j = 6, v′ = 1 vi phạm |v′| < 1 (bẫy khi max là luỹ thừa của 10).", "10⁶ cho 1.000.000/10⁶ = 1, không phải 0,1.", "10⁷ cho 0,1, không phải 1."],
      "Cần 10^j > 1.000.000 → j = 7 → v′ = 0,1. Quy tắc “10^j ≥ max” trong slide sẽ cho j = 6 và v′ = 1, trái điều kiện |v′| < 1.",
      "Dùng dấu ≥ khi max đúng bằng luỹ thừa của 10.", "j = số chữ số phần nguyên của max |v| (1.000.000 có 7 chữ số)."),
    # --- Entropy, Information Gain (4)
    Q("NB", "Entropy (C4)", "Với bài toán 2 lớp, entropy của tập có tỷ lệ <b>50/50</b> và của tập <b>chỉ một lớp</b> lần lượt là:",
      ["1 và 0", "0 và 1", "0,5 và 0", "1 và 0,5"],
      ["Đảo ngược: thuần hoàn toàn thì entropy 0.", "Nhầm entropy với tỷ lệ lớp.", "Tập thuần có entropy 0."],
      "Entropy đo độ hỗn loạn (không chắc chắn): lẫn lộn tối đa (1/2 – 1/2) cho 1 bit, thuần hoàn toàn cho 0.",
      "Đảo hai trường hợp.", "50/50 → 1 · thuần → 0."),
    Q("VD", "Entropy (C4)", "Một nút có <b>6 Yes và 2 No</b>. Entropy (log cơ số 2) của nút là:",
      ["≈ 0,8113", "≈ 0,5623", "1", "≈ 0,9183"],
      ["Dùng log tự nhiên ln thay vì log₂.", "Đó là entropy của tập 50/50.", "Đó là entropy của tỷ lệ 1/3 – 2/3."],
      f"p = 3/4 và 1/4: H = −0,75·log₂0,75 − 0,25·log₂0,25 = 0,3113 + 0,5 = {num(H(6, 2))} ≈ 0,8113.",
      "Dùng sai cơ số log.", "Hai lớp 1/4 – 3/4 → 0,8113."),
    Q("VDC", "Information Gain (C4)", "Tập D có 10 dòng (5 Yes, 5 No). Thuộc tính X chia D thành X1: 4 Yes, 0 No và X2: 1 Yes, 5 No. <b>Gain(X)</b> xấp xỉ:",
      ["0,61", "0,39", "0,35", "1"],
      ["0,39 là Info_X(D), entropy còn lại sau khi tách.", "Lấy 1 − H(X2) = 1 − 0,65, quên trọng số 6/10.", "Gain = 1 chỉ khi mọi nhánh đều thuần."],
      f"Info(D) = 1. H(X1) = 0; H(X2) = H(1/6) ≈ {num(H(1, 5))}. Info_X = 0,4·0 + 0,6·0,65 ≈ {num(0.6 * H(1, 5))}. Gain = 1 − 0,39 ≈ {num(1 - 0.6 * H(1, 5), 2)}.",
      "Nhầm Info_A(D) với Gain hoặc quên trọng số |Dj|/|D|.", "Gain(A) = Info(D) − Σ |Dj|/|D| · Info(Dj)."),
    Q("TH", "Information Gain (C4)", "Ở mỗi nút cây quyết định, ID3 chọn thuộc tính tách theo tiêu chí nào?",
      ["Gain lớn nhất (tương đương Info_A(D) nhỏ nhất)", "Entropy sau khi tách lớn nhất", "Thuộc tính có nhiều giá trị khác nhau nhất", "Thuộc tính xuất hiện đầu tiên trong bảng"],
      ["Entropy sau tách lớn nghĩa là còn lẫn lộn nhiều – tệ nhất.", "Nhiều giá trị là nguyên nhân gây thiên vị, không phải tiêu chí.", "Thứ tự cột không liên quan."],
      "Thuộc tính làm giảm độ hỗn loạn nhiều nhất được chọn. Ví dụ slide: Credit History có Gain ≈ 0,5488 nên làm nút gốc.",
      "Chọn entropy lớn nhất vì nhầm hướng.", "Gain max ⇔ Info_A(D) min."),
]

# ---------------------------------------------------------------- Chương 5: CSDL giao dịch dùng chung
DB = {1: "TT, TD, VTD", 2: "TT, TD", 3: "TT, TK", 4: "TD, VTD, BH", 5: "TT, TD, VTD, BH",
      6: "TT, TK, BH", 7: "TD, VTD", 8: "TT, TD, TK", 9: "TT, VTD", 10: "TT, TD, VTD, TK"}
_T = {k: set(v.split(", ")) for k, v in DB.items()}


def cnt(*items):
    return sum(1 for t in _T.values() if set(items) <= t)


N = len(_T)
assert (cnt("TD"), cnt("VTD"), cnt("TD", "VTD"), cnt("TT"), cnt("TT", "VTD"), cnt("TT", "TD"), cnt("TT", "TD", "VTD")) == (7, 6, 5, 8, 4, 5, 3)
_sup = Fr(cnt("TD", "VTD"), N)                       # 1/2
_conf = Fr(cnt("TD", "VTD"), cnt("TD"))              # 5/7
_lift = _conf / Fr(cnt("VTD"), N)                    # 25/21
assert _sup == Fr(1, 2) and _conf == Fr(5, 7) and abs(float(_lift) - 1.19) < 0.005
assert Fr(cnt("TT", "VTD"), cnt("TT")) / Fr(cnt("VTD"), N) == Fr(5, 6)
_DBT = ("<p>CSDL 10 giao dịch (TT = tài khoản thanh toán, TD = thẻ tín dụng, VTD = vay tiêu dùng, BH = bảo hiểm, TK = tiết kiệm):</p>"
        + table(["TID", "Sản phẩm", "TID", "Sản phẩm"], [[k, DB[k], k + 5, DB[k + 5]] for k in range(1, 6)]))

# DBSCAN trên trục số, Eps = 1, MinPts = 3 (tính cả chính điểm)
_PTS = [2, 3, 4, 5, 9, 10, 11, 15, 22]
_nb = {p: [q for q in _PTS if abs(p - q) <= 1] for p in _PTS}
_core = [p for p in _PTS if len(_nb[p]) >= 3]
_border = [p for p in _PTS if p not in _core and any(q in _core for q in _nb[p])]
_noise = [p for p in _PTS if p not in _core and p not in _border]
assert (_core, _border, _noise) == ([3, 4, 10], [2, 5, 9, 11], [15, 22])
_DBS = "Các điểm trên trục số: 2, 3, 4, 5, 9, 10, 11, 15, 22; Eps = 1, MinPts = 3 (tính cả chính điểm đang xét)."

assert abs(H(2, 2, 4) - 1.5) < 1e-12
_py, _pn = 0.6 * 0.5 * 0.4, 0.4 * 0.25 * 0.75
assert abs(_py / (_py + _pn) - 0.615) < 1e-3
assert sum([1, 3, 4, 8, 50]) / 5 == 13.2

CH5 = [
    # --- Support, Confidence, Lift (6)
    Q("VD", "Support (C5)", _DBT + "<b>Support</b> của luật {TD} ⇒ {VTD} là:",
      ["0,5", "≈ 0,714", "0,7", "≈ 0,833"],
      ["Đó là Confidence (chia cho số giao dịch có TD).", "Đó là support của riêng {TD}.", "Đó là Confidence của luật ngược VTD ⇒ TD."],
      "Giao dịch chứa cả TD và VTD: 1, 4, 5, 7, 10 → 5. Support = 5/10 = 0,5.",
      "Chia cho số giao dịch có tiền đề thay vì tổng số giao dịch.", "Support = #(X và Y) / #giao dịch."),
    Q("VD", "Confidence (C5)", _DBT + "<b>Confidence</b> của luật {TD} ⇒ {VTD} là:",
      ["≈ 0,714", "0,5", "≈ 0,833", "0,6"],
      ["Đó là Support (chia cho 10).", "Chia cho số giao dịch có VTD (6) – đó là luật ngược.", "Đó là xác suất có VTD nói chung."],
      "TD có ở 7 giao dịch (1, 2, 4, 5, 7, 8, 10); trong đó 5 giao dịch có VTD → Conf = 5/7 ≈ 0,714.",
      "Chia nhầm cho số giao dịch có hậu đề.", "Confidence = #(X và Y) / #(X)."),
    Q("VD", "Lift (C5)", _DBT + "<b>Lift</b> của luật {TD} ⇒ {VTD} xấp xỉ:",
      ["1,19", "1,02", "0,71", "0,83"],
      ["Chia Confidence cho P(TD) = 0,7 thay vì P(VTD).", "Dừng ở Confidence, chưa chia cho P(VTD).", "Lấy Support/P(VTD) = 0,5/0,6, quên chia thêm P(TD)."],
      f"Conf = 5/7 ≈ 0,714; P(VTD) = 6/10 = 0,6 → Lift = 0,714/0,6 ≈ {num(_lift, 2)}. Kiểm tra: 0,5/(0,7 × 0,6) ≈ 1,19 > 1 → quan hệ tích cực.",
      "Chia cho xác suất tiền đề thay vì hậu đề.", "Lift = Conf / P(Y) = P(X∩Y) / (P(X)·P(Y))."),
    Q("VDC", "Đổi chiều luật (C5)", _DBT + "Đổi luật {TD} ⇒ {VTD} thành <b>{VTD} ⇒ {TD}</b>. Nhận định nào đúng?",
      ["Support 0,5 và Lift ≈ 1,19 giữ nguyên; Confidence thành ≈ 0,833", "Ba chỉ số Support, Confidence, Lift giữ nguyên", "Support giữ nguyên ở 0,5; Confidence và Lift cùng thay đổi theo chiều", "Confidence giữ nguyên ≈ 0,714; Support thay đổi"],
      ["Confidence đổi vì mẫu số thành số giao dịch có VTD.", "Lift = P(X∩Y)/(P(X)P(Y)) đối xứng nên không đổi.", "Support là số giao dịch chứa cả hai, không phụ thuộc chiều."],
      "Support và Lift đối xứng theo X, Y. Confidence(VTD ⇒ TD) = 5/6 ≈ 0,833 vì mẫu số là 6 giao dịch có VTD.",
      "Nghĩ đổi chiều thì mọi chỉ số đều đổi.", "Đổi chiều: Support, Lift giữ nguyên; Confidence đổi."),
    Q("VDC", "Lift (C5)", _DBT + "Với luật <b>{TT} ⇒ {VTD}</b>, nhận định nào đúng?",
      ["Lift ≈ 0,83 < 1: có TT làm giảm khả năng có VTD", "Lift ≈ 1,2 > 1: có TT làm tăng khả năng có VTD", "Lift = 1: TT và VTD độc lập", "Confidence = 0,8 nên luật rất mạnh"],
      ["Tính sai; Conf = 4/8 = 0,5 nhỏ hơn P(VTD) = 0,6.", "Lift chỉ bằng 1 khi Conf = P(Y).", "Lấy nhầm support của TT (0,8) làm Confidence."],
      "TT có ở 8 giao dịch, trong đó 4 có VTD → Conf = 0,5; P(VTD) = 0,6 → Lift = 0,5/0,6 ≈ 0,83 < 1: quan hệ tiêu cực.",
      "Thấy Confidence 50% là kết luận luật có ích.", "Lift > 1 tích cực · = 1 độc lập · < 1 tiêu cực."),
    Q("VDC", "Ngưỡng minsup, minconf (C5)", _DBT + "Với minsup = 0,25 và minconf = 0,7, luật <b>{TT, TD} ⇒ {VTD}</b> có được giữ lại không?",
      ["Không: Support 0,3 đạt nhưng Confidence 0,6 không đạt", "Có: Support 0,3 và Confidence 0,6 đều đạt ngưỡng đã cho", "Không: Support 0,3 không đạt minsup", "Có: Confidence ≈ 0,71 đạt minconf"],
      ["0,6 < 0,7 nên Confidence không đạt.", "0,3 ≥ 0,25 nên Support đạt; lý do loại là Confidence.", "Nhầm với Confidence của luật {TD} ⇒ {VTD}."],
      "{TT, TD} có ở 5 giao dịch (1, 2, 5, 8, 10); cả ba có ở 1, 5, 10 → Support = 3/10 = 0,3 ≥ 0,25; Confidence = 3/5 = 0,6 < 0,7 → loại.",
      "Chỉ kiểm tra một ngưỡng.", "Luật được giữ khi vượt cả minsup lẫn minconf."),
    # --- Apriori (5)
    Q("NB", "Tính chất Apriori (C5)", "<b>Tính chất Apriori</b> (anti-monotone) phát biểu rằng:",
      ["Mọi tập con của một tập phổ biến đều phổ biến", "Tập cha của tập phổ biến thì cũng phổ biến", "Tập con của tập không phổ biến thì cũng không phổ biến", "Support của tập cha luôn lớn hơn support của tập con"],
      ["Tập cha có support ≤ tập con nên có thể không phổ biến.", "Tập con có support ≥ tập cha nên có thể vẫn phổ biến.", "Ngược lại: X ⊆ Y thì Sup(Y) ≤ Sup(X)."],
      "Giao dịch chứa Y thì chứa mọi tập con của Y, nên Sup(tập cha) ≤ Sup(tập con). Nhờ vậy loại sớm ứng viên có tập con không phổ biến mà không cần đếm.",
      "Đảo chiều “cha – con”.", "Con của phổ biến → phổ biến; cha của không phổ biến → không phổ biến."),
    Q("VD", "Apriori (C5)", "Tập item I có <b>6</b> item. Số tập con <b>khác rỗng</b> có thể có là:",
      ["63", "64", "62", "36"],
      ["Quên trừ tập rỗng (2⁶).", "Trừ nhầm 2.", "Tính nhầm 6²."],
      "Số tập con khác rỗng của n item là 2ⁿ − 1 = 2⁶ − 1 = 63 – lý do không thể đếm hết mà cần Apriori.",
      "Quên trừ tập rỗng.", "Số tập con khác rỗng = 2ⁿ − 1."),
    Q("VD", "Apriori (C5)", "Sau vòng 1, Apriori có <b>8</b> item phổ biến. Số ứng viên kích thước 2 được sinh ra là:",
      ["28", "64", "56", "16"],
      ["Tính 8², đếm cả cặp trùng và cặp đảo thứ tự.", "Tính 8 × 7, đếm mỗi cặp hai lần.", "Tính 8 × 2."],
      "Số cặp không thứ tự = n(n − 1)/2 = 8 × 7/2 = 28 ≈ n²/2 – điểm yếu sinh nhiều ứng viên của Apriori.",
      "Quên chia 2 vì cặp {a, b} và {b, a} là một.", "Ứng viên cỡ 2 = n(n − 1)/2."),
    Q("VD", "Apriori (C5)", "Các tập phổ biến kích thước 2 là {A, B}, {A, C}, {A, D}, {B, C}, {C, D}. Ứng viên kích thước 3 nào bị <b>loại ngay mà không cần đếm</b>?",
      ["{A, B, D}", "{A, B, C}", "{A, C, D}", "Không ứng viên nào bị loại"],
      ["Mọi tập con 2 phần tử {A, B}, {A, C}, {B, C} đều phổ biến.", "Mọi tập con {A, C}, {A, D}, {C, D} đều phổ biến.", "{A, B, D} chứa {B, D} không phổ biến nên bị loại."],
      "{A, B, D} có tập con {B, D} không nằm trong danh sách phổ biến → theo tính chất Apriori, nó chắc chắn không phổ biến, khỏi đếm.",
      "Chỉ ghép rồi đếm mà quên bước tỉa.", "Ứng viên có tập con không phổ biến → loại không cần đếm."),
    Q("VD", "Minimum support (C5)", "CSDL có 10 giao dịch, minsup = 30%. Tập {X, Y} xuất hiện trong đúng <b>3</b> giao dịch. Kết luận:",
      ["Phổ biến, vì 3/10 = 30% ≥ minsup", "Không phổ biến, vì support phải lớn hơn hẳn minsup", "Không phổ biến, vì 3 nhỏ hơn 30", "Chưa kết luận được, phải xét thêm Confidence"],
      ["Điều kiện là ≥: bằng ngưỡng vẫn phổ biến.", "So nhầm số đếm tuyệt đối với tỷ lệ phần trăm.", "Tập phổ biến chỉ xét support; Confidence dùng cho luật."],
      "Itemset phổ biến nếu support ≥ minsup. Phải so cùng dạng: 3/10 = 30% (tương đối) hoặc 3 ≥ 3 giao dịch (tuyệt đối).",
      "Dùng dấu > thay vì ≥, hoặc so số đếm với tỷ lệ.", "Phổ biến ⇔ support ≥ minsup (cùng dạng đo)."),
    # --- FP-Growth (5)
    Q("NB", "FP-Growth (C5)", "So với Apriori, <b>FP-Growth</b> quét CSDL bao nhiêu lần và có sinh ứng viên không?",
      ["Đúng 2 lần; không sinh ứng viên", "Một lần cho mỗi kích thước k; có sinh ứng viên", "Đúng 1 lần; có sinh ứng viên", "Đúng 2 lần; sinh ứng viên kích thước 2"],
      ["Đó là cách làm của Apriori.", "Lần 1 đếm item, lần 2 chèn giao dịch vào cây – cần 2 lần.", "FP-Growth tìm tập phổ biến trực tiếp trên cây, không sinh ứng viên."],
      "Lần quét 1 đếm support từng item; lần quét 2 lọc, sắp xếp và chèn từng giao dịch vào FP-tree. Sau đó khai thác trên cây.",
      "Nhớ nhầm số lần quét.", "FP-Growth: 2 lần quét, không ứng viên."),
    Q("VD", "FP-tree (C5)", "Với minsupportcount = 3, thứ tự item cố định theo support giảm dần là F, C, A, B, M (Z có count 1). Giao dịch {M, A, Z, F} được chèn vào FP-tree dưới dạng:",
      ["F, A, M", "M, A, F", "F, A, M, Z", "A, F, M"],
      ["Giữ nguyên thứ tự gốc; mọi giao dịch phải theo đúng thứ tự cố định.", "Quên bỏ Z không phổ biến.", "Sắp theo bảng chữ cái thay vì support giảm dần."],
      "Bỏ item không phổ biến (Z), sắp các item còn lại theo thứ tự cố định F, C, A, B, M → F, A, M. Cùng thứ tự thì các giao dịch mới chung tiền tố để nén.",
      "Quên lọc item không phổ biến hoặc sai thứ tự.", "Lọc item < minsup, sắp theo support giảm dần."),
    Q("VDC", "Conditional Pattern Base (C5)", "CPB của item P gồm các đường: ⟨F, C, A, M⟩ : 2, ⟨C, B⟩ : 1, ⟨F, B⟩ : 1. Với minsupportcount = 3, các item phổ biến trong CPB của P là:",
      ["{F, C}", "Không item nào đạt", "{C}", "{F, C, B}"],
      ["Đếm số đường chứa item (F: 2 đường, C: 2 đường) thay vì cộng count.", "F cũng có 2 + 1 = 3.", "B chỉ có 1 + 1 = 2 < 3."],
      "Cộng count của các đường chứa item: F = 2 + 1 = 3; C = 2 + 1 = 3; B = 1 + 1 = 2; A = M = 2. Đạt ngưỡng: F, C → tập phổ biến {F, P}, {C, P}, {F, C, P}.",
      "Đếm số đường thay vì cộng count.", "Đếm trong CPB = cộng count các đường chứa item."),
    Q("TH", "Conditional Pattern Base (C5)", "Khi lập CPB của item x, <b>count</b> của mỗi đường tiền tố được lấy theo đâu?",
      ["Count của nút x ở cuối đường đó", "Count của nút gốc của nhánh", "Count lớn nhất trên đường", "Số nút trên đường"],
      ["Nút đầu nhánh có thể được nhiều giao dịch khác dùng chung.", "Không phải quy tắc của FP-Growth.", "Số nút không liên quan count."],
      "Đường ⟨F, C, A, M⟩ dẫn tới nút P2 được ghi “: 2” vì lấy count của nút P, không phải của F (F4). Xử lý CPB từ item cuối bảng lên.",
      "Lấy count của nút đầu nhánh.", "Count đường = count nút item đang xét."),
    Q("VDC", "FP-Growth (C5)", "Conditional FP-tree của item M là một đường đơn ⟨F:3, C:3, A:3⟩ (minsupportcount = 3). Có bao nhiêu tập phổ biến <b>chứa M</b> (kể cả {M})?",
      ["8", "7", "3", "4"],
      ["Quên tập {M}.", "Chỉ đếm các tập 2 phần tử {F, M}, {C, M}, {A, M}.", "Đếm thêm {M} vào 3 tập 2 phần tử, bỏ sót tập 3 và 4 phần tử."],
      "Ghép M với mọi tổ hợp khác rỗng của {F, C, A}: 2³ − 1 = 7 tập, cộng {M} → 8.",
      "Bỏ sót tập con lớn hoặc chính {M}.", "Đường đơn k item → 2ᵏ − 1 tổ hợp ghép với item đang xét."),
    # --- ID3 / C4.5 (4)
    Q("NB", "ID3 và C4.5 (C5)", "Ghép đúng thuật toán với tiêu chí chọn thuộc tính:",
      ["ID3 – Information Gain; C4.5 – Gain Ratio", "ID3 – Gain Ratio; C4.5 – Information Gain", "ID3 – Gini; C4.5 – Entropy", "ID3 và C4.5 đều dùng Gain Ratio"],
      ["Đảo ngược.", "Slide không dùng Gini cho hai thuật toán này.", "ID3 dùng Information Gain."],
      "C4.5 chia Gain cho SplitInfo để sửa thiên vị của Information Gain với thuộc tính nhiều giá trị.",
      "Đảo tiêu chí hai thuật toán.", "ID3 ↔ Gain · C4.5 ↔ Gain Ratio."),
    Q("TH", "ID3 và C4.5 (C5)", "Khả năng nào <b>chỉ C4.5</b> có, ID3 không có?",
      ["Xử lý dữ liệu liên tục, giá trị thiếu và có post-pruning", "Dựng cây quyết định theo kiểu từ nút gốc xuống các nút lá", "Dùng entropy để đo độ hỗn loạn của tập dữ liệu", "Dự đoán nhãn lớp cho bản ghi mới chưa có nhãn"],
      ["Cả hai đều dựng cây từ trên xuống.", "Cả hai đều dựa trên entropy.", "Cả hai đều là thuật toán phân lớp."],
      "C4.5: chọn ngưỡng t để tách thuộc tính liên tục; chia bản ghi thiếu vào các nhánh theo trọng số; dựng cây đầy đủ rồi cắt nhánh (post-pruning) nên ít overfitting.",
      "Chọn đặc điểm chung của hai thuật toán.", "Chỉ C4.5: liên tục · Null · post-pruning."),
    Q("VDC", "Gain Ratio (C5)", "Thuộc tính A có Gain(A) = 0,30 và chia 8 dòng thành ba nhánh 2 / 2 / 4. <b>GainRatio(A)</b> bằng:",
      ["0,2", "0,3", "0,45", "0,15"],
      ["Quên chia cho SplitInfo.", "Nhân Gain với SplitInfo thay vì chia.", "Chia cho 2 thay vì SplitInfo."],
      "SplitInfo = −(2/8·log₂2/8)·2 − 4/8·log₂4/8 = 0,5 + 0,5 + 0,5 = 1,5 → GainRatio = 0,30/1,5 = 0,2.",
      "Nhân thay vì chia, hoặc quên SplitInfo.", "GainRatio = Gain / SplitInfo."),
    Q("TH", "Gain Ratio (C5)", "Cột Customer (mỗi khách một giá trị) có Information Gain cao nhất nhưng vô dụng để dự đoán. C4.5 khắc phục bằng cách nào?",
      ["Chia Gain cho SplitInfo, vốn lớn khi thuộc tính nhiều giá trị", "Loại bỏ mọi thuộc tính có nhiều hơn 2 giá trị khác nhau", "Cắt tỉa cây ngay trong lúc dựng (pre-pruning) để bỏ nhánh thừa", "Chuẩn hoá Min-Max cột Customer trước khi tính Gain"],
      ["C4.5 không loại cứng thuộc tính.", "C4.5 dùng post-pruning (cắt sau).", "Chuẩn hoá không làm giảm số giá trị khác nhau."],
      "Cột Customer: Gain = 1 nhưng SplitInfo = log₂8 = 3 → GainRatio = 0,333 < 0,575 của Credit History, nên Credit History vẫn được chọn.",
      "Nghĩ C4.5 cắt tỉa trước.", "Gain Ratio phạt thuộc tính nhiều giá trị."),
    # --- Bayes (4)
    Q("NB", "Naive Bayes (C5)", "Giả định <b>“naive”</b> trong Naive Bayes là:",
      ["Các thuộc tính độc lập với nhau khi đã biết lớp", "Các lớp có xác suất tiên nghiệm bằng nhau", "Dữ liệu tuân theo phân phối chuẩn", "Các thuộc tính phụ thuộc theo một đồ thị có hướng"],
      ["Naive Bayes dùng P(C) đúng theo tỷ lệ lớp trong dữ liệu.", "Không phải giả định “naive”.", "Đó là mạng Bayes, vốn bỏ giả định độc lập."],
      "Nhờ giả định độc lập có điều kiện: P(C | X) ∝ P(C) · Π P(xk | C).",
      "Lẫn Naive Bayes với mạng Bayes.", "Naive = độc lập có điều kiện khi biết lớp."),
    Q("TH", "Mạng Bayes (C5)", "Điểm khác cơ bản của <b>mạng Bayes</b> so với Naive Bayes:",
      ["Mô hình hoá phụ thuộc giữa các biến bằng đồ thị có hướng (DAG)", "Giả định mọi thuộc tính độc lập có điều kiện hoàn toàn khi đã biết lớp", "Không dùng tới xác suất có điều kiện giữa các biến", "Chỉ áp dụng cho bài toán phân cụm, không phân lớp"],
      ["Đó chính là giả định naive mà mạng Bayes bỏ đi.", "Mỗi nút kèm bảng xác suất có điều kiện theo nút cha.", "Mạng Bayes dùng cho suy luận xác suất, phân lớp."],
      "Mũi tên U → V nghĩa là V phụ thuộc trực tiếp vào U. Slide gọi “Naive Bayes Network” nhưng tên chuẩn là Bayesian Network và nó không “naive”.",
      "Tin tên gọi “Naive Bayes Network” trong slide.", "Mạng Bayes = DAG phụ thuộc + bảng xác suất có điều kiện."),
    Q("VDC", "Naive Bayes (C5)", "Cho P(Yes) = 0,6; P(x1|Yes) = 0,5; P(x2|Yes) = 0,4; P(No) = 0,4; P(x1|No) = 0,25; P(x2|No) = 0,75. Với X = (x1, x2), Naive Bayes dự đoán và xác suất chuẩn hoá P(Yes | X) là:",
      ["Yes; ≈ 0,62", "No; ≈ 0,62", "Yes; 0,12", "No; ≈ 0,38"],
      ["Tích của No (0,075) nhỏ hơn của Yes (0,12).", "0,12 là tích chưa chuẩn hoá.", "0,38 là P(No | X); lớp dự đoán là Yes."],
      "Yes: 0,6 × 0,5 × 0,4 = 0,12; No: 0,4 × 0,25 × 0,75 = 0,075 → chọn Yes. Chuẩn hoá: 0,12/(0,12 + 0,075) ≈ 0,615.",
      "Quên nhân xác suất tiên nghiệm P(C).", "So P(C)·Π P(xk|C) giữa các lớp."),
    Q("TH", "Naive Bayes (C5)", "Khi so sánh các lớp trong Naive Bayes, vì sao có thể bỏ mẫu số P(X)?",
      ["P(X) như nhau cho mọi lớp nên không đổi lớp thắng", "P(X) luôn bằng 1 với mọi bản ghi", "P(X) luôn bằng 0 nên có thể bỏ qua", "P(X) đã được tính sẵn bên trong xác suất tiên nghiệm P(C)"],
      ["P(X) là xác suất của một bản ghi cụ thể, thường rất nhỏ.", "Nếu bằng 0 công thức không xác định.", "P(C) là xác suất tiên nghiệm của lớp, không chứa P(X)."],
      "P(C | X) = P(X | C)·P(C)/P(X); mẫu chung cho mọi lớp nên chỉ cần so tử số. Muốn ra xác suất thật thì chuẩn hoá theo tổng các tử số.",
      "Nghĩ P(X) bằng 1.", "So tử số; chuẩn hoá nếu cần xác suất."),
    # --- KMeans, KMedoids (4)
    Q("VD", "KMeans và KMedoids (C5)", "Một cụm gồm các giá trị 1, 3, 4, 8, 50. <b>Tâm KMeans (mean)</b> và <b>medoid</b> lần lượt là:",
      ["13,2 và 4", "4 và 13,2", "13,2 và 8", "4 và 4"],
      ["Đảo hai khái niệm.", "Medoid là điểm có tổng khoảng cách nhỏ nhất: từ 8 là 58, từ 4 là 54.", "Mean bị 50 kéo lên, không phải 4."],
      "Mean = 66/5 = 13,2 (không trùng điểm nào, bị 50 kéo). Tổng khoảng cách: từ 1 là 61, từ 3 là 55, từ 4 là 54, từ 8 là 58, từ 50 là 184 → medoid = 4.",
      "Lấy trung vị thay vì tính tổng khoảng cách.", "Mean nhạy ngoại lai; medoid là điểm thật có tổng khoảng cách nhỏ nhất."),
    Q("TH", "Biến thể KMeans (C5)", "Dữ liệu khách hàng gồm <b>cả cột số lẫn cột phân loại</b>. Biến thể phân cụm phù hợp:",
      ["KPrototypes", "KModes", "Mini-Batch KMeans", "CLARA"],
      ["KModes chỉ dành cho dữ liệu phân loại.", "Mini-Batch KMeans tăng tốc KMeans cho Big Data, vẫn cần dữ liệu số.", "CLARA là bản lấy mẫu của KMedoids cho dữ liệu lớn."],
      "KModes thay mean bằng mode cho dữ liệu phân loại; KPrototypes lai KMeans + KModes cho dữ liệu hỗn hợp.",
      "Lẫn KModes và KPrototypes.", "Phân loại → KModes · Hỗn hợp → KPrototypes · KMedoids lớn → CLARA/CLARANS."),
    Q("TH", "Biến thể KMeans (C5)", "Muốn dùng KMedoids (chống nhiễu) nhưng dữ liệu quá lớn khiến thuật toán rất chậm. Nên chọn:",
      ["CLARA / CLARANS", "KModes", "KPrototypes", "AGNES"],
      ["KModes dành cho dữ liệu phân loại.", "KPrototypes dành cho dữ liệu hỗn hợp.", "AGNES là phân cụm phân cấp, càng chậm với dữ liệu lớn."],
      "CLARA chạy KMedoids trên vài mẫu con rồi chọn kết quả tốt nhất; CLARANS tìm medoid bằng thử ngẫu nhiên thay vì thử hết.",
      "Chọn biến thể theo loại dữ liệu thay vì theo quy mô.", "KMedoids + dữ liệu lớn → CLARA/CLARANS."),
    Q("NB", "KMeans và KMedoids (C5)", "So sánh đúng KMeans và KMedoids:",
      ["KMeans nhanh nhưng nhạy ngoại lai; KMedoids chống nhiễu nhưng chậm", "KMeans chống nhiễu tốt; KMedoids nhạy ngoại lai", "KMeans dùng điểm thật làm tâm cụm; KMedoids dùng trọng tâm ảo (mean)", "KMeans không cần biết trước số cụm k"],
      ["Đảo ngược ưu nhược.", "Đảo ngược loại tâm.", "Cả hai đều cần biết trước k."],
      "Mean (trọng tâm ảo) ↔ KMeans ↔ nhanh, nhạy ngoại lai. Medoid (điểm thật) ↔ KMedoids ↔ chống nhiễu, chậm, dùng được mọi loại dữ liệu.",
      "Đảo ưu nhược hai thuật toán.", "Mean–nhanh–nhạy · Medoid–bền–chậm."),
    # --- DBSCAN (5)
    Q("VD", "DBSCAN (C5)", _DBS + " Có bao nhiêu điểm <b>core</b>?",
      ["3", "4", "7", "2"],
      ["Tính nhầm 2 (lân cận {2, 3}) là core.", "Đếm cả các điểm border.", "Chỉ đếm một core mỗi cụm."],
      "Lân cận trong bán kính 1: 3 → {2, 3, 4}, 4 → {3, 4, 5}, 10 → {9, 10, 11} đủ 3 điểm → core. 2, 5, 9, 11 chỉ có 2 điểm.",
      "Quên tính chính điểm hoặc đếm sai lân cận.", "Core: ≥ MinPts điểm trong bán kính Eps."),
    Q("VD", "DBSCAN (C5)", _DBS + " Điểm <b>5</b> thuộc loại nào?",
      ["Border", "Core", "Noise", "Không xác định nếu không biết số cụm k"],
      ["Lân cận của 5 chỉ có {4, 5} = 2 điểm < 3.", "5 nằm trong Eps của core 4 nên không phải noise.", "DBSCAN không cần k."],
      "Border: không đủ MinPts nhưng nằm trong vùng Eps của một điểm core (ở đây là 4).",
      "Thấy không đủ MinPts là kết luận noise.", "Border = không đủ MinPts nhưng kề một core."),
    Q("VDC", "DBSCAN (C5)", _DBS + " Kết quả phân cụm là:",
      ["2 cụm và 2 điểm nhiễu", "3 cụm và 1 điểm nhiễu", "2 cụm và 4 điểm nhiễu", "1 cụm và 2 điểm nhiễu"],
      ["15 và 22 không phải core nên không tạo cụm riêng.", "Coi các điểm border là nhiễu.", "Hai nhóm {2–5} và {9–11} cách nhau xa hơn Eps nên không nối được."],
      "Cụm 1: {2, 3, 4, 5}; cụm 2: {9, 10, 11}; nhiễu: 15, 22. Số cụm do thuật toán tự tìm ra.",
      "Coi border là nhiễu.", "Cụm = core loang qua lân cận + border; còn lại là noise."),
    Q("NB", "DBSCAN (C5)", "Ưu điểm nổi bật của <b>DBSCAN</b> so với KMeans:",
      ["Không cần k, tìm cụm hình dạng bất kỳ, tự loại nhiễu", "Luôn chạy nhanh hơn KMeans trên mọi tập dữ liệu", "Không cần đặt bất kỳ tham số đầu vào nào", "Tâm cụm luôn là một điểm thật trong dữ liệu"],
      ["Slide không khẳng định điều này.", "DBSCAN cần Eps và MinPts.", "Đó là đặc điểm của KMedoids."],
      "DBSCAN coi cụm là vùng mật độ dày, loang từ điểm core, nên cụm có thể cong, dài.",
      "Nghĩ DBSCAN không có tham số.", "DBSCAN: không cần k · hình dạng bất kỳ · tự loại nhiễu · tham số Eps, MinPts."),
    Q("TH", "DBSCAN (C5)", "Theo DBSCAN, điểm <b>border</b> là điểm:",
      ["Không đủ MinPts nhưng nằm trong vùng Eps của một điểm core", "Có ít nhất MinPts điểm trong bán kính Eps của nó", "Không đủ MinPts và không nằm trong vùng Eps của điểm core nào", "Nằm ở biên ngoài cùng của toàn bộ tập dữ liệu"],
      ["Đó là điểm core.", "Đó là điểm noise.", "Border định nghĩa theo mật độ, không theo vị trí biên của tập dữ liệu."],
      "Ba loại điểm: core (đủ MinPts), border (không đủ nhưng kề core), noise (không thuộc hai loại trên).",
      "Hiểu “border” theo nghĩa hình học.", "Core · Border · Noise theo Eps và MinPts."),
    # --- Outlier & phân cụm phân cấp/lưới (3)
    Q("TH", "Phát hiện ngoại lai (C5)", "So sánh đúng hai cách phát hiện ngoại lai:",
      ["Thống kê: cần giả định phân phối, nhanh; khoảng cách: không cần, tốn tài nguyên", "Thống kê: không cần giả định phân phối; khoảng cách: cần giả định phân phối chuẩn", "Khoảng cách luôn nhanh hơn thống kê vì không cần tính trung bình", "Thống kê hợp dữ liệu nhiều chiều hơn phương pháp khoảng cách"],
      ["Đảo ngược giả định.", "Khoảng cách phải tính nhiều cặp điểm nên tốn tài nguyên.", "Khoảng cách mới là cách tổng quát cho dữ liệu nhiều chiều."],
      "Statistical-based (ví dụ Z-score |Z| > 3) sai nếu dữ liệu không theo phân phối giả định. Distance-based: điểm có ít hơn k điểm khác trong bán kính r là ngoại lai.",
      "Đảo ưu nhược hai cách.", "Thống kê: giả định + nhanh · Khoảng cách: không giả định + tốn."),
    Q("TH", "Phân cụm lưới (C5)", "Vì sao phân cụm dựa trên lưới (STING, CLIQUE) <b>rất nhanh</b> với dữ liệu lớn?",
      ["Thời gian phụ thuộc số ô lưới chứ không phụ thuộc số điểm", "Nó tính khoảng cách giữa mọi cặp điểm rồi gộp dần các cặp gần nhất", "Nó xây dendrogram từ dưới lên", "Nó chọn medoid bằng thử ngẫu nhiên"],
      ["Đó là lý do phân cụm phân cấp chậm (n(n − 1)/2 cặp).", "Đó là AGNES (phân cấp).", "Đó là CLARANS."],
      "Grid-based gom thông tin điểm vào từng ô rồi gom cụm trên các ô. Đổi lại, độ chính xác ở biên cụm phụ thuộc kích thước ô.",
      "Lẫn grid-based với hierarchical.", "Grid: theo số ô → nhanh · Hierarchical: mọi cặp điểm → chậm."),
    Q("NB", "Phân cụm phân cấp (C5)", "Phân biệt <b>AGNES</b> và <b>DIANA</b>:",
      ["AGNES gộp dần từ dưới lên; DIANA chia dần từ trên xuống", "AGNES chia dần từ trên xuống; DIANA gộp dần từ dưới lên", "AGNES là phân cụm lưới; DIANA là phân cụm mật độ", "Cả hai đều cần biết trước số cụm k khi chạy"],
      ["Đảo ngược hai hướng.", "Cả hai là phân cụm phân cấp.", "Phân cấp tạo dendrogram, cắt ở độ cao nào thì được số cụm tương ứng."],
      "AGNES: mỗi điểm là một cụm, lần lượt gộp hai cụm gần nhất. DIANA: bắt đầu một cụm chứa tất cả rồi tách dần.",
      "Đảo chiều gộp/chia.", "AGNES = Agglomerative (gộp) · DIANA = Divisive (chia)."),
]

# ---------------------------------------------------------------- Chương 6
# CPT: 5 chuỗi huấn luyện, dự đoán phần tử kế tiếp của chuỗi kết thúc bằng ⟨A, B⟩
CPT1 = {"s1": "ABCE", "s2": "BCD", "s3": "ACBDE", "s4": "CABF", "s5": "BDA"}
CPT2 = {"u1": "XYZ", "u2": "YXWZ", "u3": "XZW", "u4": "YW"}


def cpt(db, suffix):
    sim, cons = [], {}
    for k, s in db.items():
        if set(suffix) <= set(s):
            sim.append(k)
            pos = max(s.index(c) for c in suffix)
            cons[k] = s[pos + 1:]
    cnt_ = {}
    for c in cons.values():
        for e in set(c):
            cnt_[e] = cnt_.get(e, 0) + 1
    return sim, cons, {e: Fr(v, len(sim)) for e, v in cnt_.items()}


_s1, _c1, _sc1 = cpt(CPT1, "AB")
assert _s1 == ["s1", "s3", "s4", "s5"] and _c1 == {"s1": "CE", "s3": "DE", "s4": "F", "s5": ""}
assert _sc1 == {"C": Fr(1, 4), "E": Fr(1, 2), "D": Fr(1, 4), "F": Fr(1, 4)}
_s2, _c2, _sc2 = cpt(CPT2, "XY")
assert _s2 == ["u1", "u2"] and _sc2 == {"Z": Fr(1), "W": Fr(1, 2)}
_CPT1T = table(["Chuỗi", "Nội dung"], [[k, "⟨" + ", ".join(v) + "⟩"] for k, v in CPT1.items()])
_CPT2T = table(["Chuỗi", "Nội dung"], [[k, "⟨" + ", ".join(v) + "⟩"] for k, v in CPT2.items()])

# PageRank vòng 1: A→B, A→C, B→C, C→A, D→C, D→A; d = 0,85; khởi tạo PR = 1
_E = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "A"), ("D", "C"), ("D", "A")]
_out = {n: sum(1 for a, _ in _E if a == n) for n in "ABCD"}
_pr1 = {n: 0.15 + 0.85 * sum(1 / _out[a] for a, b in _E if b == n) for n in "ABCD"}
assert {k: round(v, 4) for k, v in _pr1.items()} == {"A": 1.425, "B": 0.575, "C": 1.85, "D": 0.15}
_PRG = "Đồ thị liên kết: A → B, A → C, B → C, C → A, D → C, D → A. Dùng công thức PR(X) = (1 − d) + d·Σ PR(T)/C(T), d = 0,85, vòng 0 mọi PR = 1."

CH6 = [
    # --- In-Database ML (3)
    Q("NB", "In-Database ML (C6)", "Ý chính của <b>In-Database Machine Learning</b> là gì?",
      ["Đưa code tới dữ liệu: huấn luyện, dự báo ngay trong kho", "Trích dữ liệu qua Internet sang máy chủ ML riêng để huấn luyện", "Chỉ huấn luyện mô hình trên laptop của Data Scientist", "Sao chép dữ liệu sang Data Lake trước khi huấn luyện"],
      ["Đó là cách truyền thống: tốn băng thông, trễ, rủi ro bảo mật.", "Vẫn phải kéo dữ liệu ra khỏi kho.", "Vẫn là di chuyển dữ liệu."],
      "In-Database ML loại bỏ độ trễ và chi phí dịch chuyển, dữ liệu vẫn dưới một chế độ quản trị tập trung.",
      "Nghĩ ML bắt buộc chạy ngoài kho.", "In-DB ML = code tới dữ liệu."),
    Q("TH", "In-Database ML (C6)", "Ba lợi ích của In-Database ML theo slide là:",
      ["Scalability, Governance (RBAC), Simplicity", "Discovery, Consistency, Lineage", "Transparency, Human Oversight, Data Quality", "Freshness, Volume, Distribution"],
      ["Đó là ba lợi ích của Feature Store.", "Đó là ba trụ cột của AI Act.", "Đó là ba trong năm trụ cột data observability."],
      "Scalability: tận dụng MPP, auto-scaling của kho. Governance: phân quyền RBAC đồng nhất. Simplicity: dự báo chỉ là thêm một câu SQL vào pipeline ELT.",
      "Lẫn các bộ ba khái niệm giữa các chương.", "In-DB ML: Scalability · Governance · Simplicity."),
    Q("VD", "In-Database ML (C6)", "Ngân hàng muốn <b>chỉ vai trò risk_analyst</b> được gọi mô hình chấm điểm tín dụng, theo đúng cơ chế cấp quyền đọc một bảng. Lợi ích nào của In-Database ML thể hiện ở đây?",
      ["Governance với RBAC đồng nhất", "Scalability nhờ MPP", "Simplicity khi gắn mô hình vào pipeline ELT", "Push-down của Snowpark"],
      ["Scalability nói về xử lý hàng terabyte.", "Simplicity nói về việc dự báo chỉ là một câu SQL.", "Push-down là cơ chế dịch Python sang SQL."],
      "Quyền dùng mô hình được cấp cho role giống quyền trên bảng – một hệ phân quyền cho cả dữ liệu lẫn mô hình.",
      "Chọn Scalability vì nghe quen.", "Phân quyền theo vai trò → Governance (RBAC)."),
    # --- Precision, Recall, F1 (5)
    Q("VD", "Precision (C6)", "Kiểm tra 200 hồ sơ: TP = 30, FP = 10, FN = 20, TN = 140. <b>Precision</b> của mô hình là:",
      ["0,75", "0,6", "0,85", "≈ 0,67"],
      ["Đó là Recall = 30/50.", "Đó là Accuracy = 170/200.", "Đó là F1."],
      "Precision = TP/(TP + FP) = 30/40 = 0,75: trong số hồ sơ mô hình báo dương, 75% đúng.",
      "Lẫn Precision với Recall.", "Precision = TP/(TP + FP)."),
    Q("VD", "Recall và F1 (C6)", "Một mô hình có TP = 45, FP = 15, FN = 5, TN = 135. <b>Recall</b> và <b>F1</b> lần lượt xấp xỉ:",
      ["0,9 và 0,82", "0,75 và 0,82", "0,9 và 0,675", "0,75 và 0,9"],
      ["0,75 là Precision.", "Lấy tích P·R = 0,675 thay vì 2PR/(P + R).", "Đảo Recall và Precision rồi lấy luôn Recall làm F1."],
      "Recall = 45/50 = 0,9; Precision = 45/60 = 0,75; F1 = 2·0,75·0,9/(0,75 + 0,9) ≈ 0,818.",
      "Tính F1 bằng trung bình cộng.", "Recall = TP/(TP + FN) · F1 = 2PR/(P + R)."),
    Q("VD", "F1-score (C6)", "Mô hình có Precision = 0,6 và Recall = 0,9. <b>F1</b> bằng:",
      ["0,72", "0,75", "0,54", "1,5"],
      ["Trung bình cộng (0,6 + 0,9)/2.", "Chỉ lấy tích P·R, quên nhân 2 và chia (P + R).", "Lấy tổng P + R."],
      "F1 = 2 × 0,6 × 0,9/(0,6 + 0,9) = 1,08/1,5 = 0,72 – trung bình điều hoà, bị kéo về phía giá trị nhỏ hơn.",
      "Dùng trung bình cộng.", "F1 = 2PR/(P + R)."),
    Q("VDC", "Dữ liệu mất cân bằng (C6)", "Tập kiểm tra 1.000 giao dịch có 20 giao dịch gian lận. Một mô hình đoán <b>“không gian lận” cho mọi giao dịch</b>. Nhận định nào đúng?",
      ["Accuracy 98% nhưng Recall = 0, mô hình vô dụng để bắt gian lận", "Accuracy 98% nên mô hình rất tốt", "Precision = 98% vì mô hình đoán đúng 980 trên tổng số 1.000 giao dịch", "Recall = 98% vì chỉ bỏ sót 2% dữ liệu"],
      ["Accuracy cao giả tạo do lớp âm chiếm đa số.", "Mô hình không báo dương lần nào nên Precision không xác định (TP + FP = 0).", "Recall = TP/(TP + FN) = 0/20 = 0."],
      "TN = 980, FN = 20, TP = FP = 0 → Accuracy = 98%, Recall = 0. Với dữ liệu mất cân bằng phải xem Precision, Recall, F1.",
      "Tin Accuracy khi dữ liệu mất cân bằng.", "Mất cân bằng → nhìn Recall, Precision, F1."),
    Q("TH", "Precision và Recall (C6)", "Câu hỏi nào mô tả đúng ý nghĩa của <b>Recall</b>?",
      ["Trong số ca dương thật, mô hình bắt được bao nhiêu?", "Trong số ca mô hình báo dương, bao nhiêu thật sự dương?", "Trong toàn bộ dữ liệu, mô hình đoán đúng bao nhiêu?", "Mô hình xếp ca dương cao hơn ca âm với xác suất bao nhiêu?"],
      ["Đó là Precision.", "Đó là Accuracy.", "Đó là ý nghĩa của ROC-AUC."],
      "Recall = TP/(TP + FN): độ phủ ca dương thật. Precision = TP/(TP + FP): độ chính xác khi báo dương.",
      "Đảo Precision và Recall.", "Precision: báo dương có đúng? · Recall: dương thật có bị sót?"),
    # --- CPT (5)
    Q("VDC", "CPT (C6)", "CSDL chuỗi huấn luyện như bảng. Dự đoán phần tử kế tiếp của chuỗi kết thúc bằng ⟨A, B⟩ với hậu tố kích cỡ 2. Phần tử được dự đoán và điểm của nó là:" + _CPT1T,
      ["E, điểm 0,5", "E, điểm 0,4", "E, điểm ≈ 0,67", "C, điểm 0,5"],
      ["Chia cho tổng số chuỗi (5) thay vì số chuỗi tương tự (4).", "Chỉ chia cho 3 chuỗi có mệnh đề kết quả khác rỗng; s5 vẫn là chuỗi tương tự.", "C chỉ xuất hiện trong mệnh đề kết quả của s1."],
      "Chuỗi chứa đủ A và B: s1, s3, s4, s5 (4 chuỗi). Mệnh đề kết quả (phần sau vị trí mà A, B đều đã xuất hiện): s1 → ⟨C, E⟩, s3 → ⟨D, E⟩, s4 → ⟨F⟩, s5 → ⟨⟩. Count: E = 2, C = D = F = 1 → E = 2/4 = 0,5 cao nhất.",
      "Sai mẫu số: tổng số chuỗi hoặc chỉ chuỗi có mệnh đề khác rỗng.", "Điểm CPT = số chuỗi tương tự có e / số chuỗi tương tự."),
    Q("VDC", "CPT (C6)", "CSDL chuỗi như bảng. Dự đoán phần tử kế tiếp của chuỗi kết thúc bằng ⟨X, Y⟩ (hậu tố {X, Y}). Kết quả:" + _CPT2T,
      ["Z, điểm 1,0", "Z, điểm 0,5", "W, điểm 0,5", "W, điểm 1,0"],
      ["Chia cho tổng 4 chuỗi thay vì 2 chuỗi tương tự.", "W chỉ có ở mệnh đề kết quả của u2 → 1/2; Z có ở cả hai.", "W chỉ xuất hiện 1 lần."],
      "Chuỗi chứa cả X và Y: u1, u2 (không cần đúng thứ tự). Mệnh đề: u1 → ⟨Z⟩, u2 = ⟨Y, X, W, Z⟩ → ⟨W, Z⟩. Z = 2/2 = 1,0; W = 1/2 = 0,5 → dự đoán Z.",
      "Đòi chuỗi tương tự phải đúng thứ tự X rồi Y nên bỏ u2.", "Chuỗi tương tự chỉ cần chứa đủ phần tử của hậu tố."),
    Q("NB", "CPT (C6)", "Ba cấu trúc dữ liệu của <b>Compact Prediction Tree</b> là:",
      ["Prediction Tree, Inverted Index, Lookup Table", "FP-tree, Header Table, Node-link", "Prediction Tree, Hash Table, B-tree", "Dendrogram, Inverted Index, Lookup Table"],
      ["Đó là các thành phần của FP-Growth.", "Hash Table và B-tree không thuộc CPT.", "Dendrogram là của phân cụm phân cấp."],
      "Prediction Tree: cây tiền tố lưu chuỗi. Inverted Index: bảng item × chuỗi để tìm nhanh chuỗi chứa tập item. Lookup Table: trỏ mỗi chuỗi tới nút cuối của nhánh.",
      "Lẫn cấu trúc của CPT với FP-tree.", "CPT: Tree · Inverted Index · Lookup Table."),
    Q("TH", "CPT (C6)", "Trong CPT, chuỗi huấn luyện u được coi là <b>tương tự</b> chuỗi cần dự đoán khi:",
      ["u chứa đủ mọi phần tử của hậu tố, theo thứ tự bất kỳ", "u chứa hậu tố liên tiếp và đúng thứ tự", "u có cùng độ dài với chuỗi cần dự đoán", "u bắt đầu bằng phần tử đầu của chuỗi cần dự đoán"],
      ["CPT không đòi liên tiếp hay đúng thứ tự.", "Độ dài không phải tiêu chí.", "Tiêu chí dựa vào hậu tố (phần cuối), không phải phần đầu."],
      "Ví dụ ⟨D, C, B, E⟩ không phải chuỗi tương tự của hậu tố {A, D} vì thiếu A; ⟨E, A, D, C, B⟩ thì có.",
      "Đòi đúng thứ tự như khớp chuỗi con.", "Tương tự = chứa đủ phần tử hậu tố."),
    Q("TH", "CPT (C6)", "Trong CPT, cấu trúc nào giúp tìm nhanh các chuỗi chứa đồng thời A và D (bằng phép AND hai dòng bit)?",
      ["Inverted Index", "Lookup Table", "Prediction Tree", "Count Table"],
      ["Lookup Table trỏ mỗi chuỗi tới nút cuối để lấy lại chuỗi.", "Prediction Tree lưu chuỗi dạng cây tiền tố.", "Count Table ghi điểm ứng viên sau khi đã có mệnh đề kết quả."],
      "Inverted Index là bảng item × chuỗi, ô = 1 nếu chuỗi chứa item. Dòng A = 1, 0, 1, 1; dòng D = 1, 1, 1, 1 → AND = 1, 0, 1, 1.",
      "Lẫn Inverted Index với Lookup Table.", "Tìm chuỗi chứa tập item → Inverted Index."),
    # --- PageRank (5)
    Q("VDC", "PageRank (C6)", _PRG + " <b>PR(C)</b> sau vòng 1 là:",
      ["1,85", "2,7", "1,425", "2,0"],
      ["Quên chia PR của trang nguồn cho số link ra (cộng 1 + 1 + 1).", "Đó là PR(A).", "Quên (1 − d) và d: cộng thẳng 0,5 + 1 + 0,5."],
      "C nhận link từ A (2 link ra), B (1 link ra), D (2 link ra): PR(C) = 0,15 + 0,85 × (1/2 + 1/1 + 1/2) = 0,15 + 1,7 = 1,85.",
      "Chia cho số link vào của trang đích.", "Mẫu số C(T) = số link ra của trang nguồn."),
    Q("VD", "PageRank (C6)", _PRG + " <b>PR(B)</b> sau vòng 1 là:",
      ["0,575", "1", "0,425", "0,15"],
      ["Giữ nguyên giá trị khởi tạo.", "Quên cộng (1 − d) = 0,15.", "Coi như B không có link vào."],
      "B chỉ nhận link từ A, A có 2 link ra: PR(B) = 0,15 + 0,85 × 1/2 = 0,15 + 0,425 = 0,575.",
      "Quên phần (1 − d).", "PR = (1 − d) + d × Σ PR(T)/C(T)."),
    Q("VD", "PageRank (C6)", _PRG + " <b>PR(A)</b> sau vòng 1 là:",
      ["1,425", "1,85", "1,0", "1,275"],
      ["Đó là PR(C).", "Chia nhầm PR(C) cho 2 (C chỉ có 1 link ra).", "Quên cộng (1 − d) = 0,15."],
      "A nhận link từ C (1 link ra) và D (2 link ra): PR(A) = 0,15 + 0,85 × (1 + 1/2) = 0,15 + 1,275 = 1,425.",
      "Đếm sai số link ra của trang nguồn.", "Mỗi trang nguồn chia đều PR cho các trang nó trỏ tới."),
    Q("NB", "PageRank (C6)", "Trong ví dụ PageRank của slide, damping factor d và giá trị khởi tạo PR ở vòng 0 lần lượt là:",
      ["d = 0,85; mọi PR = 1", "d = 0,15; mọi PR = 1", "d = 0,85; mọi PR = 0", "d = 0,5; mọi PR = 1/n"],
      ["0,15 là (1 − d).", "Khởi tạo bằng 0 thì vòng 1 chỉ còn (1 − d) cho mọi trang.", "Không phải giá trị dùng trong slide."],
      "d = 0,85 là xác suất tiếp tục bấm liên kết; lặp đến khi chênh lệch giữa hai vòng nhỏ hơn ε (thường 0,0001), khoảng 50 vòng thì hội tụ.",
      "Lẫn d với 1 − d.", "d = 0,85; vòng 0 PR = 1."),
    Q("TH", "PageRank (C6)", "Trong công thức PageRank, <b>C(Tᵢ)</b> là gì?",
      ["Số liên kết đi ra từ trang nguồn Tᵢ", "Số liên kết đi vào trang đích A", "Tổng số trang trong đồ thị", "Số vòng lặp đã chạy"],
      ["Bẫy hay gặp: mẫu số không phải số link vào của trang đích.", "Đó là n, không xuất hiện trong dạng công thức của slide.", "Không liên quan số vòng."],
      "Trang Tᵢ chia đều điểm của nó cho mọi trang nó trỏ tới, nên mỗi trang nhận PR(Tᵢ)/C(Tᵢ).",
      "Lấy số link vào của trang đích.", "C(T) = số link ra của T."),
    # --- BigQuery ML, Cortex (3)
    Q("NB", "BigQuery ML (C6)", "Thứ tự ba câu lệnh cốt lõi khi làm ML bằng SQL trong BigQuery ML:",
      ["CREATE MODEL → ML.EVALUATE → ML.PREDICT", "ML.PREDICT → CREATE MODEL → ML.EVALUATE", "ML.EVALUATE → CREATE MODEL → ML.PREDICT", "CREATE MODEL → ML.PREDICT → ML.TRAIN"],
      ["Phải huấn luyện trước khi dự báo.", "Phải có mô hình trước khi đánh giá.", "Không có ML.TRAIN; huấn luyện nằm trong CREATE MODEL."],
      "CREATE MODEL khởi tạo và huấn luyện (model_type: LOGISTIC_REG, LINEAR_REG…); ML.EVALUATE lấy precision, recall, ROC-AUC; ML.PREDICT dự báo trên dữ liệu mới.",
      "Bịa thêm lệnh huấn luyện riêng.", "Tạo → Đánh giá → Dự báo."),
    Q("TH", "Snowflake Cortex (C6)", "Hai loại <b>Cortex ML Functions</b> dựng sẵn được nêu trong slide là:",
      ["Forecasting và Anomaly Detection", "Classification và Clustering", "Regression và PCA", "Sentiment và Summarize"],
      ["Không phải hai hàm slide nêu cho Cortex ML Functions.", "Không phải hàm dựng sẵn của Cortex trong slide.", "Đó là hàm thuộc nhóm Cortex AI & LLM, không phải ML Functions."],
      "Cortex có hai nhóm: ML Functions (Forecasting, Anomaly Detection) và AI & LLM (gọi Llama, Mistral bằng SQL để tóm tắt, phân tích cảm xúc).",
      "Lẫn hai nhóm chức năng của Cortex.", "Cortex ML: dự báo + bất thường · Cortex LLM: tóm tắt + cảm xúc."),
    Q("TH", "BigQuery ML (C6)", "Muốn lấy precision, recall, ROC-AUC của mô hình đã huấn luyện trong BigQuery ML bằng một câu SELECT, dùng:",
      ["ML.EVALUATE", "ML.PREDICT", "CREATE MODEL", "SNOWFLAKE.CORTEX.SENTIMENT"],
      ["ML.PREDICT trả kết quả dự báo cho dữ liệu mới.", "CREATE MODEL dùng để huấn luyện.", "Đó là hàm của Snowflake Cortex."],
      "ROC-AUC từ 0,5 (đoán ngẫu nhiên) đến 1 (hoàn hảo), đo khả năng xếp hồ sơ dương cao hơn hồ sơ âm.",
      "Lẫn đánh giá với dự báo.", "Chỉ số đánh giá → ML.EVALUATE."),
    # --- Snowpark (2)
    Q("TH", "Snowpark (C6)", "Cơ chế <b>push-down</b> của Snowpark nghĩa là:",
      ["Code DataFrame Python được dịch thành SQL, chạy trong kho", "Dữ liệu được đẩy từ kho xuống máy cá nhân để chạy Python", "Python chạy trong sandbox cô lập với hạ tầng ngoài", "Mô hình được đóng gói thành UDF để gọi bằng SELECT"],
      ["Ngược lại: Zero Data Movement, dữ liệu không rời kho.", "Đó là Sandboxing.", "Đó là triển khai mô hình bằng UDF."],
      "Ví dụ chuỗi filter → group_by → agg trong Python được Snowpark dịch thành SELECT … WHERE … GROUP BY và chạy trong Snowflake.",
      "Lẫn push-down với sandbox.", "Push-down = Python → SQL chạy trong kho."),
    Q("TH", "Snowpark (C6)", "<b>Sandboxing</b> trong Secure Runtime Environments của kho dữ liệu dùng để:",
      ["Chạy code Python/R trong không gian cô lập, chặn truy cập trái phép", "Dịch code Python thành câu SQL tối ưu để chạy song song ngay trong kho", "Gọi sẵn hàng nghìn thư viện Anaconda mà không cần cài", "Tạo bản sao dữ liệu tách biệt để thử nghiệm mô hình"],
      ["Đó là push-down.", "Đó là tích hợp Anaconda.", "Đó là zero-copy cloning (Chương 1)."],
      "Secure Runtime gồm: tích hợp Anaconda, Sandboxing, Python Worksheets.",
      "Lẫn sandbox (bảo mật) với push-down (hiệu năng).", "Sandbox = cô lập để an toàn."),
    # --- Feature Store (2)
    Q("NB", "Feature Store (C6)", "Ba lợi ích của <b>Feature Store</b> theo slide là:",
      ["Discovery, Consistency, Lineage", "Scalability, Governance, Simplicity", "Accuracy, Completeness, Timeliness", "Monitor, Detect, Alert"],
      ["Đó là ba lợi ích của In-Database ML.", "Đó là các chiều chất lượng dữ liệu (Chương 4).", "Đó là các bước auditing tự động (Chương 7)."],
      "Discovery: tìm và tái sử dụng đặc trưng có sẵn. Consistency: cùng cách tính lúc huấn luyện và lúc dự báo. Lineage: truy được đặc trưng tính từ bảng nguồn nào.",
      "Lẫn bộ ba của Feature Store và In-DB ML.", "Feature Store: Discovery · Consistency · Lineage."),
    Q("VD", "Feature Store (C6)", "Phòng tín dụng tính DTI theo thu nhập <b>trước thuế</b>, phòng thẻ tính theo thu nhập <b>sau thuế</b>; hai mô hình dùng hai định nghĩa mà không ai biết. Giải pháp và lợi ích tương ứng:",
      ["Feature Store dùng chung định nghĩa – Consistency", "Model Registry – quản lý trạng thái mô hình", "AutoML – tự dò siêu tham số cho mô hình", "Snowpark push-down – dịch code Python sang SQL chạy trong kho"],
      ["Registry quản lý trạng thái mô hình, không thống nhất công thức đặc trưng.", "AutoML không giải quyết lệch định nghĩa đặc trưng.", "Push-down là cơ chế thực thi, không chuẩn hoá định nghĩa."],
      "Feature Store là kho tập trung quản lý, lưu và phân phối đặc trưng đã tính sẵn cho nhiều mô hình dùng lại, tránh tính trùng, tính lệch.",
      "Chọn công cụ MLOps khác vì nghe gần.", "Lệch định nghĩa đặc trưng → Feature Store (Consistency)."),
    # --- MLOps (3)
    Q("VD", "Model drift (C6)", "Mô hình được huấn luyện khi phần lớn khách có thu nhập 10–30 triệu; một năm sau phần lớn khách mới có thu nhập 30–60 triệu. Hiện tượng này là:",
      ["Data drift", "Concept drift", "Data leakage", "Overfitting"],
      ["Concept drift là quan hệ đầu vào → nhãn thay đổi.", "Leakage là dữ liệu huấn luyện chứa thông tin tương lai.", "Overfitting là học thuộc nhiễu của dữ liệu huấn luyện."],
      "Data drift: phân phối dữ liệu đầu vào thay đổi so với lúc huấn luyện. Giải pháp: giám sát tự động, kích hoạt huấn luyện lại khi độ chính xác tụt.",
      "Lẫn data drift với concept drift.", "Đầu vào đổi phân phối → data drift."),
    Q("VD", "Model drift (C6)", "Sau khi lãi suất tăng mạnh, khách có <b>cùng mức DTI như trước</b> nhưng tỷ lệ vỡ nợ cao hơn hẳn. Hiện tượng và hành động phù hợp:",
      ["Concept drift; giám sát và kích hoạt huấn luyện lại mô hình", "Data drift; chỉ cần chuẩn hoá lại dữ liệu đầu vào theo phân phối mới", "Data leakage; xoá cột DTI khỏi mô hình", "Overfitting; cắt tỉa cây quyết định"],
      ["Phân phối DTI không đổi; quan hệ DTI → vỡ nợ mới đổi.", "Không có thông tin tương lai lọt vào huấn luyện.", "Mô hình không học thuộc nhiễu; thế giới đã đổi."],
      "Concept drift: quan hệ giữa đầu vào và nhãn thay đổi, mô hình cũ không còn đúng → autoretraining khi độ chính xác dưới ngưỡng.",
      "Chọn data drift vì “dữ liệu thay đổi”.", "Quan hệ đầu vào → nhãn đổi → concept drift."),
    Q("TH", "MLOps (C6)", "Phân biệt <b>Model Registry</b> và <b>Model Versioning</b>:",
      ["Registry: trạng thái mô hình; Versioning: gắn mô hình với phiên bản dữ liệu và code", "Registry: gắn mô hình với commit code; Versioning: quản lý trạng thái phê duyệt", "Registry: lưu đặc trưng dùng chung; Versioning: lưu kết quả dự báo", "Hai khái niệm giống nhau, chỉ khác tên gọi của công cụ"],
      ["Đảo ngược hai khái niệm.", "Lưu đặc trưng dùng chung là Feature Store.", "Hai khái niệm có vai trò khác nhau."],
      "Registry: danh mục mô hình với trạng thái đang phát triển, đã phê duyệt, ngừng dùng. Versioning: credit_model v3 = snapshot dữ liệu 01/10 + commit a1b2c3, dựng lại được để điều tra.",
      "Đảo vai trò hai thành phần.", "Registry = trạng thái · Versioning = dữ liệu + code."),
    # --- UDF, AutoML (2)
    Q("TH", "UDF (C6)", "Đóng gói mô hình thành <b>UDF</b> trong kho mang lại điều gì?",
      ["Dự báo bằng SELECT trên từng dòng, dữ liệu không rời kho", "Huấn luyện lại mô hình tự động mỗi khi phát hiện drift", "Tự dò bộ siêu tham số tốt nhất cho mô hình", "Lưu đặc trưng dùng chung cho nhiều mô hình khác nhau"],
      ["Đó là autoretraining trong MLOps.", "Đó là AutoML.", "Đó là Feature Store."],
      "Ví dụ SELECT customer_id, predict_default(dti, utilization) FROM customers – scoring on-the-fly, tiếp nối nguyên lý In-Database ML.",
      "Lẫn UDF với các thành phần MLOps khác.", "UDF = mô hình thành hàm SQL."),
    Q("TH", "AutoML (C6)", "Đâu là một <b>siêu tham số</b> (hyperparameter) mà AutoML có thể tự dò?",
      ["Độ sâu tối đa của cây quyết định", "Trọng số mà mô hình học được sau huấn luyện", "Nhãn của dữ liệu huấn luyện", "Giá trị dự báo của mô hình cho khách mới"],
      ["Trọng số là tham số mô hình tự học ra.", "Nhãn là dữ liệu, không phải tham số.", "Dự báo là đầu ra."],
      "Siêu tham số đặt trước khi huấn luyện, mô hình không tự học ra: độ sâu cây, số cụm k, Eps và MinPts. AutoML tự động hoá feature engineering, thử nhiều thuật toán, hyperparameter tuning.",
      "Lẫn tham số học được với siêu tham số.", "Siêu tham số = đặt trước khi huấn luyện."),
]
