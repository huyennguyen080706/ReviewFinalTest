"""Sinh 4 đề thi thử trắc nghiệm (src/de1.json … de4.json) bám 40 câu của file chẩn đoán.

Mỗi đề 47 câu: đủ 40 chủ đề, trong đó câu 28 tách 6 ý và câu 31 tách 2 ý.
Câu lý thuyết: cùng ý chính, mỗi đề hỏi một kiểu. Câu tính toán: đáp án và
phương án nhiễu được tính từ số liệu; nhiễu là các lỗi sinh viên hay mắc.
Quy ước như build.py: o[0] là đáp án đúng, x[i] giải thích vì sao o[i+1] sai.
"""
import json, math, pathlib
from fractions import Fraction as Fr
from collections import Counter

SRC = pathlib.Path(__file__).resolve().parent


# ---------------------------------------------------------------- tiện ích
def num(x, nd=4):
    if isinstance(x, Fr):
        x = float(x)
    s = f"{x:.{nd}f}".rstrip("0").rstrip(".")
    return s.replace(".", ",") if s != "-0" else "0"


def fr(f):
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


def Q(lv, t, q, o, x, w, trap, mem):
    assert len(o) == 4 and len(set(o)) == 4, (t, o)
    assert len(x) == 3, t
    return {"lv": lv, "t": t, "q": q, "o": o, "w": w, "x": x, "trap": trap, "mem": mem}


def pick(correct, cands, fmt):
    """Chọn 3 nhiễu khác nhau (khác đáp án) theo thứ tự ưu tiên; cands = [(giá trị, giải thích)]."""
    seen, out = {fmt(correct)}, []
    for v, why in cands:
        s = fmt(v)
        if s not in seen:
            seen.add(s); out.append((s, why))
        if len(out) == 3:
            break
    assert len(out) == 3, (correct, cands)
    return [fmt(correct)] + [s for s, _ in out], [w for _, w in out]


def table(header, rows):
    h = "".join(f"<th>{c}</th>" for c in header)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><tr>{h}</tr>{b}</table>"


def setstr(s):
    return "{" + ", ".join(s) + "}"


# ---------------------------------------------------------------- câu lý thuyết (4 biến thể / chủ đề)
def concept(v):
    T = []
    # 1 Firebolt
    T.append([
        Q("NB", "Firebolt (C1)", "<b>Firebolt</b> được định vị là nền tảng kho dữ liệu đám mây mạnh nhất về điểm nào?",
          ["Tốc độ truy vấn cực nhanh cho phân tích thời gian thực", "Tiên phong tách rời compute và storage", "Serverless hoàn toàn, tích hợp ML bằng SQL", "Lakehouse nhẹ chạy trên nền DuckDB"],
          ["Đó là Snowflake.", "Đó là BigQuery.", "Đó là MotherDuck."],
          "Slide Chương 1: Firebolt tập trung vào tốc độ truy vấn cực nhanh cho ứng dụng phân tích thời gian thực.",
          "Lẫn đặc điểm nhận diện của các nền tảng cloud DW.", "Snowflake: tách compute/storage · BigQuery: serverless + ML · Firebolt: tốc độ · MotherDuck: DuckDB."),
        Q("TH", "Firebolt (C1)", "Trong nhóm Snowflake, BigQuery, MotherDuck và Firebolt, nền tảng nào phù hợp nhất cho <b>dashboard thời gian thực cần độ trễ truy vấn cực thấp</b>?",
          ["Firebolt", "Snowflake", "BigQuery", "MotherDuck"],
          ["Snowflake nổi bật ở kiến trúc tách compute/storage, không phải tốc độ cực hạn.", "BigQuery nổi bật ở serverless và BigQuery ML.", "MotherDuck là Lakehouse nhẹ trên DuckDB, cho quy mô nhỏ–vừa."],
          "Firebolt được thiết kế cho phân tích thời gian thực với tốc độ truy vấn cực nhanh.",
          "Chọn Snowflake vì nổi tiếng nhất.", "Thời gian thực, độ trễ thấp → Firebolt."),
        Q("TH", "Firebolt (C1)", "Phát biểu nào <b>đúng</b> về Firebolt?",
          ["Hướng tới truy vấn cực nhanh cho phân tích thời gian thực", "Là nền tảng đầu tiên tách compute khỏi storage", "Là dịch vụ serverless của Google tích hợp ML", "Là phiên bản cloud của DuckDB"],
          ["Đó là Snowflake.", "Đó là BigQuery.", "Đó là MotherDuck."],
          "Firebolt: tốc độ truy vấn cực nhanh, phục vụ phân tích thời gian thực.",
          "Gán nhầm đặc điểm của nền tảng khác cho Firebolt.", "Firebolt = tốc độ."),
        Q("NB", "Firebolt (C1)", "Điểm khác biệt cốt lõi của <b>Firebolt</b> so với Snowflake là gì?",
          ["Ưu tiên tốc độ truy vấn cực nhanh cho real-time analytics", "Không lưu dữ liệu trên cloud mà chạy on-premise", "Chỉ hỗ trợ dữ liệu phi cấu trúc như ảnh, video", "Không dùng SQL mà truy vấn hoàn toàn bằng Python"],
          ["Firebolt là cloud data warehouse, dữ liệu nằm trên cloud.", "Firebolt phục vụ phân tích dữ liệu có cấu trúc bằng SQL.", "Firebolt truy vấn bằng SQL."],
          "Snowflake nổi bật ở tách compute/storage; Firebolt nổi bật ở tốc độ cho phân tích thời gian thực.",
          "Bịa ra khác biệt về ngôn ngữ hay loại dữ liệu.", "Firebolt = tốc độ, real-time."),
    ][v - 1])
    # 2 Caching
    T.append([
        Q("NB", "Caching (C1)", "Trong quản lý chi phí Modern Data Warehouse, cơ chế nào giúp <b>tránh tính toán lại những kết quả cũ</b>?",
          ["Caching kết quả truy vấn", "Auto-suspend", "Auto-scaling", "Archive tier"],
          ["Auto-suspend tắt kho khi không có truy vấn.", "Auto-scaling tăng/giảm tài nguyên theo tải.", "Archive tier là phân tầng lưu trữ dữ liệu cũ giá rẻ."],
          "Caching giữ lại kết quả truy vấn (~24 giờ); chạy lại đúng câu đó khi dữ liệu chưa đổi thì trả kết quả cũ, không tốn compute.",
          "Lẫn caching với auto-suspend vì cả hai đều tiết kiệm chi phí.", "Truy vấn lặp lại → caching; không có truy vấn → auto-suspend."),
        Q("TH", "Caching (C1)", "Một báo cáo được chạy mỗi giờ, dữ liệu gốc không thay đổi. Cơ chế nào giúp hệ thống <b>không tốn compute</b> cho các lần chạy sau?",
          ["Result caching", "Auto-suspend", "Budget alerts", "Định dạng nén Parquet"],
          ["Auto-suspend chỉ tiết kiệm khi không có truy vấn nào chạy.", "Budget alerts chỉ cảnh báo khi vượt ngưỡng chi phí.", "Nén Parquet giảm dung lượng quét, vẫn phải tính lại."],
          "Truy vấn lặp lại, dữ liệu không đổi → trả kết quả từ cache, không quét bảng.",
          "Chọn auto-suspend vì nghĩ cứ tiết kiệm là auto-suspend.", "Caching = dùng lại kết quả cũ."),
        Q("TH", "Caching (C1)", "Trường hợp nào <b>KHÔNG</b> dùng được kết quả từ cache truy vấn?",
          ["Câu truy vấn có hàm CURRENT_TIMESTAMP()", "Chạy lại đúng câu truy vấn sau 1 giờ", "Hai người dùng chạy cùng một câu truy vấn", "Dữ liệu gốc chưa thay đổi kể từ lần chạy trước"],
          ["Cache vẫn còn hiệu lực (~24 giờ).", "Cache dùng chung khi câu truy vấn giống hệt.", "Dữ liệu chưa đổi chính là điều kiện để dùng cache."],
          "Cache không dùng được khi bảng đã đổi, câu truy vấn khác đi, hoặc có hàm không xác định như CURRENT_TIMESTAMP().",
          "Nghĩ cache luôn dùng được cho mọi truy vấn lặp lại.", "Bảng đổi / câu khác / hàm thời gian → không dùng cache."),
        Q("TH", "Caching (C1)", "Phát biểu nào phân biệt <b>đúng</b> caching và auto-suspend?",
          ["Caching: khi truy vấn lặp lại; auto-suspend: khi không có truy vấn", "Caching: tắt kho khi rảnh; auto-suspend: lưu kết quả cũ", "Cả hai đều lưu lại kết quả truy vấn trong khoảng 24 giờ", "Auto-suspend: dùng lại kết quả; caching: tăng tài nguyên"],
          ["Đảo ngược chức năng của hai cơ chế.", "Chỉ caching lưu kết quả; auto-suspend tắt tài nguyên.", "Auto-suspend không dùng lại kết quả, caching không tăng tài nguyên."],
          "Caching: dùng lại kết quả cũ. Auto-suspend: tự tắt kho tính toán khi không có truy vấn.",
          "Đảo vai trò hai cơ chế.", "Lặp lại → cache; rảnh → suspend."),
    ][v - 1])
    # 3 Data Fabric
    T.append([
        Q("TH", "Data Fabric (C1)", "Mục tiêu cuối cùng của kiến trúc <b>Data Fabric</b> là gì?",
          ["Kết nối dữ liệu rời rạc thành thể thống nhất, xóa bỏ data silo", "Sao chép toàn bộ dữ liệu về một kho trung tâm", "Thay thế hoàn toàn data warehouse bằng data lake", "Phân quyền cho từng domain tự quản dữ liệu"],
          ["Data Fabric dùng virtualization, không cần di chuyển/sao chép dữ liệu.", "Data Fabric là lớp kết nối, không thay thế kho.", "Đó là tư tưởng Data Mesh."],
          "Data Fabric: virtualization (zero-copy), abstraction layer, hybrid-cloud, tự động hóa truy cập an toàn, một cổng truy cập duy nhất → xóa data silo.",
          "Lẫn Data Fabric với Data Mesh hoặc với việc gom dữ liệu về một chỗ.", "Fabric = kết nối không di chuyển dữ liệu; Mesh = phân quyền theo domain."),
        Q("NB", "Data Fabric (C1)", "Data Fabric truy cập dữ liệu tại nguồn mà <b>không sao chép</b> nhờ cơ chế nào?",
          ["Virtualization", "Replication", "Batch ETL", "Sharding"],
          ["Replication là sao chép dữ liệu.", "Batch ETL trích xuất và nạp dữ liệu sang kho khác.", "Sharding chia dữ liệu theo phân mảnh, không liên quan truy cập tại nguồn."],
          "Virtualization cho phép truy cập dữ liệu tại nguồn (zero-copy).",
          "Nghĩ tích hợp dữ liệu thì bắt buộc phải sao chép.", "Data Fabric: virtualization, zero-copy."),
        Q("TH", "Data Fabric (C1)", "Ý nào <b>KHÔNG</b> phải mục tiêu của Data Fabric?",
          ["Di chuyển toàn bộ dữ liệu về một data lake duy nhất", "Che giấu độ phức tạp hạ tầng bằng abstraction layer", "Hỗ trợ kết nối on-premise và cloud", "Cung cấp một cổng truy cập dữ liệu duy nhất"],
          ["Đây là mục tiêu của Data Fabric.", "Hỗ trợ hybrid-cloud là mục tiêu của Data Fabric.", "Trải nghiệm thống nhất là mục tiêu của Data Fabric."],
          "Data Fabric kết nối dữ liệu mà không cần di chuyển dữ liệu.",
          "Nhầm \"thống nhất\" thành \"gom về một chỗ\".", "Thống nhất truy cập ≠ di chuyển dữ liệu."),
        Q("VD", "Data Fabric (C1)", "Doanh nghiệp có dữ liệu ở on-premise và nhiều cloud, mỗi phòng ban một kho riêng. Giải pháp kiến trúc nào giúp <b>truy cập thống nhất mà không di chuyển dữ liệu</b>?",
          ["Data Fabric", "Data Mesh", "Kho dữ liệu tập trung với ETL hằng đêm", "Data Swamp"],
          ["Data Mesh trao quyền sở hữu dữ liệu cho từng domain, trọng tâm là tổ chức.", "ETL hằng đêm phải sao chép dữ liệu.", "Data swamp là hồ dữ liệu hỗn loạn, là vấn đề chứ không phải giải pháp."],
          "Data Fabric: lớp kết nối thống nhất, virtualization, hỗ trợ hybrid-cloud, xóa data silo.",
          "Chọn Data Mesh vì cũng nói về dữ liệu phân tán.", "Không di chuyển dữ liệu + truy cập thống nhất → Data Fabric."),
    ][v - 1])
    # 4 Data Catalog
    T.append([
        Q("NB", "Data Catalog (C1)", "<b>Data Catalog</b> là gì?",
          ["Thư viện chứa thông tin và vị trí của mọi nguồn dữ liệu", "Kho lưu bản sao dự phòng của dữ liệu", "Công cụ lập lịch chạy pipeline", "Bảng fact tổng hợp các chỉ số"],
          ["Đó là backup/versioning.", "Đó là orchestrator như Airflow.", "Fact table thuộc mô hình chiều."],
          "Data Catalog: \"danh bạ\" tài sản dữ liệu – có bảng nào, ở đâu, cột nghĩa gì, ai sở hữu, ai được dùng.",
          "Lẫn catalog với nơi lưu dữ liệu.", "Catalog lưu metadata, không lưu dữ liệu."),
        Q("TH", "Data Catalog (C1)", "Thành phần nào của Data Fabric đóng vai trò \"<b>thư viện chứa thông tin và vị trí của mọi nguồn dữ liệu</b>\"?",
          ["Data Catalog", "Augmented Data Integration", "Knowledge Graph", "Data Virtualization"],
          ["Augmented Data Integration dùng AI hỗ trợ ánh xạ, tích hợp.", "Knowledge Graph liên kết ngữ nghĩa giữa các thực thể.", "Virtualization truy cập dữ liệu tại nguồn."],
          "Slide Chương 1: Data Catalog là thư viện chứa thông tin và vị trí của mọi nguồn dữ liệu.",
          "Lẫn các thành phần kỹ thuật của Data Fabric.", "Catalog = danh bạ, metadata."),
        Q("TH", "Data Catalog (C1)", "Data Catalog <b>KHÔNG</b> cung cấp thông tin nào sau đây?",
          ["Bản sao đầy đủ các dòng dữ liệu nghiệp vụ", "Bảng nào tồn tại và nằm ở đâu", "Ý nghĩa của từng cột", "Ai sở hữu và ai được dùng dữ liệu"],
          ["Đây là thông tin catalog cung cấp.", "Đây là thông tin catalog cung cấp.", "Đây là thông tin catalog cung cấp."],
          "Catalog quản lý metadata, không chứa bản sao dữ liệu.",
          "Nghĩ catalog là nơi chứa dữ liệu.", "Catalog = metadata."),
        Q("TH", "Data Catalog (C1)", "Data Catalog giúp doanh nghiệp tránh tình trạng nào?",
          ["Data swamp – không biết dữ liệu sạch nằm ở đâu", "Data skew – phân bố dữ liệu lệch giữa các node", "Overfitting – mô hình học thuộc dữ liệu", "Deadlock – các giao dịch khóa lẫn nhau"],
          ["Data skew xử lý bằng phân vùng/clustering.", "Overfitting là vấn đề của học máy.", "Deadlock là vấn đề điều khiển đồng thời."],
          "Chương 7: catalog là \"danh bạ\" tài sản dữ liệu, giúp tránh data swamp; AI-driven catalog tự gắn nhãn PII.",
          "Lẫn các thuật ngữ \"data ...\".", "Catalog chống data swamp."),
    ][v - 1])
    # 5 Bucket Policies
    T.append([
        Q("NB", "Bucket Policies (C1)", "<b>Bucket Policies</b> có chức năng gì?",
          ["Quy định quyền truy cập cho toàn bộ bucket từ bên ngoài", "Lưu nhiều phiên bản để khôi phục bản cũ", "Khóa không cho xóa/sửa trong một khoảng thời gian", "Nén dữ liệu để giảm chi phí lưu trữ"],
          ["Đó là Versioning.", "Đó là Object Lock.", "Bucket policy không nén dữ liệu."],
          "Bucket policy gắn với tài nguyên (bucket), quy định ai/từ đâu được truy cập.",
          "Lẫn ba cơ chế bảo mật Object Storage.", "Policy: quyền truy cập · Versioning: khôi phục · Object Lock: chống xóa/sửa."),
        Q("TH", "Bucket Policies (C1)", "Phân biệt đúng <b>Bucket Policy</b> và IAM Policy:",
          ["Bucket Policy gắn với tài nguyên; IAM Policy gắn với người dùng/vai trò", "Bucket Policy gắn với người dùng; IAM Policy gắn với tài nguyên", "Bucket Policy dùng để mã hóa; IAM Policy dùng để nén", "Hai loại giống nhau, chỉ khác tên nhà cung cấp"],
          ["Đảo ngược đối tượng gắn.", "Không loại nào dùng để nén/mã hóa.", "Hai loại khác nhau về đối tượng gắn quyền."],
          "Bucket policy gắn với bucket (data container); IAM policy gắn với người/vai trò.",
          "Đảo đối tượng gắn của hai loại policy.", "Bucket → tài nguyên; IAM → danh tính."),
        Q("VD", "Bucket Policies (C1)", "Muốn quy định \"<b>bucket này chỉ cho truy cập từ mạng nội bộ công ty</b>\", nên dùng cơ chế nào?",
          ["Bucket Policy", "Versioning", "Object Lock", "Lifecycle rule chuyển sang Archive"],
          ["Versioning giữ nhiều phiên bản đối tượng.", "Object Lock chống xóa/sửa trong thời hạn.", "Lifecycle rule chuyển lớp lưu trữ, không kiểm soát truy cập."],
          "Quy định truy cập toàn bucket từ bên ngoài là chức năng của Bucket Policy.",
          "Chọn Object Lock vì nghĩ \"lock\" là chặn truy cập.", "Ai/từ đâu được truy cập bucket → Bucket Policy."),
        Q("NB", "Bucket Policies (C1)", "Bucket Policies kiểm soát điều gì đối với một data container (bucket)?",
          ["Quyền truy cập toàn bucket từ bên ngoài", "Số phiên bản tối đa của mỗi đối tượng", "Thời gian lưu cache truy vấn", "Kích thước micro-partition"],
          ["Đó là cấu hình Versioning.", "Cache truy vấn thuộc kho dữ liệu, không thuộc bucket.", "Micro-partition là cơ chế của Snowflake."],
          "Bucket policy quy định quyền truy cập cho toàn bộ bucket.",
          "Lẫn với Versioning.", "Bucket policy = quyền truy cập."),
    ][v - 1])
    # 6 Micro-partition
    T.append([
        Q("NB", "Micro-partition (C2)", "Với <b>Micro-partitioning</b>, mỗi phân vùng chứa lượng dữ liệu nén khoảng bao nhiêu?",
          ["50 MB – 500 MB", "1 GB – 5 GB", "5 MB – 50 MB", "64 KB – 1 MB"],
          ["Quá lớn so với micro-partition.", "Quá nhỏ.", "Đó là cỡ khối/trang lưu trữ, không phải micro-partition."],
          "Mỗi micro-partition chứa 50–500 MB dữ liệu nén, lưu theo cột, metadata ghi min/max từng cột để pruning.",
          "Nhớ nhầm đơn vị MB/GB.", "Micro-partition: 50–500 MB nén."),
        Q("TH", "Micro-partition (C2)", "Phát biểu nào <b>đúng</b> về micro-partition trong Snowflake?",
          ["Mỗi phân vùng 50–500 MB nén, lưu theo cột", "Mỗi phân vùng 50–500 MB chưa nén, lưu theo dòng", "Người dùng phải tự định nghĩa ranh giới phân vùng", "Mỗi phân vùng 1–5 GB nén, lưu theo cột"],
          ["Dữ liệu được nén và lưu theo cột.", "Micro-partition do hệ thống tự tạo.", "Kích thước sai."],
          "Micro-partition tự động, 50–500 MB nén, columnar, có metadata min/max.",
          "Nhớ đúng con số nhưng sai trạng thái nén/hướng lưu.", "Tự động · nén · theo cột · 50–500 MB."),
        Q("TH", "Micro-partition (C2)", "Metadata của mỗi micro-partition lưu gì để hỗ trợ <b>pruning</b>?",
          ["Giá trị min/max của từng cột", "Toàn bộ chỉ mục B-tree của bảng", "Bản sao các dòng được truy vấn nhiều", "Lịch sử các câu truy vấn gần nhất"],
          ["Snowflake không dùng B-tree index.", "Metadata không lưu bản sao dữ liệu.", "Lịch sử truy vấn không phục vụ pruning."],
          "Min/max từng cột cho mỗi phân vùng (50–500 MB nén) giúp bỏ qua phân vùng không liên quan.",
          "Nghĩ pruning dựa trên index truyền thống.", "Pruning dựa trên min/max."),
        Q("NB", "Micro-partition (C2)", "\"Mỗi micro-partition chứa khoảng 1–5 GB dữ liệu nén.\" Nhận định nào đúng?",
          ["Sai, mỗi micro-partition chỉ khoảng 50–500 MB nén", "Đúng", "Sai, mỗi micro-partition khoảng 5–50 MB nén", "Sai, micro-partition không nén dữ liệu"],
          ["Con số 1–5 GB là sai.", "Con số đúng là 50–500 MB.", "Micro-partition có nén, theo cột."],
          "Micro-partition: 50–500 MB nén.",
          "Nhầm đơn vị.", "50–500 MB."),
    ][v - 1])
    # 7 Clustering key
    T.append([
        Q("TH", "Clustering Key (C2)", "Trong chiến lược Clustering, <b>Clustering Key</b> được chọn dựa trên đối tượng nào?",
          ["Cột có độ chọn lọc cao, hay xuất hiện trong WHERE", "Cột khóa chính duy nhất của bảng", "Cột có ít giá trị khác nhau nhất", "Cột chứa dữ liệu văn bản dài"],
          ["Cột quá nhiều giá trị (duy nhất) tốn công duy trì clustering.", "Cột quá ít giá trị (giới tính) pruning được ít.", "Văn bản dài không phù hợp làm khóa sắp xếp."],
          "Chọn cột hay lọc trong WHERE, độ chọn lọc cao; cột ngày thường là lựa chọn tốt.",
          "Chọn khóa chính vì nghĩ khóa duy nhất là tốt nhất.", "Clustering key: cột hay lọc, chọn lọc vừa đủ (thường là ngày)."),
        Q("TH", "Clustering Key (C2)", "Vì sao cột <b>gioi_tinh</b> không phải Clustering Key tốt?",
          ["Quá ít giá trị khác nhau nên pruning được rất ít", "Quá nhiều giá trị nên tốn chi phí duy trì", "Kiểu chuỗi không thể dùng làm khóa", "Cột này không bao giờ được truy vấn"],
          ["Đó là nhược điểm của cột duy nhất như mã giao dịch.", "Cột chuỗi vẫn có thể dùng làm khóa.", "Không phải lý do kỹ thuật."],
          "Cột ít giá trị (2–3 giá trị) chia dữ liệu quá thô, pruning kém.",
          "Lẫn hai cực: quá ít và quá nhiều giá trị.", "Quá ít giá trị → pruning kém; quá nhiều → tốn duy trì."),
        Q("VD", "Clustering Key (C2)", "Bảng giao dịch cực lớn có các cột: ma_giao_dich (duy nhất), gioi_tinh, ngay_giao_dich, ghi_chu. Cột nào phù hợp làm <b>Clustering Key</b>?",
          ["ngay_giao_dich", "ma_giao_dich", "gioi_tinh", "ghi_chu"],
          ["Cột duy nhất tốn công duy trì clustering.", "Quá ít giá trị, pruning kém.", "Văn bản tự do, không ai lọc theo cột này."],
          "Cột ngày hay xuất hiện trong WHERE, độ chọn lọc phù hợp, tối ưu range query.",
          "Chọn mã giao dịch vì là khóa duy nhất.", "Cột ngày thường là Clustering Key tốt."),
        Q("NB", "Clustering Key (C2)", "Clustering Key thường được chọn từ các cột xuất hiện ở đâu trong truy vấn?",
          ["Mệnh đề WHERE (điều kiện lọc)", "Danh sách SELECT", "Mệnh đề ORDER BY của báo cáo", "Tên bảng sau FROM"],
          ["Cột được chọn ra không quyết định pruning.", "ORDER BY không giúp bỏ qua phân vùng.", "FROM chỉ là tên bảng."],
          "Clustering tối ưu pruning cho điều kiện lọc → cột trong WHERE, độ chọn lọc cao.",
          "Nghĩ cột hay hiển thị là cột cần cluster.", "Cluster theo cột lọc."),
    ][v - 1])
    # 8 Accumulating snapshot
    T.append([
        Q("TH", "Accumulating Snapshot (C2)", "<b>Accumulating Snapshot Fact Table</b> phù hợp cho ngữ cảnh nào?",
          ["Theo dõi tiến độ quy trình nhiều giai đoạn có mốc thời gian", "Ghi từng giao dịch bán hàng riêng lẻ", "Chụp số dư tài khoản vào cuối mỗi tháng", "Lưu thuộc tính mô tả của khách hàng"],
          ["Đó là Transaction fact.", "Đó là Periodic snapshot fact.", "Đó là dimension table."],
          "Mỗi dòng là một thực thể trong cả vòng đời quy trình (đơn hàng: đặt → đóng gói → giao), được cập nhật khi qua bước mới; dùng tính lead time.",
          "Lẫn periodic và accumulating snapshot vì cùng chữ snapshot.", "Transaction: sự kiện · Periodic: theo kỳ · Accumulating: theo vòng đời."),
        Q("VD", "Accumulating Snapshot (C2)", "Cần theo dõi đơn hàng qua đặt → đóng gói → giao và <b>tính lead time giữa các bước</b>. Nên dùng loại fact table nào?",
          ["Accumulating snapshot fact table", "Transaction fact table", "Periodic snapshot fact table", "Factless fact table"],
          ["Mỗi sự kiện một dòng, khó tính lead time trên một dòng.", "Chụp theo kỳ cố định, không theo mốc quy trình.", "Chỉ ghi sự kiện xảy ra, không có mốc thời gian theo bước."],
          "Accumulating snapshot: mỗi đơn hàng một dòng, các cột ngày được cập nhật dần.",
          "Chọn transaction vì đơn hàng là giao dịch.", "Quy trình nhiều bước + lead time → accumulating."),
        Q("TH", "Accumulating Snapshot (C2)", "Đặc điểm nào chỉ có ở Accumulating Snapshot mà <b>không</b> có ở Transaction và Periodic Snapshot?",
          ["Dòng dữ liệu được cập nhật khi quy trình qua bước mới", "Mỗi dòng ứng với một sự kiện", "Mỗi dòng ứng với một đối tượng tại một kỳ", "Dữ liệu chỉ được thêm mới, không sửa"],
          ["Đó là Transaction fact.", "Đó là Periodic snapshot.", "Đó là đặc điểm của hai loại còn lại."],
          "Accumulating snapshot là loại duy nhất có dòng bị sửa (cập nhật mốc thời gian).",
          "Nghĩ fact table không bao giờ bị cập nhật.", "Accumulating: dòng bị cập nhật."),
        Q("NB", "Accumulating Snapshot (C2)", "Trong Accumulating Snapshot Fact Table, <b>một dòng</b> đại diện cho gì?",
          ["Một đối tượng trong cả vòng đời quy trình", "Một sự kiện tại một thời điểm", "Một đối tượng tại một kỳ báo cáo", "Một thuộc tính mô tả của dimension"],
          ["Đó là Transaction fact.", "Đó là Periodic snapshot.", "Đó là dimension."],
          "Ví dụ: một đơn hàng từ lúc đặt đến lúc giao.",
          "Lẫn các loại fact.", "Accumulating: một dòng = một vòng đời."),
    ][v - 1])
    # 9 Bridge
    T.append([
        Q("NB", "Bridge Table (C2)", "Chức năng của <b>Bridge Table</b> là gì?",
          ["Giải quyết quan hệ nhiều–nhiều giữa fact và dimension", "Lưu lịch sử thay đổi của dimension", "Gộp fact và dimension thành bảng rộng", "Tính trước các chỉ số tổng hợp"],
          ["Đó là SCD.", "Đó là flat/wide table.", "Đó là aggregate table."],
          "Bridge table (vd. account_key, customer_key, weight) ánh xạ quan hệ M–M; lưu ý JOIN có thể đếm trùng.",
          "Lẫn với SCD hoặc flat table.", "M–M → bridge table."),
        Q("VD", "Bridge Table (C2)", "Một tài khoản có nhiều chủ sở hữu, một khách hàng có nhiều tài khoản. Cấu trúc nào giúp mô hình hóa quan hệ này?",
          ["Bridge table (account_key, customer_key, weight)", "Thêm cột customer_key vào fact table", "SCD Type 2 cho dimension khách hàng", "Junk dimension gộp các cờ"],
          ["Một cột chỉ chứa được một khách hàng.", "SCD 2 lưu lịch sử thay đổi, không giải quyết M–M.", "Junk dimension gộp cờ ít giá trị."],
          "Quan hệ nhiều–nhiều giữa tài khoản và khách hàng → bảng cầu, có thể kèm weight để phân bổ.",
          "Chọn SCD vì nghĩ đến dimension khách hàng.", "M–M → bridge."),
        Q("TH", "Bridge Table (C2)", "Rủi ro điển hình khi JOIN qua <b>bảng cầu</b> là gì?",
          ["Bùng nổ dữ liệu, đếm trùng chỉ số", "Mất lịch sử thay đổi của dimension", "Không thể dùng khóa thay thế", "Không thể nén dữ liệu theo cột"],
          ["Lịch sử dimension thuộc SCD.", "Bridge table dùng khóa thay thế bình thường.", "Không liên quan nén."],
          "JOIN M–M nhân bản dòng fact → cần weight hoặc cẩn thận khi cộng dồn.",
          "Quên rủi ro đếm trùng.", "Bridge: giải quyết M–M, cẩn thận đếm trùng."),
        Q("TH", "Bridge Table (C2)", "Bridge Table được dùng khi giữa fact và dimension có quan hệ dạng nào?",
          ["Nhiều–nhiều", "Một–một", "Một–nhiều thông thường", "Không có quan hệ"],
          ["Một–một không cần bảng trung gian.", "Một–nhiều nối trực tiếp bằng khóa ngoại.", "Không quan hệ thì không cần nối."],
          "Bridge table dành cho quan hệ M–M.",
          "Nghĩ mọi quan hệ phức tạp đều cần bridge.", "M–M."),
    ][v - 1])
    # 10 Flat table
    T.append([
        Q("NB", "Flat table (C2)", "<b>Flat tables</b> được dùng để giảm thiểu phép tính nào?",
          ["JOIN", "GROUP BY", "SORT", "UNION"],
          ["Flat table không loại bỏ tổng hợp.", "Không phải mục tiêu chính.", "Không phải mục tiêu chính."],
          "Flat (wide) table gộp sẵn fact và dimension, truy vấn không cần JOIN.",
          "Nhầm với aggregate table (giảm GROUP BY).", "Flat → bớt JOIN; aggregate → bớt GROUP BY."),
        Q("TH", "Flat table (C2)", "Trên cloud, vì sao người ta chấp nhận denormalization thành <b>flat table</b>?",
          ["Ưu tiên tối ưu truy vấn (bớt JOIN) hơn tối ưu dung lượng", "Lưu trữ trên cloud rất đắt nên cần gộp bảng", "Để dữ liệu đạt chuẩn 3NF, tránh dư thừa", "Để giảm số cột phải lưu trong mỗi bảng"],
          ["Lưu trữ cloud rẻ, compute mới đắt.", "Denormalization đi ngược 3NF.", "Flat table nhiều cột hơn."],
          "Lưu trữ rẻ, compute đắt → gộp sẵn để tránh JOIN.",
          "Nghĩ denormalization để tiết kiệm dung lượng.", "Cloud: đổi dung lượng lấy tốc độ."),
        Q("TH", "Flat table (C2)", "Wide table gộp sẵn thông tin fact và dimension nhằm tránh thao tác gì khi truy vấn?",
          ["Nối bảng (JOIN)", "Lọc dòng (WHERE)", "Sắp xếp (ORDER BY)", "Phân trang (LIMIT)"],
          ["Vẫn phải lọc dòng.", "Vẫn có thể sắp xếp.", "Không liên quan."],
          "Flat/wide table loại bỏ phép JOIN.",
          "Chọn bừa thao tác khác.", "Flat = không JOIN."),
        Q("NB", "Flat table (C2)", "\"Flat table được dùng để giảm phép GROUP BY.\" Nhận định nào đúng?",
          ["Sai, flat table giảm phép JOIN", "Đúng", "Sai, flat table giảm phép UNION", "Sai, flat table giảm phép WHERE"],
          ["Flat table giảm JOIN.", "Không phải mục tiêu.", "Không phải mục tiêu."],
          "Flat table → bớt JOIN; aggregate table mới giảm GROUP BY.",
          "Lẫn flat với aggregate.", "Flat → JOIN."),
    ][v - 1])
    # 11 Snowflake evolution
    T.append([
        Q("TH", "Schema evolution (C3)", "Đặc tính của <b>Snowflake Evolution</b> là gì?",
          ["Tự điều chỉnh cấu trúc bảng ngay khi chạy COPY nếu file có cột mới", "Tự chuyển mô hình hình sao sang mô hình bông tuyết khi nạp", "Tự xóa các cột không còn được truy vấn sau 30 ngày", "Tự sinh test kiểm tra cột rỗng, trùng lặp cho bảng mới"],
          ["Không liên quan mô hình hóa star/snowflake.", "Không có cơ chế tự xóa cột.", "Đó là dbt schema tests."],
          "Snowflake schema evolution: COPY gặp cột mới → bảng tự thêm cột, tránh pipeline dừng hoặc mất dữ liệu âm thầm.",
          "Lẫn \"Snowflake\" nền tảng với snowflake schema.", "Evolution = tự thích ứng khi nguồn đổi schema."),
        Q("VD", "Schema evolution (C3)", "File nạp vào Snowflake bất ngờ có thêm cột mới. Tính năng nào giúp pipeline <b>không bị dừng</b>?",
          ["Schema evolution khi chạy COPY", "Time Travel", "Zero-copy cloning", "Result caching"],
          ["Time Travel truy vấn dữ liệu quá khứ.", "Cloning tạo bản sao tức thời.", "Caching dùng lại kết quả truy vấn."],
          "Schema evolution tự thêm cột trong quá trình COPY.",
          "Chọn Time Travel vì nghe quen.", "Cột mới → schema evolution."),
        Q("TH", "Schema evolution (C3)", "Mục đích chính của Snowflake schema evolution là tránh sự cố nào?",
          ["Pipeline dừng hoặc mất dữ liệu âm thầm khi nguồn đổi schema", "Truy vấn chậm do bảng lớn thiếu clustering key", "Chi phí tăng do kho tính toán không auto-suspend", "Lộ dữ liệu PII khi chia sẻ bảng ra bên ngoài"],
          ["Đó là vấn đề clustering.", "Đó là vấn đề quản lý chi phí.", "Đó là vấn đề bảo mật (CLM)."],
          "Evolution giúp hệ thống thích ứng với cột mới, không vỡ pipeline, không silent loss.",
          "Không hiểu mục đích của schema evolution.", "Chống vỡ pipeline + silent loss."),
        Q("NB", "Schema evolution (C3)", "Tính năng Snowflake tự điều chỉnh cấu trúc bảng khi file nguồn có cột mới hoạt động trong lệnh nào?",
          ["COPY", "MERGE", "CLONE", "UNDROP"],
          ["MERGE dùng cập nhật/chèn có điều kiện.", "CLONE tạo bản sao.", "UNDROP khôi phục đối tượng đã xóa."],
          "Schema evolution áp dụng ngay khi chạy COPY.",
          "Nhầm lệnh.", "Evolution ↔ COPY."),
    ][v - 1])
    # 12 Schema tests
    T.append([
        Q("NB", "Schema Tests (C3)", "Chức năng của <b>Schema Tests</b> trong dbt là gì?",
          ["Tự động kiểm tra điều kiện cơ bản như rỗng, trùng lặp", "Viết SQL riêng cho quy tắc nghiệp vụ đặc thù", "Lập lịch và điều phối thứ tự chạy các model", "Sinh tài liệu mô tả bảng và sơ đồ lineage"],
          ["Đó là Singular tests.", "Đó là orchestrator.", "Đó là dbt docs."],
          "Schema (generic) tests khai báo trong YAML: not_null, unique, accepted_values, relationships.",
          "Lẫn schema test và singular test.", "Generic/schema: YAML; singular: SQL riêng."),
        Q("TH", "Schema Tests (C3)", "Test nào <b>không</b> thuộc 4 schema test có sẵn của dbt?",
          ["row_count_greater_than", "not_null", "accepted_values", "relationships"],
          ["Có sẵn.", "Có sẵn.", "Có sẵn."],
          "4 test có sẵn: not_null, unique, accepted_values, relationships.",
          "Bịa ra test không có sẵn.", "not_null · unique · accepted_values · relationships."),
        Q("TH", "Schema Tests (C3)", "Phân biệt đúng Schema Tests và Singular Tests:",
          ["Schema test khai báo trong YAML; singular test là câu SQL viết riêng", "Schema test viết bằng Python; singular test khai báo YAML", "Schema test kiểm tra hiệu năng; singular test kiểm tra bảo mật", "Hai loại giống nhau"],
          ["Đảo vị trí khai báo và dbt không dùng Python cho test.", "Không phải mục đích của hai loại test.", "Hai loại khác nhau."],
          "Schema/generic: khai báo YAML, dbt tự sinh SQL. Singular: SQL viết tay cho quy tắc nghiệp vụ.",
          "Đảo hai loại test.", "YAML vs SQL riêng."),
        Q("VD", "Schema Tests (C3)", "Muốn tự động kiểm tra cột khóa <b>không rỗng và không trùng</b>, cách nào phù hợp nhất trong dbt?",
          ["Khai báo not_null và unique trong file YAML", "Viết singular test bằng SQL riêng", "Dùng macro Jinja để sinh dữ liệu mẫu", "Cấu hình retry trong Airflow"],
          ["Làm được nhưng thừa, đã có test có sẵn.", "Macro không phải để kiểm tra.", "Retry không kiểm tra dữ liệu."],
          "Schema tests not_null + unique khai báo trong YAML.",
          "Tự viết SQL dù đã có test có sẵn.", "Rỗng/trùng → not_null/unique."),
    ][v - 1])
    # 13 Jinja
    T.append([
        Q("NB", "Jinja (C3)", "<b>Jinja</b> là gì?",
          ["Templating engine thêm if/for/biến vào SQL tĩnh", "Công cụ điều phối pipeline dạng DAG", "Định dạng lưu trữ dạng cột", "Thư viện kiểm thử dữ liệu"],
          ["Đó là Airflow.", "Đó là Parquet.", "Đó là dbt tests/Great Expectations."],
          "Jinja tạo dynamic SQL trong dbt: macro, đổi tên bảng/schema theo môi trường.",
          "Lẫn Jinja với công cụ khác trong stack.", "Jinja = template cho SQL."),
        Q("TH", "Jinja (C3)", "Trong dbt, thành phần nào giúp bổ sung <b>cấu trúc điều khiển</b> (if, for, biến) vào câu SQL?",
          ["Jinja", "YAML", "DAG", "Seed"],
          ["YAML dùng để khai báo cấu hình và test.", "DAG mô tả phụ thuộc giữa các bước.", "Seed là file CSV nạp vào kho."],
          "Jinja biến SQL tĩnh thành dynamic SQL.",
          "Lẫn YAML (cấu hình) với Jinja (template).", "if/for trong SQL → Jinja."),
        Q("TH", "Jinja (C3)", "<b>Macro</b> trong dbt được viết bằng gì và có vai trò gì?",
          ["Jinja; đóng gói đoạn SQL lặp lại thành hàm", "YAML; khai báo test có sẵn", "Python; huấn luyện mô hình", "JSON; lưu metadata"],
          ["YAML không viết macro.", "Macro dbt không viết bằng Python.", "JSON không phải nơi viết macro."],
          "Macro = hàm Jinja tái sử dụng SQL.",
          "Nghĩ macro viết bằng Python.", "Macro = Jinja."),
        Q("VD", "Jinja (C3)", "Muốn câu SQL tự đổi tên schema theo môi trường Dev/Test/Prod trong dbt, nên dùng gì?",
          ["Biến và điều kiện Jinja", "Schema test accepted_values", "Bridge table", "Storage mirroring"],
          ["Test chỉ kiểm tra dữ liệu.", "Bridge table thuộc mô hình hóa.", "Mirroring là nhân bản dữ liệu."],
          "Jinja trừu tượng hóa tên bảng/schema theo môi trường.",
          "Không biết Jinja hỗ trợ môi trường.", "Đổi theo môi trường → Jinja."),
    ][v - 1])
    # 14 Airflow
    T.append([
        Q("TH", "Apache Airflow (C3)", "Đặc tính nào <b>đúng</b> với Apache Airflow?",
          ["Task-centric, pipeline viết thành DAG bằng Python", "Asset-centric, quản lý theo tài sản dữ liệu", "Chỉ chạy được trên một cloud duy nhất", "Không hỗ trợ retry khi tác vụ lỗi"],
          ["Đó là Dagster.", "Airflow có hàng nghìn connector đa nền tảng.", "Airflow hỗ trợ retry, cảnh báo."],
          "Airflow: chuẩn công nghiệp cho orchestration, hàng nghìn thư viện kết nối, task-centric, DAG Python.",
          "Lẫn Airflow (task-centric) với Dagster (asset-centric).", "Airflow: task · Dagster: asset."),
        Q("TH", "Apache Airflow (C3)", "So với Dagster, Airflow có tư duy thiết kế nào?",
          ["Task-centric: tập trung vào tác vụ chạy/thành công/thất bại", "Asset-centric: tập trung vào tài sản dữ liệu", "Event-centric: chỉ chạy khi có sự kiện", "Model-centric: tập trung vào mô hình ML"],
          ["Đó là Dagster.", "Không phải mô tả của Airflow.", "Không phải mô tả của Airflow."],
          "Airflow task-centric; Dagster asset-centric.",
          "Đảo hai công cụ.", "Airflow = task."),
        Q("NB", "Apache Airflow (C3)", "Pipeline trong Airflow được biểu diễn dưới dạng gì?",
          ["DAG viết bằng Python", "File YAML khai báo test", "Template Jinja trong SQL", "Bảng fact trong kho"],
          ["Đó là dbt tests.", "Đó là dbt model.", "Không liên quan."],
          "Airflow: DAG (đồ thị có hướng không chu trình) viết bằng Python.",
          "Lẫn Airflow với dbt.", "Airflow = DAG Python."),
        Q("TH", "Apache Airflow (C3)", "Vì sao Airflow được coi là <b>tiêu chuẩn công nghiệp</b> cho orchestration?",
          ["Rất phổ biến, có hàng nghìn thư viện kết nối", "Là công cụ duy nhất hỗ trợ SQL", "Tự động sinh mô hình dữ liệu", "Không cần viết code"],
          ["Airflow không phải công cụ SQL.", "Airflow không sinh mô hình.", "Airflow cần viết DAG bằng Python."],
          "Airflow phổ biến, hệ sinh thái connector lớn, task-centric, DAG Python.",
          "Nghĩ Airflow là công cụ no-code.", "Airflow: phổ biến + connector."),
    ][v - 1])
    # 15 Storage mirroring
    T.append([
        Q("NB", "Storage Mirroring (C3)", "<b>Storage Mirroring</b> có chức năng gì?",
          ["Nhân bản dữ liệu tự động, liên tục ở tầng lưu trữ", "Che dấu cột chứa dữ liệu nhạy cảm", "Nén dữ liệu theo cột", "Lưu kết quả truy vấn để dùng lại"],
          ["Đó là CLM.", "Đó là định dạng columnar.", "Đó là caching."],
          "Storage mirroring là công nghệ cốt lõi của Zero-ETL (vd. Microsoft Fabric Mirroring → OneLake).",
          "Nghĩ mirroring là sao lưu thủ công định kỳ.", "Mirroring: tự động, liên tục, tầng lưu trữ."),
        Q("TH", "Storage Mirroring (C3)", "Trong Zero-ETL, công nghệ nào <b>nhân bản dữ liệu liên tục ở tầng hệ thống vật lý</b>?",
          ["Storage Mirroring", "Batch ETL hằng đêm", "Schema evolution", "Reverse ETL"],
          ["Batch ETL không liên tục và không phải Zero-ETL.", "Schema evolution xử lý thay đổi cấu trúc.", "Reverse ETL đẩy dữ liệu từ kho ra ứng dụng."],
          "Storage mirroring nhân bản ở tầng lưu trữ, là nền tảng của Zero-ETL.",
          "Lẫn Zero-ETL với ETL truyền thống.", "Zero-ETL ← storage mirroring."),
        Q("TH", "Storage Mirroring (C3)", "Storage Mirroring hoạt động ở tầng nào?",
          ["Tầng lưu trữ vật lý", "Tầng ứng dụng BI", "Tầng truy vấn SQL", "Tầng giao diện người dùng"],
          ["Không phải tầng BI.", "Không thực hiện qua truy vấn SQL.", "Không liên quan giao diện."],
          "Nhân bản tự động, liên tục ở tầng hệ thống vật lý.",
          "Nghĩ mirroring chạy qua câu lệnh SQL.", "Mirroring = tầng lưu trữ."),
        Q("VD", "Storage Mirroring (C3)", "Microsoft Fabric Mirroring nhân bản CSDL vào OneLake là ví dụ của công nghệ nào?",
          ["Storage Mirroring trong Zero-ETL", "Data Virtualization", "Change Data Capture qua batch", "Object Lock"],
          ["Virtualization truy cập tại nguồn, không nhân bản.", "Đây không phải batch.", "Object Lock chống xóa/sửa."],
          "Fabric Mirroring = storage mirroring, nhân bản tự động liên tục.",
          "Lẫn mirroring với virtualization.", "Nhân bản tự động → mirroring."),
    ][v - 1])
    return T


# ---------------------------------------------------------------- câu tiền xử lý dạng lý thuyết
def preprocess_concepts(v):
    T = {}
    T[19] = [
        Q("TH", "Info_A(D) (C4)", "Ý nghĩa của công thức Info<sub>A</sub>(D) = Σ<sub>j=1..v</sub> (|D<sub>j</sub>|/|D|) × Info(D<sub>j</sub>) là gì?",
          ["Entropy còn lại sau khi tách D theo thuộc tính A", "Entropy của toàn bộ tập D trước khi tách", "Độ lợi thông tin của thuộc tính A", "Tỉ lệ bản ghi rơi vào nhánh j"],
          ["Đó là Info(D).", "Gain(A) = Info(D) − Info_A(D).", "Đó chỉ là trọng số |Dj|/|D|."],
          "Info_A(D) là trung bình có trọng số entropy các tập con khi tách theo A.",
          "Lẫn Info_A(D) với Gain(A).", "Gain = Info(D) − Info_A(D); ID3 chọn Gain lớn nhất."),
        Q("TH", "Info_A(D) (C4)", "Trong công thức Info<sub>A</sub>(D) = Σ (|D<sub>j</sub>|/|D|) × Info(D<sub>j</sub>), đại lượng <b>|D<sub>j</sub>|/|D|</b> là gì?",
          ["Trọng số: tỉ lệ bản ghi rơi vào nhánh j", "Xác suất lớp j trong D", "Entropy của nhánh j", "Số giá trị khác nhau của A"],
          ["Xác suất lớp là pi trong Info(D).", "Entropy nhánh là Info(Dj).", "Đó là v."],
          "|Dj|/|D| là trọng số của nhánh j.",
          "Lẫn tỉ lệ nhánh với xác suất lớp.", "Nhánh: |Dj|/|D|; lớp: pi."),
        Q("VD", "Info_A(D) (C4)", "ID3 chọn thuộc tính tách dựa trên Info<sub>A</sub>(D) như thế nào?",
          ["Chọn A có Info_A(D) nhỏ nhất (Gain lớn nhất)", "Chọn A có Info_A(D) lớn nhất", "Chọn A có nhiều giá trị nhất", "Chọn A có Info(D) nhỏ nhất"],
          ["Info_A lớn nghĩa là nhánh còn hỗn loạn.", "Số giá trị không phải tiêu chí của ID3.", "Info(D) không phụ thuộc A."],
          "Gain(A) = Info(D) − Info_A(D) → Info_A nhỏ nhất ⇔ Gain lớn nhất.",
          "Chọn ngược chiều.", "ID3: Gain max."),
        Q("TH", "Info_A(D) (C4)", "Info<sub>A</sub>(D) liên hệ với Information Gain như thế nào?",
          ["Gain(A) = Info(D) − Info_A(D)", "Gain(A) = Info_A(D) − Info(D)", "Gain(A) = Info(D) × Info_A(D)", "Gain(A) = Info_A(D) / Info(D)"],
          ["Đảo dấu, Gain sẽ âm.", "Không phải phép nhân.", "Không phải phép chia (gần với gain ratio nhưng sai)."],
          "Gain là lượng entropy giảm đi sau khi tách theo A.",
          "Đảo thứ tự phép trừ.", "Gain = trước − sau."),
    ][v - 1]
    T[20] = [
        Q("NB", "Entropy (C4)", "Công thức Info(D) = −Σ<sub>i=1..m</sub> p<sub>i</sub> log<sub>2</sub>(p<sub>i</sub>) đo đại lượng gì?",
          ["Mức hỗn loạn (không chắc chắn) về nhãn lớp của D", "Độ lệch chuẩn của thuộc tính", "Độ tương quan giữa hai thuộc tính", "Tỉ lệ dữ liệu bị thiếu"],
          ["Đó là σ.", "Đó là hệ số tương quan.", "Không liên quan."],
          "Entropy: lượng thông tin trung bình (bit) để xác định lớp; 2 lớp: [0, 1].",
          "Lẫn entropy với các thống kê khác.", "Entropy = độ hỗn loạn nhãn lớp."),
        Q("TH", "Entropy (C4)", "Trong Info(D) = −Σ p<sub>i</sub> log<sub>2</sub>(p<sub>i</sub>), vì sao có <b>dấu trừ</b>?",
          ["Vì log2(pi) ≤ 0 nên dấu trừ làm kết quả không âm", "Để đổi đơn vị từ bit sang nat", "Để chuẩn hóa về [0, 1] với mọi số lớp", "Vì pi có thể âm"],
          ["Đổi đơn vị là đổi cơ số log.", "Với m > 2 lớp entropy có thể > 1.", "Xác suất không âm."],
          "pi ∈ (0, 1] ⇒ log2 pi ≤ 0.",
          "Không hiểu vai trò dấu trừ.", "Dấu trừ → entropy ≥ 0."),
        Q("TH", "Entropy (C4)", "Với 2 lớp, Info(D) bằng <b>1</b> khi nào?",
          ["Hai lớp chia đều 50/50", "Tất cả bản ghi thuộc một lớp", "Một lớp chiếm 90%", "Không bao giờ bằng 1"],
          ["Khi đó entropy = 0.", "Entropy ≈ 0,469.", "Đạt 1 khi 50/50."],
          "Hai lớp: entropy ∈ [0, 1]; = 0 khi thuần, = 1 khi 50/50.",
          "Đảo hai trường hợp cực.", "Thuần → 0; cân bằng → 1."),
        Q("NB", "Entropy (C4)", "Đơn vị đo của Info(D) = −Σ p<sub>i</sub> log<sub>2</sub>(p<sub>i</sub>) là gì?",
          ["Bit", "Byte", "Nat", "Phần trăm"],
          ["Byte không dùng cho entropy.", "Nat dùng khi log cơ số e.", "Entropy không đo bằng %."],
          "log cơ số 2 → đơn vị bit.",
          "Lẫn bit/nat.", "log2 → bit; ln → nat."),
    ][v - 1]
    T[21] = [
        Q("NB", "Z-score (C4)", "Công thức <b>Z-Score Normalization</b> là:",
          ["v′ = (v − μ) / σ", "v′ = (v − min) / (max − min)", "v′ = v / 10^j", "v′ = (v − μ) / (max − min)"],
          ["Đó là Min-Max.", "Đó là Decimal scaling.", "Trộn sai hai công thức."],
          "Sau z-score: μ = 0, σ = 1; v′ = số độ lệch chuẩn cách trung bình.",
          "Lẫn ba phương pháp chuẩn hóa.", "Z: μ, σ · Min-Max: min, max · Decimal: 10^j."),
        Q("VD", "Z-score (C4)", "Thuộc tính có μ = 50, σ = 10. Giá trị <b>70</b> sau Z-Score Normalization bằng bao nhiêu?",
          ["2", "0,2", "20", "1,4"],
          ["Chia cho 100 thay vì σ.", "Quên chia cho σ.", "Lấy 70/50."],
          "z = (70 − 50)/10 = 2: cao hơn trung bình 2 độ lệch chuẩn.",
          "Quên chia σ hoặc chia nhầm.", "z = (v − μ)/σ."),
        Q("TH", "Z-score (C4)", "Vì sao Z-Score phù hợp hơn Min-Max khi dữ liệu có <b>outlier</b>?",
          ["Một giá trị cực lớn không dồn các giá trị khác về sát 0", "Z-score luôn cho kết quả trong [0, 1]", "Z-score loại bỏ hẳn outlier", "Z-score không cần tính trung bình"],
          ["Z-score không giới hạn trong [0, 1].", "Z-score không xóa dữ liệu.", "Z-score cần μ và σ."],
          "Min-Max bị max cực lớn kéo méo; z-score dùng μ, σ nên bền hơn.",
          "Nghĩ z-score cho kết quả trong [0, 1].", "Outlier → z-score; ngưỡng |Z| > 3."),
        Q("TH", "Z-score (C4)", "Dùng Z-score để phát hiện outlier, ngưỡng thường dùng là:",
          ["|Z| > 3", "|Z| > 0,5", "Z < 0", "Z > 1"],
          ["Quá nhỏ, gần như mọi điểm đều bị coi là outlier.", "Z âm chỉ là dưới trung bình.", "Z > 1 rất phổ biến."],
          "|Z| > 3 là ngưỡng thông dụng.",
          "Nghĩ z âm là bất thường.", "|Z| > 3 → outlier."),
    ][v - 1]
    T[22] = [
        Q("NB", "Decimal scaling (C4)", "<b>Decimal Scaling</b> chuẩn hóa dữ liệu bằng cách nào?",
          ["v′ = v/10^j (j nhỏ nhất để mọi |v′| < 1)", "v′ = (v − μ)/σ với μ, σ của thuộc tính", "v′ = v/max với max là giá trị lớn nhất", "v′ = log10(v) rồi làm tròn 1 chữ số"],
          ["Đó là z-score.", "Không phải decimal scaling.", "Đó là log transform."],
          "Dời dấu thập phân sang trái j chữ số.",
          "Lẫn với các phương pháp khác.", "Decimal: chia 10^j."),
        Q("VD", "Decimal scaling (C4)", "Giá trị tuyệt đối lớn nhất của thuộc tính là <b>986</b>. Theo Decimal Scaling, 986 trở thành:",
          ["0,986", "9,86", "0,0986", "1"],
          ["j = 2 chưa đủ vì |v′| phải < 1.", "j = 4 thừa, j phải nhỏ nhất.", "Kết quả phải < 1."],
          "10^j > 986 ⇒ j = 3 ⇒ 0,986.",
          "Chọn j chưa đủ hoặc thừa.", "j nhỏ nhất để |v′| < 1."),
        Q("VD", "Decimal scaling (C4)", "Số dư từ −750.000 đến 3.500.000. Theo Decimal Scaling, j và giá trị chuẩn hóa của 3.500.000 là:",
          ["j = 7; 0,35", "j = 6; 3,5", "j = 7; 3,5", "j = 8; 0,035"],
          ["|v′| = 3,5 ≥ 1, chưa đạt.", "Tính sai phép chia.", "j phải nhỏ nhất."],
          "max|v| = 3.500.000 ⇒ j = 7 ⇒ 0,35; −750.000 ⇒ −0,075.",
          "Lấy j bằng số chữ số trừ 1.", "10^j > max|v|."),
        Q("VD", "Decimal scaling (C4)", "Giá trị lớn nhất là <b>45.000</b>. Decimal Scaling chọn j bằng bao nhiêu?",
          ["5", "4", "6", "3"],
          ["45.000/10^4 = 4,5 ≥ 1.", "j = 6 thừa, j phải nhỏ nhất.", "45.000/10^3 = 45."],
          "45.000/10^5 = 0,45 < 1 ⇒ j = 5.",
          "Lấy số chữ số − 1.", "j nhỏ nhất để |v′| < 1."),
    ][v - 1]
    T[23] = [
        Q("NB", "Equal-frequency (C4)", "<b>Equal-frequency Binning</b> chia dữ liệu theo nguyên tắc nào?",
          ["Mỗi bin chứa số bản ghi bằng nhau", "Mỗi bin có độ rộng khoảng bằng nhau", "Mỗi bin có trung bình bằng nhau", "Số bin bằng số giá trị khác nhau"],
          ["Đó là equal-width.", "Không phải nguyên tắc chia bin.", "Không phải binning."],
          "Equal-frequency: số bản ghi mỗi bin bằng nhau, hợp dữ liệu lệch.",
          "Lẫn equal-frequency với equal-width.", "Frequency = số lượng; width = độ rộng."),
        Q("VD", "Equal-frequency (C4)", "Chia 9 hạn mức 10, 12, 15, 18, 20, 22, 25, 40, 70 thành 3 nhóm bằng <b>Equal-frequency</b>. Nhóm cao nhất là:",
          ["{25, 40, 70}", "{70}", "{40, 70}", "{22, 25, 40, 70}"],
          ["Đó là kết quả equal-width (độ rộng 20).", "Không đủ 3 phần tử.", "Thừa phần tử."],
          "9 giá trị / 3 nhóm = 3 giá trị mỗi nhóm: {10,12,15}, {18,20,22}, {25,40,70}.",
          "Áp nhầm equal-width.", "Equal-frequency: chia đều số lượng."),
        Q("VD", "Equal-frequency (C4)", "Chia 12 giá trị 5, 7, 8, 10, 13, 15, 20, 22, 30, 35, 50, 90 thành 4 nhóm bằng <b>Equal-frequency</b>. Nhóm thứ hai là:",
          ["{10, 13, 15}", "{7, 8, 10}", "{13, 15, 20}", "{10, 13, 15, 20}"],
          ["Lệch một vị trí.", "Lệch một vị trí.", "Nhóm phải có 3 phần tử."],
          "12/4 = 3 phần tử mỗi nhóm: {5,7,8}, {10,13,15}, {20,22,30}, {35,50,90}.",
          "Đếm lệch vị trí.", "Số phần tử mỗi nhóm = n/k."),
        Q("TH", "Equal-frequency (C4)", "Với dữ liệu lệch (skewed), vì sao Equal-frequency thường tốt hơn Equal-width?",
          ["Equal-width dồn phần lớn bản ghi vào một bin", "Equal-frequency luôn có độ rộng bin bằng nhau", "Equal-width không xử lý được số âm", "Equal-frequency loại bỏ outlier"],
          ["Đó là equal-width.", "Equal-width xử lý được số âm.", "Binning không loại outlier."],
          "Ví dụ slide: equal-width cho nhóm 1 có 7 khách, nhóm 2 và 3 mỗi nhóm 1.",
          "Đảo đặc điểm hai phương pháp.", "Skewed → equal-frequency."),
    ][v - 1]
    T[24] = [
        Q("NB", "Discretization (C4)", "<b>Discretization</b> (rời rạc hóa) là gì?",
          ["Biến thuộc tính liên tục thành các khoảng/nhãn rời rạc", "Đưa giá trị về [0, 1]", "Giảm số chiều bằng tổ hợp tuyến tính", "Điền giá trị thiếu bằng trung bình"],
          ["Đó là chuẩn hóa Min-Max.", "Đó là PCA.", "Đó là xử lý missing value."],
          "Ví dụ thu nhập → Thấp/Trung bình/Cao; kỹ thuật equal-width, equal-frequency.",
          "Lẫn rời rạc hóa với chuẩn hóa.", "Discretization: liên tục → rời rạc."),
        Q("TH", "Discretization (C4)", "Kỹ thuật nào thường dùng để thực hiện <b>Discretization</b>?",
          ["Equal-width và Equal-frequency Binning", "Z-score và Min-Max", "PCA và SVD", "Apriori và FP-Growth"],
          ["Đó là chuẩn hóa.", "Đó là giảm chiều.", "Đó là khai phá luật kết hợp."],
          "Rời rạc hóa dùng binning.",
          "Lẫn nhóm kỹ thuật.", "Discretization ← binning."),
        Q("TH", "Discretization (C4)", "Rời rạc hóa thường đi kèm với việc xây dựng cấu trúc nào?",
          ["Phân cấp khái niệm (concept hierarchy)", "Cây FP-tree", "Ma trận hiệp phương sai", "Bảng cầu"],
          ["FP-tree thuộc khai phá luật.", "Hiệp phương sai thuộc PCA.", "Bảng cầu thuộc mô hình chiều."],
          "Concept hierarchy: ngày < tháng < quý < năm.",
          "Không liên hệ được discretization với hierarchy.", "Discretization + concept hierarchy."),
        Q("TH", "Discretization (C4)", "Vì sao ID3, Apriori cần dữ liệu đã qua Discretization?",
          ["Các thuật toán này làm việc với giá trị rời rạc", "Để dữ liệu có phân phối chuẩn", "Để giảm số dòng của bảng", "Để mã hóa dữ liệu nhạy cảm"],
          ["Rời rạc hóa không tạo phân phối chuẩn.", "Rời rạc hóa giảm số giá trị khác nhau, không giảm số dòng.", "Không phải mục đích bảo mật."],
          "Mục tiêu: giảm số giá trị khác nhau, hỗ trợ thuật toán chỉ nhận giá trị rời rạc.",
          "Nhầm giảm giá trị với giảm dòng.", "ID3/Apriori cần dữ liệu rời rạc."),
    ][v - 1]
    T[25] = [
        Q("NB", "PCA (C4)", "Phép biến đổi <b>PCA</b> dùng để làm gì?",
          ["Giảm số chiều, giữ lại tối đa phương sai", "Chuẩn hóa dữ liệu về [0, 1]", "Chọn giữ nguyên một số cột gốc", "Rời rạc hóa thuộc tính liên tục"],
          ["Đó là Min-Max.", "Đó là feature selection.", "Đó là discretization."],
          "PCA: biến đổi tuyến tính tạo cột mới (thành phần chính) giữ tối đa phương sai.",
          "Lẫn PCA với feature selection.", "PCA tạo cột mới; selection giữ cột cũ."),
        Q("TH", "PCA (C4)", "Khác biệt giữa <b>PCA</b> và feature selection là:",
          ["PCA tạo cột mới từ tổ hợp tuyến tính; feature selection giữ cột gốc", "PCA giữ cột gốc; feature selection tạo cột tổ hợp mới", "Cả hai đều tăng số chiều để mô hình học tốt hơn", "PCA dùng cho thuộc tính phân loại; selection cho thuộc tính số"],
          ["Đảo ngược.", "Cả hai giảm chiều.", "PCA dùng cho dữ liệu số."],
          "PC1 = 0,6x1 + 0,5x2 + … là cột mới.",
          "Đảo hai khái niệm.", "PCA = cột mới."),
        Q("TH", "PCA (C4)", "Các thành phần chính trong <b>PCA</b> là:",
          ["Vector riêng ứng trị riêng lớn nhất của ma trận hiệp phương sai", "Các cột gốc có phương sai nhỏ nhất của dữ liệu", "Vector trung bình của từng cột sau chuẩn hóa", "Các cột gốc có tương quan cao nhất với nhãn"],
          ["PCA giữ phương sai lớn.", "Trung bình chỉ dùng để căn giữa dữ liệu.", "Không liên quan."],
          "Thành phần chính = eigenvector của ma trận hiệp phương sai, sắp theo eigenvalue giảm dần.",
          "Nghĩ PCA chọn cột gốc.", "PC ← eigenvector hiệp phương sai."),
        Q("TH", "PCA (C4)", "Tiêu chí giữ lại thông tin của <b>PCA</b> là:",
          ["Tối đa hóa phương sai được giữ lại", "Tối thiểu hóa số dòng", "Tối đa hóa entropy nhãn lớp", "Tối đa hóa support"],
          ["PCA không giảm số dòng.", "Entropy thuộc cây quyết định.", "Support thuộc luật kết hợp."],
          "PCA là phép biến đổi tuyến tính giữ lại tối đa phương sai.",
          "Lẫn tiêu chí của các thuật toán khác.", "PCA ↔ phương sai."),
    ][v - 1]
    return T


# ---------------------------------------------------------------- câu tính toán
def entropy(*c):
    n = sum(c)
    return -sum(x / n * math.log2(x / n) for x in c if x)


def q16(v):
    g, b, lg, lb = {1: (6, 4, "Good", "Bad"), 2: (8, 2, "Yes", "No"), 3: (5, 5, "Good", "Bad"), 4: (9, 3, "Mua", "Không mua")}[v]
    n = g + b; p, q = g / n, b / n
    H = entropy(g, b)
    o, x = pick(H, [
        (-(p * math.log(p) + q * math.log(q)), "Dùng ln thay cho log2 (ra đơn vị nat)."),
        (1 - p * p - q * q, "Đó là chỉ số Gini, không phải entropy."),
        (-(math.log2(p) + math.log2(q)), "Quên nhân với pi."),
        (-(p * math.log10(p) + q * math.log10(q)), "Dùng log10."),
    ], lambda z: num(z, 3))
    stem = {1: f"Dataset D có 2 lớp: <b>{g} {lg}</b> và <b>{b} {lb}</b>. Entropy Info(D) bằng bao nhiêu?",
            2: f"Tập huấn luyện có <b>{g} mẫu {lg}</b> và <b>{b} mẫu {lb}</b>. Độ hỗn loạn (entropy) của tập này là:",
            3: f"Tập D gồm <b>{g} khách {lg}</b> và <b>{b} khách {lb}</b>. Info(D) bằng:",
            4: f"Có <b>{g} bản ghi lớp {lg}</b> và <b>{b} bản ghi lớp {lb}</b>. Tính Info(D) (làm tròn 3 chữ số)."}[v]
    return Q("VD", "Entropy (C4)", stem, o, x,
             f"Info(D) = −{g}/{n}·log2({g}/{n}) − {b}/{n}·log2({b}/{n}) ≈ {num(H, 3)}.",
             "Dùng sai cơ số log hoặc nhầm với Gini.", "Entropy dùng log2; 2 lớp 50/50 → 1.")


def q17(v):
    mn, mx, val, u = {1: (5, 10, 8, "triệu"), 2: (20, 70, 45, "triệu"), 3: (2, 12, 9.5, "điểm"), 4: (3, 15, 6, "triệu")}[v]
    r = (val - mn) / (mx - mn)
    o, x = pick(r, [
        (val / mx, "Lấy v/max, quên trừ min."),
        ((val - mn) / mx, "Chia cho max thay vì (max − min)."),
        ((mx - val) / (mx - mn), "Tính khoảng cách tới max (đảo chiều)."),
        ((val - mn) / val, "Chia cho chính v."),
    ], lambda z: num(z, 3))
    stem = {1: f"Thu nhập thấp nhất <b>{mn} {u}</b>, cao nhất <b>{mx} {u}</b>. Thu nhập <b>{num(val)} {u}</b> sau Min-Max về [0, 1] bằng:",
            2: f"Chi tiêu dao động từ <b>{mn}</b> đến <b>{mx} {u}</b>. Giá trị <b>{num(val)} {u}</b> sau Min-Max Normalization về [0, 1] là:",
            3: f"Điểm tín dụng trong khoảng <b>{mn}–{mx}</b>. Điểm <b>{num(val)}</b> chuẩn hóa Min-Max về [0, 1] bằng:",
            4: f"Doanh thu nhỏ nhất <b>{mn} {u}</b>, lớn nhất <b>{mx} {u}</b>. Doanh thu <b>{num(val)} {u}</b> sau Min-Max về [0, 1] là:"}[v]
    return Q("VD", "Min-Max (C4)", stem, o, x, f"v′ = ({num(val)} − {mn}) / ({mx} − {mn}) = {num(r, 3)}.",
             "Quên trừ min hoặc chia nhầm mẫu.", "v′ = (v − min)/(max − min).")


def q18(v):
    lo, hi, k = {1: (100, 700, 3), 2: (200, 1000, 4), 3: (50, 500, 3), 4: (100, 600, 5)}[v]
    w = (hi - lo) / k
    f = lambda a: f"{num(a[0], 2)} – {num(a[1], 2)}"
    o, x = pick((lo, lo + w), [
        ((lo, lo + (hi - lo) / (k - 1)), f"Chia cho k − 1 = {k - 1} thay vì k."),
        ((0, hi / k), "Lấy max/k, bỏ qua giá trị nhỏ nhất."),
        ((lo, lo + hi / k), "Tính độ rộng = max/k thay vì (max − min)/k."),
        ((lo + w, lo + 2 * w), "Đó là nhóm thứ hai."),
    ], f)
    unit = {1: "triệu", 2: "triệu", 3: "triệu", 4: "nghìn"}[v]
    stem = {1: f"Ngân hàng chia khách hàng thành <b>{k} nhóm</b> theo Equal-width Binning; hạn mức từ {lo} đến {hi} {unit}. Nhóm thấp nhất có khoảng:",
            2: f"Hạn mức tín dụng từ <b>{lo}</b> đến <b>{hi} {unit}</b>, chia <b>{k} nhóm</b> bằng Equal-width. Khoảng của nhóm thấp nhất là:",
            3: f"Số dư tài khoản từ <b>{lo}</b> đến <b>{hi} {unit}</b>, chia <b>{k} nhóm</b> theo Equal-width Binning. Nhóm thấp nhất là:",
            4: f"Giá trị đơn hàng từ <b>{lo}</b> đến <b>{hi} {unit}</b>, chia <b>{k} nhóm</b> bằng Equal-width. Nhóm thấp nhất có khoảng:"}[v]
    return Q("VD", "Equal-width (C4)", stem, [s + f" {unit}" for s in o], x,
             f"Width = ({hi} − {lo})/{k} = {num(w)} ⇒ nhóm thấp nhất {num(lo)} – {num(lo + w)}.",
             "Chia cho k − 1 hoặc quên trừ min.", "Width = (max − min)/k.")


def q26(v):
    data, k, day, what = {1: ([75, 78, 76, 80, 82, 81], 3, 4, "giá dầu (USD)"), 2: ([75, 78, 76, 80, 82, 81], 3, 5, "giá dầu (USD)"),
                          3: ([60, 62, 61, 65, 67, 66], 3, 5, "giá vàng (triệu/lượng)"), 4: ([10, 12, 14, 16, 18, 20], 4, 6, "lượt truy cập (nghìn)")}[v]
    m = lambda a, b: sum(data[a:b]) / (b - a)
    sma = m(day - k, day)
    o, x = pick(sma, [
        (m(day - k - 1, day - 1), f"Dùng {k} ngày trước ngày {day} (hiểu thành dự báo), không tính ngày {day}."),
        (m(0, day), "Lấy trung bình mọi ngày tới ngày đang xét, bỏ qua kích thước cửa sổ."),
        (m(day - k + 1, min(day + 1, len(data))) if day < len(data) else m(day - k - 2, day - 2), "Lệch cửa sổ một ngày."),
        (sum(data[day - k:day]) / (k + 1), "Chia cho k + 1."),
    ], lambda z: num(z, 2))
    series = "; ".join(f"N{i + 1}: {x_}" for i, x_ in enumerate(data))
    stem = f"Theo dõi {what} 6 ngày liên tiếp ({series}). Với cửa sổ <b>k = {k}</b>, <b>SMA ngày {day}</b> bằng:"
    return Q("VD", "SMA (C4)", stem, o, x,
             f"SMA tại ngày n là trung bình k giá trị gần nhất tính cả ngày n: ({' + '.join(map(str, data[day - k:day]))})/{k} = {num(sma, 2)}.",
             "Không tính ngày đang xét hoặc lệch cửa sổ.", "Cửa sổ SMA kết thúc tại chính ngày n.")


def q27(v):
    n = {1: 6, 2: 8, 3: 5, 4: 10}[v]
    c = n * (n - 1) // 2
    o, x = pick(c, [(n * (n - 1), "Tính chỉnh hợp (có thứ tự) thay vì tổ hợp."), (n * n, "Lấy n²."), (2 ** n - n - 1, "Đếm mọi tập con ≥ 2 phần tử, không chỉ cặp."), (2 * n, "Lấy 2n.")], str)
    stem = {1: f"Có <b>{n}</b> item đơn lẻ phổ biến. Số itemset 2 phần tử Apriori sinh ra để kiểm tra là:",
            2: f"Sau lần quét đầu, Apriori tìm được <b>{n}</b> item phổ biến. Số ứng viên C<sub>2</sub> là:",
            3: f"Với <b>{n}</b> item đơn phổ biến, Apriori phải đếm support của bao nhiêu cặp ứng viên?",
            4: f"Có <b>{n}</b> item phổ biến kích thước 1. Số itemset 2 phần tử được sinh ra là:"}[v]
    return Q("TH", "Apriori ứng viên (C5)", stem, o, x, f"C({n},2) = {n}×{n - 1}/2 = {c}.",
             "Nhầm tổ hợp với chỉnh hợp.", "Ứng viên cỡ 2 = n(n−1)/2.")


DB = {
    1: (["abc", "abcde", "b", "cde", "c", "bcd", "cde", "ce"], "c", "de", 4, "bcd"),
    2: (["abd", "acde", "bd", "bce", "abde", "de", "ade", "ac"], "a", "de", 3, "abd"),
    3: (["bc", "abce", "be", "bcd", "ab", "bce", "cd", "abc", "bde", "bce"], "b", "ce", 4, "abc"),
    4: (["ace", "abc", "cd", "acde", "ae", "ace", "bce", "ac"], "c", "ae", 3, "abc"),
}


def sup(db, it):
    return Fr(sum(1 for t in db if set(it) <= set(t)), len(db))


def q28(v):
    db, X, Y, ms, it = DB[v]
    tb = table(["TID", "Itemset"], [(i + 1, setstr(t)) for i, t in enumerate(db)])
    XY = "".join(sorted(set(X + Y)))
    sxy, sx, sy = sup(db, XY), sup(db, X), sup(db, Y)
    L = f"{setstr(X)} → {setstr(Y)}"
    ff = lambda z: f"{fr(z)} ≈ {num(z)}" if Fr(z).denominator != 1 else fr(z)
    f2 = lambda z: num(z, 4)
    out = []
    lev = sxy - sx * sy
    o, x = pick(lev, [(sxy - sx, "Lấy Sup(X∪Y) − Sup(X)."), (sxy / (sx * sy), "Đó là Lift (chia thay vì trừ)."), (sxy - sy, "Lấy Sup(X∪Y) − Sup(Y)."), (sx * sy, "Chỉ tính phần Sup(X)×Sup(Y).")], f2)
    out.append(Q("VD", "Leverage (C5)", f"Với L: <b>{L}</b>, Leverage(L) bằng bao nhiêu? Biết Leverage(X→Y) = Sup(X∪Y) − Sup(X)×Sup(Y) và CSDL giao dịch:{tb}", o, x,
                 f"Sup({setstr(XY)}) = {fr(sxy)}, Sup({setstr(X)}) = {fr(sx)}, Sup({setstr(Y)}) = {fr(sy)} ⇒ Leverage = {fr(sxy)} − {fr(sx)}×{fr(sy)} = {fr(lev)} ≈ {num(lev)}.",
                 "Lẫn công thức Leverage với Lift.", "Leverage = hiệu; Lift = thương. Leverage > 0 ⇔ Lift > 1."))
    o, x = pick(sxy, [(sx, "Đó là Sup(X), chỉ vế trái."), (sxy / sx, "Đó là Confidence."), (sy, "Đó là Sup(Y), chỉ vế phải."), (sx * sy, "Lấy Sup(X)×Sup(Y) – giá trị kỳ vọng nếu độc lập."), (sxy / sy, "Đó là Sup(X∪Y)/Sup(Y).")], f2)
    out.append(Q("TH", "Support (C5)", f"Với luật L: <b>{L}</b>, Sup(L) bằng bao nhiêu? CSDL giao dịch:{tb}", o, x,
                 f"Sup(L) = Sup({setstr(XY)}) = {fr(sxy)}.", "Lấy support của một vế thay vì cả luật.", "Sup(X→Y) = Sup(X∪Y)."))
    conf = sxy / sx
    o, x = pick(conf, [(sxy / sy, "Chia cho Sup(Y) (đó là confidence của luật ngược)."), (sxy, "Đó là Support."), (conf / sy, "Đó là Lift.")], f2)
    out.append(Q("VD", "Confidence (C5)", f"Confidence của luật L: <b>{L}</b> bằng bao nhiêu? CSDL giao dịch:{tb}", o, x,
                 f"Conf = Sup(X∪Y)/Sup(X) = {fr(sxy)} / {fr(sx)} = {fr(conf)} ≈ {num(conf)}.", "Chia nhầm cho Sup(Y).", "Conf chia cho vế TRÁI."))
    lift = conf / sy
    o, x = pick(lift, [(conf / sx, "Chia cho Sup(X) thay vì Sup(Y)."), (conf, "Đó là Confidence."), (lev, "Đó là Leverage."), (sxy / sy, "Thiếu bước chia cho Sup(X).")], f2)
    out.append(Q("VD", "Lift (C5)", f"Lift của luật L: <b>{L}</b> bằng bao nhiêu? CSDL giao dịch:{tb}", o, x,
                 f"Lift = Conf/Sup(Y) = {fr(conf)} / {fr(sy)} = {fr(lift)} ≈ {num(lift)} ({'tương quan dương' if lift > 1 else 'tương quan âm' if lift < 1 else 'độc lập'}).",
                 "Chia nhầm cho Sup(X).", "Lift = Conf/Sup(Y); > 1 dương, < 1 âm, = 1 độc lập."))
    cnt = Counter(i for t in db for i in t)
    keep = sorted([i for i in cnt if cnt[i] >= ms], key=lambda i: (-cnt[i], i))
    drop = sorted(i for i in cnt if cnt[i] < ms)
    asc = sorted(keep, key=lambda i: (cnt[i], i))
    gt = [i for i in keep if cnt[i] > ms]
    cands = [(asc, "Sắp tăng dần thay vì giảm dần."), (keep + drop, "Không loại item dưới minsup."), (sorted(keep), "Chỉ sắp theo chữ cái, bỏ qua tần suất."), (gt, "Loại cả item có count bằng minsup (phải ≥)."), (list(reversed(keep)), "Đảo ngược thứ tự."),
             ([keep[1], keep[0]] + keep[2:], f"Đặt {keep[1]} trước {keep[0]} dù count({keep[1]}) = {cnt[keep[1]]} < count({keep[0]}) = {cnt[keep[0]]}." if cnt[keep[1]] < cnt[keep[0]] else "Xếp sai thứ tự khi count bằng nhau."),
             (keep[:-1], f"Bỏ sót {keep[-1]} (count = {cnt[keep[-1]]} vẫn ≥ minsup).")]
    o, x = pick(keep, cands, lambda s: ", ".join(s))
    out.append(Q("VDC", "FP-Growth sắp xếp (C5)", f"FP-Growth với <b>minsup = {ms}</b> (số lần): chuỗi item cố định (sau lọc và sắp xếp) dùng dựng FP-tree là gì? CSDL giao dịch:{tb}", o, x,
                 f"Đếm: {', '.join(f'{i}={cnt[i]}' for i in sorted(cnt))}. Loại {', '.join(drop) or '(không)'}; sắp giảm dần theo count, bằng nhau xếp theo chữ cái.",
                 "Quên loại item dưới minsup hoặc sắp sai chiều.", "Lọc ≥ minsup, sắp giảm dần tần suất."))
    c = sum(1 for t in db if set(it) <= set(t))
    N = len(db)
    cands = []
    for pair in (it[:2], it[1:], it[0] + it[2]):
        cands.append((sum(1 for t in db if set(pair) <= set(t)), f"Chỉ đếm cặp {setstr(pair)}."))
    cands.append((sum(1 for t in db if len(set(it) & set(t)) >= 2), "Đếm cả giao dịch chỉ chứa 2 trong 3 item."))
    cands.append((sum(1 for t in db if set(it) & set(t)), "Đếm giao dịch chứa ít nhất một item."))
    cands.append((c + 1, "Đếm thừa một giao dịch chứa gần đủ itemset."))
    o, x = pick(c, cands, lambda k: f"{k}/{N}")
    out.append(Q("TH", "Support 3-itemset (C5)", f"Độ hỗ trợ của itemset <b>{setstr(it)}</b> là bao nhiêu? CSDL giao dịch:{tb}", o, x,
                 f"Chỉ giao dịch chứa đủ cả {', '.join(it)}: {c}/{len(db)}.", "Đếm giao dịch chứa một phần itemset.", "Support: giao dịch chứa ĐỦ mọi item."))
    return out


CPB = {
    1: ([("X", [("Y", 4)]), ("Y", [("X", 4), ("T", 3)]), ("Z", [("X", 3), ("Y", 4), ("T", 3)]), ("T", [("Y", 4), ("Z", 3)])], 4, "X"),
    2: ([("P", [("Q", 5), ("R", 2)]), ("Q", [("P", 5), ("R", 4), ("S", 3)]), ("R", [("P", 2), ("Q", 4), ("S", 5)]), ("S", [("Q", 3), ("R", 5)])], 4, "P"),
    3: ([("A", [("B", 3), ("C", 2)]), ("B", [("A", 3), ("C", 4), ("D", 2)]), ("C", [("A", 2), ("B", 4), ("D", 3)]), ("D", [("B", 2), ("C", 3)])], 3, "A"),
    4: ([("M", [("N", 6), ("K", 4)]), ("N", [("M", 6), ("K", 5), ("L", 3)]), ("K", [("M", 4), ("N", 5), ("L", 5)]), ("L", [("N", 3), ("K", 5)])], 5, "M"),
}


def q29(v):
    rows, ms, ex = CPB[v]
    tb = table(["Item", "Elements's occurrences"], [(i, "{" + ", ".join(f"{a}:{c}" for a, c in el) + "}") for i, el in rows])

    def sets(th, strict=False):
        out = []
        for i, el in rows:
            for a, c in el:
                if (c > th if strict else c >= th):
                    s = tuple(sorted((i, a)))
                    if s not in out: out.append(s)
        return out
    good = [s for s in sets(ms) if ex not in s]
    fmt = lambda L: ", ".join("{" + ", ".join(s) + "}" for s in sorted(L)) or "Không có tập nào"
    o, x = pick(good, [
        (sets(ms), f"Không loại tập chứa {ex}."),
        ([s for s in sets(ms - 1) if ex not in s], f"Giữ cả phần tử có count = {ms - 1} < minsup."),
        ([s for s in sets(ms, True) if ex not in s], "Dùng điều kiện > minsup thay vì ≥."),
        ([s for s in sets(ms) if ex in s], f"Chọn ngược: các tập chứa {ex}."),
    ], fmt)
    return Q("VDC", "Conditional Pattern Base (C5)", f"Cho một phần bảng Conditional Pattern Base:{tb}Với FP-Growth, <b>minsup = {ms}</b>, các tập phổ biến 2 item <b>không chứa {ex}</b> là:", o, x,
             f"Mỗi dòng giữ phần tử có count ≥ {ms} rồi ghép với item của dòng; bỏ tập chứa {ex} ⇒ {fmt(good)}.",
             "Dùng > thay vì ≥, hoặc quên loại item theo đề.", "Count ≥ minsup mới phổ biến.")


def q30(v):
    stem = {1: "Thông thường, ngưỡng <b>minsup</b> được chọn là bao nhiêu?", 2: "Cặp ngưỡng thường dùng cho (minsup, minconf) là:",
            3: "\"Ngưỡng minsup thường được đặt khoảng 50%.\" Nhận định nào đúng?", 4: "Ngưỡng minsup phổ biến thường ở mức:"}[v]
    o = {1: ["0,01 (1%)", "0,5 (50%)", "0,8 (80%)", "0,1 (10%)"], 2: ["(0,01; 0,8)", "(0,8; 0,01)", "(0,5; 0,5)", "(0,1; 0,1)"],
         3: ["Sai, minsup thường khoảng 1%", "Đúng", "Sai, minsup thường khoảng 80%", "Sai, minsup thường khoảng 30%"], 4: ["1%", "80%", "50%", "25%"]}[v]
    x = {1: ["Quá cao, gần như không có tập phổ biến.", "Đó là minconf.", "Không phải giá trị thông dụng trong tài liệu."],
         2: ["Đảo minsup và minconf.", "Không phải giá trị thông dụng.", "Không phải giá trị thông dụng."],
         3: ["50% là quá cao.", "80% là minconf.", "Không phải giá trị thông dụng."],
         4: ["Đó là minconf.", "Quá cao.", "Không phải giá trị thông dụng."]}[v]
    return Q("NB", "Ngưỡng minsup (C5)", stem, o, x, "Slide Chương 5: minsup thường 0,01 (1%), minconf thường 0,8.", "Lẫn minsup với minconf.", "minsup 1% · minconf 80%.")


PR = {
    1: ([(1, 2), (2, 5), (3, 1), (3, 2), (3, 4), (3, 5), (4, 3), (4, 5), (5, 4)], (2, 1)),
    2: ([(1, 2), (1, 3), (2, 3), (3, 1), (4, 1), (4, 3), (5, 4)], (3, 1)),
    3: ([(1, 2), (1, 4), (2, 3), (3, 1), (3, 5), (4, 3), (5, 1), (5, 2), (5, 4)], (3, 4)),
    4: ([(1, 2), (1, 3), (1, 4), (2, 4), (3, 1), (3, 4), (4, 1), (5, 4)], (4, 1)),
}


def q31(v):
    edges, pages = PR[v]
    out = {n: [b for a, b in edges if a == n] for n in range(1, 6)}
    g = "; ".join(f"{n} → {', '.join(map(str, out[n]))}" for n in range(1, 6))
    res = []
    for pg in pages:
        ins = [a for a, b in edges if b == pg]
        s = sum(1 / len(out[a]) for a in ins)
        pr = 0.15 + 0.85 * s
        o, x = pick(pr, [(0.85 * s, "Quên cộng (1 − d) = 0,15."), (0.15 + 0.85 * len(ins), "Không chia PR cho số liên kết ra C(T)."), (0.15 / 5 + 0.85 * s, "Dùng (1 − d)/N của dạng chuẩn hóa, trong khi tài liệu dùng (1 − d)."), (0.15 + 0.5 * s, "Dùng d = 0,5.")], lambda z: num(z, 4))
        terms = " + ".join(f"1/{len(out[a])}" for a in ins)
        res.append(Q("VDC", f"PageRank trang {pg} (C6)",
                     f"PageRank của <b>trang {pg}</b> sau vòng lặp đầu tiên là bao nhiêu? PageRank mọi trang khởi tạo bằng 1, d = 0,85. Đồ thị liên kết (trang → các trang được trỏ tới): {g}.",
                     o, x, f"Trang {pg} nhận liên kết từ {', '.join(map(str, ins))}: PR = 0,15 + 0,85×({terms}) = {num(pr, 4)}.",
                     "Quên chia cho số liên kết ra hoặc quên (1 − d).", "PR(A) = (1 − d) + d·Σ PR(T)/C(T)."))
    return res


CPTD = {
    1: (["ABCDF", "DCBE", "EADCB", "EGADBC"], "DC"),
    2: (["ABCD", "BCED", "ACBE", "CBDF", "BACF"], "BC"),
    3: (["ABDC", "BDAE", "DBCA", "ADBE", "CDBA"], "DB"),
    4: (["EBAC", "ABEDC", "BEAF", "CEBA", "BAED"], "BE"),
}


def q32(v):
    seqs, q = CPTD[v]
    sim = [s for s in seqs if all(c in s for c in q)]
    cnt = Counter()
    for s in sim:
        p = max(s.index(c) for c in q); cnt.update(set(s[p + 1:]) - set(q))
    rank = sorted(cnt, key=lambda k: (-cnt[k], k))
    win = rank[0]
    assert cnt[win] > cnt[rank[1]]
    nxt = Counter(s[s.index(q[-1]) + 1] for s in seqs if q[-1] in s and s.index(q[-1]) + 1 < len(s))
    cands = [(r, f"{r} chỉ đạt {cnt[r]}/{len(sim)}.") for r in rank[1:]] + [(q[0], "Phần tử đã có trong chuỗi cần dự đoán."), (q[-1], "Phần tử đã có trong chuỗi cần dự đoán.")]
    o, x = pick(win, cands, str)
    lst = ", ".join(f"s{i + 1} = ⟨{', '.join(s)}⟩" for i, s in enumerate(seqs))
    return Q("VDC", "CPT dự đoán (C6)", f"Tập huấn luyện CPT gồm: {lst}. Dự đoán phần tử tiếp theo của chuỗi <b>⟨{', '.join(q)}⟩</b>: phần tử có điểm cao nhất là:",
             o, x, f"Chuỗi tương tự (chứa đủ {', '.join(q)}): {len(sim)}. Đếm phần sau vị trí cả {', '.join(q)} đã xuất hiện: " + ", ".join(f"{k} = {cnt[k]}/{len(sim)}" for k in rank) + f" ⇒ {win}.",
             "Chọn phần tử đứng ngay sau trong một chuỗi hoặc chọn phần tử đã có trong truy vấn.", "CPT: tìm chuỗi tương tự (AND Inverted Index) → đếm hậu tố → chọn điểm cao nhất.")


def q33(v):
    return [
        Q("TH", "Cấu trúc CPT (C6)", "Trong CPT, cấu trúc nào dùng phép <b>AND giữa các dòng</b> để tìm nhanh chuỗi tương tự?",
          ["Inverted Index", "Prediction Tree", "Lookup Table", "Count Table"],
          ["Prediction Tree lưu chuỗi dạng cây tiền tố.", "Lookup Table trỏ tới nút cuối của mỗi chuỗi.", "Count Table dùng ở bước tính điểm."],
          "Inverted Index: bảng item × chuỗi (1 nếu chuỗi chứa item).", "Lẫn vai trò 3 cấu trúc của CPT.", "Tree: lưu · Index: tìm tương tự · Lookup: khôi phục chuỗi."),
        Q("NB", "Cấu trúc CPT (C6)", "Vai trò của <b>Lookup Table</b> trong CPT là:",
          ["Trỏ tới nút cuối của mỗi chuỗi để khôi phục chuỗi", "Đánh dấu chuỗi nào chứa item nào", "Lưu các chuỗi dưới dạng cây tiền tố", "Đếm điểm các phần tử dự đoán"],
          ["Đó là Inverted Index.", "Đó là Prediction Tree.", "Đó là Count Table."],
          "Lookup Table: từ nút cuối đi ngược lên gốc là khôi phục toàn bộ chuỗi.", "Lẫn vai trò 3 cấu trúc.", "Lookup = con trỏ tới nút cuối."),
        Q("TH", "Cấu trúc CPT (C6)", "Trong <b>Prediction Tree</b> của CPT, hai chuỗi có chung phần đầu được lưu như thế nào?",
          ["Dùng chung nhánh tiền tố từ gốc", "Lưu thành hai nhánh tách biệt hoàn toàn", "Chỉ lưu chuỗi dài hơn", "Sắp xếp lại item theo chữ cái rồi lưu"],
          ["Như vậy không tiết kiệm nút.", "Mất dữ liệu.", "CPT giữ đúng thứ tự trong chuỗi."],
          "Prediction Tree là cây tiền tố, giữ đúng thứ tự.", "Nghĩ CPT sắp xếp item như FP-tree.", "Tree = cây tiền tố, giữ thứ tự."),
        Q("TH", "CPT+ nén cây (C6)", "Trong CPT+, ký hiệu <b>x = AB</b> trên cây có ý nghĩa gì?",
          ["Chuỗi con hay gặp AB được thay bằng một nút mới để nén cây", "x là một item mới xuất hiện trong dữ liệu", "x là phần tử dự đoán cho chuỗi AB", "x là chỉ mục của chuỗi s2 trong Lookup Table"],
          ["x không phải item gốc của dữ liệu.", "x không phải kết quả dự đoán.", "Lookup Table chỉ trỏ tới nút."],
          "CPT+ nén chuỗi con thường gặp thành một ký hiệu để tiết kiệm nút.", "Nghĩ x là item thật.", "CPT+ = nén chuỗi con phổ biến."),
    ][v - 1]


GR = {"s": ["AB", "AD", "AG", "BE", "BF", "DF", "EG", "FC"], "t": ["AC", "AE", "BC", "CD", "EF", "BG", "FG"]}


def trav(edges):
    adj = {}
    for a, b in edges:
        adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
    seen, qq = ["A"], ["A"]
    while qq:
        u = qq.pop(0)
        for w in sorted(adj[u]):
            if w not in seen: seen.append(w); qq.append(w)
    d = []

    def go(u):
        d.append(u)
        for w in sorted(adj[u]):
            if w not in d: go(w)
    go("A")
    return seen, d


def q34_35(v):
    if v in (1, 2):
        b = [Q("NB", "BFS (C9)", "<b>BFS (Breadth-First Search)</b> dùng cấu trúc dữ liệu nào?", ["Hàng đợi (queue, FIFO)", "Ngăn xếp (stack, LIFO)", "Hàng đợi ưu tiên theo trọng số", "Cây nhị phân tìm kiếm"],
               ["Đó là DFS.", "Đó là Dijkstra.", "Không dùng cho BFS."], "BFS duyệt theo từng mức, dùng queue.", "Lẫn queue (BFS) với stack (DFS).", "BFS–queue; DFS–stack."),
             Q("TH", "BFS (C9)", "Ứng dụng nào phù hợp nhất với <b>BFS</b> trong knowledge graph?", ["Tìm thực thể liên quan gần nhất, đường đi ít cạnh nhất", "Duyệt ontology đến khái niệm con sâu nhất", "Xây cây phân cấp taxonomy nhiều tầng", "Tìm chuỗi liên kết dài nhất"],
               ["Đó là ứng dụng của DFS.", "Đó là ứng dụng của DFS.", "Đó là ứng dụng của DFS."], "BFS mở rộng theo chiều ngang: gợi ý gần, kết bạn, đường ngắn nhất.", "Lẫn ứng dụng BFS và DFS.", "Gần nhất → BFS; sâu nhất → DFS.")][v - 1]
        d = [Q("NB", "DFS (C9)", "<b>DFS (Depth-First Search)</b> hoạt động theo nguyên tắc nào?", ["Đi hết một nhánh tới khi cụt rồi quay lui", "Thăm hết các đỉnh cùng mức rồi mới xuống mức sau", "Luôn chọn cạnh có trọng số nhỏ nhất", "Thăm các đỉnh theo thứ tự bậc giảm dần"],
               ["Đó là BFS.", "Đó là Prim/Dijkstra.", "Không phải DFS."], "DFS dùng stack (LIFO) hoặc đệ quy.", "Lẫn DFS với BFS.", "DFS = sâu trước, stack."),
             Q("TH", "DFS (C9)", "Ứng dụng nào phù hợp nhất với <b>DFS</b>?", ["Duyệt ontology tìm khái niệm con nhiều tầng", "Gợi ý kết bạn bạn-của-bạn gần nhất", "Tìm đường đi ít cạnh nhất", "Tìm sản phẩm liên quan trực tiếp"],
               ["Đó là BFS.", "Đó là BFS.", "Đó là BFS."], "DFS khám phá quan hệ sâu nhiều tầng, taxonomy, chuỗi liên kết dài.", "Lẫn ứng dụng BFS/DFS.", "Sâu → DFS.")][v - 1]
        return [b, d]
    edges = GR["s"] if v == 3 else GR["t"]
    bf, df = trav(edges)
    g = ", ".join(f"{a}–{b}" for a, b in edges)
    rev = list(reversed(bf[1:]))
    j = lambda s: ", ".join(s)
    o, x = pick(bf, [(df, "Đó là thứ tự DFS."), (["A"] + rev, "Đảo ngược thứ tự sau A."), (["A"] + sorted(bf[1:]), "Chỉ sắp theo chữ cái, không theo mức.")], j)
    b = Q("VD", "BFS (C9)", f"Đồ thị vô hướng có các cạnh: {g}. Duyệt <b>BFS</b> từ A (xét đỉnh kề theo thứ tự chữ cái). Thứ tự thăm là:", o, x,
          f"Queue: thăm hết đỉnh kề của A rồi mới xuống mức sau ⇒ {j(bf)}.", "Lẫn thứ tự BFS và DFS.", "BFS theo mức; DFS theo nhánh.")
    o, x = pick(df, [(bf, "Đó là thứ tự BFS."), (["A"] + list(reversed(df[1:])), "Đảo ngược thứ tự sau A."), (["A"] + sorted(df[1:]), "Chỉ sắp theo chữ cái.")], j)
    d = Q("VD", "DFS (C9)", f"Đồ thị vô hướng có các cạnh: {g}. Duyệt <b>DFS</b> từ A (xét đỉnh kề theo thứ tự chữ cái). Thứ tự thăm là:", o, x,
          f"Đi sâu theo đỉnh kề nhỏ nhất chưa thăm, cụt thì quay lui ⇒ {j(df)}.", "Lẫn thứ tự BFS và DFS.", "DFS: đi sâu, quay lui.")
    return [b, d]


def tail(v):
    T = []
    T.append([
        Q("NB", "Blockchain (C9)", "Dữ liệu thô trên Blockchain tồn tại ở dạng nào?", ["Byte/hex (chuỗi thập lục phân)", "Bảng quan hệ đã chuẩn hóa", "File CSV theo ngày", "JSON có schema rõ ràng"],
          ["Bảng quan hệ là kết quả sau Blockchain ETL.", "Không phải dạng lưu on-chain.", "Dữ liệu thô chưa có schema dễ đọc."], "On-chain data ở dạng byte/hex khó đọc, phân tán; cần Blockchain ETL.", "Nghĩ dữ liệu on-chain đã sẵn dạng bảng.", "Thô = hex → decode bằng ABI → bảng."),
        Q("TH", "Blockchain (C9)", "Vì sao dữ liệu on-chain cần qua <b>Blockchain ETL</b> mới dùng được cho BI?", ["Vì dữ liệu thô ở dạng hex khó đọc, phân tán", "Vì dữ liệu on-chain có thể bị sửa", "Vì blockchain không lưu lịch sử giao dịch", "Vì dữ liệu on-chain bị mã hóa bằng khóa riêng"],
          ["On-chain ghi vĩnh viễn, không sửa được.", "Blockchain lưu toàn bộ lịch sử.", "Dữ liệu công khai, minh bạch."], "Node Ingestion (RPC) → Event Decoding (ABI) → bảng quan hệ.", "Nghĩ dữ liệu blockchain bị mã hóa bí mật.", "Minh bạch nhưng khó đọc."),
        Q("TH", "Blockchain (C9)", "File <b>ABI</b> đóng vai trò gì trong Blockchain ETL?", ["Dịch chuỗi hex thành tên hàm và tham số", "Kết nối tới node qua RPC", "Lưu khóa riêng của ví", "Nén dữ liệu giao dịch"],
          ["Đó là bước Node Ingestion.", "ABI không chứa khóa.", "ABI không nén."], "Event Decoding dùng ABI để giải mã dữ liệu hex.", "Lẫn các bước Blockchain ETL.", "ABI = từ điển giải mã hex."),
        Q("NB", "Blockchain (C9)", "Dữ liệu đọc trực tiếp từ node Blockchain qua RPC có dạng như thế nào?", ["Chuỗi hex khó đọc", "Bảng fact đã tổng hợp", "Báo cáo PDF", "Vector embedding"],
          ["Cần ETL mới thành bảng.", "Không phải dạng dữ liệu on-chain.", "Embedding thuộc vector DB."], "Dữ liệu thô on-chain ở dạng byte/hex.", "Nghĩ RPC trả về dữ liệu đã xử lý.", "RPC → hex."),
    ][v - 1])
    T.append([
        Q("NB", "IVFFLAT (C8–9)", "<b>IVFFLAT</b> là gì?", ["Một loại vector index giúp tìm bản ghi tương đồng rất nhanh", "Định dạng file lưu bảng theo cột để nén tốt hơn", "Thuật toán sắp xếp item trước khi dựng FP-tree", "Kỹ thuật che dấu cột chứa dữ liệu nhạy cảm"],
          ["Đó là Parquet.", "Không liên quan FP-tree.", "Đó là CLM."], "IVFFLAT: vector index phục vụ semantic search, tìm hàng triệu bản ghi trong vài ms.", "Lẫn với thuật ngữ khác.", "IVFFLAT = vector index (ANN)."),
        Q("TH", "IVFFLAT (C8–9)", "Trong IVFFLAT, phần <b>\"FLAT\"</b> có nghĩa là gì?", ["Vector trong mỗi vùng được lưu nguyên, không nén", "Không gian vector không được chia vùng", "Dữ liệu được làm phẳng thành bảng", "Mọi vector có cùng độ dài 1"],
          ["IVF chính là chia vùng.", "Không liên quan flat table.", "Không phải chuẩn hóa độ dài."], "IVF: KMeans chia vùng (Voronoi); FLAT: lưu nguyên, khác IVF-PQ có nén.", "Lẫn FLAT với flat table.", "IVF = chia vùng; FLAT = không nén."),
        Q("TH", "IVFFLAT (C8–9)", "IVFFLAT thuộc nhóm kỹ thuật tìm kiếm nào?", ["ANN – Approximate Nearest Neighbor", "Exact k-NN quét toàn bộ", "Full-text search theo từ khóa", "B-tree range search"],
          ["IVFFLAT chấp nhận gần đúng để nhanh hơn.", "Semantic search tìm theo ý nghĩa, không theo từ khóa.", "Không phải chỉ mục B-tree."], "ANN: chỉ xét vài vùng gần câu hỏi nhất.", "Nghĩ vector index luôn chính xác tuyệt đối.", "IVFFLAT = ANN."),
        Q("VD", "IVFFLAT (C8–9)", "IVFFLAT chia không gian thành <b>1.000 vùng</b>, mỗi lần tìm chỉ xét <b>10 vùng</b>. Số phép tính giảm khoảng:", ["100 lần", "10 lần", "1.000 lần", "10.000 lần"],
          ["Chia nhầm.", "Đó là số vùng, không phải tỉ lệ.", "Nhân nhầm."], "1.000 / 10 = 100 lần.", "Tính sai tỉ lệ.", "Giảm ≈ số vùng / số vùng xét."),
    ][v - 1])
    T.append([
        Q("NB", "CLM (C7)", "<b>CLM</b> là gì?", ["Column-level Masking: che dấu dữ liệu nhạy cảm ở cấp cột", "Row-level Security: lọc dòng theo người truy cập", "Cloud Lifecycle Management", "Customer Lifetime Model"],
          ["Đó là RLS.", "Không phải nghĩa trong tài liệu.", "Không phải nghĩa trong tài liệu."], "CLM ẩn/mã hóa một phần PII mà không đổi cấu trúc bảng.", "Lẫn CLM với RLS.", "RLS lọc dòng; CLM che cột."),
        Q("TH", "CLM (C7)", "Phân biệt đúng <b>CLM</b> và RLS:", ["CLM che giá trị cột nhạy cảm; RLS lọc dòng theo người truy cập", "CLM lọc dòng theo người truy cập; RLS che giá trị cột", "CLM xóa hẳn cột nhạy cảm; RLS xóa dòng không được phép", "Hai cơ chế giống nhau, chỉ khác tên theo nhà cung cấp"],
          ["Đảo ngược.", "Không xóa dữ liệu.", "Hai cơ chế khác nhau."], "RLS: nhân viên vùng A chỉ thấy khách vùng A; CLM: 091xxxx888.", "Đảo hai cơ chế.", "Row ↔ dòng; Column ↔ cột."),
        Q("VD", "CLM (C7)", "Số điện thoại hiển thị dạng <b>091xxxx888</b> là ví dụ của kỹ thuật nào?", ["Column-level Masking", "Row-level Security", "Differential Privacy", "Object Lock"],
          ["RLS lọc dòng, không che giá trị.", "Differential privacy thêm nhiễu thống kê.", "Object Lock chống xóa/sửa file."], "CLM che một phần giá trị PII.", "Lẫn với differential privacy.", "Che một phần giá trị → CLM."),
        Q("TH", "CLM (C7)", "Đặc điểm nào đúng với <b>CLM</b>?", ["Ẩn một phần dữ liệu PII mà không đổi cấu trúc bảng", "Xóa hẳn cột nhạy cảm khỏi bảng", "Chỉ áp dụng cho dữ liệu đã nén", "Thay đổi kiểu dữ liệu của cột"],
          ["Không xóa cột.", "Không liên quan nén.", "Không đổi cấu trúc."], "CLM giữ nguyên cấu trúc bảng.", "Nghĩ masking là xóa.", "Masking ≠ xóa."),
    ][v - 1])
    T.append([
        Q("NB", "AI Act (C7)", "<b>AI Act</b> là gì?", ["Đạo luật AI của EU phân loại hệ thống AI theo mức rủi ro", "Luật bảo vệ dữ liệu cá nhân của EU năm 2018", "Tiêu chuẩn kỹ thuật cho vector database", "Bộ quy tắc của Mỹ về bản quyền dữ liệu"],
          ["Đó là GDPR.", "Không phải tiêu chuẩn kỹ thuật.", "Không phải luật Mỹ."], "AI Act (EU) áp dụng toàn diện từ 2026; 4 mức rủi ro; 3 trụ cột Transparency, Human Oversight, Data Quality.", "Lẫn AI Act với GDPR.", "GDPR: dữ liệu cá nhân · AI Act: rủi ro AI."),
        Q("TH", "AI Act (C7)", "Theo AI Act, <b>chấm điểm công dân (social scoring)</b> thuộc mức rủi ro nào?", ["Unacceptable – bị cấm", "High – kiểm soát nghiêm ngặt", "Limited – bắt buộc dán nhãn", "Minimal – tự do vận hành"],
          ["High: chấm điểm tín dụng, tuyển dụng.", "Limited: chatbot, deepfake.", "Minimal: ứng dụng rủi ro thấp."], "Unacceptable: social scoring, AI thao túng hành vi → cấm.", "Lẫn mức High và Unacceptable.", "Social scoring → cấm."),
        Q("NB", "AI Act (C7)", "Ý nào <b>KHÔNG</b> thuộc 3 trụ cột bắt buộc của AI Act?", ["Open source bắt buộc", "Transparency", "Human Oversight", "Data Quality"],
          ["Là trụ cột.", "Là trụ cột.", "Là trụ cột."], "3 trụ cột: Transparency, Human Oversight, Data Quality.", "Bịa thêm trụ cột.", "Minh bạch · Giám sát · Chất lượng dữ liệu."),
        Q("VD", "AI Act (C7)", "Hệ thống AI <b>chấm điểm tín dụng</b> của Fintech thuộc mức rủi ro nào theo AI Act?", ["High – kiểm soát nghiêm ngặt", "Unacceptable – bị cấm", "Limited – chỉ cần dán nhãn", "Minimal – tự do"],
          ["Cấm là social scoring.", "Limited là chatbot, deepfake.", "Tín dụng ảnh hưởng lớn tới quyền lợi."], "High: tín dụng, tuyển dụng, hạ tầng thiết yếu.", "Lẫn chấm điểm tín dụng với social scoring.", "Tín dụng → High; social scoring → cấm."),
    ][v - 1])
    T.append([
        Q("TH", "Multi-level mining (C4)", "Khả năng <b>truy vấn nhiều cấp</b> liên quan đến dạng khai phá dữ liệu nào?", ["Multi-level Mining", "Sequential Pattern Mining", "Outlier Detection", "Text Mining"],
          ["Khai phá mẫu tuần tự theo thời gian.", "Phát hiện bất thường.", "Khai phá văn bản."], "Multi-level mining: luật kết hợp ở nhiều mức trừu tượng dựa trên concept hierarchy.", "Lẫn với các dạng khai phá khác.", "Nhiều cấp → multi-level + concept hierarchy."),
        Q("TH", "Multi-level mining (C4)", "Multi-level Mining dựa trên cấu trúc nào?", ["Phân cấp khái niệm (concept hierarchy)", "Cây FP-tree", "Ma trận hiệp phương sai", "Inverted Index"],
          ["FP-tree dùng nén giao dịch.", "Đó là PCA.", "Đó là CPT."], "Concept hierarchy: chi nhánh < tỉnh < vùng.", "Lẫn cấu trúc dữ liệu.", "Multi-level ↔ hierarchy."),
        Q("VD", "Multi-level mining (C4)", "Một luật không đủ phổ biến ở mức <b>chi nhánh</b> nhưng xuất hiện khi gộp lên mức <b>vùng</b>. Đây là dạng khai phá nào?", ["Multi-level Mining", "Discretization", "Clustering", "Sequential mining"],
          ["Rời rạc hóa là tiền xử lý.", "Phân cụm không sinh luật kết hợp.", "Không liên quan thứ tự thời gian."], "Gộp lên mức trừu tượng cao hơn để luật đủ support.", "Không nhận ra yếu tố \"mức\".", "Gộp/tách mức → multi-level."),
        Q("TH", "Multi-level mining (C4)", "Thao tác <b>roll-up/drill-down</b> để tìm nguyên nhân gốc rễ gắn với dạng khai phá nào?", ["Multi-level Mining", "PCA", "Equal-frequency Binning", "PageRank"],
          ["PCA giảm chiều.", "Binning là rời rạc hóa.", "PageRank xếp hạng trang."], "Doanh số vùng giảm → drill-down xuống tỉnh → chi nhánh.", "Không liên hệ OLAP với multi-level.", "Roll-up/drill-down ↔ multi-level."),
    ][v - 1])
    T.append([
        Q("NB", "Damping factor (C6)", "<b>Damping factor</b> thường được dùng với giá trị bao nhiêu?", ["0,85", "0,15", "0,5", "1"],
          ["Đó là (1 − d).", "Không phải giá trị thường dùng.", "d = 1 thì không có nhảy ngẫu nhiên."], "d = 0,85; (1 − d) = 0,15.", "Lẫn d với 1 − d.", "d = 0,85."),
        Q("TH", "Damping factor (C6)", "Ý nghĩa của <b>d = 0,85</b> trong PageRank là:", ["85% tiếp tục bấm liên kết, 15% nhảy ngẫu nhiên", "85% nhảy ngẫu nhiên, 15% bấm liên kết", "85% trang được xếp hạng cao", "Mỗi vòng PageRank giảm 15%"],
          ["Đảo ngược.", "Không phải nghĩa của d.", "Không phải nghĩa của d."], "Random surfer: d = xác suất tiếp tục theo liên kết.", "Đảo d và 1 − d.", "d = theo link; 1 − d = nhảy."),
        Q("NB", "Damping factor (C6)", "Trong công thức PageRank, phần <b>(1 − d)</b> thường bằng:", ["0,15", "0,85", "0,5", "0,05"],
          ["Đó là d.", "Không phải.", "Không phải."], "d = 0,85 ⇒ 1 − d = 0,15.", "Lẫn d với 1 − d.", "1 − d = 0,15."),
        Q("NB", "Damping factor (C6)", "\"Damping factor trong PageRank thường được chọn là 0,5.\" Nhận định nào đúng?", ["Sai, thường là 0,85", "Đúng", "Sai, thường là 0,15", "Sai, thường là 1"],
          ["Không phải 0,5.", "0,15 là 1 − d.", "d = 1 bỏ mất nhảy ngẫu nhiên."], "d = 0,85.", "Lẫn d với 1 − d.", "d = 0,85."),
    ][v - 1])
    return T


def build(v):
    qs = concept(v)                       # 1–15
    pc = preprocess_concepts(v)
    qs += [q16(v), q17(v), q18(v), pc[19], pc[20], pc[21], pc[22], pc[23], pc[24], pc[25], q26(v), q27(v)]
    qs += q28(v) + [q29(v), q30(v)] + q31(v) + [q32(v), q33(v)] + q34_35(v) + tail(v)
    assert len(qs) == 47, len(qs)
    return qs


if __name__ == "__main__":
    for v in (1, 2, 3, 4):
        (SRC / f"de{v}.json").write_text(json.dumps({"questions": build(v)}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"de{v}.json · {len(build(v))} câu")
