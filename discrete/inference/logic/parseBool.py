import re
import numpy as np

# global rel


def parse(question):
    if not re.match("^[A-D \s + () ']*$", question):
        
        return 0
    else:
        
        chuoi_nhap = ''.join(question.split())
        chuoi_nhap = chuoi_nhap.replace("A'", "a")
        chuoi_nhap = chuoi_nhap.replace("B'", "b")
        chuoi_nhap = chuoi_nhap.replace("C'", "c")
        chuoi_nhap = chuoi_nhap.replace("D'", "d")

        global arr
        global tblon
        global ham_f
        global karf
        global vi_tri_o
        global matran
        global so_phan_tu

        arr = chuoi_nhap.split('+')
        ham_f = ham_f_tap_hop_dathuc(arr)
        so_phan_tu = len(ham_f)

        # chuyển chuỗi thành biểu đồ Kar(f)
        # print("dạng ma trận :\n", Kar_f(arr))
        print("list nhập vào ", arr)

        #kiểm tra 1 đơn thức có chứa phủ định của nó ko?
        if check_trung(arr)==0:
            return 0

        karf = Kar_f(arr)
        print("karf ", karf)
        print("dạng ma trận :\n", xuat_ma_tran(karf))

        tblon = te_bao_lon_f(arr)
        matran = xuat_ma_tran(karf)
        for i in range(0, 4):
            for j in range(0, 4):
                if matran[i][j] == 0:
                    matran[i][j] = ' '
        tam = kqphutoitieu(arr)
        cac_phu_tu_karf = tam[0]
        da_thuc_toi_tieu = tam[1]
        ####
        # chuyển định dạng để in các tế bào lớn
        # [[0, 0], [0, 1], [1, 0], [1, 1], 'AC']
        tbl = []
        for i in range(len(tblon)):
            k = ham_f_tap_hop(tblon[i])
            k.append(parsechuan(tblon[i]))
            tbl.append(k)

        ####
        for i in range(len(tblon)):
            tblon[i] = parsechuan(tblon[i])
        print("các tế bào lớn :", tblon)
        print("số lượng các tế bào lớn :", len(tblon))

        return question, matran, tbl, cac_phu_tu_karf, da_thuc_toi_tieu, str_html

###
def check_trung(arr):
    for i in range(len(arr)):
        if ("A" in arr[i]) and ("a" in arr[i]):
            return 0
        if ("B" in arr[i]) and ("b" in arr[i]):
            return 0
        if ("C" in arr[i]) and ("c" in arr[i]):
            return 0
        if ("D" in arr[i]) and ("d" in arr[i]):
            return 0
    return 1

def parsechuan(chuoi_nhap):
    chuoi_nhap = chuoi_nhap.replace("a", "A'")
    chuoi_nhap = chuoi_nhap.replace("b", "B'")
    chuoi_nhap = chuoi_nhap.replace("c", "C'")
    chuoi_nhap = chuoi_nhap.replace("d", "D'")
    return chuoi_nhap


def Sorting(lst):
    lst.sort(key=len)
    return lst


def chuyendoi(day):
    # chuyển sang chuỗi
    a = str(day)
    b = "[], "
    # loại bỏ dấu [ ] và ,
    for char in b:
        a = a.replace(char, "")

    # chuyển sang tên tế bào lớn tương ứng
    c = []
    for i in range(len(a)):
        c.append(tra_ve_tbl(int(a[i])))
    e = str(c)
    f = "']["
    for char in f:
        e = e.replace(char, " ")
    d = ","
    for char in d:
        e = e.replace(char, "+")
    return e


def sapxep(cac_da_thuc):
    b = []
    a = []
    tam2 = []
    tam = cac_da_thuc
    for i in range(len(tam)):
        k = str(tam[i])
        for j in "[],":
            k = k.replace(j, " ")
        a.append(k)
    for k in range(len(a)):
        string = a[k]
        tam1 = [int(s) for s in string.split() if s.isdigit()]
        tam2.append(tam1)
    #sắp xếp các đa thức theo số lượng các phần tử 
    for u in range(len(tam2)-1):
        for v in range(u+1, len(tam2)):
            if len(tam2[u]) > len(tam2[v]):
                k = tam2[u]
                tam2[u] = tam2[v]
                tam2[v] = k
    for i in range(len(tam2)):
        a1 = tam2[i]
        a1.sort()
    return tam2


def kqphutoitieu(arr):
    global str_html
    str_html = ''
    k = tim_vi_tri_o()
    tam = tim_cac_da_thuc(vi_tri_o, [], [], 0)
    tam = sapxep(tam)
    cac_da_thuc = []
    # print("\nCác phủ tìm được từ Kar(f) là: ")
    for i in range(len(tam)):
        k = tam[i]
        # print("f%s: " % (i+1), parsechuan(chuyendoi(k)))
        cac_da_thuc.append(parsechuan(chuyendoi(k)))
    toi_tieu = tim_cac_da_thuc_toi_tieu(tam)
    return cac_da_thuc, toi_tieu


def tim_cac_da_thuc_toi_tieu(cac_da_thuc):
    ### Chuyển về dang [5 2 2 3 3] để so sánh
    #sắp xếp
    cac_da_thuc = sapxep(cac_da_thuc)
    tam = []
    tam1 = []
    for i in range(len(cac_da_thuc)):
        c = []
        k = cac_da_thuc[i]
        for j in range(len(k)):
            a = tra_ve_tbl(k[j])
            b = len(a)
            c.append(b)
        tam.append(c)
    ###chèn phần tử đầu là số lượng đơn thức tương ứng
    for i in range(len(tam)):
        k = tam[i]
        dau = [len(k)]
        tam[i] = dau+tam[i]
    ###
    n = len(cac_da_thuc)
    cac_da_thuc_con_xet = []
    ###
    for i in range(0, n):
        cac_da_thuc_con_xet.append(i)

    cac_da_thuc2 = tam
    for i in range(0, n-1):
        da_thuc_i = cac_da_thuc2[i]
        if i not in cac_da_thuc_con_xet:
            next
        for j in range(i+1, n):
            da_thuc_j = cac_da_thuc2[j]
            if j not in cac_da_thuc_con_xet:
                next
            if da_thuc_i[0] > da_thuc_j[0]:
                co_i = 0
                co_j = 1
            elif da_thuc_i[0] < da_thuc_j[0]:
                co_i = 1
                co_j = 0
            else:
                for u in range(len(da_thuc_i)):
                    if da_thuc_i[u] < da_thuc_j[u]:
                        co_i = 1
                        co_j = 0
                        break
                    elif da_thuc_i[u] > da_thuc_j[u]:
                        co_i = 0
                        co_j = 1
                        break
                    else:
                        co_i = 0
                        co_j = 0

            if co_i == co_j:
                next
            elif co_i > co_j:
                cac_da_thuc_con_xet = [
                    item for item in cac_da_thuc_con_xet if item not in [j]]
            else:
                cac_da_thuc_con_xet = [
                    item for item in cac_da_thuc_con_xet if item not in [i]]

    # print("So sanh (cac) phu tren ta tim duoc (cac) da thuc toi tieu: ")
    trave_da_thuc_toi_tieu = []
    for i in range(len(cac_da_thuc_con_xet)):
        for j in range(len(cac_da_thuc)):
            if cac_da_thuc_con_xet[i] == j:
                trave_da_thuc_toi_tieu.append(
                    parsechuan(chuyendoi(cac_da_thuc[j])))
                # print("f%s :" % (i+1), parsechuan(chuyendoi(cac_da_thuc[j])))
    return trave_da_thuc_toi_tieu


def makeTable_Phu(myArray, cach, k):

    A = [' ', 'A', 'A', 'A\'', 'A\'', ' ']
    B = [' ', 'B\'', 'B', 'B', 'B\'', ' ']
    C = ['C', 'C', 'C\'', 'C\'']
    D = ['D\'', 'D', 'D', 'D\'']

    result = '<table style="text-align: center;width: 40%;margin-left:' + \
        str(cach)+'%;">'

    result += "<tr>"
    for i in range(len(A)):
        result += "<td style='width:15%;'>" + A[i] + "</td>"
    result += "</tr>"
    for i in range(len(myArray)):
        result += "<tr >"
        result += "<td style='width:15%;'>" + C[i] + "</td>"
        for j in range(len(myArray[i])):
            if myArray[i][j] in k:
                result += "<td style='width:15%;color:red;background-color: aqua;border: 1px solid;border-color: black !important;' >" + \
                    str(myArray[i][j]) + "</td>"
            # if myArray[i][j] == " ":
            #    result += "<td style='width:15%;border: 1px solid;border-color: black !important;' >" + \
            #        str(myArray[i][j]) + "</td>"
            else:
                result += "<td style='width:15%;color:red;border: 1px solid;border-color: black !important;' >" + \
                    str(myArray[i][j]) + "</td>"

        result += "<td style='width:15%;'>" + D[i] + "</td>"
        result += "</tr>"

    result += "<tr>"
    for i in range(len(A)):
        result += "<td style='width:15%;'>" + B[i] + "</td>"

    result += "</tr>"
    result += "</table>"
    return result


def tim_cac_da_thuc(vi_tri_o, cac_o_da_dung, cac_te_bao_lon_da_dung, so_dau_cach):
    global str_html

    cach = ""
    for i in range(so_dau_cach):
        cach = cach+" "

    cach_html = ''
    for i in range(so_dau_cach):
        cach_html += '&nbsp;'

    tam = tim_cac_te_bao_lon_bat_buoc(vi_tri_o, so_dau_cach)
    cac_te_bao_lon_bat_buoc = tam[1]
    cac_te_bao_lon_bat_buoc = [cac_te_bao_lon_bat_buoc+cac_te_bao_lon_da_dung]

    if len(tam[2]) != 0:

        str_html += f"<div>{cach_html}Các tế bào lớn đã chọn phủ các ô : </div>"

        k = phu_cac_o(tam[2])+cac_o_da_dung

        str_html += makeTable_Phu(matran, so_dau_cach, k)

        # print(cach+"các tế bào lớn đã chọn phủ các ô ")
        # print(cach, phu_cac_o(tam[2]))

    for i in reversed(cac_te_bao_lon_bat_buoc):
        if i == []:
            cac_te_bao_lon_bat_buoc.remove(i)

    if len(tam[0]) == 0:
        cac_phu = parsechuan(chuyendoi(cac_te_bao_lon_bat_buoc))
        str_html += f"<div style='color:red;'><strong >{cach_html}ta có phủ : " + \
            cac_phu+"</strong></div>"

        # print(cach+"ta có phủ ", cac_phu)
        return cac_te_bao_lon_bat_buoc
    vi_tri_cac_o_da_dung = [item for item in vi_tri_o if item not in tam[0]]

    for i in range(len(vi_tri_cac_o_da_dung)):
        k = vi_tri_cac_o_da_dung[i]
        cac_o_da_dung.append(k[-1]-15)

    vi_tri_o = Sorting(tam[0].copy())
    cac_da_thuc = []
    n = len(vi_tri_o[0])-1
    vi_tri_con = vi_tri_o[0]
    cac_te_bao_lon_can_xet = vi_tri_con[0:-1]

    # print(cach+"Ô %s bị phủ bởi các tế bào lớn " % (vi_tri_con[-1]-15))

    str_html += f"<div>{cach_html}Ô " + \
        str(vi_tri_con[-1]-15)+" bị phủ bởi các tế bào lớn : "
    tbl = []
    for h in range(len(cac_te_bao_lon_can_xet)):
        # print(cach+"    "+parsechuan(tra_ve_tbl(cac_te_bao_lon_can_xet[h])))
        tbl.append(parsechuan(tra_ve_tbl(cac_te_bao_lon_can_xet[h])))
    string3 = ''
    dem = 0
    for m in tbl:
        if dem == len(tbl)-1:
            string3 += f"{m}"
        else:
            string3 += f"{m} , "
        dem += 1
    str_html += string3+"</div>"

    for i in range(0, n):
        vi_tri_te_bao_lon_tam = cac_te_bao_lon_can_xet[i]
        vi_tri_o_phu = vi_tri_o
        cac_phan_tu_loai = []
        cac_o_da_dung_phu = cac_o_da_dung
        for j in range(len(vi_tri_o)):
            kl = vi_tri_o[j]
            if vi_tri_te_bao_lon_tam in kl:
                vi_tri_o_phu = [
                    item for item in vi_tri_o_phu if item not in [vi_tri_o[j]]]
                # print("các ô đã dùng phủ", cac_o_da_dung_phu)
                if (kl[-1]-15) not in cac_o_da_dung_phu:
                    cac_o_da_dung_phu.append(kl[-1]-15)

                if len(vi_tri_o[j]) == 2:
                    cac_phan_tu_loai.append(vi_tri_o[j])
                    next

                tam = [item for item in kl
                       if item not in [vi_tri_te_bao_lon_tam]]

                vi_tri_o = [
                    item for item in vi_tri_o if item not in [vi_tri_o[j]]]
                vi_tri_o.append(tam)

                vi_tri_o = Sorting(vi_tri_o)
        # loại bỏ những phần tử trùng
        cac_o_da_dung_phu = list(set(cac_o_da_dung_phu))
        # print(cach+"Nếu chọn tế bào lớn %s " %
        #      parsechuan(tra_ve_tbl(vi_tri_te_bao_lon_tam)))
        str_html += f'<div>{cach_html}Nếu chọn tế bào lớn ' + \
            parsechuan(tra_ve_tbl(vi_tri_te_bao_lon_tam)) + \
            '. Các ô được phủ là: </div>'
        cac_o_da_dung_phu.sort()
        # print(cach+"Các ô được phủ là : ", cac_o_da_dung_phu)
        # str_html += f'<div>{cach_html}Các ô được phủ là : ' + \
        #    str(cac_o_da_dung_phu)+'</div>'
        str_html += makeTable_Phu(matran, so_dau_cach, cac_o_da_dung_phu)

        vi_tri_o = [item for item in vi_tri_o if item not in cac_phan_tu_loai]

        tam2 = [vi_tri_te_bao_lon_tam]
        tam3 = tam2+cac_te_bao_lon_bat_buoc

        cac_da_thuc = cac_da_thuc + \
            tim_cac_da_thuc(vi_tri_o_phu, cac_o_da_dung_phu,
                            tam3, so_dau_cach+7)

    return cac_da_thuc


###


def xuat_ma_tran(karf):
    tam = 1
    for i in range(0, 4):
        for j in range(0, 4):
            if karf[i][j] == 1:
                karf[i][j] = tam
                tam = tam+1

    return karf


def tim_vi_tri_o():
    vi_tri = 0
    global vi_tri_o
    vi_tri_o = []
    # tạo array vi_tri_o có số phần tử bằng
    # số phần tử của ham_f[tap_hop]
    for kh in range(len(ham_f)):
        vi_tri_o.append([])
    # duyệt hết từng phần tử của cac_te_bao_lon
    # so sánh với vị trí trong ham_f[tap_hop]
    # =>sẽ biết đc vị trí của ô đó
    for i in range(len(tblon)):
        tam = tblon[i]
        vtri_tblon = ham_f_tap_hop(tam)
        for q in vtri_tblon:
            for j in range(len(ham_f)):
                if q == ham_f[j]:
                    vi_tri = j
            vi_tri_o[vi_tri].append(i)

    for k in range(len(vi_tri_o)):
        vi_tri_o[k].append(k+16)

    # print("vị trí ô= ", vi_tri_o)
    # vi_tri_o cho biết mỗi ô của Kar(f) có bao nhiêu
    # tế bào lớn chứa nó
    return vi_tri_o

# trả về tế bào lớn tướng ứng với ô


def tra_ve_tbl(vtri):
    for i in range(len(tblon)):
        if i == vtri:
            return tblon[i]


def phu_cac_o(tblon):
    matrix = xuat_ma_tran(karf).copy()
    phu = []
    for i in range(len(tblon)):
        k = kar_f_don_thuc(tblon[i])
        for u in range(0, 4):
            for v in range(0, 4):
                if k[u][v] == 1 and matrix[u][v] not in phu:
                    phu.append(matrix[u][v])
    phu.sort()
    return phu


def tim_cac_te_bao_lon_bat_buoc(vi_tri_o, so_dau_cach):
    global str_html
    cach = ""
    for i in range(so_dau_cach):
        cach = cach+" "

    cach_html = ''
    for i in range(so_dau_cach):
        cach_html += '&nbsp;'
    te_bao_lon_bat_buoc2 = []
    te_bao_lon_bat_buoc = []
    te_bao_de_in = []
    phan_tu_can_loai = []
    trave_TBBB = []
    for i in range(len(vi_tri_o)):
        vt = vi_tri_o[i]
        if len(vt) == 2:
            if vt[0] not in te_bao_lon_bat_buoc:
                te_bao_lon_bat_buoc.append(vt[0])
                te_bao_de_in.append(vt)
    # in ra
    for k in range(len(te_bao_de_in)):
        l = te_bao_de_in[k]
        # print(cach+"Ô %s chỉ bị phủ bởi tế bào lớn %s, chọn %s " %
        #      (l[1]-15, parsechuan(tra_ve_tbl(l[0])), parsechuan(tra_ve_tbl(l[0]))))
        str_html += f'<div>{cach_html}Ô '+str(l[1]-15)+' chỉ bị phủ bởi tế bào lớn '+parsechuan(
            tra_ve_tbl(l[0]))+', chọn '+parsechuan(tra_ve_tbl(l[0]))+'</div>'
        trave_TBBB.append(tra_ve_tbl(l[0]))

    for i in range(len(vi_tri_o)):
        k = [item for item in te_bao_lon_bat_buoc if item in vi_tri_o[i]]
        if len(k) != 0:
            phan_tu_can_loai.append(vi_tri_o[i])
    vi_tri_o = [item for item in vi_tri_o if item not in phan_tu_can_loai]

    return vi_tri_o, te_bao_lon_bat_buoc, trave_TBBB


###
# khởi tạo ma trận
def Kar():
    matrix = np.array([["AbCd", "ABCd", "aBCd", "abCd"],
                       ["AbCD", "ABCD", "aBCD", "abCD"],
                       ["AbcD", "ABcD", "aBcD", "abcD"],
                       ["Abcd", "ABcd", "aBcd", "abcd"]])

    return matrix

# chuyển đơn thức thành ma trận


def kar_f_don_thuc(char):
    p = 0
    dem = 0
    k = Kar()
    rel = []
    matrix2 = []
    for i in range(0, 4):
        rel.append([0, 0, 0, 0])
        matrix2.append([0, 0, 0, 0])
    while p < len(char):
        n = char[p]
        # đếm đơn thức có bao nhiêu kí tự
        # xuống dưới lấy lại vị trí
        dem = dem+1
        for i in range(0, 4):
            for j in range(0, 4):
                m = k[i][j]
                if m.find(n) != -1:
                    rel[i][j] = rel[i][j]+1

        p = p+1
    for i in range(0, 4):
        for j in range(0, 4):
            if rel[i][j] == dem:
                rel[i][j] = 1
            else:
                rel[i][j] = 0

    return rel

# chuyển đa thức thành biểu đồ Kar(f)


def Kar_f(chuoi_nhap):
    # khởi tạo 2 ma trận để lưu tạm kq ss chuỗi
    # matrix2 = np.zeros((4, 4))
    rel = []
    matrix2 = []
    for i in range(0, 4):
        rel.append([0, 0, 0, 0])
        matrix2.append([0, 0, 0, 0])

    rel2 = rel.copy()
    # rel = np.zeros((4, 4))
    # print("relllllllllllllll",rel2)
    k = Kar()
    h = 0
    n = ""
    dem = 0

    while h < len(chuoi_nhap):
        char = chuoi_nhap[h]
        p = 0
        # lấy từng kí tự của từng thành phần ra ss với
        # ma trận Kar
        while p < len(char):
            n = char[p]
            # đếm đơn thức có bao nhiêu kí tự
            # xuống dưới lấy lại vị trí
            dem = dem+1
            for i in range(0, 4):
                for j in range(0, 4):
                    m = k[i][j]
                    if m.find(n) != -1:
                        rel[i][j] = rel[i][j]+1
            p = p+1

        # lấy vị trí
        for i in range(0, 4):
            for j in range(0, 4):
                if rel[i][j] == dem:
                    rel[i][j] = 1
                else:
                    rel[i][j] = 0
        # vị trí cần lấy của dãy đa thức
        for i in range(0, 4):
            for j in range(0, 4):
                if rel[i][j] == 1:
                    matrix2[i][j] = 1
        rel = rel2
        dem = 0
        h = h+1
    # trả kq về ma trận matrix2
    return matrix2


# trả về vị trí của từng đơn thức
def ham_f_tap_hop(donthuc):
    vi_tri = []
    k = kar_f_don_thuc(donthuc)
    for i in range(0, 4):
        for j in range(0, 4):
            if k[i][j] == 1:
                vi_tri.append([i, j])

    return vi_tri

# trả về vị trí của đa thức


def ham_f_tap_hop_dathuc(dathuc):
    vi_tri = []
    k = Kar_f(dathuc)
    for i in range(0, 4):
        for j in range(0, 4):
            if k[i][j] == 1:
                vi_tri.append([i, j])

    return vi_tri
# lấy 4 ô kề


def te_bao_lon_f(arr):
    #### TÌM TẾ BÀO LỚN CÓ 8 PHẦN TỬ #####
    te_bao_lon = []
    cac_o_con = ham_f_tap_hop_dathuc(arr)
    ma_tran_chu = Kar()
    dem = 0
    # array dãy
    day = ["A", "B", "C", "D", "a", "b", "c", "d"]
    # Karf ban đầu
    karf = Kar_f(arr)
    for p in range(0, 8):
        dem = 0
        k = Kar_f(day[p])
        # kiểm tra day(i) là tế bào lớn của Kar(f) không
        for i in range(0, 4):
            for j in range(0, 4):
                if karf[i][j] == k[i][j] == 1:
                    dem = dem+1
                    bien = day[p]

        if dem == 8:
            te_bao_lon.append(bien)
            karf_day_i = ham_f_tap_hop(bien)
            cac_o_con = [item for item in cac_o_con if item not in karf_day_i]

    #### TÌM TẾ BÀO LỚN CÓ 4 PHẦN TỬ #####
    if (len(cac_o_con) == 0):
        return te_bao_lon

    tbl_8pt = te_bao_lon.copy()
    ham_f = ham_f_tap_hop_dathuc(arr)

    for i in range(0, 8):
        for j in range(i+1, 8):
            dem = 0
            kiemtra = day[i]+day[j]

            # h: chuyển đơn thức thành dạng ma trận
            h = kar_f_don_thuc(kiemtra)
            # K: Kar({day(i),day(j)})
            K = ham_f_tap_hop(kiemtra)
            """
                hg: kiểm tra tế bào 4 biến này có nằm trong
                tế bào 8 biến không ?
            """
            hg = [item for item in ham_f_tap_hop(
                kiemtra) if item in ham_f_tap_hop_dathuc(tbl_8pt)]
            if len(hg) != 4:
                # kiểm tra K có là tế bào lớn 4 ptu
                for u in range(0, 4):
                    for v in range(0, 4):
                        if karf[u][v] == h[u][v] == 1:
                            dem = dem+1

                if dem == 4:
                    te_bao_lon.append(kiemtra)
                    cac_o_con = [item for item in cac_o_con if item not in K]

        # hoán vị dãy [8-i] và day[i]
        # để không xuất hiện các đơn thức như BB',CC'
        tam = day[7-i]
        day[7-i] = day[7]
        day[7] = tam
    """
    for i in range(4, 8):
        for j in range(i+1, 8):
            dem = 0
            kiemtra = day[i]+day[j]
            # h: chuyển đơn thức thành dạng list
            h = kar_f_don_thuc(kiemtra)
            # K: Kar({day(i),day(j)})
            K = ham_f_tap_hop(kiemtra)

            """
    # hg: kiểm tra tế bào 4 biến này có nằm trong
    # tế bào 8 biến không ?
    """
        hg = [item for item in ham_f_tap_hop(
            kiemtra) if item in ham_f_tap_hop_dathuc(tbl_8pt)]
        if len(hg) != 4:
            # kiểm tra K có là tế bào lớn 4 ptu
            for u in range(0, 4):
                for v in range(0, 4):
                    if karf[u][v] == h[u][v] == 1:
                        dem = dem+1
            if dem == 4:
                te_bao_lon.append(kiemtra)
                cac_o_con = [item for item in cac_o_con if item not in K]
"""
    #### TÌM TẾ BÀO LỚN CÓ 2 PHẦN TỬ #####
    if (len(cac_o_con) == 0):
        return te_bao_lon

    for i in reversed(range(0, len(cac_o_con))):
        list_4_o = []
        o_con = cac_o_con[i]

        # Lấy lại vị trí 4 ô con xung quanh
        k1 = o_con[0]
        k2 = o_con[1]

        o_1 = [k1 % 4, (k2-1) % 4]
        o_2 = [k1 % 4, (k2+1) % 4]
        o_3 = [(k1-1) % 4, k2 % 4]
        o_4 = [(k1+1) % 4, k2 % 4]

        list_4_o.append(o_1)
        list_4_o.append(o_2)
        list_4_o.append(o_3)
        list_4_o.append(o_4)

        for a in list_4_o:
            if a in ham_f_tap_hop_dathuc(arr):
                # loại o_con khỏi cac_o_con
                for o in cac_o_con:
                    while True:
                        try:
                            cac_o_con.remove(o_con)
                        except:
                            break
                # nhằm đảm bảo chỉ xét {o_con, a} 1 lần
                if a in cac_o_con:
                    continue
                #
                # thêm {o_con, a} vào te_bao_lon
                vt_ai = a[0]
                vt_aj = a[1]
                # lấy lại dạng đơn thức (chuỗi) của a và o_con
                for u in range(0, 4):
                    for v in range(0, 4):
                        if u == vt_ai and v == vt_aj:
                            gtri_1 = ma_tran_chu[u][v]

                vt_o_con_i = o_con[0]
                vt_o_con_j = o_con[1]

                for u in range(0, 4):
                    for v in range(0, 4):
                        if u == vt_o_con_i and v == vt_o_con_j:
                            gtri_2 = ma_tran_chu[u][v]
                tb_can_them = ""
                # So sánh gtr_1 và gtri_2 nếu trùng chữ cái thì lấy

                for q in range(0, 4):
                    if gtri_1[q] == gtri_2[q]:
                        tb_can_them = tb_can_them+gtri_1[q]

                te_bao_lon.append(tb_can_them)

    #### TÌM TẾ BÀO LỚN CÓ 1 PHẦN TỬ #####
    for i in range(0, len(cac_o_con)):
        gtri = cac_o_con[i]
        vt_i = gtri[0]
        vt_j = gtri[1]

        for u in range(0, 4):
            for v in range(0, 4):
                if u == vt_i and v == vt_j:
                    tb_them = ma_tran_chu[u][v]
        te_bao_lon.append(tb_them)
    return te_bao_lon
