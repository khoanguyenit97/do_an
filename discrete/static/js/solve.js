function solve() {
    $("#problem-submit").click(function () {
        
        //Question: Lấy lại giá trị đề
        var ques = $("textarea#problem-content-input").val();
        if (ques === "") {
            alert("Bạn cần nhập đề bài");
            return false;
        }
        //type: Loại bài toán cần giải
        let type = $("select#problem-type-select option:selected").val();
        //Lấy giá trị thẻ đầu vào => chuyển sang Ajax
        let CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
       

        //Chuyển thành chuỗi JSON gửi đi
        let postData = {
            data: JSON.stringify({
                question: ques,
                type: type,
            }),
            //Chuyển dữ liệu sang Ajax
            csrfmiddlewaretoken: CSRFtoken
        };

        $.post('/solve', postData, function (json) {
            displayResult(json);
        }, 'json');
    });
}

function displayResult(json) {  
    
    let answerDiv = $("#answer");
    answerDiv.empty();

    var simplify_rule_dict = {
        1: { name: "Phủ định của phủ định", index: "1.2.6.1" },
        2: { name: "Luật phủ định", index: "1.2.6.1" },
        3: { name: "Luật về phần tử bù", index: "1.2.6.8" },
        4: { name: "Luật thống trị", index: "1.2.6.9" },
        5: { name: "Luật trung hòa", index: "1.2.6.7" },
        6: { name: "Luật lũy đẳng", index: "1.2.6.6" },
        7: { name: "Luật hấp thụ", index: "1.2.6.10" },
        8: { name: "Luật kéo theo", index: "1.2.6.11" },
        9: { name: "Luật phân phối", index: "1.2.6.5" },
        10: { name: "Quy tắc gom nhóm và rút gọn", index: "1.2.6.12" },
        11: { name: "Luật De Morgan", index: "1.2.6.2" },
    };

    var inference_rule_dict = {
        1: { name: "Quy tắc Modus Ponens", index: "1.3.1" },
        2: { name: "Quy tắc Modus Tollens", index: "1.3.3" },
        3: { name: "Tam đoạn luận", index: "1.3.2" },
        4: { name: "Tam đoạn luận rời", index: "1.3.4" },
        5: { name: "Quy tắc đơn giản", index: "1.3.8" },
        6: { name: "Quy tắc phủ định", index: "1.3.9" },
        7: { name: "Quy tắc chứng minh theo trường hợp", index: "1.3.6" },
        8: { name: "Quy tắc mâu thuẫn", index: "1.3.5" },
        9: { name: "Luật De Morgan", index: "1.2.6.2" },
        10: { name: "Quy tắc nối", index: "1.3.10" },
        11: { name: "Quy tắc nối", index: "1.3.10" },
    };
    
    if (json['success']) {
        let type = json['type'];
        let answer = json['answer'];

        switch (type) {
            case "1":
                displayBool(answer, answerDiv);
                break;
            case "2":
                displayResultForSimplify(answer, answerDiv, simplify_rule_dict);
                break;
            case "3":
                displayResultForEquivalent(answer, answerDiv, simplify_rule_dict);
                break;
            case "4":
                displayResultForInference(answer, answerDiv, inference_rule_dict);
                break;            
            
            default:
                break;
        }
    } else {
        alert(json['msg']);
    }
}


function generateRuleSpan(rule, index) {
    return `<span class="linkable" data-index="${index}" onclick="#">${rule}</span>`;
}

function onClickRuleKnowledge(domElement) {
    let index = domElement.dataset.index;
    $('#lookup-tab').toggleClass('active show');
    $('#solve-tab').toggleClass('active show');
    $('#lookup').toggleClass('active show');
    $('#solve').toggleClass('active show');
    selectIndexItem(index);
}

function makeTable_Karf(myArray) {
    var A = [' ', 'A', 'A', 'A\'', 'A\'', ' ']
    var B = [' ', 'B\'', 'B', 'B', 'B\'', ' ']
    var C = ['C', 'C', 'C\'', 'C\'']
    var D = ['D\'', 'D', 'D', 'D\'']

    var result = "<table style='text-align: center;width: 40%;margin-left: 10%;' >";
    result += "<tr>";
    for (var i = 0; i < A.length; i++) {
        result += "<td style='width:15%;'>" + A[i] + "</td>";
    }

    result += "</tr>";
    for (var i = 0; i < myArray.length; i++) {

        result += "<tr >";
        result += "<td style='width:15%;'>" + C[i] + "</td>";
        for (var j = 0; j < myArray[i].length; j++) {

            if (myArray[i][j] > 0) {

                result += "<td style='width:15%;color:red;background-color: aqua;border: 1px solid;border-color: black !important;' >" + myArray[i][j] + "</td>";
            }
            else {
                result += "<td style='width:15%;border: 1px solid;border-color: black !important;' >" + myArray[i][j] + "</td>";
            }
        }
        result += "<td style='width:15%;'>" + D[i] + "</td>";
        result += "</tr>";
    }
    result += "<tr>";
    for (var i = 0; i < A.length; i++) {
        result += "<td style='width:15%;'>" + B[i] + "</td>";
    }

    result += "</tr>";
    result += "</table>";

    return result;
}

function makeTable_TBL(myArray, tbl) {

    var A = [' ', 'A', 'A', 'A\'', 'A\'', ' ']
    var B = [' ', 'B\'', 'B', 'B', 'B\'', ' ']
    var C = ['C', 'C', 'C\'', 'C\'']
    var D = ['D\'', 'D', 'D', 'D\'']

    var result = "<table style='text-align: center;width: 40%;margin-left: 10%;' >";
    result += "<tr>";
    for (var i = 0; i < A.length; i++) {
        result += "<td style='width:15%;'>" + A[i] + "</td>";
    }
    result += "</tr>";
    
    for (var i = 0; i < myArray.length; i++) {

        result += "<tr >";
        result += "<td style='width:15%;'>" + C[i] + "</td>";
        for (var j = 0; j < myArray[i].length; j++) {
            var k = [i, j]            
            a = JSON.stringify(tbl);
            b = JSON.stringify(k);
            var c = a.indexOf(b);

            if (c != -1) {

                result += "<td style='width:15%;color:red;background-color: aqua;border: 1px solid;border-color: black !important;' >" + myArray[i][j] + "</td>";
            } else {
                if (myArray[i][j] > 0) {
                    result += "<td style='width:15%;color:red;border: 1px solid;border-color: black !important;' >" + myArray[i][j] + "</td>";
                }
                else {
                    result += "<td style='width:15%;border: 1px solid;border-color: black !important;' >" + myArray[i][j] + "</td>";
                }
            }

        }
        result += "<td style='width:15%;'>" + D[i] + "</td>";
        result += "</tr>";
    }
    result += "<tr>";
    for (var i = 0; i < A.length; i++) {
        result += "<td style='width:15%;'>" + B[i] + "</td>";
    }
    result += "</tr>";
    result += "</table>";
    return result;
}

function displayBool(json, answerDiv) {
    
    let de_quy = json["de_quy"]
    let ques = json["ques"];
    let te_bao_lon = json["te_bao_lon"];
    let karf = json["karf"];
    let cac_phu_tu_karf = json["cac_phu_tu_karf"];
    let da_thuc_toi_tieu = json["da_thuc_toi_tieu"]
    var answerHTML = `<div style="font-size:20px;color:blue !important;">`
    answerHTML += `<div>Kết quả rút gọn của biểu thức :  ${ques}</div>`;
    answerHTML += `<div>Kar(f) là :</div>`    
    answerHTML += makeTable_Karf(karf)
    answerHTML += `</table>`

    answerHTML += `<div>Các tế bào lớn của kar(f) là: </div>`

    for (let index = 0; index < te_bao_lon.length; ++index) {
        
        var k = te_bao_lon[index]
        var tbl = k.pop()

        answerHTML += `<div>Tế bào lớn ${tbl}</div>`
        answerHTML += makeTable_TBL(karf, te_bao_lon[index])
        /*`<div>${te_bao_lon[index]}</div>`*/
    }

    answerHTML += de_quy
    answerHTML += `<div>Các phủ tìm được từ Kar(f) là :</div>`
    answerHTML += `<table style= "margin-left: 41px;">`
    for (let index = 0; index < cac_phu_tu_karf.length; ++index) {
        let phu = cac_phu_tu_karf[index];
        answerHTML += `<tr><td>f${index + 1} =  ${phu}</td></tr>`;
    }
    answerHTML += `</table>`
    answerHTML += `<div>So sánh các phủ trên ta tìm được các đa thức tối tiểu :</div>`
    answerHTML += `<table style= "margin-left: 41px;">`
    for (let index = 0; index < da_thuc_toi_tieu.length; ++index) {
        let da_thuc = da_thuc_toi_tieu[index];
        answerHTML += `<tr><td>f${index + 1} =  ${da_thuc}</td></tr>`;
    }

    answerHTML += `</table>`
    answerDiv.append(answerHTML);

}
//Hàm xử lý chính
function displayResultForSimplify(json, answerDiv, dict) {
    
    let expr = json["expr"];
    let min_expr = json["min"];
    let steps = json["steps"];
    var answerHTML = `<div>Kết quả rút gọn của biểu thức ${expr}:</div><table class="answer-table">`;
    answerHTML += `<tr>${expr}</tr>`;
    for (let index = 0; index < steps.length; ++index) {
        let step = steps[index];
        let rule = step['rule'];
        answerHTML += `<tr><td>⇔ ${step['expr']}</td><td>${generateRuleSpan(dict[rule].name, dict[rule].index)}</td></tr>`;
    }
    answerHTML += `</table>`;
    answerDiv.append(answerHTML);
}


function displayResultForEquivalent(json, answerDiv, dict) {
    let result = json["result"];
    let expr1 = json["expr_1"];
    let expr2 = json["expr_2"];

    var answerHTML = ``;
    if (result) {
        answerHTML = `<div>Hai biểu thức ${expr1} và ${expr2} tương đương với nhau vì:</div>`;
    } else {
        answerHTML = `<div>Hai biểu thức ${expr1} và ${expr2} không tương đương với nhau vì:</div>`;
    }
    answerHTML += `<table class="answer-table">`;

    let steps1 = json["steps_1"];
    answerHTML += `<tr>${expr1}</tr>`;
    for (let index = 0; index < steps1.length; ++index) {
        let step = steps1[index];
        let rule = step['rule'];
        answerHTML += `<tr><td>⇔ ${step['expr']}</td><td>${generateRuleSpan(dict[rule].name, dict[rule].index)}</td></tr>`;
    }
    answerHTML += `</table><div>Và:</div><table class="answer-table">`;
    let steps2 = json["steps_2"];
    answerHTML += `<tr>${expr2}</tr>`;
    for (let index = 0; index < steps2.length; ++index) {
        let step = steps2[index];
        let rule = step['rule'];
        answerHTML += `<tr><td>⇔ ${step['expr']}</td><td>${generateRuleSpan(dict[rule].name, dict[rule].index)}</td></tr>`;
    }
    answerHTML += `</table>`;

    answerDiv.append(answerHTML);
}

function displayResultForInference(json, answerDiv, dict) {
    
    let result = json["result"];

    var answerHTML = ``;
    if (result) {
        answerHTML = `<div>Ta có:</div><table class="answer-table">`;
        let steps = json["steps"];
        for (let index = 0; index < steps.length; ++index) {
            let step = steps[index];
            let rules = step['rules'];
            var rulesString = '';
            for (let j = 0; j < rules.length; ++j) {
                rulesString += "(" + rules[j] + ")";
                if (j < rules.length - 1) {
                    rulesString += ', ';
                }
            }
            if (index === steps.length - 1) {
                answerHTML += `<tr><td>${index + 1}) ${step['fact']} (ĐPCM)</td>`;
            } else {
                answerHTML += `<tr><td>${index + 1}) ${step['fact']}</td>`;
            }
            if (rulesString !== '') {
                let rule = step['rule'];
                answerHTML += `<td>Từ ${rulesString} và ${generateRuleSpan(dict[rule].name, dict[rule].index)}</td></tr>`;
            } else {
                answerHTML += `<td>(Giả thuyết)</td></td></tr>`;
            }

        }
        answerHTML += `</table>`;
    } else {
        answerHTML = `<span>Không thể chứng minh suy luận là đúng với những giả thuyết đang có</span>`;
    }

    answerDiv.append(answerHTML);
}


function observeSelection() {
    let currentValue = $("select#problem-type-select option:selected").val();
    selectedTypeChanged(currentValue);

    $("#problem-type-select").on('change', function () {
        let selection = this.value;
        selectedTypeChanged(selection)
    });
}

function selectedTypeChanged(selection) {
    
    let guide = $("#input-guide");
    guide.empty();
    $("#answer").empty();
    $("#problem-content-input").val('');

    switch (selection) {
        case "1":
            guide.load("static/guide/bool.html");
            break;
        case "2":
            guide.load("static/guide/simplify.html");
            break;
        case "3":
            guide.load("static/guide/equal.html");
            break;
        case "4":
            guide.load("static/guide/inference.html");
            break;        
        
        default:
            break;
    }
}