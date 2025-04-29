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
MAX_TABLES_PER_CATEGORY = 15

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

for category in CATEGORIES:
    print(f"\n=== Processing Category: {category['text']} ===")