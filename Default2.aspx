<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Default2.aspx.cs" Inherits="speech.Default2" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
    <link type="text/css" rel="stylesheet" href="css/app.css" />
    <link rel="stylesheet" href="css/font-awesome/css/font-awesome.min.css" />
    <title>空中‘反黑’智能频谱监测系统</title>
</head>
<body>
    <form id="form1" runat="server">
        <asp:ScriptManager ID="scrpitManager1" runat="server"></asp:ScriptManager>
        <div class="header">
            <img src="img/title.png" class="title" />
        </div>
        <div class="content">
            <div class="left">
                <asp:UpdatePanel ID="up1" runat="server">
                    <ContentTemplate>
                        <div class="block-one">
                            <table>
                                <tr>
                                    <td>
                                        <asp:Button ID="btnJT" runat="server" class="button button-blue" Text="解调" OnClick="btnJT_Click" />
                                    </td>
                                    <td>
                                        <asp:Button ID="btnStop" runat="server" class="button button-blue" Text="停止" OnClick="btnStop_Click" />
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <asp:Button ID="btnPPT" runat="server" class="button button-blue" Text="频谱图" OnClick="btnPPT_Click" />
                                    </td>
                                    <td>
                                        <asp:Button ID="btnExit" runat="server" class="button button-red" Text="退&nbsp;&nbsp;出" OnClick="btnExit_Click" />
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <asp:Button ID="btnStartScan" runat="server" class="button button-red" Text="开始扫描" OnClick="btnStartScan_Click" />
                                    </td>
                                    <td>
                                        <asp:Button ID="btnStopScan" runat="server" class="button button-red" Text="停止扫描" OnClick="btnStopScan_Click" />
                                    </td>
                                </tr>
                            </table>
                        </div>
                        <div class="block-two block-panel">
                            <div class="block-title">
                                <span>选择单个频点停留时间</span>
                            </div>
                            <div class="block-content">
                                <%--<div class="timeBlankBlock"></div>--%>
                                <div class="block-two-buttons">
                                    <table>
                                        <tr>
                                            <td>
                                                <asp:Button ID="btn10S" runat="server" class="button button-blue" Text="10S" OnClick="btn10s_Click" />
                                            </td>
                                            <td>
                                                <asp:Button ID="btn20S" runat="server" class="button button-blue" Text="20S" OnClick="btn20S_Click" />
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>
                                                <asp:Button ID="btn30S" runat="server" class="button button-blue" Text="30S" OnClick="btn30S_Click" />
                                            </td>
                                            <td>
                                                <asp:Button ID="btn40S" runat="server" class="button button-blue" Text="40S" OnClick="btn40S_Click" />
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>
                                                <asp:Button ID="btn50S" runat="server" class="button button-blue" Text="50S" OnClick="btn50S_Click" />
                                            </td>
                                            <td>
                                                <asp:Button ID="btn60S" runat="server" class="button button-blue" Text="60S" OnClick="btn60S_Click" />
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>
                                                <asp:Button ID="btn70S" runat="server" class="button button-blue" Text="70S" OnClick="btn70S_Click" />
                                            </td>
                                            <td>
                                                <asp:Button ID="btn80S" runat="server" class="button button-blue" Text="80S" OnClick="btn80S_Click" />
                                            </td>
                                        </tr>
                                    </table>
                                </div>
                            </div>
                        </div>
                        <div class="block-three block-panel">
                            <div class="block-title">
                                <span>设置中心频率</span>
                            </div>
                            <div class="block-content">
                                <div class="centerFreq">
                                    <asp:TextBox ID="txtCenterFreq" runat="server" Style="background: rgba(0, 0, 0, 0); float: left;"></asp:TextBox>
                                    <asp:Button ID="btnSubmit" runat="server" class="button button-blue" Text="确定" OnClick="btnSubmit_Click" />
                                </div>
                            </div>
                        </div>
                        <div class="block-three block-panel">
                            <div class="block-title">
                                <span>语音识别选择</span>
                            </div>
                            <div class="block-content">
                                <div class="centerFreq">
                                    <asp:DropDownList ID="ddlVoice" runat="server" Style="background: rgba(0, 0, 0, 0); width: 200px; height: 30px; color: #23a3b7">
                                        <asp:ListItem Text="百度云语音识别" Selected="True"></asp:ListItem>
                                        <asp:ListItem Text="华为云语音识别"></asp:ListItem>
                                        <asp:ListItem Text="讯飞语音识别"></asp:ListItem>
                                    </asp:DropDownList>

                                </div>
                            </div>
                        </div>

                    </ContentTemplate>
                </asp:UpdatePanel>
            </div>

            <div class="right">
                <div class="chart">
                    <div class="chartHeader">
                        <table width="100%">
                            <tr>
                                <td style="width: 50px;"><span class="chartTitle">频谱图</span></td>
                                <td><span class="chartInfo"></span><span class="scanInfo" style="float: right; margin-right: 10px;"></span></td>

                                <td class="bl" style="width: 200px; text-align: center;">
                                    <a href="#"><i class="fa fa-refresh" aria-hidden="true"></i>
                                        <div id="CurrentFreq"></div>
                                    </a>
                                </td>
                            </tr>
                        </table>
                    </div>

                    <div class="chartContent">
                        <div id="lineChart"></div>
                        <canvas id="myCanvas" width="2048" style="width: 95%; height: 250px; margin-left: 2.5%;">Your browser does not support the HTML5 canvas tag.
                        </canvas>
                        <canvas id="waterFall" width="2048" style="height: 1px;">Your browser does not support the HTML5 canvas tag.
                        </canvas>
                    </div>
                </div>
                <div class="bottom">

                    <div class="bottomLeft">

                        <div class="block-four block-panel2">
                            <div class="block-title">
                                <span>广播内容</span>
                            </div>
                            <div id="VoiceTextList" class="block-content" style="overflow-y: auto; height: 150px;">
                                <div class="" style="font-size: 11px; color: white;">
                                    <ul id="FreqVoiceTextList">
                                    </ul>
                                </div>
                            </div>
                        </div>

                        <div class="block-five block-panel2">
                            <div class="block-title">
                                <span>黑广播</span>
                            </div>
                            <div class="block-content" style="overflow-y: auto; height:65px;">
                                <div class="" style="font-size: 11px; color: white;">
                                    <ul id="IllegalList">
                                    </ul>
                                </div>
                            </div>
                        </div>

                    </div>

                    <div class="bottomRight">
                        <div class="block-six block-panel">
                            <div class="block-title">
                                <span>接收的广播频道列表</span>
                            </div>
                            <div class="block-content">
                                <div class="receiveBlankBlock" style="overflow-y: auto; height: 138px;">
                                    <div class="" style="font-size: 11px; color: white;">
                                        <ul id="FreqList">
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="block-six block-panel" style="margin-top: 20px;">
                            <div class="block-title">
                                <span>可疑的广播频道列表</span>
                            </div>
                            <div class="block-content">
                                <div class="receiveBlankBlock" style="overflow-y: auto; height:53px;">
                                    <div class="" style="font-size: 11px; color: white;">
                                        <ul id="kyFreqList">
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </form>
    <script type="text/javascript" src="js/jquery-1.11.0.js"></script>
    <script src="https://cdn.bootcss.com/sweetalert/2.1.2/sweetalert.min.js"></script>
    <script src="js/echarts/echarts.min.js"></script>
    <script type="text/javascript">
        $(function () {

            setInterval(function () {
                //获取广播文本
                $.ajax({
                    type: "Post",
                    url: "Default2.aspx/GetVoiceText",
                    contentType: "application/json;charset=utf-8",
                    dataType: "json",
                    success: function (res) {

                        //var uArray = $("#FreqVoiceTextList li");
                        //if (uArray.length > 20)
                        //    $("#FreqVoiceTextList").html("");

                        if (res.d.length > 0) {
                            var r = jQuery.parseJSON(res.d);
                            $("#FreqVoiceTextList").html("");
                            //for (var i = 0; i < r.length; i++) {
                            //    var Freq = r[i];
                            ////var now = new Date().Format("yyyy-MM-dd HH:mm:ss");
                            //var myDate = new Date();
                            ////获取当前年
                            //var year = myDate.getFullYear();
                            ////获取当前月
                            //var month = myDate.getMonth() + 1;
                            ////获取当前日
                            //var date = myDate.getDate();
                            //var h = myDate.getHours();       //获取当前小时数(0-23)
                            //var m = myDate.getMinutes();     //获取当前分钟数(0-59)
                            //var s = myDate.getSeconds();
                            //var now = year + '-' + month + "-" + date + " " + h + ':' + m + ":" + s;

                            for (var i = 0; i < r.length; i++) {
                                $("#FreqVoiceTextList").append("<li style='margin-top: 10px;'><span style='color:#f98e52;'>时间：</span>" + r[i].time.replace('T', ' ') + "&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#f98e52;'>频点：</span>" + r[i].frequency + "MHz&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#f98e52;'>广播文本：</span>" + r[i].text + "</li>");
                                //if (uArray.length > 0) {
                                //    for (var j = 0; j < uArray.length; j++) {
                                //        var text = uArray[j].innerText;
                                //        if (!(isContains(text, r[i].frequency) && isContains(text, r[i].text))) {
                                //            $("#FreqVoiceTextList").append("<li style='margin-top: 10px;'><span style='color:#f98e52;'>时间：</span>" + r[i].time + "&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#f98e52;'>频点：</span>" + r[i].frequency + "MHz&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#f98e52;'>广播文本：</span>" + r[i].text + "</li>");

                                //        }
                                //    }
                                //}
                                //else {

                                //    $("#FreqVoiceTextList").append("<li style='margin-top: 10px;'><span style='color:#f98e52;'>时间：</span>" + r[i].time + "&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#f98e52;'>频点：</span>" + r[i].frequency + "MHz&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#f98e52;'>广播文本：</span>" + r[i].text + "</li>");
                                //}
                            }
                            //}
                        }
                    },
                    error: function (xmlReq, err, c) {
                        $(".chartInfo").text("error:" + err);
                    }
                });

                //获取当前广播频点列表
                $.ajax({
                    type: "Post",
                    url: "Default2.aspx/GetFreqList",
                    contentType: "application/json;charset=utf-8",
                    dataType: "json",
                    success: function (res) {
                        if (res.d.length > 0) {
                            var r = jQuery.parseJSON(res.d);
                            $("#FreqList").html("");

                            for (var i = 0; i < r.length; i++) {
                                $("#FreqList").append("<li style='margin-top: 10px;'>" + r[i].now_list_freq + "MHz" + "</li>");
                            }
                        }
                    },
                    error: function (xmlReq, err, c) {
                        $(".chartInfo").text("error:" + err);
                    }

                });

                //获取可疑广播频点列表
                $.ajax({
                    type: "Post",
                    url: "Default2.aspx/GetKyFreqList",
                    contentType: "application/json;charset=utf-8",
                    dataType: "json",
                    success: function (res) {
                        $("#kyFreqList").html("");

                        if (res.d.length > 0) {
                            var r = jQuery.parseJSON(res.d);

                            for (var i = 0; i < r.length; i++) {
                                $("#kyFreqList").append("<li style='margin-top: 10px;'>" + r[i].doubtful_freq_list + "MHz" + "</li>");
                            }
                        }
                    },
                    error: function (xmlReq, err, c) {
                        $(".chartInfo").text("error:" + err);
                    }

                });

                //获取当前扫描状态和频点停留时间
                $.ajax({
                    type: "Post",
                    url: "Default2.aspx/GetScanInfo",
                    contentType: "application/json;charset=utf-8",
                    dataType: "json",
                    success: function (res) {
                        if (res.d.length > 0) {

                            var r = jQuery.parseJSON(res.d);
                            var scan_time = r[0].scan_time;
                            var scan = r[1].scan_time == "1" ? "正在扫描" : "停止扫描"
                            $(".scanInfo").html("扫描状态：" + scan + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;当前频点停留时间：" + scan_time + "S");
                        }
                    },
                    error: function (xmlReq, err, c) {
                        $(".chartInfo").text("error:" + err);
                    }

                });

                //获取黑广播数据
                $.ajax({
                    type: "Post",
                    url: "Default2.aspx/GetIllegal",
                    contentType: "application/json;charset=utf-8",
                    dataType: "json",
                    success: function (res) {
                        

                        if (res.d.length > 0) {
                            var r = jQuery.parseJSON(res.d);
                            var uArray = $("#IllegalList li");
                            if (r.length > uArray.length) {
                                swal("发现黑广播！", {
                                    buttons: false,
                                    icon: "error",
                                    timer: 2000,
                                });
                            }

                            $("#IllegalList").html("");
                            ////var now = new Date().Format("yyyy-MM-dd HH:mm:ss");
                            //var myDate = new Date();
                            ////获取当前年
                            //var year = myDate.getFullYear();
                            ////获取当前月
                            //var month = myDate.getMonth() + 1;
                            ////获取当前日
                            //var date = myDate.getDate();
                            //var h = myDate.getHours();       //获取当前小时数(0-23)
                            //var m = myDate.getMinutes();     //获取当前分钟数(0-59)
                            //var s = myDate.getSeconds();
                            //var now = year + '-' + month + "-" + date + " " + h + ':' + m + ":" + s;

                            for (var i = 0; i < r.length; i++) {
                                $("#IllegalList").append("<li style='margin-top: 10px;'><span style='color:#f98e52;'>时间：</span>" + r[i].time.replace('T', ' ') + "&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#f98e52;'>频点：</span>" + r[i].frequency + "MHz&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#f98e52;'>关键词：</span>" + r[i].keyword + "</li>");

                                //if (uArray.length > 0) {
                                //    var text = uArray[uArray.length - 1].innerText;
                                //    if (!(isContains(text, r[i].frequency) && isContains(text, r[i].keyword))) {
                                //        $("#IllegalList").append("<li style='margin-top: 10px;'><span style='color:#f98e52;'>时间：</span>" + now + "&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#f98e52;'>频点：</span>" + r[i].frequency + "MHz&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#f98e52;'>关键词：</span>" + r[i].keyword + "</li>");

                                //        swal("发现黑广播！", {
                                //            buttons: false,
                                //            icon: "error",
                                //            timer: 2000,
                                //        });  
                                //    }
                                //}
                                //else {

                                //    $("#IllegalList").append("<li style='margin-top: 10px;'><span style='color:#f98e52;'>时间：</span>" + now + "&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#f98e52;'>频点：</span>" + r[i].frequency + "MHz&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#f98e52;'>关键词：</span>" + r[i].keyword + "</li>");
                                //    swal("发现黑广播！", {
                                //        buttons: false,
                                //        icon: "error",
                                //        timer: 2000,
                                //    });
                                //}
                            }
                        }
                    },
                    error: function (xmlReq, err, c) {
                        $(".chartInfo").text("error:" + err);
                    }
                });

                //获取当前监听频点
                $.ajax({
                    type: "Post",
                    url: "Default2.aspx/GetCurrentFreq",
                    contentType: "application/json;charset=utf-8",
                    dataType: "json",
                    success: function (res) {
                        if (res.d.length > 0) {
                            var r = jQuery.parseJSON(res.d);
                            $("#CurrentFreq").html("当前监听频点：" + r + "MHz");
                        }
                    },
                    error: function (xmlReq, err, c) {
                        $(".chartInfo").text("error:" + err);
                    }

                });
            }, 2000);

            var myChart = echarts.init(document.getElementById('lineChart')); //绘制频谱图

            //瀑布图配置
            var row = 0;
            var c = document.getElementById("waterFall");
            var ctx = c.getContext("2d");
            var view = document.getElementById("myCanvas");
            var width = view.scrollWidth;
            //alert("scrollWidth:" + width + "//clientWidth:" + view.clientWidth + "// offsetWidth:" + view.offsetWidth );
            var Viewctx = view.getContext("2d");
            var imgData = ctx.createImageData(<%=Lines%>, 1);
            var ss = getColor(); //ShadeColor("rgb(41,108,128)", "rgb(83,190,75)", 100);

            setInterval(function () {

                $.ajax({
                    type: "Post",
                    url: "Default2.aspx/LineData",
                    //data: "{'msg':'hello'}",
                    contentType: "application/json;charset=utf-8",
                    dataType: "json",
                    success: function (res) {

                        var yData = eval(res.d); //2048个数据点

                        var xData = [];
                        for (var i = 0; i < <%=Lines%>; i++) {
                            xData.push(i); //X轴1~4096
                        }

                        //绘制瀑布图
                        for (var i = 0; i < imgData.data.length; i += 4) {

                            var index = squeeze(Number(yData[i / 4]), 20, 70);
                            var color = ss[index];
                            imgData.data[i + 0] = color[0];
                            imgData.data[i + 1] = color[1];
                            imgData.data[i + 2] = color[2];
                            imgData.data[i + 3] = 255;
                        }
                        ctx.putImageData(imgData, 0, 0);

                        if (row > <%=Rows%>) {
                            row = 0;
                            Viewctx.clearRect(0, 0,<%=Lines %>,<%=Rows+1%>);
                        }
                        else {
                            //(img,0,0,400,266,0,0,300,150);
                            Viewctx.drawImage(ctx.canvas, 0, 0, 2048, 1, 0, row, 2048, 1);
                            //Viewctx.drawImage(ctx.canvas, 0, row);
                            row++;
                        }

                        //频谱折线图配置
                        var option = {
                            //animation: false,
                            grid: {
                                x: '2.5%',
                                y: 25,
                                x2: '2.5%',
                                y2: 25,
                            },
                            tooltip: {
                                trigger: 'axis',

                                axisPointer: {
                                    animation: false
                                }
                            },
                            xAxis: {
                                axisLabel: {
                                    interval: 200, // 自定义显示X轴坐标显示间隔
                                    max: 2047,
                                    formatter: (val) => {
                                        if (val === '0') {
                                            // eslint-disable-next-line
                                            val = '88MHz';
                                        }
                                        if (val === '201') {
                                            // eslint-disable-next-line
                                            val = '90MHz';
                                        }
                                        if (val === '402') {
                                            // eslint-disable-next-line
                                            val = '92MHz';
                                        }
                                        if (val === '603') {
                                            // eslint-disable-next-line
                                            val = '94MHz';
                                        }
                                        if (val === '804') {
                                            // eslint-disable-next-line
                                            val = '96MHz';
                                        }
                                        if (val === '1005') {
                                            // eslint-disable-next-line
                                            val = '98MHz';
                                        }
                                        if (val === '1206') {
                                            // eslint-disable-next-line
                                            val = '100MHz';
                                        }
                                        if (val === '1407') {
                                            // eslint-disable-next-line
                                            val = '102MHz';
                                        }
                                        if (val === '1608') {
                                            // eslint-disable-next-line
                                            val = '104MHz';
                                        }
                                        if (val === '1809') {
                                            // eslint-disable-next-line
                                            val = '106MHz';
                                        }
                                        if (val === '2010') {
                                            // eslint-disable-next-line
                                            val = '108MHz';
                                        }
                                        return val;
                                    },
                                    textStyle: {
                                        color: '#ddd'
                                    }
                                },
                                axisLine: {
                                    lineStyle: {
                                        color: '#ddd'
                                    }
                                },
                                data: xData,
                                show: true
                            },
                            yAxis: {

                                axisLine: {
                                    show: false
                                },
                                axisTick: {
                                    show: false
                                },
                                axisLabel: {
                                    textStyle: {
                                        color: '#ddd'
                                    }
                                },
                                scale: true,
                                show: false
                            },
                            series: [{
                                smooth: true,
                                lineStyle: {
                                    color: '#23a3b7'
                                },
                                type: 'line',
                                showSymbol: false,
                                yEhoverAnimation: false,
                                data: yData
                            }]
                        };

                        myChart.setOption(option);
                    },
                    error: function (xmlReq, err, c) {
                        $(".chartInfo").text("error:" + err);
                    }
                });
            }, 200)
        });
    </script>
    <script>
        //生成渐变色，从绿色到红色的渐变
        function ShadeColor(colorMAX, colorMIN, num) {

            var colorMAX = colorMAX.toLowerCase();
            var colorMIN = colorMIN.toLowerCase();

            colorMAX = colorMAX.slice(4, -1).split(",");
            colorMIN = colorMIN.slice(4, -1).split(",");
            var colors = [];
            var level = num;
            while (level--) {
                //A + (B-A) * N / Step
                var red = Number(colorMIN[0]) + (Number(colorMAX[0]) - Number(colorMIN[0])) / num * level;
                var green = Number(colorMIN[1]) + (Number(colorMAX[1]) - Number(colorMIN[1])) / num * level;
                var blue = Number(colorMIN[2]) + (Number(colorMAX[2]) - Number(colorMIN[2])) / num * level;
                var c = [];
                c.push(red);
                c.push(green);
                c.push(blue);
                colors.push(c);
            }
            return colors;
        }

        function squeeze(data, min, max) {
            if (data < min)
                return 0;
            else if (data > max)
                return 100;
            else
                return Math.round((data - min) / (max - min) * 100);
        }

        function isContains(str, substr) {
            return str.indexOf(substr) >= 0;
        }

        function getColor() {
            var full = 101;    //数据总数
            var r = 0;
            var g = 0;
            var b = 0;
            var colors = [];
            for (i = 0; i < full; i++) {

                //if (i < full / 3) {
                //    r = 255;
                //    g = Math.ceil(255 * 3 * i / full);
                //    b = 0;
                //} else if (i < full / 2) {
                //    r = Math.ceil(750 - i * (250 * 6 / full));
                //    g = 255;
                //    b = 0;
                //} else if (i < full * 2 / 3) {
                //    r = 0;
                //    g = 255;
                //    b = Math.ceil(i * (250 * 6 / full) - 750);
                //} else if (i < full * 5 / 6) {
                //    r = 0;
                //    g = Math.ceil(1250 - i * (250 * 6 / full));
                //    b = 255;
                //} else {
                //    r = Math.ceil(150 * i * (6 / full) - 750);
                //    g = 0;
                //    b = 255;
                //}
                //r = intval(min(255, ($x * 1.0 / $threshold * 255)) * $brightness)
                //g = intval(max(0, min(255, (2 - $x * 1.0 / $threshold) * 255)) * $brightness)

                r = Math.round(Math.min(255, (i * 1.0 / 50 * 255) * 1));
                g = Math.round(Math.max(0, Math.min(255, (2 - i * 1 / 50) * 255)) * 1);
                var c = [];
                c.push(r);
                c.push(g);
                c.push(b);
                colors.push(c);
            }
            return colors;
        }

        /**************************************时间格式化处理************************************/
        function dateFtt(fmt, date) { //author: meizz 
            var o = {
                "M+": date.getMonth() + 1,     //月份 
                "d+": date.getDate(),     //日 
                "h+": date.getHours(),     //小时 
                "m+": date.getMinutes(),     //分 
                "s+": date.getSeconds(),     //秒 
                "q+": Math.floor((date.getMonth() + 3) / 3), //季度 
                "S": date.getMilliseconds()    //毫秒 
            };
            if (/(y+)/.test(fmt))
                fmt = fmt.replace(RegExp.$1, (date.getFullYear() + "").substr(4 - RegExp.$1.length));
            for (var k in o)
                if (new RegExp("(" + k + ")").test(fmt))
                    fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
            return fmt;
        }
    </script>
</body>
</html>
