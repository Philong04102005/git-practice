import pandas as pd
fanpage = [
    "BẤT ĐỘNG SẢN - MUA BÁN NHÀ ĐẤT HÀ NỘI ✅",
    "BẤT ĐỘNG SẢN HÀ NỘI ✅️",
    "🏡 BẤT ĐỘNG SẢN HÀ NỘI",
    "MUA BÁN BẤT ĐỘNG SẢN HÀ NỘI ✅",
    "BẤT ĐỘNG SẢN HÀ NỘI ✅",
    "Bất động sản Hà Nội",
    "Mua bán Bất Động Sản HÀ NỘI ✅",
    "Bất động sản Hà Nội",
    "BẤT ĐỘNG SẢN HÀ NỘI 🏘️",
    "Bất Động Sản Hà Nội",
    "Mua Bán Bất Động Sản HÀ NỘI ✅",
    "Mua bán bất động sản HÀ NỘI - Nhà đất Hà Nội ✅",
    "BẤT ĐỘNG SẢN HÀ NỘI - HỘI MUA BÁN NHÀ ĐẤT CHÍNH CHỦ",
    "BẤT ĐỘNG SẢN - MUA BÁN NHÀ ĐẤT HÀ NỘI ✅",
    "Bất Động Sản Hà Nội",
    "BẤT ĐỘNG SẢN HÀ NỘI ✅",
    "Bất Động Sản Hà Nội",
    "Bất Động Sản Hà Nội",
    "BẤT ĐỘNG SẢN HÀ NỘI",
    "Mua bán BĐS Nhà Đất Hà Nội",
    "https://www.facebook.com/groups/430905622975797/",
    "BẤT ĐỘNG SẢN HÀ NỘI",
    "Bất động sản Hà Nội",
    "BẤT ĐỘNG SẢN HÀ NỘI - MUA VÀ BÁN",
    "Nhà Đất BĐS Hà Nội Chính Chủ ✅"
]
facebook_groups = [
    "https://www.facebook.com/groups/batdongsantungphan/",
    "https://www.facebook.com/groups/groupbatdongsanhanoivn/",
    "https://www.facebook.com/groups/bds2hanoi/",
    "https://www.facebook.com/groups/hoiniengranghnoi/",
    "https://www.facebook.com/groups/446687191496416/",
    "https://www.facebook.com/groups/1341025385922584/",
    "https://www.facebook.com/groups/1036031467638279/",
    "https://www.facebook.com/groups/505769052949575/",
    "https://www.facebook.com/groups/1452630678157228/",
    "https://www.facebook.com/groups/batdongsanhanoi.viet/",
    "https://www.facebook.com/groups/1387287665544197/",
    "https://www.facebook.com/groups/249336878156780/",
    "https://www.facebook.com/groups/1891173918068652/",
    "https://www.facebook.com/groups/859316832902122/",
    "https://www.facebook.com/groups/1330816713720648/",
    "https://www.facebook.com/groups/285736614961804/",
    "https://www.facebook.com/groups/865782621533327/",
    "https://www.facebook.com/groups/1409548486429083/",
    "https://www.facebook.com/groups/978999467221417/",
    "https://www.facebook.com/groups/808574477477699/",
    "https://www.facebook.com/groups/430905622975797/",
    "https://www.facebook.com/groups/batdongsanhanoi8888/",
    "https://www.facebook.com/groups/815809976641880/",
    "https://www.facebook.com/groups/2675203102635742/",
    "https://www.facebook.com/groups/922322716405431/"

]
df = pd.DataFrame({
    "Fanpage": fanpage,
    "Link": facebook_groups
})
#Xuất file
df.to_csv("data/group/group3.csv", index = False)