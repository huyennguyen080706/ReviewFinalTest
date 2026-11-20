"""Ngân hàng câu hỏi Chương 7–9, bám các hộp "Hay ra thi" trong GiangGiai_Chuong7-9.pdf."""
import math
from collections import deque
from fractions import Fraction as Fr
from de_common import Q, num, table

# ---------------------------------------------------------------- kiểm tra số liệu
_KA = table(["Nhóm tuổi", "Mã vùng", "Số dòng"], [["20–29", "700**", "3"], ["30–39", "701**", "2"], ["40–49", "702**", "4"]])
assert min(3, 2, 4) == 2


def cos(a, b):
    return sum(x * y for x, y in zip(a, b)) / math.sqrt(sum(x * x for x in a) * sum(y * y for y in b))


_q = (1, 0, 1)
_docs = {"d1": (1, 1, 0), "d2": (0, 1, 1), "d3": (2, 0, 1), "d4": (0, 2, 0)}
_cs = {k: cos(_q, v) for k, v in _docs.items()}
assert max(_cs, key=_cs.get) == "d3" and abs(_cs["d3"] - 0.9487) < 1e-4 and abs(_cs["d1"] - 0.5) < 1e-12
assert abs(cos((1, 2, 2), (2, 1, 2)) - 8 / 9) < 1e-12

# Đồ thị cho BFS/DFS, duyệt đỉnh kề theo bảng chữ cái
_G = {"A": "BC", "B": "ADE", "C": "AF", "D": "BG", "E": "BG", "F": "C", "G": "DE"}


def bfs(s):
    seen, out, qu = {s}, [], deque([s])
    while qu:
        u = qu.popleft(); out.append(u)
        for v in _G[u]:
            if v not in seen:
                seen.add(v); qu.append(v)
    return out


def dfs(s, seen=None):
    seen = seen if seen is not None else []
    seen.append(s)
    for v in _G[s]:
        if v not in seen:
            dfs(v, seen)
    return seen


_BFS, _DFS = ",".join(bfs("A")), ",".join(dfs("A"))
assert _BFS == "A,B,C,D,E,F,G" and _DFS == "A,B,D,G,E,C,F", (_BFS, _DFS)
_GTXT = "Đồ thị vô hướng có các cạnh A–B, A–C, B–D, B–E, C–F, D–G, E–G. Xuất phát từ A, khi có nhiều đỉnh kề thì chọn theo thứ tự bảng chữ cái."
_fmt = lambda s: " → ".join(s.split(","))

assert 2000 // 20 == 100 and 4096 // 128 == 32
assert Fr(32, 10) * 10 ** 18 == 3_200_000_000_000_000_000 and Fr(2_750_000, 10 ** 6) == Fr(11, 4)
assert 8 * 100 == 800

# ======================================================================= CHƯƠNG 7 (24 câu)
CH7 = [
    # --- EU AI Act (4)
    Q("NB", "EU AI Act (C7)", "Theo EU AI Act, hệ thống <b>chấm điểm tín dụng</b> của ngân hàng thuộc mức rủi ro nào?",
      ["High risk", "Limited risk", "Minimal risk", "Unacceptable risk"],
      ["Limited là chatbot, deepfake – chỉ cần minh bạch, dán nhãn.", "Minimal là bộ lọc spam, game AI.", "Unacceptable là bị cấm hẳn, ví dụ social scoring."],
      "Bốn mức: Unacceptable (cấm), High (tín dụng, tuyển dụng, y tế – yêu cầu nghiêm ngặt), Limited (chatbot – minh bạch), Minimal (spam filter – gần như không ràng buộc).",
      "Nhầm chấm điểm tín dụng với social scoring.", "Tín dụng → High · Chatbot → Limited · Social scoring → Unacceptable."),
    Q("TH", "EU AI Act (C7)", "Một ngân hàng triển khai <b>chatbot</b> tư vấn sản phẩm. Theo AI Act, nghĩa vụ chính là:",
      ["Minh bạch: cho khách biết họ đang nói chuyện với AI", "Bị cấm triển khai trong lãnh thổ EU", "Không có nghĩa vụ nào", "Đánh giá sự phù hợp nghiêm ngặt như hệ thống tín dụng"],
      ["Cấm hẳn chỉ áp dụng cho mức Unacceptable.", "Minimal mới gần như không ràng buộc.", "Đó là yêu cầu của mức High."],
      "Chatbot thuộc Limited risk: nghĩa vụ minh bạch, dán nhãn nội dung do AI tạo.",
      "Đẩy chatbot lên High vì dùng trong ngân hàng.", "Limited = phải dán nhãn AI."),
    Q("NB", "EU AI Act (C7)", "Ba trụ cột yêu cầu của AI Act được slide nêu là:",
      ["Transparency, Human Oversight, Data Quality", "Scalability, Governance (RBAC), Simplicity", "Discovery, Consistency, Lineage", "Freshness, Volume, Distribution, Schema"],
      ["Đó là lợi ích của In-Database ML.", "Đó là lợi ích của Feature Store.", "Đó là các trụ cột data observability."],
      "Transparency: giải thích được; Human Oversight: con người giám sát, can thiệp được; Data Quality: dữ liệu huấn luyện đủ chất lượng, không thiên lệch. Lineage đáp ứng yêu cầu truy vết (traceability).",
      "Lẫn các bộ ba giữa các chương.", "AI Act: Transparency · Human Oversight · Data Quality."),
    Q("TH", "EU AI Act (C7)", "Hệ thống <b>chấm điểm công dân</b> dựa trên hành vi xã hội để quyết định quyền lợi (social scoring) thuộc mức nào?",
      ["Unacceptable risk – bị cấm", "High risk – được phép nếu kiểm định", "Limited risk – chỉ cần dán nhãn", "Minimal risk – không ràng buộc"],
      ["Social scoring không được phép dù có kiểm định.", "Dán nhãn chỉ áp dụng cho chatbot, deepfake.", "Đây là mức rủi ro cao nhất."],
      "Unacceptable gồm social scoring, thao túng hành vi… bị cấm hoàn toàn trong EU.",
      "Lẫn social scoring với credit scoring.", "Social scoring → cấm."),
    # --- Lineage (3)
    Q("VD", "Data lineage (C7)", "Đội dữ liệu sắp đổi kiểu một cột trong bảng nguồn và muốn biết <b>dashboard, mô hình nào sẽ bị ảnh hưởng</b>. Đây là:",
      ["Impact analysis – đi xuôi theo lineage", "Root-cause analysis – đi ngược theo lineage", "Data masking", "Row-level security"],
      ["Root-cause đi ngược từ kết quả sai về nguồn lỗi.", "Masking che dữ liệu nhạy cảm.", "RLS lọc dòng theo người truy vấn."],
      "Impact analysis: nguồn thay đổi → cái gì phía sau bị ảnh hưởng (xuôi). Root-cause: báo cáo sai → lỗi nằm ở đâu phía trước (ngược).",
      "Đảo chiều hai loại phân tích.", "Impact xuôi · Root-cause ngược."),
    Q("TH", "Data lineage (C7)", "Dashboard doanh thu sáng nay hiển thị số sai. Đội dữ liệu lần theo lineage <b>ngược lên</b> các bảng trung gian để tìm bước gây lỗi. Đây là:",
      ["Root-cause analysis", "Impact analysis", "Audit trail", "Semantic search"],
      ["Impact analysis đi xuôi từ thay đổi ở nguồn.", "Audit trail là nhật ký truy cập bất biến.", "Semantic search tìm dữ liệu theo nghĩa."],
      "Root-cause analysis đi ngược từ kết quả sai về nguồn, giảm MTTR.",
      "Đảo xuôi/ngược.", "Kết quả sai → đi ngược → root-cause."),
    Q("NB", "Data lineage (C7)", "Theo slide, data lineage đáp ứng yêu cầu nào của EU AI Act?",
      ["Traceability – truy vết được dữ liệu và mô hình", "Cấm hẳn hệ thống social scoring", "Dán nhãn mọi nội dung do AI tạo ra cho người dùng cuối", "Mã hoá dữ liệu khi lưu trữ"],
      ["Đó là quy định cho mức Unacceptable.", "Đó là nghĩa vụ mức Limited.", "Mã hoá là kiểm soát bảo mật, không phải lineage."],
      "Lineage ghi lại dữ liệu đi từ nguồn nào, qua biến đổi nào, tới bảng/mô hình nào – nền tảng cho truy vết và giải trình.",
      "Nghĩ lineage chỉ là công cụ kỹ thuật, không liên quan pháp lý.", "Lineage ↔ Traceability."),
    # --- RLS & masking (3)
    Q("VD", "RLS và masking (C7)", "Nhân viên chi nhánh Hà Nội chỉ được thấy khách hàng của Hà Nội; tổng đài viên thấy đủ khách nhưng số điện thoại bị che. Hai kỹ thuật lần lượt là:",
      ["Row-level security; Dynamic data masking", "Dynamic data masking; Row-level security", "k-anonymity; Differential privacy", "Zero-copy sharing; Object Lock"],
      ["Đảo ngược: RLS lọc dòng, masking che cột.", "Đó là kỹ thuật ẩn danh khi công bố dữ liệu.", "Không liên quan phân quyền theo người xem."],
      "RLS lọc dòng; masking che giá trị cột. Cả hai dựa vào danh tính/vai trò người truy vấn, không đổi dữ liệu gốc, không đổi cấu trúc bảng.",
      "Đảo vai trò RLS và masking.", "RLS = lọc dòng · Masking = che cột."),
    Q("VD", "Dynamic masking (C7)", "Chính sách masking giữ <b>3 chữ số đầu và 3 chữ số cuối</b>, thay phần giữa bằng x. Số 0987654321 hiển thị cho tổng đài viên là:",
      ["098xxxx321", "098xxx4321", "xxxxxxx321", "0987xxx321"],
      ["Giữ 4 chữ số cuối thay vì 3.", "Che cả 3 chữ số đầu.", "Giữ 4 chữ số đầu thay vì 3."],
      "10 chữ số: giữ 098 và 321, che 4 chữ số giữa → 098xxxx321. Dữ liệu gốc trong bảng không đổi; người có quyền vẫn thấy số đầy đủ.",
      "Đếm sai số ký tự bị che.", "Masking che lúc truy vấn, không sửa dữ liệu gốc."),
    Q("TH", "RLS và masking (C7)", "Phát biểu nào <b>đúng</b> về RLS và dynamic masking?",
      ["Không đổi dữ liệu gốc hay cấu trúc bảng; kết quả tuỳ người xem", "Ghi đè dữ liệu gốc trong bảng bằng giá trị đã che, theo từng vai trò", "Tạo một bảng sao riêng cho từng phòng ban", "Chỉ áp dụng được khi xuất dữ liệu ra file CSV"],
      ["Masking động áp dụng lúc đọc, không ghi đè.", "Không cần sao chép bảng.", "Áp dụng ngay trên truy vấn trong kho."],
      "Chính sách gắn vào bảng/cột, kho tự áp theo vai trò khi truy vấn; cùng một câu SELECT, người khác nhau thấy kết quả khác nhau.",
      "Nghĩ masking sửa dữ liệu lưu trữ.", "Cùng bảng – khác người xem – khác kết quả."),
    # --- Data sharing (3)
    Q("NB", "Secure data sharing (C7)", "Đặc điểm của <b>zero-copy data sharing</b> (ví dụ Snowflake Secure Data Sharing):",
      ["Không sao chép, dữ liệu luôn mới, thu hồi quyền có hiệu lực ngay", "Xuất file CSV và gửi cho bên nhận qua FTP hằng đêm", "Bên nhận giữ một bản sao độc lập, cập nhật theo lịch", "Thu hồi quyền chỉ có hiệu lực khi bên nhận tự xoá bản sao của họ"],
      ["Đó là cách chia sẻ truyền thống, dữ liệu cũ và khó thu hồi.", "Zero-copy không tạo bản sao.", "Không có bản sao nên thu hồi là có hiệu lực ngay."],
      "Bên nhận đọc trực tiếp dữ liệu của bên chia sẻ qua metadata, dùng compute của mình. Nền tảng kỹ thuật là tách rời compute và storage.",
      "Nghĩ chia sẻ là gửi bản sao.", "Zero-copy: không chép · live · thu hồi ngay."),
    Q("TH", "Secure data sharing (C7)", "Nền tảng kỹ thuật cho phép chia sẻ dữ liệu zero-copy là gì?",
      ["Tách rời compute và storage", "Lưu dữ liệu theo hàng trong RDBMS", "Chạy ETL hằng đêm sang tài khoản đối tác", "Mã hoá dữ liệu bằng blockchain"],
      ["Lưu theo hàng không liên quan chia sẻ.", "ETL sang đối tác chính là sao chép.", "Blockchain không phải cơ chế chia sẻ của kho."],
      "Vì dữ liệu nằm ở tầng storage độc lập, bên nhận có thể dùng compute riêng để đọc cùng bản dữ liệu mà không cần chép.",
      "Không nối kiến thức Chương 1 với Chương 7.", "Zero-copy sharing ← decoupling compute/storage."),
    Q("VD", "Secure data sharing (C7)", "Ngân hàng chia sẻ bảng tỷ giá cho đối tác qua Secure Data Sharing, sau đó chấm dứt hợp đồng và thu hồi quyền. Điều gì xảy ra?",
      ["Đối tác mất quyền truy cập ngay, vì họ chưa từng có bản sao", "Đối tác vẫn giữ bản sao đầy đủ đến hết tháng", "Đối tác vẫn giữ dữ liệu cũ nhưng không nhận thêm cập nhật mới nào", "Ngân hàng phải gửi yêu cầu đối tác tự xoá file"],
      ["Zero-copy không tạo bản sao.", "Không có dữ liệu cũ nào nằm phía đối tác.", "Không cần, vì không có file nào được gửi đi."],
      "Thu hồi share là bên nhận không còn đọc được nữa – lợi thế lớn so với gửi file.",
      "Suy diễn theo kiểu chia sẻ bằng file.", "Thu hồi share = mất quyền ngay."),
    # --- Differential privacy & k-anonymity (4)
    Q("TH", "Differential privacy (C7)", "Trong differential privacy, giảm tham số <b>ε</b> thì:",
      ["Riêng tư cao hơn nhưng kết quả kém chính xác hơn", "Riêng tư thấp hơn và kết quả chính xác hơn", "Riêng tư cao hơn và kết quả chính xác hơn", "Không ảnh hưởng gì vì ε chỉ là tên phiên bản"],
      ["Đảo ngược.", "Có đánh đổi: thêm nhiễu nhiều thì kém chính xác.", "ε là ngân sách riêng tư, quyết định lượng nhiễu."],
      "ε nhỏ → thêm nhiều nhiễu → khó suy ra cá nhân → riêng tư cao, độ chính xác thấp.",
      "Đảo chiều ε.", "ε nhỏ = riêng tư cao = kém chính xác."),
    Q("VD", "k-anonymity (C7)", "Sau khi tổng quát hoá quasi-identifier, dữ liệu có các nhóm như bảng. Bộ dữ liệu đạt <b>k-anonymity</b> với k bằng bao nhiêu?" + _KA,
      ["2", "3", "4", "9"],
      ["Lấy nhóm đầu tiên thay vì nhóm nhỏ nhất.", "Lấy nhóm lớn nhất.", "Lấy tổng số dòng."],
      "k-anonymity: mọi nhóm QI có ít nhất k dòng → k = kích thước nhóm nhỏ nhất = 2.",
      "Lấy nhóm lớn nhất hoặc tổng.", "k = nhóm QI nhỏ nhất."),
    Q("TH", "k-anonymity (C7)", "Hai kỹ thuật dùng để đạt k-anonymity là:",
      ["Generalization và suppression", "Thêm nhiễu vào kết quả truy vấn và giới hạn ε", "Row-level security và masking", "Hashing và Merkle tree"],
      ["Đó là differential privacy.", "Đó là kiểm soát truy cập theo người xem.", "Đó là kỹ thuật toàn vẹn dữ liệu (Chương 9)."],
      "Generalization: thay giá trị cụ thể bằng khoảng (tuổi 27 → 20–29, mã vùng 70012 → 700**). Suppression: xoá hoặc che các dòng/giá trị quá hiếm.",
      "Lẫn k-anonymity với differential privacy.", "k-anonymity sửa dữ liệu: generalize + suppress."),
    Q("VD", "k-anonymity (C7)", "Một bộ dữ liệu cần đạt k = 3 nhưng có một nhóm QI chỉ gồm 1 khách hàng có hồ sơ rất hiếm, tổng quát hoá thêm thì mất hết ý nghĩa. Cách xử lý phù hợp:",
      ["Suppression: loại hoặc che dòng hiếm đó", "Thêm nhiễu Laplace vào kết quả truy vấn", "Áp dụng row-level security cho dòng đó", "Tăng ε lên để nới lỏng ràng buộc"],
      ["Đó là differential privacy, sửa kết quả chứ không sửa dữ liệu công bố.", "RLS không làm dữ liệu công bố đạt k-anonymity.", "ε là tham số của differential privacy."],
      "Khi tổng quát hoá không đủ, suppression bỏ các dòng ngoại lệ để mọi nhóm còn lại đạt ≥ k.",
      "Trộn công cụ của DP vào k-anonymity.", "Nhóm quá hiếm → suppression."),
    # --- Data catalog (3)
    Q("TH", "Data catalog (C7)", "Định nghĩa “<b>khách hàng hoạt động</b> = có giao dịch trong 90 ngày” nên nằm ở đâu trong data catalog?",
      ["Business Glossary", "Technical Metadata", "Audit trail", "Merkle root"],
      ["Technical Metadata chứa kiểu dữ liệu, schema, freshness.", "Audit trail ghi ai truy cập gì.", "Merkle root dùng xác minh toàn vẹn log."],
      "Business Glossary định nghĩa thuật ngữ nghiệp vụ (churn, khách hoạt động); Technical Metadata mô tả cấu trúc kỹ thuật.",
      "Lẫn định nghĩa nghiệp vụ với metadata kỹ thuật.", "Thuật ngữ nghiệp vụ → Glossary · kiểu/schema/freshness → Technical."),
    Q("NB", "AI-powered catalog (C7)", "Ba thành phần của <b>AI-powered data catalog</b> theo slide:",
      ["Semantic Search, Lineage Integration, Trust Score", "Producer, Broker, Consumer", "Connector, Global catalog, Predicate pushdown", "Monitor, Detect, Alert"],
      ["Đó là thành phần Kafka (Chương 8).", "Đó là thành phần federated query (Chương 9).", "Đó là các bước auditing tự động."],
      "Semantic Search: tìm theo nghĩa; Lineage Integration: thấy nguồn gốc ngay trong catalog; Trust Score: điểm tin cậy dựa trên chất lượng, mức sử dụng.",
      "Lẫn bộ thành phần giữa các công nghệ.", "AI catalog: Search · Lineage · Trust Score."),
    Q("TH", "Data catalog (C7)", "Thông tin “cột <code>txn_date</code> có kiểu DATE, bảng cập nhật lúc 6 giờ mỗi sáng” thuộc loại metadata nào?",
      ["Technical Metadata", "Business Glossary", "Trust Score", "Audit trail"],
      ["Glossary định nghĩa thuật ngữ nghiệp vụ.", "Trust Score là điểm tin cậy tổng hợp.", "Audit trail ghi lịch sử truy cập."],
      "Kiểu dữ liệu, schema, độ mới (freshness) là technical metadata.",
      "Lẫn hai loại metadata.", "Kiểu, schema, freshness → Technical."),
    # --- Bias (2)
    Q("TH", "AI bias (C7)", "Ghép đúng kỹ thuật giảm thiên lệch với giai đoạn: (1) resampling/reweighting, (2) thêm ràng buộc công bằng vào hàm loss, (3) điều chỉnh ngưỡng quyết định theo nhóm.",
      ["(1) pre-processing, (2) in-processing, (3) post-processing", "(1) in-processing, (2) pre-processing, (3) post-processing", "(1) post-processing, (2) in-processing, (3) pre-processing", "(1) pre-processing, (2) post-processing, (3) in-processing"],
      ["Resampling sửa dữ liệu trước khi huấn luyện.", "Chỉnh ngưỡng là sau khi có mô hình.", "Ràng buộc trong loss là trong lúc huấn luyện."],
      "Pre: sửa dữ liệu. In: sửa quá trình học. Post: sửa đầu ra/ngưỡng.",
      "Nhầm giai đoạn của resampling.", "Dữ liệu → pre · loss → in · ngưỡng → post."),
    Q("NB", "AI bias (C7)", "Theo slide, nguồn gốc chủ yếu của thiên lệch (bias) trong mô hình AI là:",
      ["Dữ liệu lịch sử phản ánh định kiến trong quá khứ", "Bản thân thuật toán học máy được thiết kế có định kiến", "Phần cứng GPU tính sai", "Người dùng nhập câu hỏi sai"],
      ["Thuật toán chỉ học lại những gì có trong dữ liệu.", "Không phải nguồn gốc bias.", "Không phải nguồn gốc bias."],
      "Mô hình học từ dữ liệu quá khứ nên tái tạo định kiến có trong đó (ví dụ từ chối cho vay nhiều hơn ở một nhóm).",
      "Đổ lỗi cho thuật toán.", "Bias đến từ dữ liệu lịch sử."),
    # --- Auditing (2)
    Q("NB", "Auditing tự động (C7)", "Thứ tự bốn bước của auditing tự động theo slide:",
      ["Monitor → Detect → Alert → Report", "Detect → Monitor → Report → Alert", "Alert → Detect → Monitor → Report", "Monitor → Alert → Detect → Report"],
      ["Phải giám sát trước mới phát hiện được.", "Cảnh báo chỉ sau khi đã phát hiện.", "Phát hiện phải trước cảnh báo."],
      "Giám sát liên tục → phát hiện bất thường → cảnh báo người phụ trách → báo cáo cho kiểm toán/cơ quan quản lý.",
      "Đảo Detect và Alert.", "Monitor → Detect → Alert → Report."),
    Q("TH", "Audit trail (C7)", "Yêu cầu quan trọng nhất với <b>audit trail</b> là gì?",
      ["Bất biến: không ai, kể cả quản trị viên, sửa hay xoá được", "Chỉ lưu trong 24 giờ để tiết kiệm", "Cho phép quản trị viên chỉnh sửa khi cần, miễn là có ghi chú lý do", "Lưu ở tầng Gold cùng KPI"],
      ["Nhật ký kiểm toán phải lưu đủ lâu theo quy định.", "Cho phép sửa thì mất giá trị chứng cứ.", "Tầng lưu trữ không phải yêu cầu cốt lõi."],
      "Audit trail ghi ai truy cập dữ liệu gì, khi nào; phải immutable (ví dụ Object Lock hoặc neo Merkle root lên blockchain) mới có giá trị pháp lý.",
      "Nghĩ admin được phép sửa log.", "Audit trail = immutable."),
]

# ======================================================================= CHƯƠNG 8 (18 câu)
_COS = table(["Tài liệu", "Vector"], [[k, "(" + ", ".join(map(str, v)) + ")"] for k, v in _docs.items()])
CH8 = [
    # --- Descriptive vs actionable, Object Tables (3)
    Q("NB", "Descriptive và actionable (C8)", "Câu hỏi nào thuộc phân tích <b>descriptive</b>?",
      ["Doanh thu quý trước của từng chi nhánh là bao nhiêu?", "Khách hàng nào có khả năng rời bỏ tháng tới?", "Nên gửi ưu đãi nào cho từng khách để giữ chân?", "Nếu tăng lãi suất 1% thì dư nợ thay đổi ra sao?"],
      ["Đó là predict (dự đoán) – thuộc actionable.", "Đó là prescribe (đề xuất hành động).", "Đó là phân tích dự báo theo kịch bản, thuộc actionable."],
      "Descriptive trả lời “điều gì đã xảy ra”; actionable gồm predict (sẽ xảy ra gì) và prescribe (nên làm gì).",
      "Nghĩ mọi câu có số liệu là descriptive.", "Đã xảy ra → descriptive · Sẽ/nên → actionable."),
    Q("TH", "Object Tables (C8)", "<b>Object Tables</b> (BigQuery) cho phép điều gì?",
      ["Dùng SQL truy vấn file phi cấu trúc tại chỗ, không di chuyển dữ liệu", "Chuyển file ảnh, PDF thành bảng quan hệ bằng một job ETL", "Lưu các object ít dùng xuống archive tier cho rẻ", "Khoá object để không ai xoá hay sửa được trong thời hạn lưu trữ quy định"],
      ["Không cần ETL, file vẫn nằm tại chỗ.", "Đó là phân tầng lưu trữ.", "Đó là Object Lock."],
      "Object Table là bảng metadata trỏ tới file trên Cloud Storage; kết hợp mô hình AI để phân tích nội dung ảnh, văn bản bằng SQL.",
      "Lẫn Object Tables với Object Lock.", "Object Tables = SQL trên file phi cấu trúc."),
    Q("TH", "Semantic search (C8)", "Câu hỏi “thẻ hết tiền” tìm được tài liệu “card has no balance” dù không chung từ nào. Cơ chế cho phép điều này:",
      ["Semantic search: embeddings của hai câu gần nhau", "Keyword search khớp chính xác từng từ khoá", "Full-text index so khớp theo chuỗi ký tự", "Row-level security lọc các dòng theo người đặt câu hỏi"],
      ["Keyword search khớp chữ nên không tìm được.", "Index ký tự vẫn khớp chữ.", "RLS không liên quan tìm kiếm."],
      "Embedding biểu diễn nghĩa thành vector; câu cùng nghĩa (kể cả khác ngôn ngữ) có vector gần nhau, đo bằng cosine similarity.",
      "Nghĩ tìm kiếm luôn cần trùng từ.", "Khớp nghĩa → embeddings · Khớp chữ → keyword."),
    # --- Cosine (3)
    Q("VDC", "Cosine similarity (C8)", "Vector truy vấn q = (1, 0, 1). Tài liệu nào <b>gần q nhất</b> theo cosine similarity?" + _COS,
      ["d3, cosine ≈ 0,949", "d1, cosine = 0,5", "d4, cosine = 0", "d2, cosine = 1"],
      ["d1 = (1,1,0): 1/(√2·√2) = 0,5, kém d3.", "d4 vuông góc với q nên cosine = 0, xa nhất.", "d2: 1/(√2·√2) = 0,5, không phải 1."],
      f"cos(q, d3) = (2 + 0 + 1)/(√2·√5) = 3/√10 ≈ {num(_cs['d3'], 3)}; d1 và d2 đều 0,5; d4 = 0 → d3 gần nhất.",
      "Chọn theo tích vô hướng hoặc độ dài vector.", "cos = A·B / (‖A‖·‖B‖)."),
    Q("VD", "Cosine similarity (C8)", "Cho q = (1, 2, 2) và d = (2, 1, 2). Cosine similarity của q và d là:",
      ["≈ 0,889", "8", "≈ 0,667", "1"],
      ["8 là tích vô hướng, chưa chia cho tích độ dài.", "Chia 8 cho 12 (tổng các thành phần) thay vì tích độ dài 9.", "Chỉ bằng 1 khi hai vector cùng hướng."],
      "q·d = 2 + 2 + 4 = 8; ‖q‖ = ‖d‖ = 3 → cos = 8/9 ≈ 0,889.",
      "Quên chuẩn hoá theo độ dài.", "cos = tích vô hướng / tích độ dài."),
    Q("TH", "Cosine similarity (C8)", "Cosine similarity của hai embedding bằng <b>0</b> nghĩa là:",
      ["Hai vector vuông góc – không liên quan về nghĩa", "Hai câu giống hệt nhau", "Hai câu trái nghĩa hoàn toàn", "Một trong hai vector có độ dài (chuẩn) bằng 0 nên không xác định"],
      ["Giống hệt (cùng hướng) cho cosine = 1.", "Ngược hướng cho cosine = −1.", "Vector độ dài 0 làm cosine không xác định."],
      "Cosine đo góc giữa hai vector, không phụ thuộc độ dài: 1 cùng hướng, 0 vuông góc, −1 ngược hướng.",
      "Nghĩ 0 là trái nghĩa.", "1 giống · 0 không liên quan · −1 ngược."),
    # --- RAG (3)
    Q("NB", "RAG (C8)", "Thứ tự bốn bước của RAG theo slide:",
      ["Ingestion → Embedding → Retrieval → Generation", "Embedding → Ingestion → Generation → Retrieval", "Retrieval → Embedding → Ingestion → Generation", "Ingestion → Retrieval → Embedding → Generation"],
      ["Phải nạp tài liệu trước khi nhúng; sinh câu trả lời là bước cuối.", "Phải có embedding trước mới truy hồi được.", "Truy hồi cần embedding có sẵn."],
      "Nạp và chia nhỏ tài liệu → nhúng thành vector → truy hồi đoạn liên quan với câu hỏi → LLM sinh câu trả lời dựa trên đoạn đó.",
      "Đảo Retrieval và Embedding.", "Ingest → Embed → Retrieve → Generate."),
    Q("TH", "RAG (C8)", "Mục đích chính của RAG là:",
      ["Giảm hallucination, dùng dữ liệu riêng mà không huấn luyện lại LLM", "Huấn luyện lại LLM từ đầu trên dữ liệu doanh nghiệp", "Nén mô hình LLM để chạy vừa bộ nhớ RAM của máy chủ nội bộ doanh nghiệp", "Thay thế hoàn toàn kho dữ liệu bằng một mô hình LLM"],
      ["RAG không huấn luyện lại mô hình.", "Nén vector là PQ (Chương 9).", "RAG dùng dữ liệu trong kho, không thay kho."],
      "LLM nhận thêm ngữ cảnh truy hồi từ tài liệu nội bộ nên trả lời có căn cứ và cập nhật.",
      "Nghĩ RAG là fine-tuning.", "RAG = truy hồi + sinh, không train lại."),
    Q("VD", "RAG (C8)", "Chatbot nội bộ trả lời sai chính sách phí vì LLM không biết quy định mới ban hành tuần trước. Cách khắc phục ít tốn kém và phù hợp nhất:",
      ["Dùng RAG: nạp quy định mới vào vector store để truy hồi", "Huấn luyện lại LLM từ đầu mỗi tuần một lần", "Tăng nhiệt độ sinh để câu trả lời đa dạng và tự nhiên hơn", "Chuyển chatbot sang tìm kiếm theo từ khoá"],
      ["Rất đắt và chậm so với cập nhật tài liệu.", "Tăng nhiệt độ làm tăng bịa đặt.", "Keyword search không sinh câu trả lời và kém khớp nghĩa."],
      "Chỉ cần thêm tài liệu mới vào bước Ingestion/Embedding; câu trả lời dựa trên đoạn văn được truy hồi.",
      "Chọn train lại vì nghĩ là cách duy nhất cập nhật kiến thức.", "Kiến thức mới → thêm vào RAG."),
    # --- Generative BI (2)
    Q("NB", "Generative BI (C8)", "Ba bước của Generative BI theo slide:",
      ["Natural Query → Auto-SQL → Instant Insight", "Ingestion → Embedding → Retrieval → Generation", "Monitor → Detect → Alert", "Bối cảnh → Vấn đề → Giải pháp → Hành động"],
      ["Đó là các bước RAG.", "Đó là các bước auditing.", "Đó là cấu trúc kể chuyện dữ liệu."],
      "Người dùng hỏi bằng ngôn ngữ tự nhiên → hệ thống sinh SQL → trả kết quả, biểu đồ ngay.",
      "Lẫn các chuỗi bước giữa các chủ đề.", "GenBI: hỏi → SQL → insight."),
    Q("TH", "Generative BI (C8)", "Lợi ích chính của Generative BI với người dùng kinh doanh là:",
      ["Xoá rào cản SQL: hỏi bằng ngôn ngữ tự nhiên vẫn ra số liệu", "Thay thế toàn bộ đội kỹ sư dữ liệu", "Tự chủ động lập kế hoạch phân tích và đề xuất hành động kinh doanh", "Không cần semantic layer hay định nghĩa chỉ số"],
      ["Vẫn cần kỹ sư xây dữ liệu nền.", "Đó là Agentic BI.", "Semantic layer giúp sinh SQL đúng định nghĩa."],
      "Generative BI trả lời khi được hỏi; Agentic BI mới chủ động.",
      "Nhầm Generative với Agentic BI.", "GenBI = hỏi tự nhiên, không cần SQL."),
    # --- Kafka (3)
    Q("NB", "Apache Kafka (C8)", "Trong Kafka, <b>offset</b> là gì?",
      ["Vị trí của một bản ghi trong partition", "Tên của một chủ đề dữ liệu", "Máy chủ lưu trữ dữ liệu", "Ứng dụng ghi dữ liệu vào một topic của Kafka"],
      ["Đó là topic.", "Đó là broker.", "Đó là producer."],
      "Producer ghi, consumer đọc, broker lưu; topic chia thành partition; offset là vị trí trong partition, consumer nhớ offset để đọc tiếp.",
      "Lẫn thuật ngữ Kafka.", "Offset = vị trí trong partition."),
    Q("TH", "Apache Kafka (C8)", "Lợi ích kiến trúc chính của Kafka giữa hệ nguồn và các hệ tiêu thụ:",
      ["Tách rời bên gửi và bên nhận: producer không cần biết consumer là ai", "Bắt buộc producer và consumer chạy cùng tốc độ", "Producer gửi trực tiếp dữ liệu vào từng consumer", "Dữ liệu bị xoá ngay khi một consumer đọc xong để giải phóng dung lượng broker"],
      ["Consumer đọc theo tốc độ riêng nhờ offset.", "Producer chỉ ghi vào topic.", "Kafka giữ bản ghi theo thời gian lưu, nhiều consumer đọc được."],
      "Broker lưu sự kiện bền vững; nhiều consumer độc lập đọc cùng topic; phát lại được từ offset cũ (nền tảng kiến trúc Kappa).",
      "Nghĩ Kafka là hàng đợi đọc xong thì mất.", "Kafka tách producer ↔ consumer."),
    Q("TH", "Apache Kafka (C8)", "Thành phần Kafka nào <b>lưu trữ</b> dữ liệu và phục vụ các yêu cầu đọc/ghi?",
      ["Broker", "Producer", "Consumer", "Offset"],
      ["Producer ghi dữ liệu.", "Consumer đọc dữ liệu.", "Offset chỉ là vị trí."],
      "Một cụm Kafka gồm nhiều broker; mỗi partition được lưu và nhân bản trên các broker.",
      "Lẫn producer với broker.", "Broker = máy chủ lưu."),
    # --- Storytelling, write-back (2)
    Q("NB", "Data storytelling (C8)", "Thứ tự một câu chuyện dữ liệu theo slide:",
      ["Bối cảnh → Vấn đề → Giải pháp → Hành động", "Vấn đề → Bối cảnh → Hành động → Giải pháp", "Giải pháp → Vấn đề → Bối cảnh → Hành động", "Hành động → Giải pháp → Vấn đề → Bối cảnh"],
      ["Phải đặt bối cảnh trước khi nêu vấn đề.", "Bắt đầu bằng giải pháp khiến người nghe không hiểu vì sao.", "Đảo ngược toàn bộ."],
      "Đặt bối cảnh → chỉ ra vấn đề trong dữ liệu → đề xuất giải pháp → kêu gọi hành động cụ thể.",
      "Nêu giải pháp trước vấn đề.", "Bối cảnh → Vấn đề → Giải pháp → Hành động."),
    Q("TH", "Write-back (C8)", "Tính năng <b>write-back</b> của dashboard nghĩa là:",
      ["Ghi ngược dữ liệu, hành động từ dashboard vào hệ thống nghiệp vụ", "Dashboard tự viết lại câu SQL phía sau để truy vấn chạy nhanh hơn", "Ghi lại lịch sử những ai đã xem dashboard", "Sao lưu định kỳ dashboard sang archive tier cho rẻ"],
      ["Đó là tối ưu truy vấn.", "Đó là audit log.", "Không liên quan."],
      "Ví dụ quản lý duyệt hạn mức, gán việc cho nhân viên ngay trên dashboard – đóng vòng từ insight đến hành động.",
      "Hiểu write-back là ghi log.", "Write-back = dashboard → hệ thống nghiệp vụ."),
    # --- Agentic BI (2)
    Q("TH", "Agentic BI (C8)", "Khác biệt cốt lõi giữa Generative BI và Agentic BI:",
      ["Generative trả lời khi được hỏi; Agentic tự chủ động phân tích, đề xuất", "Generative tự chủ động phân tích; Agentic chỉ trả lời khi được hỏi", "Generative cần người dùng viết SQL; Agentic thì không cần", "Hai khái niệm giống nhau, chỉ khác tên gọi thương mại"],
      ["Đảo ngược.", "Generative BI cũng không cần người dùng viết SQL.", "Hai khái niệm khác nhau về mức tự chủ."],
      "Agentic BI có thể tự phát hiện bất thường, tự chạy phân tích nhiều bước và đề xuất hành động mà không cần câu hỏi đầu vào.",
      "Đảo vai trò hai loại BI.", "Generative = bị động · Agentic = chủ động."),
    Q("VD", "Agentic BI (C8)", "Hệ thống tự phát hiện doanh số thẻ tín dụng vùng miền Trung giảm 15%, tự truy nguyên do và gửi đề xuất chiến dịch cho giám đốc vùng mà không ai hỏi. Đây là:",
      ["Agentic BI", "Generative BI", "Descriptive dashboard truyền thống", "Semantic search"],
      ["Generative BI cần người dùng đặt câu hỏi.", "Dashboard truyền thống chỉ hiển thị số liệu.", "Semantic search chỉ tìm tài liệu theo nghĩa."],
      "Chủ động phát hiện → phân tích → đề xuất là dấu hiệu của Agentic BI.",
      "Chọn Generative BI vì có AI.", "Không ai hỏi mà vẫn làm → Agentic."),
]

# ======================================================================= CHƯƠNG 9 (24 câu)
CH9 = [
    # --- Polyglot, CAP (3)
    Q("VD", "Polyglot persistence (C9)", "Hồ sơ sản phẩm có thuộc tính thay đổi liên tục giữa các dòng sản phẩm. Theo polyglot persistence, nên lưu ở:",
      ["Document store (ví dụ MongoDB)", "RDBMS với schema cố định, chuẩn 3NF", "Key-value store", "Graph database"],
      ["Schema cứng khó theo kịp thuộc tính thay đổi.", "Key-value hợp cache/session.", "Graph hợp dữ liệu nhiều quan hệ."],
      "Polyglot: mỗi loại dữ liệu một công nghệ phù hợp. Giao dịch cần ACID → RDBMS; schema thay đổi → document; cache/session → key-value; quan hệ phức tạp → graph.",
      "Dùng một CSDL cho mọi thứ.", "Schema linh hoạt → document."),
    Q("NB", "Polyglot persistence (C9)", "Lưu <b>phiên đăng nhập (session)</b> và cache cần đọc/ghi cực nhanh theo khoá, nên dùng:",
      ["Key-value store (ví dụ Redis)", "Document store (ví dụ MongoDB)", "Data Warehouse", "Graph database"],
      ["Document hợp hồ sơ có cấu trúc linh hoạt.", "Kho dữ liệu dành cho phân tích, không cho session.", "Graph dành cho quan hệ."],
      "Key-value: truy cập theo khoá, độ trễ cực thấp.",
      "Chọn document vì quen.", "Cache/session → key-value."),
    Q("TH", "Tính nhất quán (C9)", "Trong kiến trúc polyglot của slide, các hệ NoSQL vệ tinh và kho trung tâm thường có mô hình nhất quán nào?",
      ["Vệ tinh: eventual consistency; kho trung tâm: strong consistency", "Vệ tinh: strong consistency; kho trung tâm: eventual consistency", "Cả hai đều eventual consistency", "Cả hai đều không cần nhất quán"],
      ["Đảo ngược.", "Kho trung tâm phục vụ báo cáo chuẩn cần nhất quán mạnh.", "Nhất quán là yêu cầu cơ bản."],
      "NoSQL ưu tiên sẵn sàng và mở rộng, chấp nhận dữ liệu đồng bộ dần; kho trung tâm là nguồn sự thật nên cần nhất quán mạnh.",
      "Đảo mô hình nhất quán.", "Vệ tinh eventual · trung tâm strong."),
    # --- BFS/DFS (4)
    Q("VD", "BFS (C9)", _GTXT + " Thứ tự duyệt <b>BFS</b> là:",
      [_fmt(_BFS), _fmt(_DFS), "A → B → D → E → G → C → F", "A → C → B → F → E → D → G"],
      ["Đó là thứ tự DFS (đi sâu rồi quay lui).", "Đi hết nhánh B trước khi thăm C – không theo từng cấp.", "Chọn đỉnh kề ngược thứ tự bảng chữ cái."],
      "BFS dùng hàng đợi: cấp 1 B, C; cấp 2 D, E (từ B), F (từ C); cấp 3 G → " + _fmt(_BFS) + ".",
      "Đi sâu như DFS.", "BFS ↔ queue ↔ theo cấp."),
    Q("VDC", "DFS (C9)", _GTXT + " Thứ tự duyệt <b>DFS</b> (đệ quy) là:",
      [_fmt(_DFS), _fmt(_BFS), "A → B → D → G → C → E → F", "A → B → E → G → D → C → F"],
      ["Đó là thứ tự BFS.", "Sau G phải thăm E (kề G, chưa thăm) trước khi quay về C.", "Từ B phải chọn D trước E theo bảng chữ cái."],
      "A → B → D → G → (G kề E chưa thăm) E → quay lui về A → C → F.",
      "Quên đi tiếp sang đỉnh kề chưa thăm trước khi quay lui.", "DFS ↔ stack/đệ quy ↔ đi sâu rồi quay lui."),
    Q("NB", "BFS và DFS (C9)", "Ghép đúng cấu trúc dữ liệu hỗ trợ:",
      ["BFS – queue; DFS – stack hoặc đệ quy", "BFS – stack; DFS – queue", "BFS và DFS đều dùng queue", "BFS – hàng đợi ưu tiên (heap); DFS – hash table"],
      ["Đảo ngược.", "DFS cần cơ chế quay lui (LIFO).", "Không phải cấu trúc của hai thuật toán."],
      "Queue (FIFO) cho duyệt theo từng cấp; stack (LIFO) cho đi sâu rồi quay lui.",
      "Đảo queue và stack.", "BFS–queue · DFS–stack."),
    Q("TH", "BFS và DFS (C9)", "Trong đồ thị không trọng số (ví dụ mạng quan hệ khách hàng), muốn tìm <b>đường ngắn nhất</b> (ít bước nhất) giữa hai người, dùng:",
      ["BFS", "DFS", "PageRank", "Merkle tree"],
      ["DFS có thể đi đường vòng rất dài trước.", "PageRank đo tầm quan trọng của nút.", "Merkle tree dùng kiểm tra toàn vẹn."],
      "BFS duyệt theo từng cấp nên lần đầu gặp đích chính là qua số cạnh ít nhất.",
      "Chọn DFS vì “đi thẳng tới đích”.", "Đường ngắn nhất (không trọng số) → BFS."),
    # --- ANN (3)
    Q("NB", "ANN (C9)", "Ghép đúng thuật toán ANN với ý tưởng:",
      ["HNSW – đồ thị phân cấp; IVF – phân cụm Voronoi; PQ – nén vector", "HNSW – nén vector; IVF – đồ thị phân cấp; PQ – phân cụm Voronoi", "HNSW – phân cụm Voronoi; IVF – nén vector; PQ – đồ thị phân cấp", "Cả ba đều là tìm kiếm chính xác bằng cách vét cạn"],
      ["Đảo HNSW, IVF, PQ.", "Đảo cả ba.", "ANN là gần đúng, đổi chút độ chính xác lấy tốc độ."],
      "HNSW: đồ thị nhiều tầng, nhảy xa ở tầng trên rồi tinh chỉnh ở tầng dưới. IVF: chỉ tìm trong vài cụm gần. PQ: nén vector để vừa RAM.",
      "Lẫn ba thuật toán.", "HNSW đồ thị · IVF cụm · PQ nén."),
    Q("VD", "IVF (C9)", "Kho có 1 triệu vector được IVF chia thành <b>2.000</b> cụm; mỗi truy vấn chỉ quét <b>20</b> cụm gần nhất (giả sử các cụm đều nhau). Số vector phải so sánh giảm khoảng bao nhiêu lần so với vét cạn?",
      ["100 lần", "20 lần", "2.000 lần", "10 lần"],
      ["Lấy số cụm quét làm tỷ lệ.", "Lấy tổng số cụm làm tỷ lệ.", "Tính nhầm 200/20."],
      "Quét 20/2.000 = 1% số cụm → khoảng 10.000 vector thay vì 1.000.000 → giảm 100 lần.",
      "Lấy nhầm một trong hai con số.", "Tỷ lệ giảm = tổng cụm / số cụm quét."),
    Q("VD", "Product Quantization (C9)", "Một vector 1.024 chiều kiểu float32 chiếm <b>4.096 byte</b>. PQ nén nó thành <b>128 byte</b>. Tỷ lệ nén là:",
      ["32 lần", "8 lần", "128 lần", "4 lần"],
      ["Tính nhầm 1.024/128.", "Lấy số byte sau nén làm tỷ lệ.", "Chỉ tính 4 byte mỗi float."],
      "4.096/128 = 32 lần – giúp hàng trăm triệu vector vừa RAM, đổi lại khoảng cách chỉ gần đúng.",
      "Lấy số chiều thay cho số byte.", "Tỷ lệ nén = kích thước gốc / kích thước nén."),
    # --- Blockchain (3)
    Q("NB", "Blockchain ETL (C9)", "Thứ tự ba bước Blockchain ETL theo slide:",
      ["Node Ingestion → Event Decoding → Data Normalization", "Event Decoding → Node Ingestion → Data Normalization", "Data Normalization → Event Decoding → Node Ingestion", "Node Ingestion → Data Normalization → Event Decoding"],
      ["Phải lấy dữ liệu thô từ node trước khi giải mã.", "Đảo ngược toàn bộ.", "Phải giải mã sự kiện trước khi chuẩn hoá đơn vị."],
      "Lấy block/log qua RPC → giải mã log thành sự kiện bằng ABI → chuẩn hoá (Wei → Ether, timestamp → UTC).",
      "Chuẩn hoá trước khi giải mã.", "RPC → ABI → Normalize."),
    Q("VD", "Blockchain ETL (C9)", "Một giao dịch ghi giá trị <b>3,2 × 10¹⁸ Wei</b>. Sau bước chuẩn hoá, giá trị bằng bao nhiêu Ether?",
      ["3,2 ETH", "3,2 × 10⁹ ETH", "0,32 ETH", "32 ETH"],
      ["Chia cho 10⁹ (Gwei) thay vì 10¹⁸.", "Sai một bậc 10.", "Sai một bậc 10."],
      "1 Ether = 10¹⁸ Wei → 3,2 × 10¹⁸ / 10¹⁸ = 3,2 ETH.",
      "Nhầm Wei với Gwei.", "1 ETH = 10¹⁸ Wei."),
    Q("VD", "Blockchain ETL (C9)", "Token USDT có 6 chữ số thập phân. Giá trị thô trong log là <b>2.750.000</b>. Giá trị sau chuẩn hoá là:",
      ["2,75 USDT", "2.750.000 USDT", "0,00275 USDT", "27,5 USDT"],
      ["Chưa chia cho 10⁶.", "Chia cho 10⁹.", "Chia cho 10⁵."],
      "Giá trị thực = giá trị thô / 10^decimals = 2.750.000 / 10⁶ = 2,75. Mỗi token có số decimals riêng (ETH 18, USDT 6).",
      "Áp nhầm 18 chữ số của ETH cho mọi token.", "Chuẩn hoá = thô / 10^decimals."),
    # --- Merkle (2)
    Q("TH", "Merkle tree (C9)", "Cây Merkle có 4 lá L1–L4: H12 = hash(H1, H2), H34 = hash(H3, H4), Root = hash(H12, H34). Sửa nội dung <b>L2</b> thì:",
      ["H2, H12 và Root thay đổi; H34 giữ nguyên", "Chỉ H2 thay đổi, Root giữ nguyên", "Mọi nút trong cây, kể cả H34, đều thay đổi", "Chỉ Root thay đổi"],
      ["Hash cha phụ thuộc hash con nên thay đổi lan lên tận Root.", "H34 không phụ thuộc L2.", "H2 và H12 cũng phải đổi trước khi Root đổi."],
      "Thay đổi lan dọc đường từ lá lên gốc; nhánh còn lại giữ nguyên. Vì vậy so Root là phát hiện được bất kỳ sửa đổi nào.",
      "Nghĩ chỉ nút lá đổi.", "Sửa 1 lá → đổi cả đường lên Root."),
    Q("TH", "Merkle tree (C9)", "Để chống sửa nhật ký kiểm toán, slide đề xuất đưa gì lên blockchain?",
      ["Chỉ Merkle root của cả lô log", "Toàn bộ log thô của mỗi ngày", "Một bản sao của kho dữ liệu", "Khoá mã hoá của quản trị viên"],
      ["Lưu dữ liệu thô lên chuỗi rất đắt và lộ thông tin.", "Không cần và không khả thi.", "Đưa khoá lên chuỗi là rủi ro bảo mật."],
      "Merkle root nhỏ gọn nhưng đại diện cho cả lô; sửa một log bất kỳ làm root tính lại khác root đã neo trên chuỗi.",
      "Nghĩ phải lưu hết dữ liệu lên blockchain.", "Chỉ neo root lên chuỗi."),
    # --- Federated (3)
    Q("NB", "Federated query (C9)", "<b>Federated query</b> là:",
      ["Một câu SQL đọc nhiều nguồn mà không ETL dữ liệu về một chỗ", "Sao chép mọi nguồn về kho trung tâm bằng ETL rồi mới truy vấn", "Chia một bảng lớn thành nhiều partition theo ngày", "Chạy nhiều câu SQL song song trên cùng một nguồn"],
      ["Đó là cách tích hợp truyền thống.", "Đó là phân vùng.", "Đó là song song hoá trên một nguồn."],
      "Ba thành phần: connector (nói chuyện với từng nguồn), global catalog (biết bảng nào ở đâu), predicate pushdown (đẩy điều kiện lọc xuống nguồn).",
      "Nghĩ phải chép dữ liệu trước.", "Federated = một SQL, nhiều nguồn, không ETL."),
    Q("TH", "Predicate pushdown (C9)", "Câu federated query có <code>WHERE year = 2026</code> trên một bảng ở PostgreSQL. <b>Predicate pushdown</b> giúp:",
      ["Nguồn tự lọc trước, chỉ gửi các dòng năm 2026 qua mạng", "Kéo toàn bộ bảng qua mạng về rồi lọc ở engine trung tâm", "Tạo index trên cột year ở nguồn", "Sao lưu bảng năm 2026 sang archive"],
      ["Đó là trường hợp không pushdown – tốn băng thông.", "Pushdown không tạo index.", "Không liên quan sao lưu."],
      "Đẩy điều kiện lọc xuống nguồn giảm lượng dữ liệu truyền qua mạng – thường là chi phí lớn nhất của truy vấn liên nguồn.",
      "Nghĩ engine trung tâm luôn lọc.", "Pushdown = lọc tại nguồn."),
    Q("TH", "Federated query (C9)", "Trong kiến trúc federated query, thành phần nào biết <b>bảng nào nằm ở nguồn nào</b>?",
      ["Global catalog", "Connector", "Predicate pushdown", "Broker"],
      ["Connector thực hiện giao tiếp với từng nguồn cụ thể.", "Pushdown là kỹ thuật tối ưu lọc.", "Broker là thành phần Kafka."],
      "Global catalog là danh mục metadata hợp nhất; engine tra catalog để lập kế hoạch truy vấn.",
      "Lẫn catalog và connector.", "Catalog biết ở đâu · Connector kết nối."),
    # --- Joins (3)
    Q("VD", "Distributed join (C9)", "Bảng giao dịch <b>20 GB</b> phân tán trên <b>8</b> máy cần JOIN với bảng chi nhánh <b>100 MB</b>. Dùng broadcast join thì tổng lượng dữ liệu bảng nhỏ gửi qua mạng khoảng bao nhiêu?",
      ["800 MB", "100 MB", "20 GB", "2,5 GB"],
      ["Chỉ tính một bản, trong khi mỗi máy cần một bản.", "Đó là xáo trộn bảng lớn (hash join).", "20 GB/8 là phần bảng lớn trên mỗi máy."],
      "Broadcast: gửi bảng nhỏ tới cả 8 máy → 8 × 100 MB = 800 MB, rẻ hơn nhiều so với xáo trộn 20 GB.",
      "Quên nhân với số máy.", "Broadcast = kích thước bảng nhỏ × số máy."),
    Q("TH", "Distributed join (C9)", "Hai bảng đều rất lớn (hàng trăm GB) cần JOIN trên cụm phân tán. Chiến lược phù hợp:",
      ["Hash (shuffle) join: các dòng cùng khoá về cùng máy", "Broadcast join: gửi nguyên một bảng lớn tới mọi máy trong cụm", "Nested loop join chạy trên một máy duy nhất", "Không thể JOIN hai bảng lớn trên cụm phân tán"],
      ["Broadcast bảng lớn tới mọi máy quá tốn mạng và RAM.", "Một máy không đủ tài nguyên.", "Hash join xử lý được."],
      "Bảng nhỏ nối bảng lớn → broadcast; hai bảng lớn → hash join.",
      "Dùng broadcast cho mọi trường hợp.", "Nhỏ–lớn → broadcast · Lớn–lớn → hash."),
    Q("TH", "Cost-based optimizer (C9)", "Trong hệ phân tán, cost-based optimizer chọn kế hoạch JOIN dựa trên:",
      ["Chi phí ước tính, gồm cả chi phí truyền qua mạng", "Chỉ số dòng của bảng lớn nhất trong truy vấn", "Thứ tự viết các bảng trong câu SQL", "Chỉ chi phí CPU"],
      ["Cần cả thống kê của mọi bảng.", "Optimizer không phụ thuộc thứ tự viết.", "Bỏ qua mạng là sai lầm lớn trong hệ phân tán."],
      "Truyền dữ liệu giữa các máy thường đắt nhất nên optimizer phải tính chi phí mạng.",
      "Quên chi phí mạng.", "CBO phân tán: CPU + IO + mạng."),
    # --- RTO/RPO (3)
    Q("VD", "RTO và RPO (C9)", "Bản sao lưu gần nhất lúc <b>14:00</b>; sự cố xảy ra lúc <b>14:25</b>; hệ thống chạy lại lúc <b>15:10</b> với dữ liệu khôi phục từ bản 14:00. Lượng dữ liệu mất và thời gian chết lần lượt là:",
      ["25 phút và 45 phút", "45 phút và 25 phút", "70 phút và 45 phút", "25 phút và 70 phút"],
      ["Đảo hai đại lượng.", "Tính mất dữ liệu từ 14:00 tới 15:10.", "Tính thời gian chết từ lúc sao lưu thay vì lúc sự cố."],
      "Dữ liệu mất = 14:25 − 14:00 = 25 phút (đo theo RPO). Thời gian chết = 15:10 − 14:25 = 45 phút (đo theo RTO).",
      "Đảo RTO và RPO.", "RPO = mất bao nhiêu dữ liệu · RTO = chết bao lâu."),
    Q("VDC", "RTO và RPO (C9)", "Hệ thống cam kết <b>RPO = 15 phút, RTO = 30 phút</b>, sao lưu mỗi 20 phút (09:20, 09:40…). Sự cố lúc <b>09:38</b>, chạy lại lúc <b>10:00</b>. Kết luận đúng:",
      ["Vi phạm RPO, đạt RTO", "Đạt RPO, vi phạm RTO", "Đạt cả RPO và RTO", "Vi phạm cả RPO và RTO"],
      ["Mất 18 phút dữ liệu > 15 phút cam kết; thời gian chết 22 phút vẫn trong 30.", "Mất 18 phút > 15 phút nên RPO bị vi phạm.", "Thời gian chết 22 phút ≤ 30 nên RTO đạt."],
      "Dữ liệu mất = 09:38 − 09:20 = 18 phút > 15 → vi phạm RPO (chu kỳ sao lưu 20 phút vốn không bảo đảm được RPO 15). Thời gian chết = 10:00 − 09:38 = 22 phút ≤ 30 → đạt RTO.",
      "Đảo vai trò hai chỉ số.", "RPO so với lượng dữ liệu mất · RTO so với thời gian chết."),
    Q("TH", "Nhân bản dữ liệu (C9)", "So sánh nhân bản <b>đồng bộ</b> và <b>bất đồng bộ</b>:",
      ["Đồng bộ: RPO ≈ 0 nhưng ghi chậm; bất đồng bộ: ghi nhanh, RPO > 0", "Đồng bộ: ghi nhanh, RPO > 0; bất đồng bộ: RPO ≈ 0, ghi chậm", "Cả hai đều cho RPO = 0 và tốc độ ghi như nhau", "Bất đồng bộ luôn cho RTO bằng 0 vì không phải chờ"],
      ["Đảo ngược.", "Có đánh đổi giữa tốc độ ghi và mất dữ liệu.", "Nhân bản không quyết định RTO bằng 0."],
      "Đồng bộ chờ bản sao xác nhận mới báo ghi xong → không mất dữ liệu nhưng chậm; bất đồng bộ báo xong ngay → nhanh nhưng có độ trễ dữ liệu chưa sang.",
      "Đảo đặc điểm hai cách.", "Sync: RPO≈0, chậm · Async: nhanh, RPO>0."),
]
