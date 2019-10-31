<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Default.aspx.cs" Inherits="speech.Default" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
    <link type="text/css" rel="stylesheet" href="css/app.css" />
    <link rel="stylesheet" href="css/font-awesome/css/font-awesome.min.css" />
    <title>空中反黑智能频谱监测软件</title>
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
                                        <asp:Button ID="btnStopScan" runat="server" class="button button-red" Text="开始扫描" OnClick="btnStopScan_Click" />
                                    </td>
                                    <td>
                                        <asp:Button ID="btnQT" runat="server" class="button button-red" Text="强制退出" OnClick="btnQT_Click" />
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <asp:Button ID="btnClose" runat="server" class="button button-red" Text="断开连接" OnClick="btnClose_Click" />
                                    </td>
                                    <td></td>
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

                    </ContentTemplate>
                </asp:UpdatePanel>
            </div>

            <div class="right">
                <div class="chart">
                    <div class="chartHeader">
                        <table width="100%">
                            <tr>
                                <td style="width: 50px;"><span class="chartTitle">频谱图</span></td>
                                <td><span class="chartInfo"></span></td>
                                <td class="bl" style="width: 100px;">
                                    <input type="range" name="points" min="0" max="100" style="display: none;" />
                                </td>
                                <td class="bl" style="width: 50px; text-align: center;">
                                    <a href="#"><i class="fa fa-play" aria-hidden="true"></i></a>
                                </td>
                                <td class="bl" style="width: 50px; text-align: center;">
                                    <a href="#"><i class="fa fa-refresh" aria-hidden="true"></i></a>
                                </td>
                            </tr>
                        </table>
                    </div>

                    <div class="chartContent">
                        <div id="lineChart"></div>
                    </div>
                    <div class="">
                        <div id="waterfallChart"></div>
                    </div>
                </div>
                <div class="bottom">

                    <div class="bottomLeft">

                        <div class="block-four block-panel2">
                            <div class="block-title">
                                <span>广播内容</span>
                            </div>
                            <div id="VoiceTextList" class="block-content" style="overflow-y: auto;">
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
                            <div class="block-content">
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
                                <div class="receiveBlankBlock">
                                    <div class="" style="font-size: 11px; color: white;">
                                        <ul id="FreqList">
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
    <script src="js/echarts/echarts.min.js"></script>
    <script type="text/javascript">
        $(function () {

            setInterval(function () {
                //获取广播文本
                $.ajax({
                    type: "Post",
                    url: "Default.aspx/GetVoiceText",
                    contentType: "application/json;charset=utf-8",
                    dataType: "json",
                    success: function (res) {
                        if (res.d.length > 0) {
                            var r = jQuery.parseJSON(res.d);
                            //$("#FreqVoiceTextList").html("");
                            for (var i = 0; i < r.length; i++) {
                                var Freq = r[i];
                                //var now = new Date().Format("yyyy-MM-dd HH:mm:ss");
                                var myDate = new Date();
                                //获取当前年
                                var year = myDate.getFullYear();
                                //获取当前月
                                var month = myDate.getMonth() + 1;
                                //获取当前日
                                var date = myDate.getDate();
                                var h = myDate.getHours();       //获取当前小时数(0-23)
                                var m = myDate.getMinutes();     //获取当前分钟数(0-59)
                                var s = myDate.getSeconds();
                                var now = year + '-' + month + "-" + date + " " + h + ':' + m + ":" + s;
                                $("#FreqVoiceTextList").append("<li style='margin-top: 10px;'><span style='color:#f98e52;'>时间：</span>" + now + "&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#f98e52;'>频点：</span>" + Freq.frequency + "MHz&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#f98e52;'>广播文本：</span>" + Freq.text + "</li>");
                                if ($("#FreqVoiceTextList li").length > 9)
                                    $("#FreqVoiceTextList").html("");
                            }
                        }
                    },
                    error: function (xmlReq, err, c) {
                        $(".chartInfo").text("error:" + err);
                    }
                });

                //获取当前广播频点列表
                $.ajax({
                    type: "Post",
                    url: "Default.aspx/GetFreqList",
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

                //获取黑广播数据
                $.ajax({
                    type: "Post",
                    url: "Default.aspx/GetIllegal",
                    contentType: "application/json;charset=utf-8",
                    dataType: "json",
                    success: function (res) {
                        if (res.d.length > 0) {
                            var r = jQuery.parseJSON(res.d);
                            //$("#IllegalList").html("");
                            //var now = new Date().Format("yyyy-MM-dd HH:mm:ss");
                            var myDate = new Date();
                            //获取当前年
                            var year = myDate.getFullYear();
                            //获取当前月
                            var month = myDate.getMonth() + 1;
                            //获取当前日
                            var date = myDate.getDate();
                            var h = myDate.getHours();       //获取当前小时数(0-23)
                            var m = myDate.getMinutes();     //获取当前分钟数(0-59)
                            var s = myDate.getSeconds();
                            var now = year + '-' + month + "-" + date + " " + h + ':' + m + ":" + s;
                            for (var i = 0; i < r.length; i++) {
                                $("#IllegalList").append("<li style='margin-top: 10px;'><span style='color:#f98e52;'>时间：</span>" + now + "&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#f98e52;'>频点：</span>" + r[i].frequency + "MHz&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#f98e52;'>关键词：</span>" + r[i].keyword + "</li>");
                                if ($("#IllegalList li").length > 20)
                                    $("#IllegalList").html("");
                            }
                        }
                    },
                    error: function (xmlReq, err, c) {
                        $(".chartInfo").text("error:" + err);
                    }
                });
            }, 5000);

            var myChart = echarts.init(document.getElementById('lineChart')); //频谱图

            var myChart1 = echarts.init(document.getElementById('waterfallChart')); //瀑布图

            setInterval(function () {
                $.ajax({
                    type: "Post",
                    url: "Default.aspx/LineData",
                    //data: "{'msg':'hello'}",
                    contentType: "application/json;charset=utf-8",
                    dataType: "json",
                    success: function (res) {

                        var yData = eval(res.d); //40960个数据点,10行数据

                        console.log(yData);

                        var xData = [];
                        //var xPData = [];
                        var yPData = [];
                        var pData = [];
                        for (var i = 0; i < <%=Lines%>; i++) {
                            xData.push(i); //X轴1~4096
                        }

                        function generateData() {
                            var data = [];
                            for (var i = 0; i < <%=Lines%>; i++) {  //
                                for (var j = 0; j < <%=Rows%>; j++) {
                                    data.push([i, j, yData[<%=Lines%> * j + i]]);
                                }
                                //xPData.push(i);
                            }
                            for (var j = 0; j < <%=Rows%>; j++) {
                                yPData.push(j);
                            }
                            return data;
                        }

                        var pData = generateData();

                        //频谱图配置
                        var option = {
                            //animation: false,
                            grid: {
                                x: 50,
                                y: 25,
                                x2: 25,
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
                                    interval: 248, // 自定义显示X轴坐标显示间隔
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
                        }

                        //瀑布图配置
                        option1 = {
                            tooltip: {},
                            grid: {
                                right: 20,
                                left: 100
                            },
                            xAxis: {
                                type: 'category',
                                textStyle: {
                                    color: '#ddd'
                                },
                                data: xData,
                                show: true,
                                position: 'top'
                            },
                            yAxis: {
                                type: 'category',
                                textStyle: {
                                    color: '#ddd'
                                },
                                data: yPData,
                                show: false,
                                inverse: true
                            },
                            visualMap: {
                                type: 'piecewise',
                                min: 40,
                                max: 120,
                                calculable: true,
                                realtime: false,
                                textStyle: {
                                    color: '#ddd'
                                },
                                splitNumber: 5,
                                inRange: {
                                    color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
                                }
                            },
                            series: [{
                                name: '瀑布图',
                                type: 'heatmap',
                                data: pData,
                                itemStyle: {
                                    emphasis: {
                                        borderColor: '#333',
                                        borderWidth: 1
                                    }
                                },
                                progressive: 0,
                                animation: false,
                                animationThreshold: 200
                            }]
                        };

                        myChart.setOption(option);

                        myChart1.setOption(option1);
                    },
                    error: function (xmlReq, err, c) {
                        $(".chartInfo").text("error:" + err);
                    }
                });
            }, 500)
        });
    </script>
</body>
</html>
