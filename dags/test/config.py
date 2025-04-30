#------- CONFIGURATION FILE FOR PXWEB DATA EXTRACTION -------#

BASE_URL = "https://pxweb.gso.gov.vn/api/v1/vi/"

CATEGORIES = [
    {"dbid": "Công nghiệp", "text": "Công nghiệp"},
    {"dbid": "Đầu tư", "text": "Đầu tư"},
    {"dbid": "Doanh nghiệp", "text": "Doanh nghiệp"},
    {"dbid": "Dân số và lao động", "text": "Dân số và lao động"},
    {"dbid": "Giáo dục", "text": "Giáo dục"}
]

OUTPUT_BASE_PATH = "/home/data"
MAX_TABLES_PER_CATEGORY = 72

#------- MAPPINGS FOR DATA EXTRACTION -------#


province_mapping = {
    "0": "CẢ NƯỚC", "1": "Đồng bằng sông Hồng", "2": "Hà Nội", "3": "Vĩnh Phúc", "4": "Bắc Ninh",
    "5": "Quảng Ninh", "6": "Hải Dương", "7": "Hải Phòng", "8": "Hưng Yên", "9": "Thái Bình",
    "10": "Hà Nam", "11": "Nam Định", "12": "Ninh Bình", "13": "Trung du và miền núi phía Bắc",
    "14": "Hà Giang", "15": "Cao Bằng", "16": "Bắc Kạn", "17": "Tuyên Quang", "18": "Lào Cai",
    "19": "Yên Bái", "20": "Thái Nguyên", "21": "Lạng Sơn", "22": "Bắc Giang", "23": "Phú Thọ",
    "24": "Điện Biên", "25": "Lai Châu", "26": "Sơn La", "27": "Hoà Bình",
    "28": "Bắc Trung Bộ và Duyên hải miền Trung", "29": "Thanh Hoá", "30": "Nghệ An",
    "31": "Hà Tĩnh", "32": "Quảng Bình", "33": "Quảng Trị", "34": "Thừa Thiên Huế",
    "35": "Đà Nẵng", "36": "Quảng Nam", "37": "Quảng Ngãi", "38": "Bình Định", "39": "Phú Yên",
    "40": "Khánh Hoà", "41": "Ninh Thuận", "42": "Bình Thuận", "43": "Tây Nguyên",
    "44": "Kon Tum", "45": "Gia Lai", "46": "Đắk Lắk", "47": "Đắk Nông", "48": "Lâm Đồng",
    "49": "Đông Nam Bộ", "50": "Bình Phước", "51": "Tây Ninh", "52": "Bình Dương",
    "53": "Đồng Nai", "54": "Bà Rịa - Vũng Tàu", "55": "TP.Hồ Chí Minh",
    "56": "Đồng bằng sông Cửu Long", "57": "Long An", "58": "Tiền Giang", "59": "Bến Tre",
    "60": "Trà Vinh", "61": "Vĩnh Long", "62": "Đồng Tháp", "63": "An Giang",
    "64": "Kiên Giang", "65": "Cần Thơ", "66": "Hậu Giang", "67": "Sóc Trăng",
    "68": "Bạc Liêu", "69": "Cà Mau"
}

year_mapping = {
    "0": "2012", "1": "2013", "2": "2014", "3": "2015", "4": "2016", "5": "2017",
    "6": "2018", "7": "2019", "8": "2020", "9": "2021", "10": "2022",
    "11": "Sơ bộ 2023", "12": "2023", "13": "Sơ bộ 2024"
}

industry_mapping = {
    "0": "TOÀN NGÀNH CÔNG NGHIỆP", "1": "Khai khoáng", "2": "Công nghiệp chế biến, chế tạo",
    "3": "Sản xuất và phân phối điện", "4": "Cung cấp nước, xử lý rác thải, nước thải"
}

# Region mapping dictionary (Vietnamese to standardized)
REGION_MAPPING = {
    'Đồng bằng sông Hồng': 'Đồng bằng sông Hồng',
    'Trung du và miền núi phía Bắc': 'Trung du miền núi Bắc Bộ',
    'Bắc Trung Bộ và Duyên hải miền Trung': 'Bắc Trung Bộ',
    'Duyên hải Nam Trung Bộ': 'Đồng bằng Duyên Hải miền Trung',
    'Đông Nam Bộ': 'Đông Nam Bộ',
    'Tây Nguyên': 'Tây Nguyên',
    'Đồng bằng sông Cửu Long': 'Đồng bằng sông Cửu Long',
    # Add alternative spellings or variations
    'Bắc Trung Bộ': 'Bắc Trung Bộ',
    'Đồng bằng Duyên Hải miền Trung': 'Đồng bằng Duyên Hải miền Trung',
    'Trung du miền núi Bắc Bộ': 'Trung du miền núi Bắc Bộ',
}

# List of aggregated areas to exclude (national average, regional totals)
AGGREGATES_TO_EXCLUDE = [
    'CẢ NƯỚC', 'Cả nước', 'Tổng số', 'TOÀN QUỐC', 
    'Đồng bằng sông Hồng', 'Trung du và miền núi phía Bắc', 
    'Bắc Trung Bộ và Duyên hải miền Trung', 'Tây Nguyên', 
    'Đông Nam Bộ', 'Đồng bằng sông Cửu Long',
    'Trung du miền núi Bắc Bộ', 'Bắc Trung Bộ', 'Đồng bằng Duyên Hải miền Trung'
]

# Mapping of provinces to regions 
PROVINCE_TO_REGION_MAPPING = {
    # Bắc Trung Bộ
    'Hà Tĩnh': 'Bắc Trung Bộ',
    'Nghệ An': 'Bắc Trung Bộ',
    'Quảng Bình': 'Bắc Trung Bộ',
    'Quảng Trị': 'Bắc Trung Bộ',
    'Thanh Hóa': 'Bắc Trung Bộ',
    'Thừa Thiên - Huế': 'Bắc Trung Bộ',

    # Đồng bằng Duyên Hải miền Trung
    'Bình Định': 'Đồng bằng Duyên Hải miền Trung',
    'Bình Thuận': 'Đồng bằng Duyên Hải miền Trung',
    'Đà Nẵng': 'Đồng bằng Duyên Hải miền Trung',
    'Khánh Hòa': 'Đồng bằng Duyên Hải miền Trung',
    'Ninh Thuận': 'Đồng bằng Duyên Hải miền Trung',
    'Phú Yên': 'Đồng bằng Duyên Hải miền Trung',
    'Quảng Nam': 'Đồng bằng Duyên Hải miền Trung',
    'Quảng Ngãi': 'Đồng bằng Duyên Hải miền Trung',

    # Đồng bằng sông Cửu Long
    'An Giang': 'Đồng bằng sông Cửu Long',
    'Bạc Liêu': 'Đồng bằng sông Cửu Long',
    'Bến Tre': 'Đồng bằng sông Cửu Long',
    'Cà Mau': 'Đồng bằng sông Cửu Long',
    'Cần Thơ': 'Đồng bằng sông Cửu Long',
    'Đồng Tháp': 'Đồng bằng sông Cửu Long',
    'Hậu Giang': 'Đồng bằng sông Cửu Long',
    'Kiên Giang': 'Đồng bằng sông Cửu Long',
    'Long An': 'Đồng bằng sông Cửu Long',
    'Sóc Trăng': 'Đồng bằng sông Cửu Long',
    'Tiền Giang': 'Đồng bằng sông Cửu Long',
    'Trà Vinh': 'Đồng bằng sông Cửu Long',
    'Vĩnh Long': 'Đồng bằng sông Cửu Long',

    # Đồng bằng sông Hồng
    'Bắc Ninh': 'Đồng bằng sông Hồng',
    'Hà Nam': 'Đồng bằng sông Hồng',
    'Hà Nội': 'Đồng bằng sông Hồng',
    'Hải Dương': 'Đồng bằng sông Hồng',
    'Hải Phòng': 'Đồng bằng sông Hồng',
    'Hưng Yên': 'Đồng bằng sông Hồng',
    'Nam Định': 'Đồng bằng sông Hồng',
    'Ninh Bình': 'Đồng bằng sông Hồng',
    'Quảng Ninh': 'Đồng bằng sông Hồng',
    'Thái Bình': 'Đồng bằng sông Hồng',
    'Vĩnh Phúc': 'Đồng bằng sông Hồng',

    # Đông Nam Bộ
    'Bà Rịa - Vũng Tàu': 'Đông Nam Bộ',
    'Bình Dương': 'Đông Nam Bộ',
    'Bình Phước': 'Đông Nam Bộ',
    'Đồng Nai': 'Đông Nam Bộ',
    'Tây Ninh': 'Đông Nam Bộ',
    'TP. Hồ Chí Minh': 'Đông Nam Bộ',

    # Tây Nguyên
    'Đắk Lắk': 'Tây Nguyên',
    'Đắk Nông': 'Tây Nguyên',
    'Gia Lai': 'Tây Nguyên',
    'Kon Tum': 'Tây Nguyên',
    'Lâm Đồng': 'Tây Nguyên',

    # Trung du miền núi Bắc Bộ
    'Bắc Giang': 'Trung du miền núi Bắc Bộ',
    'Bắc Kạn': 'Trung du miền núi Bắc Bộ',
    'Cao Bằng': 'Trung du miền núi Bắc Bộ',
    'Điện Biên': 'Trung du miền núi Bắc Bộ',
    'Hà Giang': 'Trung du miền núi Bắc Bộ',
    'Hòa Bình': 'Trung du miền núi Bắc Bộ',
    'Lai Châu': 'Trung du miền núi Bắc Bộ',
    'Lạng Sơn': 'Trung du miền núi Bắc Bộ',
    'Lào Cai': 'Trung du miền núi Bắc Bộ',
    'Phú Thọ': 'Trung du miền núi Bắc Bộ',
    'Sơn La': 'Trung du miền núi Bắc Bộ',
    'Thái Nguyên': 'Trung du miền núi Bắc Bộ',
    'Tuyên Quang': 'Trung du miền núi Bắc Bộ',
    'Yên Bái': 'Trung du miền núi Bắc Bộ'
}

# Province name standardization to handle variants of the same province
PROVINCE_NAME_STANDARDIZATION = {
    'TP.Hồ Chí Minh': 'TP. Hồ Chí Minh',
    'Tp. Hồ Chí Minh': 'TP. Hồ Chí Minh',
    'TP Hồ Chí Minh': 'TP. Hồ Chí Minh',
    'Thành phố Hồ Chí Minh': 'TP. Hồ Chí Minh',
    'Thừa Thiên Huế': 'Thừa Thiên - Huế',
    'Thừa Thiên-Huế': 'Thừa Thiên - Huế',
    'Bà Rịa Vũng Tàu': 'Bà Rịa - Vũng Tàu',
    'Bà Rịa-Vũng Tàu': 'Bà Rịa - Vũng Tàu',
    'TP. Đà Nẵng': 'Đà Nẵng',
    'Tp. Đà Nẵng': 'Đà Nẵng',
    'TP Đà Nẵng': 'Đà Nẵng',
    'TP. Hà Nội': 'Hà Nội',
    'Tp. Hà Nội': 'Hà Nội',
    'TP Hà Nội': 'Hà Nội',
    'TP. Hải Phòng': 'Hải Phòng',
    'Tp. Hải Phòng': 'Hải Phòng',
    'TP Hải Phòng': 'Hải Phòng',
    'TP. Cần Thơ': 'Cần Thơ',
    'Tp. Cần Thơ': 'Cần Thơ', 
    'TP Cần Thơ': 'Cần Thơ'
}

JOINED_COLS = {
    "region": "Region",
    "province": "Province",
    "Năng suất lao động phân theo địa phương": "Labor Productivity (VND/person)",
    "Dân số trung bình phân theo địa phương giới tính và thành thị nông thôn": "Average Population (thousand people)",
    "Số nam giới": "Male Population (thousand people)",
    "Số nữ giới": "Female Population (thousand people)",
    "Số dân thành thị": "Urban Population (thousand people)",
    "Số dân nông thôn": "Rural Population (thousand people)",
    'Diện tích(Km2)': 'Area (Km²)',
    'Mật độ dân số': 'Population Density (people/Km²)',
    "Chỉ số sản xuất công nghiệp phân theo địa phương": "Industrial Production Index (%)",
    "Diện tích sàn xây dựng nhà tự xây tự ở hoàn thành trong năm của hộ dân cư phân theo địa phương": "Self-built Housing Floor Area (m²)",
    "Diện tích sàn xây dựng nhà ở hoàn thành trong năm phân theo địa phương": "Completed Housing Floor Area (m²)",
    "Doanh thu thuần sản xuất kinh doanh của các doanh nghiệp đang hoạt động có kết quả sản xuất kinh doanh phân theo địa phương": "Enterprise Revenue (VND)",
    "Giá trị tài sản cố định và đầu tư tài chính dài hạn của các doanh nghiệp đang hoạt động có kết quả sản xuất kinh doanh tại thời điểm 31_12 hàng năm phân theo địa phương": "Fixed Assets Value (VND)",
    "Lao động trong các cơ sở kinh tế cá thể phi nông nghiệp phân theo địa phương": "Non-agricultural Individual Labor (people)",
    "Lợi nhuận trước thuế của doanh nghiệp đang hoạt động có kết quả sản xuất kinh doanh phân theo địa phương": "Pre-tax Profit (VND)",
    "Số cơ sở kinh tế cá thể phi nông nghiệp phân theo địa phương": "Non-agricultural Individual Establishments",
    "Số doanh nghiệp đang hoạt động có kết quả sản xuất kinh doanh tại thời điểm 31_12 hàng năm phân theo địa phương": "Operating Enterprises",
    "Số doanh nghiệp đang hoạt động có kết quả sản xuất kinh doanh tại thời điểm 31_12 phân theo quy mô lao động và theo địa phương": "Enterprises by Labor Size",
    "Số doanh nghiệp đang hoạt động có kết quả sản xuất kinh doanh tại thời điểm 31_12 phân theo quy mô vốn và theo địa phương": "Enterprises by Capital Size",
    "Số doanh nghiệp đang hoạt động tại thời điểm 31_12 hàng năm bình quân trên 1000 dân phân theo địa phương": "Enterprises per 1000 People",
    "Số doanh nghiệp đang hoạt động tại thời điểm 31_12 hàng năm phân theo địa phương": "Active Enterprises",
    "Số doanh nghiệp đăng ký thành lập mới phân theo địa phương": "Newly Registered Enterprises",
    "Số hợp tác xã đang hoạt động có kết quả sản xuất kinh doanh tại thời điểm 31_12 hàng năm phân theo địa phương": "Active Cooperatives",
    "Số lao động nữ trong các doanh nghiệp đang hoạt động có kết quả sản xuất kinh doanh tại thời điểm 31_12 hàng năm phân theo địa phương": "Female Labor in Enterprises (people)",
    "Số lao động trong hợp tác xã đang hoạt động có kết quả sản xuất kinh doanh tại thời điểm 31_12 hàng năm phân theo địa phương": "Cooperative Labor (people)",
    "Thu nhập bình quân một tháng của người lao động trong doanh nghiệp đang hoạt động có kết quả sản xuất kinh doanh phân theo địa phương": "Average Monthly Income (VND)",
    "Trang bị tài sản cố định bình quân 1 lao động của doanh nghiệp đang hoạt động có kết quả sản xuất kinh doanh phân theo địa phương": "Fixed Assets per Worker (VND)",
    "Tổng số lao động trong các doanh nghiệp đang hoạt động có kết quả sản xuất kinh doanh tại thời điểm 31_12 hàng năm phân theo địa phương": "Total Enterprise Labor (people)",
    "Tổng thu nhập của người lao động trong doanh nghiệp đang hoạt động có kết quả sản xuất kinh doanh phân theo địa phương": "Total Labor Income (VND)",
    "Tỷ suất lợi nhuận của doanh nghiệp đang hoạt động có kết quả sản xuất kinh doanh phân theo địa phương": "Profit Margin (%)",
    "Vốn sản xuất kinh doanh bình quân hàng năm của các doanh nghiệp đang hoạt động có kết quả sản xuất kinh doanh phân theo địa phương": "Average Annual Capital (VND)",
    "Số trường hợp tử vong được đăng ký khai tử phân theo địa phương": "Registered Deaths (people)",
    "Số vụ ly hôn đã xét xử phân theo địa phương và theo cấp xét xử": "Divorce Cases",
    "Tuổi kết hôn trung bình lần đầu phân theo địa phương": "Average First Marriage Age (years)",
    "Tỷ số giới tính của dân số phân theo địa phương": "Sex Ratio (%)"
}

year_mapping = {
    "0": "2012", "1": "2013", "2": "2014", "3": "2015", "4": "2016", "5": "2017",
    "6": "2018", "7": "2019", "8": "2020", "9": "2021", "10": "2022",
    "11": "Sơ bộ 2023", "12": "2023", "13": "Sơ bộ 2024"
}

industry_mapping = {
    "0": "TOÀN NGÀNH CÔNG NGHIỆP", "1": "Khai khoáng", "2": "Công nghiệp chế biến, chế tạo",
    "3": "Sản xuất và phân phối điện", "4": "Cung cấp nước, xử lý rác thải, nước thải"
}

S3_BUCKET = "test-flowsight-bucket"
S3_KEY = "data/final.csv"
AWS_CONN_ID = "aws_default"
OUTPUT_FILE_PATH = "/home/data/joined_data/final.csv"